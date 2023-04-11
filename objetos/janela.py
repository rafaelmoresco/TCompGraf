import math
from typing import List, Literal, Tuple, Union
from objetos.objetos import Objetos
from coordenada import Coordenada2D
from objetos.objetos_mundo import WorldObject
from clipper import Clipper

class Window(WorldObject):
    __clipping_method: Literal['liang_barsky', 'cohen_sutherland']

    def __init__(self, top_left: Coordenada2D, top_right: Coordenada2D, bottom_left: Coordenada2D):
        self.__clipping_method = 'liang_barsky'
        super().__init__(coordinates=[top_left, top_right, bottom_left])

    def coord_to_window_system(self, drawable: Objetos.Drawable) -> Objetos.Drawable:
        points = [self._transform_coord(p) for p in drawable.pontos]
        lines = [[self._transform_coord(line[0]), self._transform_coord(line[1])] for line in drawable.linhas]
        return Objetos.Drawable(lines, points, drawable.cor)


    def clip(self, drawable: Objetos.Drawable) -> Objetos.Drawable:
        # applies clipping and appends if clipped is not null
        points = [clipped_p for p in drawable.pontos if (clipped_p := self.clip_point(p)) is not None]
        lines = [clipped_l for line in drawable.linhas if (clipped_l := self.clip_line(line)) is not None]
        return Objetos.Drawable(lines, points, drawable.cor)

    def clip_line(self, line: List[Coordenada2D]) -> Union[Tuple[Coordenada2D, Coordenada2D], None]:
        if self.__clipping_method == 'liang_barsky':
            return Clipper.liang_barsky_clip(line[0], line[1])
        elif self.__clipping_method == 'cohen_sutherland':
            return Clipper.cohen_sutherland_clip(line[0], line[1])

    def clip_point(self, point: Coordenada2D) -> Union[Coordenada2D, None]:
        return point if point.x >= -1 and point.x <= 1 and point.y >= -1 and point.y <= 1 else None

    @property
    def top_left(self) -> Coordenada2D:
        return self._coordinates[0]

    @property
    def top_right(self) -> Coordenada2D:
        return self._coordinates[1]

    @property
    def bottom_left(self) -> Coordenada2D:
        return self._coordinates[2]

    @property
    def height(self) -> float:
        return Coordenada2D.distancia(self.top_left, self.bottom_left)

    @property
    def width(self) -> float:
        return Coordenada2D.distancia(self.top_left, self.top_right)
    
    def set_clipping_method(self, method: Literal['liang_barsky', 'cohen_sutherland']):
        self.__clipping_method = method

    def move_left(self, amount):
        movement_vector = -(self.top_right - self.top_left).normalize() * amount * self.width
        self.translate(movement_vector)

    def move_right(self, amount):
        movement_vector = (self.top_right - self.top_left).normalize() * amount * self.width
        self.translate(movement_vector)

    def move_up(self, amount):
        movement_vector = -(self.bottom_left - self.top_left).normalize() * amount * self.height
        self.translate(movement_vector)

    def move_down(self, amount):
        movement_vector = (self.bottom_left - self.top_left).normalize() * amount * self.height
        self.translate(movement_vector)

    # Returns the angle between the window up and the y-axis
    def _get_angle(self):
        y_axis: Coordenada2D = Coordenada2D.up()
        w_up: Coordenada2D = self.top_left-self.bottom_left
        return math.degrees(math.atan2(w_up.y*y_axis.x - w_up.x*y_axis.y, w_up.x*y_axis.x + w_up.y*y_axis.y))

    def _transform_coord(self, coord: Coordenada2D):
        new_point = Coordenada2D(coord.copy())
        new_point.translate(-self.get_window_center())
        new_point.rotate(self._get_angle())
        new_point.x = new_point.x / (self.width * 0.5)
        new_point.y = new_point.y / (self.height * 0.5)
        return new_point

    def get_window_center(self) -> Coordenada2D:
        center = self.bottom_left + ((self.top_left-self.bottom_left)*0.5)
        return center + ((self.top_right - self.top_left)*0.5)

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")
