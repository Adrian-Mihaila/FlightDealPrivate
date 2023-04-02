import html
from data_manager import DataManager
from data_manager import STEINHQ_ENDPOINT_U, STEINHQ_HEADER
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import smtplib
import imaplib
import email
import json
import requests
from datetime import datetime, timedelta
from flight_data import FlightData
import pandas as pd
from IPython.display import HTML


tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=180)

API_KEY = "8nrhLLE0o2OiHKRLWq0GDuWbKkQ2DKJh"
API_ENDPOINT_QUERY = "https://tequila-api.kiwi.com/locations/query"
API_ENDPOINT_SEARCH = "https://tequila-api.kiwi.com/v2/search"
HEADERS = {
    "apikey": API_KEY
}

sheet_data_users = DataManager().get_email_list()


def check_flights(origin_destination, city_destination_code, destination_nights):
    """Passes the parameters, requests all the flight details from API
    and save only the required ones to print the destination city and the price"""
    values_dict = {}
    if destination_nights == "4_nights":
        params = {
            "fly_from": origin_destination,
            "fly_to": city_destination_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months_from_now.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 4,
            "flight_type": "round",
            "curr": "EUR",
            "select_airlines": "0B",  # avoid blue air
            "select_airlines_exclude": "True",
            "adults": 1,
            "sort": "price",
            "asc": "1"
        }
    elif destination_nights == "7_nights":
        params = {
            "fly_from": origin_destination,
            "fly_to": city_destination_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months_from_now.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 4,
            "nights_in_dst_to": 7,
            "flight_type": "round",
            "curr": "EUR",
            "select_airlines": "0B",  # avoid blue air
            "select_airlines_exclude": "True",
            "adults": 1,
            "sort": "price",
            "asc": "1"
        }
    elif destination_nights == "14_nights":
        params = {
            "fly_from": origin_destination,
            "fly_to": city_destination_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months_from_now.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 6,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "curr": "EUR",
            "select_airlines": "0B",  # avoid blue air
            "select_airlines_exclude": "True",
            "adults": 1,
            "sort": "price",
            "asc": "1"
        }

    def no_stopover():
        try:
            params["max_stopovers"] = 0
            flight_response = requests.get(url=API_ENDPOINT_SEARCH, params=params, headers=HEADERS)
            flight_data = flight_response.json()["data"][0]
            # print(flight_data)
            current_flight_data_0 = FlightData(
                flight_price=flight_data["price"],
                origin_city=flight_data["route"][0]["cityFrom"],
                origin_airport=flight_data["route"][0]["flyFrom"],
                destination_city=flight_data["route"][0]["cityTo"],
                destination_airport=flight_data["route"][0]["flyTo"],
                destination_country=flight_data["countryTo"]["name"],
                out_date=flight_data["route"][0]["local_departure"].split("T")[0],
                return_date=flight_data["route"][1]["local_departure"].split("T")[0],
                nights_in_destination=flight_data["nightsInDest"],
                flight_ticket=flight_data["deep_link"]
            )
            values_dict["current_flight_data_0"] = current_flight_data_0.flight_price
            return current_flight_data_0
        except IndexError:
            return

    def one_stopover():
        try:
            params["max_stopovers"] = 2
            flight_response = requests.get(url=API_ENDPOINT_SEARCH, params=params, headers=HEADERS)
            flight_data = flight_response.json()["data"][0]
            # print(flight_data)
            current_flight_data_1 = FlightData(
                flight_price=flight_data["price"],
                origin_city=flight_data["route"][0]["cityFrom"],
                origin_airport=flight_data["route"][0]["flyFrom"],
                destination_city=flight_data["cityTo"],
                destination_airport=flight_data["flyTo"],
                destination_country=flight_data["countryTo"]["name"],
                out_date=flight_data["route"][0]["local_departure"].split("T")[0],
                return_date=flight_data["route"][-1]["local_departure"].split("T")[0],
                nights_in_destination=flight_data["nightsInDest"],
                stop_overs=1,
                flight_ticket=flight_data["deep_link"]
            )
            values_dict["current_flight_data_1"] = current_flight_data_1.flight_price
            # route_dict = []
            # for _ in flight_data["route"]:
            #     route_dict.append(_['cityFrom'])
            # print(f"route_dict: {route_dict}")
            return current_flight_data_1
        except IndexError:
            return

    def two_stopover():
        try:
            params["max_stopovers"] = 4
            flight_response = requests.get(url=API_ENDPOINT_SEARCH, params=params, headers=HEADERS)
            flight_data = flight_response.json()["data"][0]
            # print(flight_data)
            current_flight_data_2 = FlightData(
                flight_price=flight_data["price"],
                origin_city=flight_data["route"][0]["cityFrom"],
                origin_airport=flight_data["route"][0]["flyFrom"],
                destination_city=flight_data["cityTo"],
                destination_airport=flight_data["flyTo"],
                destination_country=flight_data["countryTo"]["name"],
                out_date=flight_data["route"][0]["local_departure"].split("T")[0],
                return_date=flight_data["route"][-1]["local_departure"].split("T")[0],
                nights_in_destination=flight_data["nightsInDest"],
                stop_overs=2,
                flight_ticket=flight_data["deep_link"]
            )
            values_dict["current_flight_data_2"] = current_flight_data_2.flight_price
            # route_dict = []
            # for _ in flight_data["route"]:
            #     route_dict.append(_['cityFrom'])
            # print(f"route_dict: {route_dict}")
            return current_flight_data_2
        except IndexError:
            return

    test_1 = no_stopover()
    test_2 = one_stopover()
    test_3 = two_stopover()

    sorted_dict = {k: v for k, v in sorted(values_dict.items(), key=lambda item: item[1])}
    cheapest_flight = list(sorted_dict.keys())[0]

    if cheapest_flight == "current_flight_data_2":
        return test_3
    elif cheapest_flight == "current_flight_data_1":
        return test_2
    elif cheapest_flight == "current_flight_data_0":
        return test_1
    else:
        return test_1


class NotificationManager:
    """Configures and sends the email"""

    def __init__(self):
        """Configures the email's credentials"""

        self.sender_address = "my.pythondroid@gmail.com"
        self.sender_pass = "juawybogorauuxfz"
        self.mail_content = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style type="text/css">
          table {
            background: white;
            border-radius:3px;
            border-collapse: collapse;
            height: auto;
            max-width: 900px;
            padding:5px;
            width: 100%;
            animation: float 5s infinite;
          }
          th {
            color:#D5DDE5;;
            background:#1b1e24;
            border-bottom: 4px solid #9ea7af;
            font-size:14px;
            font-weight: 300;
            padding:10px;
            text-align:center;
            vertical-align:middle;
          }
          tr {
            border-top: 1px solid #C1C3D1;
            border-bottom: 1px solid #C1C3D1;
            border-left: 1px solid #C1C3D1;
            color:#666B85;
            font-size:16px;
            font-weight:normal;
          }
          tr:hover td {
            background:#4E5066;
            color:#FFFFFF;
            border-top: 1px solid #22262e;
          }
          td {
            background:#FFFFFF;
            padding:10px;
            text-align:left;
            vertical-align:middle;
            font-weight:300;
            font-size:13px;
            border-right: 1px solid #C1C3D1;
          }
          td:nth-child(n+4):nth-child(-n+6) {
          text-align:center;
          background-color:blue;
          }
        </style>
      </head>
      <body>
        <h2>Today's best flight deals:</h2>"""

    def update_email_list(self):
        """Reads the emails with new user's credentials and updates the google sheet"""

        # https://www.systoolsgroup.com/imap/
        gmail_host = 'imap.gmail.com'

        # set connection
        mail = imaplib.IMAP4_SSL(gmail_host)

        # login
        mail.login(self.sender_address, self.sender_pass)

        # select inbox
        mail.select("INBOX")

        # select specific mails
        _, selected_mails = mail.search(None, '(SUBJECT "New member alert")')

        # total number of mails from specific user
        selected_mails_list = selected_mails[0].split()
        # print("Total Messages from webwave@webwavecms.com:", len(selected_mails_list))
        query_list = []
        for num in selected_mails_list:
            # _, data = mail.fetch(num, '(RFC822)')
            # _, bytes_data = data[0]
            _, data = mail.fetch(num, '(RFC822)')
            bytes_data = data[0][1]

            # convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)

            for part in email_message.walk():
                # print(part.__getitem__("div"))
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    message = part.get_payload(decode=True)

                    message_object = email.message_from_string(message.decode())
                    soup = BeautifulSoup(message_object.get_payload(), "html.parser")
                    mail_content = soup.find_all(name="div", class_="content")

                    content_str = ""
                    for content in mail_content:
                        content_str += content.getText().strip() + " "
                    data_list = (content_str.split())
                    first_name = data_list[1]
                    last_name = data_list[2]
                    email_data = data_list[0].lower()
                    credentials_dict = {
                        "First Name": first_name,
                        "Last Name": last_name,
                        "Email": email_data
                    }
                    query_list.append(credentials_dict)
        return query_list

    def create_email(self):
        """Append the flight details for each found flight deal to the mail_content and send the email"""

        with open("destination_data.json", "r") as data_file:  # /home/ruganar/FlightDealPrivate/
            destination_data = json.load(data_file)

        data_dict = {}
        pandas_df = pd.DataFrame(data_dict, columns=["Destination Country:", "Fly from:", "Fly to:", "Stop overs:",
                                                     "Departure/Return:", "Nights:", "Ticket:", "Fare:"])

        for nights_list in destination_data:  # destination_data[:-3:-1]:  # the last two items, reversed
            for city in destination_data[nights_list]:  # {key: [{}, {}], key: [{}, {}], key: [{}, {}]}
                try:
                    flight = check_flights(origin_destination="OTP", city_destination_code=city["IATA Code"],
                                           destination_nights=nights_list)
                    # flight = check_flights(origin_destination="CLJ", city_destination_code="CFU",
                    #                        destination_nights=nights_list)
                    if flight.stop_overs == 2:
                        pandas_df.loc[len(pandas_df)] = [flight.destination_country,
                                                         f"{flight.origin_city}-{flight.origin_airport}",
                                                         f"{flight.destination_city}-{flight.destination_airport}", 2,
                                                         f"{flight.out_date} to {flight.return_date}",
                                                         flight.nights_in_destination,
                                                         f"<a href={flight.flight_ticket}>Buy ticket!</a>",
                                                         flight.flight_price]

                    elif flight.stop_overs == 1:
                        pandas_df.loc[len(pandas_df)] = [flight.destination_country,
                                                         f"{flight.origin_city}-{flight.origin_airport}",
                                                         f"{flight.destination_city}-{flight.destination_airport}", 1,
                                                         f"{flight.out_date} to {flight.return_date}",
                                                         flight.nights_in_destination,
                                                         f"<a href={flight.flight_ticket}>Buy ticket!</a>",
                                                         flight.flight_price]

                    else:
                        pandas_df.loc[len(pandas_df)] = [flight.destination_country,
                                                         f"{flight.origin_city}-{flight.origin_airport}",
                                                         f"{flight.destination_city}-{flight.destination_airport}", 0,
                                                         f"{flight.out_date} to {flight.return_date}",
                                                         flight.nights_in_destination,
                                                         f"<a href={flight.flight_ticket}>Buy ticket!</a>",
                                                         flight.flight_price]

                    break
                except IndexError:
                    continue
        sorted_df = pandas_df.sort_values("Fare:")
        table_df = sorted_df.to_html()
        self.mail_content += html.unescape(table_df)

        # End of the email
        self.mail_content += """<br><br>
        <p><i>Ensure that you open the ticket link in a private window to get the actual price, 
        however the price can change at any time. If you wish to 
        unsubscribe from this email, please reply with "Unsubscribe".</i></p>
        <p>My flight club can be found <a href=https://y3kksc.webwave.dev/info>here</a> and feel free to share it.</p>
        <h2>Happy Travels,<br>Adrian Mihăilă</h2>
        </body></html>"""

        # Get the email list
        email_list = [row["Email"].strip() for row in sheet_data_users]  # call the old list
        new_email_list = self.update_email_list()  # call the new email list of dictionaries

        # Update the sheet with new users
        if len(new_email_list) != 0:
            for credentials_dict in new_email_list:
                if credentials_dict["Email"] in email_list:
                    continue
                else:
                    print("New user found")
                    email_list.append(credentials_dict["Email"])
                    query = [credentials_dict]
                    add_new_user = requests.post(url=STEINHQ_ENDPOINT_U, json=query, headers=STEINHQ_HEADER)
                    add_new_user.raise_for_status()

        # Send the email to each recipient
        for _ in email_list[:1]:
            self.send_email(mail_content=self.mail_content, receiver_address_list=_.split())  # Send email

    def send_email(self, mail_content, receiver_address_list):
        """Sends the email"""

        receiver_address = receiver_address_list

        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = self.sender_address
        message["To"] = ", ".join(receiver_address)  # receiver_address Needs to be a STRING
        message["Subject"] = "Low price alert"  # The subject line

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, "html"))

        # Create SMTP session for sending the mail
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # enable security
            connection.login(self.sender_address, self.sender_pass)  # login with mail_id and password
            text = message.as_string()
            connection.sendmail(self.sender_address, receiver_address, text)  # receiver_address Needs to be a LIST
