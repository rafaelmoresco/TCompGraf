from typing import List, Tuple
from model.displayable import Displayable
from model.coordinate import Coordinate2D

class Dot(Displayable):
    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        super().__init__(name, coordinates)

    def __constraint_check(self):
        if len(self.get_coordinates()) != 1:
            raise Exception("A dot must have exactly one coordinate")