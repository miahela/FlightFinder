from classes.Line import Line
from typing import List, Tuple
import datetime

class AllLines:
    all_lines: List[Line] = []

    def __init__(self, departures: List[str], arrivals: List[str], start_date: str, end_date: str):
        self.all_lines = self.create_all_lines(departures, arrivals, start_date, end_date)

    def create_all_lines(self, departures: List[str], arrivals: List[str], start_date: str, end_date: str):
        all_lines: List[Line] = []
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        delta = end_date - start_date

        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            formatted_date = day.strftime('%y%m%d')
            for departure in departures:
                for arrival in arrivals:
                    all_lines.append(Line(departure, arrival, formatted_date))
        return all_lines

    def get_all_lines(self):
        return self.all_lines
    

    @staticmethod
    def run_tests():
        departures = ["SKP", "JFK"]
        arrivals = ["MAD", "LAX"]
        start_date = "2023-05-01"
        end_date = "2023-05-10"
        lines = AllLines(departures, arrivals, start_date, end_date)

        assert len(lines.get_all_lines()) == 40, "Should have 20 Line objects for 2 departures, 2 arrivals and 5 days"

        print("All tests passed!")

if __name__ == "__main__":
    AllLines.run_tests()
