from notification_manager import NotificationManager
# from datetime import datetime, timedelta
# import time

notification_manager = NotificationManager()

# # Get the destination code for each city in the google sheet and update it
# def get_destination_code(self, city_name):
#     """Returns the flight code according to the destination's city name"""
#
#     params = {
#         "term": city_name,
#         "location_types": "city"
#     }
#     flight_response = requests.get(url=API_ENDPOINT_QUERY, params=params, headers=HEADERS)
#     flight_code = flight_response.json()["locations"][0]["code"]
#     return flight_code
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

# # Run the method only once every day
# notification_manager.create_email()  # only for testing
# while True:
#     today = datetime.today()
#     tomorrow = today.replace(day=today.day, hour=5, minute=0, second=0, microsecond=0) + timedelta(days=1)
#     delta_t = tomorrow-today
#
#     seconds_remaining = delta_t.seconds+1
#     print(f'Remaining seconds: {seconds_remaining}')
#     time.sleep(seconds_remaining)
#     notification_manager.create_email()
#     print("Mail Sent")
notification_manager.create_email()
print("Mail Sent")
