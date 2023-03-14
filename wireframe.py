from typing import List
from coordenada import Coordenada2D
from objetos import Objetos

class Wireframe(Objetos):
    def __init__(self, nome: str, coordenadas: List[Coordenada2D] = None) -> None:
        super().__init__(nome, coordenadas)

    def __verificador_de_limites(self):
        if len(self.__cordinates) < 3:
            raise Exception("A wireframe have a least 3 coordinates")