import json

class Line:
    def __init__(self, departure, arrival, departure_date):
        self.departure = departure
        self.arrival = arrival
        self.departure_date = departure_date
        self.link = (
                "https://www.skyscanner.com/transport/flights/"
                + self.departure
                + "/"
                + self.arrival
                + "/"
                + departure_date
                + "/"
                + "?adultsv2=1&cabinclass=economy&childrenv2=&currency=EUR&inboundaltsenabled=false&is_banana_refferal=true&outboundaltsenabled=false&qp_prevScreen=HOMEPAGE&ref=home&rtn=0&stops=!direct"
            )

    def toJson(self):
        return json.dumps(self.__dict__)