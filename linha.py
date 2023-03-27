from typing import List
from coordenada import Coordenada2D
from objetos import Objetos

class Linha(Objetos):

    def __constraint_check(self):
        if len(self.__coordinates) != 2:
            raise Exception("A line must have exactly two coordinates")