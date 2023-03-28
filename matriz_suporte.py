from __future__ import annotations
from math import pi
from typing import List, TYPE_CHECKING
from math import cos, sin
from itertools import starmap
from operator import mul

if TYPE_CHECKING:
    from coordenada import Coordenada2D


class MatrixHelper:
    @staticmethod
    def degrees_to_radians(angle: float) -> float:
        return angle * (pi/180)

    @staticmethod
    def dot(vector: List[float], matrix: List[List[float]]) -> List[List[float]]:
        return [sum(starmap(mul, zip(vector, col))) for col in zip(*matrix)]

    @staticmethod
    # Recebe o vetor da translação e retorna a matriz para aplicar a operação
    def translation_matrix(v: Coordenada2D) -> List[List[float]]:
        return [
            [1,   0,   0],
            [0,   1,   0],
            [v.x, v.y, 1]
        ]

    @staticmethod
    def scale_matrix(s: Coordenada2D) -> List[List[float]]:
        return [
            [s.x, 0,  0],
            [0,  s.y, 0],
            [0,  0,   1]
        ]

    # Cria matriz de rotação com o angulo recebido de parametro
    @staticmethod
    def rotation_matrix(angle: float) -> List[List[float]]:
        a = MatrixHelper.degrees_to_radians(angle)
        return [
            [cos(a), -sin(a), 0],
            [sin(a),  cos(a), 0],
            [  0,       0,    1]
        ]