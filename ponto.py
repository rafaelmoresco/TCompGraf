from typing import List, Tuple
from objetos import Objetos
from coordenada import Coordenada2D

class Ponto(Objetos):
    def __init__(self, nome: str, coordenadas: List[Coordenada2D] = None) -> None:
        super().__init__(nome, coordenadas)