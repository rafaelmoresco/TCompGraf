from typing import List
from coordenada import Coordenada2D
from objetos import Objetos

# Poligono
class Wireframe(Objetos):
    def __constraint_check(self):
        if len(self.__coordinates) < 3:
            raise Exception("A wireframe have a least 3 coordinates")