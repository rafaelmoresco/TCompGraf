from typing import List
from coordenada import Coordenada
from dataclasses import dataclass
from objetos.objetos_mundo import WorldObject
from abc import abstractmethod

#Classe abstrata de objetos a serem desenhados
class Objetos(WorldObject):
    __nome: str
    __cor: str

    @dataclass
    class Drawable:
        linhas: List[List[Coordenada]]
        pontos: List[Coordenada]
        cor: str

    def __init__(self, nome: str, cor: str,  coordenadas: List[Coordenada] = None) -> None:
        super().__init__(coordinates=coordenadas)
        self._nome = nome
        self._cor = cor

    def get_nome(self) -> str:
        return self._nome

    def get_cor(self) -> str:
        return self._cor
        
    def set_cor(self, cor: str) -> None:
        # cor é '#rgb' ou '#rrggbb'
        self._cor = cor

    def get_drawable(self):
        return Objetos.Drawable(
            linhas=self._get_drawable_lines(),
            pontos=self._get_drawable_points(),
            cor=self._cor)

    @abstractmethod
    def _get_drawable_lines(self):
        pass

    @abstractmethod
    def _get_drawable_points(self):
        pass