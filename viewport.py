from tkinter import *
from typing import List, Literal
from objetos.objetos import Objetos
from objetos.janela import Window
from coordenada import Coordenada2D, Coordenada3D

# Classe relacionada as operações de viewport 
class Viewport:
    __canvas: Canvas
    __window: Window
    __world_origin: Coordenada2D
    __border_width = 50

    LINE_WIDTH = 3
    POINT_WIDTH = 4

    QNTD_ZOOM = 1.1
    VELOCIDADE_NAVEGACAO = 0.07
    QNTD_ROTACAO_WINDOW = 15
    QNTD_MOVIMENTO_WINDOW = 30

    def __init__(self, canvas: Canvas):
        self.__canvas = canvas
        self.__canvas.update()
        self.__window = Window(
            top_left=Coordenada3D(0, self.get_height(), -30),
            top_right=Coordenada3D(self.get_width(), self.get_height(), -30),
            bottom_left=Coordenada3D(0, 0, -30)
        )
        self.__world_origin = Coordenada2D(0, 0)
        self.__draw_viewport()

    def __draw_viewport(self):
        lines = [(-1, -1, 1, -1), (-1, 1, 1, 1), (-1, 1, -1, -1), (1, 1, 1, -1)]
        for x1, y1, x2, y2 in lines:
                self.__draw_line(
                    Coordenada2D(x1, y1),
                    Coordenada2D(x2, y2),
                    '#f00',
                    1
                )

    def __draw_line(self, coord1: Coordenada2D, coord2: Coordenada2D, cor: str, line_width: int = None):
        if not line_width: line_width = Viewport.LINE_WIDTH    
        coord1 = self.__tranform_coord(coord1)
        coord2 = self.__tranform_coord(coord2)
        self.__canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y,
                                  width=line_width, fill=cor)

    def __draw_point(self, coord: Coordenada2D, cor: str):
        coord = self.__tranform_coord(coord)
        self.__canvas.create_oval(coord.x, coord.y, coord.x, coord.y,
                                  width=Viewport.POINT_WIDTH, outline=cor)

    def __zoom(self, amount):
        self.__window.scale_around_self(Coordenada3D(amount, amount, amount))

    def __tranform_coord(self, coord: Coordenada2D) -> Coordenada2D:
        x = (coord[0] + 1)*0.5*self.get_width()
        y = (1 - (coord[1] + 1)*0.5) *self.get_height()
        x += self.__border_width
        y += self.__border_width
        return Coordenada2D(x, y)
    
    def set_clipping_method(self, method: Literal['liang_barsky', 'cohen_sutherland']):
        self.__window.set_clipping_method(method)

    def get_window(self) -> Window:
        return self.__window

    def set_window(self, new_window: Window) -> None:
        self.__window = new_window

    def draw(self, display_file: List[Objetos]):
        self.__canvas.delete('all')
        self.__draw_viewport()
        for displayable in display_file:
            drawable = self.__window.coord_to_window_system(displayable.get_drawable())
            drawable = self.__window.clip(drawable)
            for point in drawable.pontos:
                self.__draw_point(Coordenada2D(point), drawable.cor)
            for line in drawable.linhas:
                if line:
                    self.__draw_line(Coordenada2D(line[0]), Coordenada2D(line[1]), drawable.cor)

        self.__canvas.update()

    def get_width(self) -> int:
        return self.__canvas.winfo_width() - 2*self.__border_width

    def get_height(self) -> int:
        return self.__canvas.winfo_height() - 2*self.__border_width

    def zoom_in(self) -> None:
        self.__zoom(1/Viewport.QNTD_ZOOM)

    def zoom_out(self) -> None:
        self.__zoom(Viewport.QNTD_ZOOM)

    def navigate(self, direcao: Literal['up', 'down', 'left', 'right', 'forward', 'backward']):
        amount =  Viewport.VELOCIDADE_NAVEGACAO
        if direcao == 'up':
            self.__window.move_up(amount)
        elif direcao == 'down':
            self.__window.move_down(amount)
        elif direcao == 'left':
            self.__window.move_left(amount)
        elif direcao == 'right':
            self.__window.move_right(amount)
        elif direcao == 'forward':
            self.__window.move_forward(Viewport.QNTD_MOVIMENTO_WINDOW)
        elif direcao == 'backward':
            self.__window.move_forward(-Viewport.QNTD_MOVIMENTO_WINDOW)

    def tilt(self, direction: Literal['up', 'down', 'left', 'right']) -> None:
        axis_vector: Coordenada3D = self.__window.up
        if direction == 'up' or direction == 'down':
            axis_vector = self.__window.right
        amount = Viewport.QNTD_ROTACAO_WINDOW
        if direction == 'down' or direction == 'left':
            amount = -amount
        self.__window.rotate_around_self(amount, axis_vector=axis_vector)

    def rotate_window(self, direcao: Literal['left', 'right']):
        amount = -Viewport.QNTD_ROTACAO_WINDOW if direcao == 'left' else Viewport.QNTD_ROTACAO_WINDOW
        self.__window.rotate_around_point(angle=amount, point=self.__window.get_window_center(), axis_vector=self.__window.view_vector)