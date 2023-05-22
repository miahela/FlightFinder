import json

class Flight:
    def __init__(self, departure, arrival, departure_date, arrival_date, travel_time, price, link):
        self.departure = departure
        self.arrival = arrival
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.travel_time = travel_time
        self.price = price
        self.link = link

    def toJson(self):
        return json.dumps(self.__dict__)