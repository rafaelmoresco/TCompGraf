from typing import List
from coordenada import Coordenada2D
from objetos import Objetos

class Linha(Objetos):
    def __init__(self, nome: str, coordenadas: List[Coordenada2D] = None) -> None:
        super().__init__(nome, coordenadas)
