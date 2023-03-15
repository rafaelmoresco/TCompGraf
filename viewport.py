from tkinter import *
from typing import List, Literal
from display_file import DisplayFile
from objetos import Objetos
from ponto import Ponto
from linha import Linha
from coordenada import Coordenada2D

class Viewport:
    __canvas: Canvas
    __window: List[Coordenada2D]
    __world_origin: Coordenada2D

    LINE_WIDTH = 3
    LINE_COLOR = "black"

    POINT_WIDTH = 5
    POINT_COLOR = "black"

    ZOOM_AMOUNT = 0.1

    NAVIGATION_SPEED = 50

    def __init__(self, canvas: Canvas):
        self.__canvas = canvas
        self.__canvas.update()
        self.__window = [Coordenada2D(0, 0), Coordenada2D(self.get_width(), self.get_height())]
        self.__world_origin = Coordenada2D(0, 0)

    def __draw_line(self, coord1, coord2):
        self.__canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y,
                                  width=Viewport.LINE_WIDTH, fill=Viewport.LINE_COLOR)

    def __draw_point(self, coord):
        self.__canvas.create_oval(coord.x, coord.y, coord.x, coord.y,
                                  width=Viewport.POINT_WIDTH, fill=Viewport.POINT_COLOR)

    def __zoom(self, amount):
        window_size_x = self.__window[1].x - self.__window[0].x
        window_size_y = self.__window[1].y - self.__window[0].y
        self.__window[1] = Coordenada2D(
            self.__window[1].x + amount*window_size_x ,
            self.__window[1].y + amount*window_size_y
        )

    def __move_window(self, movement_vector: Coordenada2D):
        self.__window[0].x += movement_vector.x
        self.__window[0].y += movement_vector.y
        self.__window[1].x += movement_vector.x
        self.__window[1].y += movement_vector.y

    def __tranform_coord(self, coord) -> Coordenada2D:
        w_min = self.__window[0]
        w_max = self.__window[1]
        v_max = Coordenada2D(self.get_width(), self.get_height())
        v_min = self.__world_origin

        x = (coord.x - w_min.x) * (v_max.x - v_min.x) / (
                    w_max.x - w_min.x)
        y = (1 - (coord.y - w_min.y)  / (
                w_max.y - w_min.y)) * (v_max.y - v_min.y)
        return Coordenada2D(x, y)

    def draw(self, display_file: List[Objetos]):
        self.__canvas.delete('all')
        for displayable in display_file:
            coordinates = displayable.get_coordenadas()
            for i in range(len(coordinates)):
                coord = self.__tranform_coord(coordinates[i])
                self.__draw_point(coord)

                if i < len(coordinates) - 1:
                    next_coord = self.__tranform_coord(coordinates[i + 1])
                    self.__draw_line(coord, next_coord)
                else:
                    if not isinstance(displayable, Ponto) and not isinstance(displayable, Linha):
                        first_coord = self.__tranform_coord(coordinates[0])
                        self.__draw_line(coord, first_coord)

        self.__canvas.update()

    def get_width(self) -> int:
        return self.__canvas.winfo_width()

    def get_height(self) -> int:
        return self.__canvas.winfo_height()

    def zoom_in(self) -> None:
        self.__zoom(-Viewport.ZOOM_AMOUNT)

    def zoom_out(self) -> None:
        self.__zoom(Viewport.ZOOM_AMOUNT)

    def navigate(self, direcao: Literal['up', 'down', 'left', 'right']):
        if direcao == 'up':
            self.__move_window(Coordenada2D(0, Viewport.NAVIGATION_SPEED))
        elif direcao == 'down':
            self.__move_window(Coordenada2D(0, -Viewport.NAVIGATION_SPEED))
        elif direcao == 'left':
            self.__move_window(Coordenada2D(-Viewport.NAVIGATION_SPEED, 0))
        elif direcao == 'right':
            self.__move_window(Coordenada2D(Viewport.NAVIGATION_SPEED, 0))
