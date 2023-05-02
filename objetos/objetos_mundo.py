from coordenada import Coordenada, Coordenada3D
from typing import List, Literal
from matriz_suporte import MatrixHelper
from abc import ABC, abstractmethod


class WorldObject(ABC):
    _coordinates: List[Coordenada]

    def __init__(self, coordinates: List[Coordenada]) -> None:
        self._coordinates = coordinates
        self._constraint_check()

    def add_coordinate(self, x, y):
        return self._coordinates

    @abstractmethod
    def _constraint_check(self):
        pass

    def rotate(self, angle, axis: Literal['x', 'y', 'z'] = 'z', axis_vector: Coordenada3D = None):
        if axis_vector is None:
            self.transform([MatrixHelper.get_rotation_matrix(angle, axis)])
        else:
            if axis is None:
                axis = 'z'
            y_rotation = 0
            x_rotation = 0
            if axis_vector:
                new_axis = Coordenada3D(axis_vector)
                y_rotation = new_axis.y_rotation_to_align_with_z()
                new_axis.rotate(-y_rotation, 'y')
                x_rotation = new_axis.x_rotation_to_align_with_z()
                self.transform([
                    # Align with arbitrary axis with z
                    MatrixHelper.get_rotation_matrix(angle=-y_rotation, axis='y'),
                    MatrixHelper.get_rotation_matrix(angle=-x_rotation, axis='x'),
                    # Rotates
                    MatrixHelper.get_rotation_matrix(angle, axis),
                    # Rotates back
                    MatrixHelper.get_rotation_matrix(angle=x_rotation, axis='x'),
                    MatrixHelper.get_rotation_matrix(angle=y_rotation, axis='y'),
                    # Return to previous rotation
                ])

    def translate(self, movement_vector: Coordenada):
        self.transform([MatrixHelper.translation_matrix(Coordenada3D(movement_vector))])

    def scale(self, scale_vector: Coordenada3D):
        self.transform([MatrixHelper.scale_matrix(scale_vector)])

    # Transforms polygon based on a list of transform operations, represented by matrices
    def transform(self, transformations_matrices: list):
        for coord in self._coordinates:
            coord.transform(transformations_matrices)

    def get_center_coord(self) -> Coordenada3D:
        dimensions = self._coordinates[0].limit_size
        axis_sum = [0 for i in range(dimensions)]
        for coord in self._coordinates:
            for i in range(dimensions):
                axis_sum[i] += coord[i]

        l = float(len(self._coordinates))
        return Coordenada3D(Coordenada3D(axis_sum)*(1/l))

    def rotate_around_self(self, angle: float, axis: Literal['x', 'y', 'z'] = 'z', axis_vector: Coordenada3D = None): # angle in degrees
        point = self.get_center_coord()
        self.rotate_around_point(angle=angle, point=point, axis=axis, axis_vector=axis_vector)

    def scale_around_self(self, scale_vector: Coordenada3D):
        center_coord = self.get_center_coord()
        self.transform([
            # Translate to origin
            MatrixHelper.translation_matrix(-center_coord),  # TODO: investigate translation backwards
            # Scale
            MatrixHelper.scale_matrix(scale_vector),
            # Translate back to the same position
            MatrixHelper.translation_matrix(center_coord)
        ])

    def rotate_around_point(self, angle: float, point: Coordenada3D, axis: Literal['x', 'y', 'z'] = 'z', axis_vector: Coordenada3D = None): # angle in degrees
        if axis is None:
            axis = 'z'
        translation_vector = Coordenada3D(point)
        y_rotation = 0
        x_rotation = 0
        if axis_vector:
            new_axis = Coordenada3D(axis_vector)
            y_rotation = new_axis.y_rotation_to_align_with_z()
            new_axis.rotate(-y_rotation, 'y')
            x_rotation = new_axis.x_rotation_to_align_with_z()
        self.transform([
            # Translate to origin
            # Align with arbitrary axis with z
            MatrixHelper.get_rotation_matrix(angle=-y_rotation, axis='y'),
            MatrixHelper.get_rotation_matrix(angle=-x_rotation, axis='x'),
            # Rotates
            MatrixHelper.get_rotation_matrix(angle, axis),
            # Rotates back
            MatrixHelper.get_rotation_matrix(angle=x_rotation, axis='x'),
            MatrixHelper.get_rotation_matrix(angle=y_rotation, axis='y'),
            # Return to previous rotation
            MatrixHelper.translation_matrix(translation_vector)
        ])