from typing import List
from matriz_suporte import MatrixHelper

# Precisamos implementar a classe Coordenada2D de verdade dessa vez
class Coordenada2D(List):

    def __init__(self, x, y: float):
        if isinstance(x, list):
            super(Coordenada2D, self).__init__(x)
        else:
            super(Coordenada2D, self).__init__([x, y])

    @property
    def x(self):
        return self.__getitem__(0)

    @x.setter
    def x(self, value: float):
        self[0] = value

    @property
    def y(self):
        return self.__getitem__(1)

    @y.setter
    def y(self, value: float):
        self[1] = value

    def __neg__(self):
        return Coordenada2D(-self.x, -self.y)

    def __add__(self, other):
        return Coordenada2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    # Transforma as coordenadas
    def transform(self, transformations_matrices: list):
        vector = self.copy()
        vector.append(float(1))
        for t in transformations_matrices:
            vector = MatrixHelper.dot(vector, t)

        # Define as novas coordenadas removendo o terceiro elemento da matriz
        self.x = vector[0]
        self.y = vector[1]

    def rotate(self, angle):
        self.transform([MatrixHelper.rotation_matrix(angle)])

    def translate(self, movement_vector):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])