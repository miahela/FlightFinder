import json
from typing import List
from classes.Line import Line
import logging

class CompletedLines:
    completed_lines: List[Line] = []
    folder_to_save = "data"

    def __init__(self):
        self.completed_lines = self.read_completed_lines()
    
    def add_completed_line(self, completed_line: Line):
        if not self.check_if_duplicate_line(completed_line):
            self.completed_lines.append(completed_line)
            try:
                with open(f"{self.folder_to_save}/completed_lines.jsonl", "a") as f:
                    f.write(json.dumps(completed_line.__dict__) + "\n")
            except Exception as e:
                logging.error(e)
                print("--ERROR-- saving flight to file")

    def check_if_duplicate_line(self, lineToCheck: Line):
        for flight in self.completed_lines:
            if flight.departure == lineToCheck.departure and flight.arrival == lineToCheck.arrival and flight.departure_date == lineToCheck.departure_date:
                return True
        return False
    
    def read_completed_lines(self):
        completed_lines: List[Line] = []
        try:
            with open(f"{self.folder_to_save}/completed_lines.jsonl", "r") as f:
                for line in f:
                    lineRead = json.loads(line)
                    flight = Line(lineRead["departure"], lineRead["arrival"], lineRead["departure_date"])
                    completed_lines.append(flight)
            return completed_lines
        except Exception as e:
            logging.error(e)
            print("--ERROR-- reading completed flights from file")
            return completed_lines
        