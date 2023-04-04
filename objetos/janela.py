import math
from typing import List
from objetos.objetos import Objetos
from coordenada import Coordenada2D
from objetos.objetos_mundo import WorldObject

class Window(WorldObject):

    def __init__(self, top_left: Coordenada2D, top_right: Coordenada2D, bottom_left: Coordenada2D):
        super().__init__(coordinates=[top_left, top_right, bottom_left])

    def coord_to_window_system(self, displayables: List[Objetos]):
        displayables_copy = displayables.copy()
        linhas = []
        pontos = []
        for displayable in displayables_copy:
            drawable = displayable.get_drawable()
            for p in drawable.pontos:
                pontos.append(self._transform_coord(p))

            for linha in drawable.linhas:
                linhas.append([
                    self._transform_coord(linha[0]),
                    self._transform_coord(linha[1])
                    ])

        return Objetos.Drawable(linhas=linhas, pontos=pontos, cor='#000')

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
        return Coordenada2D.distance(self.top_left, self.bottom_left)

    @property
    def width(self) -> float:
        return Coordenada2D.distance(self.top_left, self.top_right)

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
        # TODO: change this approach
        return math.degrees(math.atan2(w_up.y*y_axis.x - w_up.x*y_axis.y, w_up.x*y_axis.x + w_up.y*y_axis.y))

    def _transform_coord(self, coord: Coordenada2D):
        new_point = Coordenada2D(coord.copy())
        new_point.translate(-self.get_window_center())
        new_point.rotate(self._get_angle())
        new_point.x = new_point.x / (self.width * 0.5)
        new_point.y = new_point.y / (self.height * 0.5)
        print(self._get_angle())
        return new_point

    def get_window_center(self) -> Coordenada2D:
        center = self.bottom_left + ((self.top_left-self.bottom_left)*0.5)
        return center + ((self.top_right - self.top_left)*0.5)

    def _constraint_check(self):
        if len(self._coordinates) != 3:
            raise Exception("A window must have exactly 3 coordinates")
