from dataclasses import dataclass


@dataclass
class ElectricityReading:
    time: int
    reading: float

    def __init__(self, json):

        if not isinstance(json, dict):
            raise ValueError("The provided input must be a Dictionary.")

        if "time" not in json:
            raise ValueError("The time is missing!")
        if "reading" not in json:
            raise ValueError("The reading are missing!")
        
        try:
            self.time = int(json["time"])
            self.reading = float(json["reading"])
        except (ValueError, TypeError) as e:
            raise ValueError("The Invalid Data!")
        
        if self.reading < 0:
            raise ValueError("Reading can not be negative!")
        
        if self.time <= 0:
            raise ValueError("The time must be positive!")
        
        
    def to_json(self):
        return {
            "time": self.time,
            "reading": self.reading,
        }
