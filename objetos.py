from typing import List
from coordenada import Coordenada2D

#Classe abstrata de objetos a serem desenhados
class Objetos:
    __nome: str
    __coordenadas: List[Coordenada2D]

    def __init__(self, nome: str, coordenadas: List[Coordenada2D] = None) -> None:
        self.__nome = nome
        self.__coordenadas = coordenadas

    def add_coordenada(self, x, y):
        self.__coordenadas.append(Coordenada2D(x, y))

    def get_coordenadas(self) -> List[Coordenada2D]:
        return self.__coordenadas
    
    def get_nome(self) -> str:
        return self.__nome