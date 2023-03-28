from typing import List
from coordenada import Coordenada2D
from matriz_suporte import  MatrixHelper

#Classe abstrata de objetos a serem desenhados
class Objetos:
    __nome: str
    __cor: str
    __coordenadas: List[Coordenada2D]

    def __init__(self, nome: str, cor: str,  coordenadas: List[Coordenada2D] = None) -> None:
        self.__nome = nome
        self.__cor = cor
        self.__coordenadas = coordenadas

    def add_coordenada(self, x, y):
        self.__coordenadas.append(Coordenada2D(x, y))

    def get_coordenadas(self) -> List[Coordenada2D]:
        return self.__coordenadas
    
    def get_nome(self) -> str:
        return self.__nome

    def get_cor(self) -> str:
        return self.__cor
        
    def set_cor(self, cor: str) -> None:
        # cor é '#rgb' ou '#rrggbb'
        self.__cor = cor

    def rotate(self, angle):
        self.transform([MatrixHelper.rotation_matrix(angle)])

    def translate(self, movement_vector: Coordenada2D):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector: Coordenada2D):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])

    # Transforma os poligonos representado pelas matrizes
    def transform(self, transformations_matrices: list):
        for coord in self.__coordenadas:
            coord.transform(transformations_matrices)

    def get_center_coord(self):
        sum_x = 0
        sum_y = 0
        for coord in self.__coordenadas:
            sum_x += coord.x
            sum_y += coord.y

        l = float(len(self.__coordenadas))
        return Coordenada2D(sum_x/l, sum_y/l)

    def rotate_around_self(self, angle: float):
        self.rotate_around_point(angle=angle, point=self.get_center_coord())

    def scale_around_self(self, scale_vector: Coordenada2D):
        center_coord = self.get_center_coord()
        self.transform([
            # Translada pra origem
            MatrixHelper.translation_matrix(-center_coord),
            # Escala
            MatrixHelper.scale_matrix(scale_vector),
            # Translada de volta para a posição original
            MatrixHelper.translation_matrix(center_coord)
        ])

    def rotate_around_point(self, angle: float, point: Coordenada2D):
        translation_vector = point
        self.transform([
            # Translada pra origem
            MatrixHelper.translation_matrix(-translation_vector),
            # Rotaciona
            MatrixHelper.rotation_matrix(angle),
            # Translada de volta para a posição original
            MatrixHelper.translation_matrix(translation_vector)
        ])