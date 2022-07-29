import requests

# SHEETY_ENDPOINT = "https://api.sheety.co/0c245a21a61b260b01e5fd774a4dabfc/flightDeals/prices"
# SHEETY_HEADER = {"Authorization": "Basic YWRyaWFubWloYWlsYTpEbG9qJGx0JnI8cl4+d3x6NkkqOA=="}
STEINHQ_ENDPOINT = "https://api.steinhq.com/v1/storages/62de759bbca21f053ea568cb/prices"
STEINHQ_ENDPOINT_U = "https://api.steinhq.com/v1/storages/62de759bbca21f053ea568cb/users"
STEINHQ_HEADER = {"Authorization": "Basic YWRyaWFubWloYWlsYTpEbG9qJGx0JnI8cl4+d3x6NkkqOA=="}


class DataManager:
    """Returns Google Sheet rows in a list."""

    def __init__(self):
        self.sheet_response = requests.get(url=STEINHQ_ENDPOINT, headers=STEINHQ_HEADER)  # for prices
        self.sheet_response_u = requests.get(url=STEINHQ_ENDPOINT_U, headers=STEINHQ_HEADER)  # for users
        self.destination_data = {}

    def get_destination_data(self):
        self.destination_data = self.sheet_response.json()  # ["prices"] only for sheety
        # print(self.destination_data)
        return self.destination_data

    def get_email_list(self):
        users_data = self.sheet_response_u.json()
        return users_data
