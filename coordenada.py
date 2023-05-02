import math
from typing import List, Literal
from matriz_suporte import MatrixHelper
import numbers


class Coordenada(List):
    limit_size = -1

    def __init__(self, x):
        if self.limit_size != -1:
            super().__init__(x[0:self.limit_size].copy())
        else:
            super().__init__(x.copy())


    def __neg__(self):
        return type(self)([-e for e in self])

    def __add__(self, other):
        result = []
        for i in range(len(self)):
            result.append(self[i] + other[i])
        return type(self)(result)

    def __sub__(self, other):
        return self.__add__(-other)

    @property
    def length(self):
        result = 0
        for e in self:
            result += e*e
        return math.sqrt(result)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return type(self)([e * other for e in self])
        elif isinstance(other, Coordenada) and len(self) == len(other):
            return type(self)(MatrixHelper.cross(self, other))
        else:
            raise Exception(f'Coordinate can only be multiplied by numbers, not by {type(other)}')

    def normalize(self):
        return type(self)([e/self.length for e in self])

    @staticmethod
    def distancia(coord1, coord2) -> float:
        return (coord2-coord1).length

    @classmethod
    def up(cls):
        up = []
        for i in range(cls.limit_size):
            up.append(0 if i != 1 else 1)

        return cls(up)

        # Transforms coordinate based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        vector = self.copy()
        vector.append(float(1))
        vector = [vector]
        for t in transformations_matrices:
            vector = MatrixHelper.mul(vector, t)

        # Defines the new coordinates, by removing the third element in the matrix
        for i in range(len(self)):
            self[i] = vector[0][i]

    def rotate(self, angle, axis: Literal['x', 'y', 'z']):
        self.transform([MatrixHelper.get_rotation_matrix(angle, axis)])

    def translate(self, movement_vector):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])


class Coordenada2D(Coordenada):
    limit_size = 2
    def __init__(self, x, y: float = None):
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


class Coordenada3D(Coordenada2D):
    limit_size = 3
    
    def __init__(self, x, y: float = None, z: float = None):
        if isinstance(x, list):
            super(Coordenada3D, self).__init__(x)
        else:
            if z is None:
                z = 1
            super(Coordenada3D, self).__init__([x, y, z])

    @property
    def z(self):
        return self.__getitem__(2)

    @z.setter
    def z(self, value: float):
        self[2] = value
    
    def y_rotation_to_align_with_z(self): # angle to align with z
        h = Coordenada3D(self.copy())
        h.y = 0
        c = 1 if h.x >= 0 else -1
        if h.length == 0:
            return 0
        return c * math.degrees(math.acos(h.z / h.length))

    def x_rotation_to_align_with_z(self):# angle to align with z
        h = Coordenada3D(self.copy())
        h.x = 0
        c = 1 if h.y >= 0 else -1
        if h.length == 0:
            return 0
        return c * math.degrees(math.acos(h.z / h.length))

    def z_rotation_to_align_with_y(self):# angle to align with z
        h = Coordenada3D(self.copy())
        h.z = 0
        c = -1 if h.x >= 0 else 1
        if h.length == 0:
            return 0
        return c * math.degrees(math.acos(h.y / h.length))