import math
import numpy
from typing import List, Literal, Tuple, Union
from objetos.objetos import Objetos
from coordenada import Coordenada2D, Coordenada3D
from objetos.objetos_mundo import WorldObject
from clipper import Clipper
from matriz_suporte import MatrixHelper

class Window(WorldObject):
    __clipping_method: Literal['liang_barsky', 'cohen_sutherland']

    def __init__(self, top_left: Coordenada3D, top_right: Coordenada3D, bottom_left: Coordenada3D, center_back: Coordenada3D = None):
        self.__clipping_method = 'liang_barsky'
        super().__init__(coordinates=[top_left, top_right, bottom_left])
        if center_back is None:
            center_back = self.get_window_center() - self.view_vector
            self._coordinates.append(center_back)

    @property
    def transformation_matrix(self) -> List[List[float]]:
        temp_window = Window(Coordenada3D(self.top_left.copy()),
                             Coordenada3D(self.top_right.copy()),
                             Coordenada3D(self.bottom_left.copy()),
                             Coordenada3D(self.center_back.copy()))
        matrix = []
        # Translate everything so the window is in the origin
        translation = -self.center_back
        matrix.append(MatrixHelper.translation_matrix(translation))

        y_rotation = -(temp_window.view_vector.y_rotation_to_align_with_z())
        matrix.append(MatrixHelper.get_rotation_matrix(y_rotation, 'y'))
        temp_window.rotate(y_rotation, 'y')

        x_rotation = -(temp_window.view_vector.x_rotation_to_align_with_z())
        matrix.append(MatrixHelper.get_rotation_matrix(x_rotation, 'x'))
        temp_window.rotate(x_rotation, 'x')

        z_rotation = (-(temp_window.up.z_rotation_to_align_with_y()))
        matrix.append(MatrixHelper.get_rotation_matrix(z_rotation, 'z'))

        return matrix

    def coord_to_window_system(self, drawable: Objetos.Drawable) -> Objetos.Drawable:
        points = [self._transform_coord(p) for p in drawable.pontos]
        lines = [[self._transform_coord(line[0]), self._transform_coord(line[1])] for line in
                 drawable.linhas]
        return Objetos.Drawable(lines, points, drawable.cor)

    def clip(self, drawable: Objetos.Drawable) -> Objetos.Drawable:
        # applies clipping and appends if clipped is not null
        for p in drawable.pontos:
            if p.z <= 0: return Objetos.Drawable([[]], [], drawable.cor)
        points = [clipped_p for p in drawable.pontos if (clipped_p := self.clip_point(p)) is not None]
        lines = [clipped_l for line in drawable.linhas if (clipped_l := self.clip_line(line)) is not None]
        return Objetos.Drawable(lines, points, drawable.cor)

    def clip_line(self, line: List[Coordenada2D]) -> Union[Tuple[Coordenada2D, Coordenada2D], None]:
        if self.__clipping_method == 'liang_barsky':
            return Clipper.liang_barsky_clip(line[0], line[1])
        elif self.__clipping_method == 'cohen_sutherland':
            return Clipper.cohen_sutherland_clip(line[0], line[1])

    def clip_point(self, point: Coordenada3D) -> Union[Coordenada3D, None]:
        return point if point.x >= -1 and point.x <= 1 and point.y >= -1 else None

    @property
    def top_left(self) -> Coordenada3D:
        return Coordenada3D(self._coordinates[0])

    @property
    def top_right(self) -> Coordenada3D:
        return Coordenada3D(self._coordinates[1])

    @property
    def bottom_left(self) -> Coordenada3D:
        return Coordenada3D(self._coordinates[2])

    @property
    def center_back(self) -> Coordenada3D:
        return Coordenada3D(self._coordinates[3])

    @property
    def view_vector(self) -> Coordenada3D:
        up = self.bottom_left - self.top_left
        left = self.top_left - self.top_right
        back = up * left
        return Coordenada3D(-back.normalize())

    @property
    def height(self) -> float:
        return Coordenada2D.distancia(self.top_left, self.bottom_left)

    @property
    def width(self) -> float:
        return Coordenada2D.distancia(self.top_left, self.top_right)

    @property
    def up(self) -> Coordenada3D:
        return Coordenada3D((self.bottom_left - self.top_left).normalize())

    @property
    def right(self) -> Coordenada3D:
        return Coordenada3D((self.top_left - self.top_right).normalize().copy())
    
    def set_clipping_method(self, method: Literal['liang_barsky', 'cohen_sutherland']):
        self.__clipping_method = method

    def move_left(self, amount):
        movement_vector = -self.right * amount * self.width
        self.translate(movement_vector)

    def move_right(self, amount):
        movement_vector = self.right * amount * self.width
        self.translate(movement_vector)

    def move_up(self, amount):
        movement_vector = self.up * amount * self.height
        self.translate(movement_vector)

    def move_down(self, amount):
        movement_vector = -self.up * amount * self.height
        self.translate(movement_vector)

    def move_forward(self, amount):
        movement_vector = self.view_vector * amount
        self.translate(movement_vector)

    # Returns the angle between the window up and the y-axis
    def get_tilt_angle(self):
        y_axis: Coordenada2D = Coordenada2D.up()
        w_up: Coordenada2D = self.top_left - self.bottom_left
        return math.degrees(math.atan2(w_up.y * y_axis.x - w_up.x * y_axis.y, w_up.x * y_axis.x + w_up.y * y_axis.y))

    def _get_rotation_with_y(sel, view_vector):
        h = Coordenada3D(view_vector.copy())
        h.y = 0
        c = 1 if h.x >= 0 else -1
        return c*math.degrees(math.acos(h.z/h.length))

    def _get_rotation_with_x(self, view_vector):
        h = Coordenada3D(view_vector.copy())
        h.x = 0
        c = 1 if h.y >= 0 else -1
        return c * math.degrees(math.acos(h.z / h.length))

    def get_center_coord(self) -> Coordenada3D:
        return self.get_window_center()

    def _transform_coord(self, coord: Coordenada3D) -> Coordenada3D:
        new_point = Coordenada3D(coord.copy())
        new_point.transform(self.transformation_matrix)
        new_point.x = new_point.x / (self.width * 0.5)
        new_point.y = new_point.y / (self.height * 0.5)
        return self.__project_in_perspective(new_point)

    def get_window_center(self) -> Coordenada3D:
        center = self.bottom_left + ((self.top_left - self.bottom_left) * 0.5)
        return center + ((self.top_right - self.top_left) * 0.5)

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")

    def __project_in_perspective(self, coord: Coordenada3D) -> Coordenada3D:
        d = self.center_back.z
        # if coord.z == 0: coord.z = 1 # TODO: coord z = 1?
        coord.x = d * coord.x / coord.z
        coord.y = d * coord.y / coord.z
        return coord
