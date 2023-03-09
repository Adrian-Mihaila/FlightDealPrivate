import requests
from datetime import datetime, timedelta
from flight_data import FlightData

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=180)

API_KEY = "8nrhLLE0o2OiHKRLWq0GDuWbKkQ2DKJh"
API_ENDPOINT_QUERY = "https://tequila-api.kiwi.com/locations/query"
API_ENDPOINT_SEARCH = "https://tequila-api.kiwi.com/v2/search"
HEADERS = {
    "apikey": API_KEY
}


class FlightSearch:
    """Returns Flight destination code."""

    def check_flights(self, origin_destination, city_destination_code):
        """Passes the parameters, requests all the flight details from API
        and save only the required ones to print the destination city and the price"""
        values_dict = {}
        params = {
            "fly_from": origin_destination,
            "fly_to": city_destination_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months_from_now.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 16,
            "flight_type": "round",
            # "one_for_city": 1,  # return cheapest flights but doesn't work with round trips
            "curr": "EUR",
            "select_airlines": "0B",  # avoid blue air
            "select_airlines_exclude": "True",
            "sort": "price",
            "asc": "1"
        }

        def no_stopover():
            try:
                params["max_stopovers"] = 0
                flight_response = requests.get(url=API_ENDPOINT_SEARCH, params=params, headers=HEADERS)
                flight_data = flight_response.json()["data"][0]

                current_flight_data_0 = FlightData(
                    flight_price=flight_data["price"],
                    origin_city=flight_data["route"][0]["cityFrom"],
                    origin_airport=flight_data["route"][0]["flyFrom"],
                    destination_city=flight_data["route"][0]["cityTo"],
                    destination_airport=flight_data["route"][0]["flyTo"],
                    destination_country=flight_data["countryTo"]["name"],
                    out_date=flight_data["route"][0]["local_departure"].split("T")[0],
                    return_date=flight_data["route"][1]["local_departure"].split("T")[0],
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

                current_flight_data_1 = FlightData(
                    flight_price=flight_data["price"],
                    origin_city=flight_data["route"][0]["cityFrom"],
                    origin_airport=flight_data["route"][0]["flyFrom"],
                    destination_city=flight_data["cityTo"],
                    destination_airport=flight_data["flyTo"],
                    destination_country=flight_data["countryTo"]["name"],
                    out_date=flight_data["route"][0]["local_departure"].split("T")[0],
                    return_date=flight_data["route"][-1]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city_1=flight_data["route"][0]["cityTo"],
                    flight_ticket=flight_data["deep_link"]
                )
                values_dict["current_flight_data_1"] = current_flight_data_1.flight_price
                return current_flight_data_1
            except IndexError:
                return

        def two_stopover():
            try:
                params["max_stopovers"] = 4
                flight_response = requests.get(url=API_ENDPOINT_SEARCH, params=params, headers=HEADERS)
                flight_data = flight_response.json()["data"][0]
                print(flight_data)
                current_flight_data_2 = FlightData(
                    flight_price=flight_data["price"],
                    origin_city=flight_data["route"][0]["cityFrom"],
                    origin_airport=flight_data["route"][0]["flyFrom"],
                    destination_city=flight_data["cityTo"],
                    destination_airport=flight_data["flyTo"],
                    destination_country=flight_data["countryTo"]["name"],
                    out_date=flight_data["route"][0]["local_departure"].split("T")[0],
                    return_date=flight_data["route"][-1]["local_departure"].split("T")[0],
                    stop_overs=2,
                    flight_ticket=flight_data["deep_link"]
                )
                values_dict["current_flight_data_2"] = current_flight_data_2.flight_price
                return current_flight_data_2
            except IndexError:
                return

        test_1 = no_stopover()
        test_2 = one_stopover()
        test_3 = two_stopover()

        sorted_dict = {k: v for k, v in sorted(values_dict.items(), key=lambda item: item[1])}
        print(sorted_dict)
        cheapest_flight = next(iter(sorted_dict))

        if cheapest_flight == "current_flight_data_2":
            return test_3
        elif cheapest_flight == "current_flight_data_1":
            return test_2
        elif cheapest_flight == "current_flight_data_0":
            return test_1

    def get_destination_code(self, city_name):
        """Returns the flight code according to the destination's city name"""

        params = {
            "term": city_name,
            "location_types": "city"
        }
        flight_response = requests.get(url=API_ENDPOINT_QUERY, params=params, headers=HEADERS)
        flight_code = flight_response.json()["locations"][0]["code"]
        return flight_code
