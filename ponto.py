from typing import List, Tuple
from objetos import Objetos
from coordenada import Coordenada2D

class Ponto(Objetos):
    def __constraint_check(self):
        if len(self.__coordinates) != 1:
            raise Exception("Ponto precisa de uma coordenada")