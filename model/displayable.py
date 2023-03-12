from typing import List
from model.coordinate import Coordinate2D

# Abstract class
class Displayable:
    # private attributes
    __name: str
    __coordinates: List[Coordinate2D]

    def __init__(self, name: str, coordinates: List[Coordinate2D] = None) -> None:
        self.__name = name
        self.__coordinates = coordinates
        self.__constraint_check()
        if not issubclass(type(self), Displayable):
            raise Exception("Displayable is an abstract class, it is not supposed to be instantiated")

    # public methods
    def add_coordinate(self, x, y):
        self.__coordinates.append(Coordinate2D(x, y))
        self.__constraint_check()

    def get_coordinates(self) -> List[Coordinate2D]:
        return self.__coordinates
    
    def get_name(self) -> str:
        return self.__name

    def __constraint_check(self):
        pass