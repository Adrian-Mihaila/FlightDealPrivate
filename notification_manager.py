from data_manager import DataManager
from flight_search import FlightSearch
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sheet_data = DataManager().get_destination_data()
sheet_data_users = DataManager().get_email_list()
search = FlightSearch()


class NotificationManager:
    """Configures and sends the email"""

    def __init__(self):
        """Configures the email addresses and password"""

        self.sender_address = "mihaila.adrian.and.joanne@gmail.com"
        self.sender_pass = "oebxjqjkuolumvlf"
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
        </style>
      </head>
      <body>
        <h2>Today's best flight deals:</h2>
      <table>
      <thead>
            <tr style="border: 1px solid #1b1e24;">
                <tr>
                  <th>Destination Country:</th>
                  <th>Fly from:</th>
                  <th>Fly to:</th>
                  <th>Stop overs:</th>
                  <th>Dates:</th>
                  <th>Ticket:</th>
                  <th>Fare:</th>
                </tr> """

    def create_email(self):
        """Append the flight details for each found flight deal to the mail_content and send the email"""

        for row in sheet_data:
            try:
                flight = search.check_flights(origin_destination="OTP", city_destination_code=row["IATA Code"])
                if flight.flight_price < int(row["Lowest Price"]):
                    if flight.stop_overs > 0:
                        self.mail_content += f"<tr><td>✈️{flight.destination_country}</td>" \
                                        f"<td>{flight.origin_city}-{flight.origin_airport}</td>" \
                                        f"<td>{flight.destination_city}-{flight.destination_airport}</td>" \
                                        f"<td>{flight.stop_overs} stop over, via {flight.via_city}</td>" \
                                        f"<td>{flight.out_date} to {flight.return_date}</td>" \
                                        f"<td><a href={flight.flight_ticket}>Buy ticket!</a></td>" \
                                        f"<td>€{flight.flight_price}</td></tr>"
                    else:
                        self.mail_content += f"<tr><td>✈️{flight.destination_country}</td>" \
                                        f"<td>{flight.origin_city}-{flight.origin_airport}</td>" \
                                        f"<td>{flight.destination_city}-{flight.destination_airport}</td>" \
                                        f"<td>No stop overs</td>" \
                                        f"<td>{flight.out_date} to {flight.return_date}</td>" \
                                        f"<td><a href={flight.flight_ticket}>Buy ticket!</a></td>" \
                                        f"<td>€{flight.flight_price}</td></tr>"
            except IndexError:
                continue

        # Send the email
        self.mail_content += "</thead></table></body></html><br><br><h3>Regards,<br>Adrian Mihăilă</h2>"
        email_list = [row["Email"] for row in sheet_data_users]

        for email in email_list:
            self.send_email(mail_content=self.mail_content, receiver_address_list=email.split())
        # print(email_list)

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
        print("Mail Sent")
