import random
from enum import Enum

class RouletteType(Enum):
    AMERICAN = "american"
    EUROPEAN = "european"
    FAIR = "fair"

class Roulette:
    def __init__(self, roulette_type: RouletteType):
        self.type = roulette_type
        self.red_numbers = {
            1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
        }
        self._initialize_wheel()

    def _initialize_wheel(self):
        if self.type == RouletteType.AMERICAN:
            self.numbers = list(range(0, 37)) + ['00']
            self.green_numbers = {0, '00'}
        elif self.type == RouletteType.EUROPEAN:
            self.numbers = list(range(0, 37))
            self.green_numbers = {0}
        elif self.type == RouletteType.FAIR:
            self.numbers = list(range(1, 37))
            self.green_numbers = set()
        
    def spin(self) -> dict:
        number = random.choice(self.numbers)
        color = (
            'green' if number in self.green_numbers else
            'red' if number in self.red_numbers else
            'black'
        )
        return {"number": number, "color": color}