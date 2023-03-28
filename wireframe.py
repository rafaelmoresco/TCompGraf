from typing import List
from coordenada import Coordenada2D
from objetos import Objetos

# Poligono
class Wireframe(Objetos):
    def __constraint_check(self):
        if len(self.__coordinates) < 3:
            raise Exception("Poligono precisa de no minimo 3 coordenadas")