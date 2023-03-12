from typing import List
from model.coordinate import Coordinate2D
from model.displayable import Displayable

class Wireframe(Displayable):
    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        super().__init__(name, coordinates)

    def __constraint_check(self):
        if len(self.__cordinates) < 3:
            raise Exception("A wireframe have a least 3 coordinates")