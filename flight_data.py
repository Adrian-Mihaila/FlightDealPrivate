

class FlightData:
    """Structures the flight data."""

    def __init__(self, flight_price, origin_city, origin_airport, destination_city,
                 destination_airport, destination_country, out_date, return_date,
                 flight_ticket, stop_overs=0, nights_in_destination=""):

        self.flight_price = flight_price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.destination_country = destination_country
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.flight_ticket = flight_ticket
        self.nights_in_destination = nights_in_destination
