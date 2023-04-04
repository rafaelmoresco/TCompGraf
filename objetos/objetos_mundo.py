from coordenada import Coordenada2D
from typing import List
from matriz_suporte import MatrixHelper
from abc import ABC, abstractmethod


class WorldObject(ABC):
    _coordinates: List[Coordenada2D]

    def __init__(self, coordinates: List[Coordenada2D]) -> None:
        self._coordinates = coordinates
        self._constraint_check()

    def add_coordinate(self, x, y):
        self._coordinates.append(Coordenada2D(x, y))
        self._constraint_check()

    def get_coordinates(self) -> List[Coordenada2D]:
        return self._coordinates

    @abstractmethod
    def _constraint_check(self):
        pass

    def rotate(self, angle):
        self.transform([MatrixHelper.rotation_matrix(angle)])

    def translate(self, movement_vector: Coordenada2D):
        self.transform([MatrixHelper.translation_matrix(movement_vector)])

    def scale(self, scale_vector: Coordenada2D):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])

    # Transforms polygon based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        for coord in self._coordinates:
            coord.transform(transformations_matrices)

    def get_center_coord(self):
        sum_x = 0
        sum_y = 0
        for coord in self._coordinates:
            sum_x += coord.x
            sum_y += coord.y

        l = float(len(self._coordinates))
        return Coordenada2D(sum_x/l, sum_y/l)

    def rotate_around_self(self, angle: float): # angle in degrees
        self.rotate_around_point(angle=angle, point=self.get_center_coord())

    def scale_around_self(self, scale_vector: Coordenada2D):
        center_coord = self.get_center_coord()
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-center_coord),  # TODO: investigate translation backwards
            # Scale
            MatrixHelper.scale_matrix(scale_vector),
            # Translate back to the same position
            MatrixHelper.translation_matrix(center_coord)
        ])

    def rotate_around_point(self, angle: float, point: Coordenada2D): # angle in degrees
        translation_vector = point
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-translation_vector),
            # Rotates
            MatrixHelper.rotation_matrix(angle),
            # Translate back to the same position
            MatrixHelper.translation_matrix(translation_vector)
        ])