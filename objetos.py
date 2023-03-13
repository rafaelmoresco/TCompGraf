from typing import List
from coordenada import Coordenada2D

class Objetos:
    __nome: str
    __coordenadas: List[Coordenada2D]

    def __init__(self, nome: str, coordenadas: List[Coordenada2D] = None) -> None:
        self.__nome = nome
        self.__coordenadas = coordenadas
        self.__verificador_de_limites()
        if not issubclass(type(self), Objetos):
            raise Exception("Displayable is an abstract class, it is not supposed to be instantiated")

    def add_coordinate(self, x, y):
        self.__coordenadas.append(Coordenada2D(x, y))
        self.__verificador_de_limites()

    def get_coordinates(self) -> List[Coordenada2D]:
        return self.__coordenadas
    
    def get_nome(self) -> str:
        return self.__nome

    def __verificador_de_limites(self):
        pass