from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import time

sheet_data = DataManager().get_destination_data()
sheet_data_users = DataManager().get_email_list()
search = FlightSearch()
notification_manager = NotificationManager()


# # Get the destination code for each city in the google sheet and update it
# print(sheet_data)
# for row in sheet_data:
#     if row["iataCode"] == "":
#         updated_row = {
#             "price": {
#                 "iataCode": search.get_destination_code(row["city"])
#             }
#         }
#         requests.put(url=f"{SHEETY_ENDPOINT}/{row['id']}", json=updated_row, headers=SHEETY_HEADER)

# Update prices in google sheet
# for row in sheet_data:
#     try:
#         flight = search.check_flights(origin_destination="OTP", city_destination_code=row["IATA Code"])
#         updated_row = {
#             "Lowest Price": flight.flight_price + 10
#         }
#         x = requests.put(url=f"{STEINHQ_ENDPOINT}", json=updated_row, headers=STEINHQ_HEADER)
#         x.raise_for_status()
#     except IndexError:
#         continue

# # Send email for best deals

def create_email():
    mail_content = """
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

    # Append the flight details for each found flight deal to the mail_content
    for row in sheet_data:
        try:
            flight = search.check_flights(origin_destination="OTP", city_destination_code=row["IATA Code"])
            if flight.flight_price < int(row["Lowest Price"]):
                if flight.stop_overs > 0:
                    mail_content += f"<tr><td>✈️{flight.destination_country}</td>" \
                                    f"<td>{flight.origin_city}-{flight.origin_airport}</td>" \
                                    f"<td>{flight.destination_city}-{flight.destination_airport}</td>" \
                                    f"<td>{flight.stop_overs} stop over, via {flight.via_city}</td>" \
                                    f"<td>{flight.out_date} to {flight.return_date}</td>" \
                                    f"<td><a href={flight.flight_ticket}>Buy ticket!</a></td>" \
                                    f"<td>€{flight.flight_price}</td></tr>"
                else:
                    mail_content += f"<tr><td>✈️{flight.destination_country}</td>" \
                                    f"<td>{flight.origin_city}-{flight.origin_airport}</td>" \
                                    f"<td>{flight.destination_city}-{flight.destination_airport}</td>" \
                                    f"<td>No stop overs</td>" \
                                    f"<td>{flight.out_date} to {flight.return_date}</td>" \
                                    f"<td><a href={flight.flight_ticket}>Buy ticket!</a></td>" \
                                    f"<td>€{flight.flight_price}</td></tr>"
        except IndexError:
            continue

    # Send the email
    mail_content += "</thead></table></body></html><br><br><h3>Regards,<br>Adrian Mihăilă</h2>"
    email_list = [row["Email"] for row in sheet_data_users]

    for email in email_list:
        notification_manager.send_email(mail_content=mail_content, receiver_address_list=email.split())
    # print(email_list)


# Run the method only once every day
create_email()
# while True:
#     time.sleep(60)
#     if
