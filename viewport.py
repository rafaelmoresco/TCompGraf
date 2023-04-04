from tkinter import *
from typing import List, Literal
from objetos.objetos import Objetos
from objetos.janela import Window
from coordenada import Coordenada2D

# Classe relacionada as operações de viewport 
class Viewport:
    __canvas: Canvas
    __window: Window
    __world_origin: Coordenada2D

    LINE_WIDTH = 3
    POINT_WIDTH = 4

    ZOOM_AMOUNT = 1.1
    NAVIGATION_SPEED = 0.1
    WINDOW_ROTATION_AMOUNT = 15

    def __init__(self, canvas: Canvas):
        self.__canvas = canvas
        self.__canvas.update()
        self.__window = Window(
            top_left=Coordenada2D(0, self.get_height()),
            top_right=Coordenada2D(self.get_width(), self.get_height()),
            bottom_left=Coordenada2D(0, 0)
        )
        self.__world_origin = Coordenada2D(0, 0)

    def __draw_line(self, coord1: Coordenada2D, coord2: Coordenada2D, cor: str):        
        coord1 = self.__tranform_coord(coord1)
        coord2 = self.__tranform_coord(coord2)
        self.__canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y,
                                  width=Viewport.LINE_WIDTH, fill=cor)

    def __draw_point(self, coord: Coordenada2D, cor: str):
        coord = self.__tranform_coord(coord)
        self.__canvas.create_oval(coord.x, coord.y, coord.x, coord.y,
                                  width=Viewport.POINT_WIDTH, outline=cor)

    def __zoom(self, amount):
        self.__window.scale_around_self(Coordenada2D(amount, amount))

    def __tranform_coord(self, coord: Coordenada2D) -> Coordenada2D:
        x = (coord[0] + 1)*0.5*self.get_width()
        y = (1 - (coord[1] + 1)*0.5) *self.get_height()
        return Coordenada2D(x, y)

    def get_window(self) -> Window:
        return self.__window

    def set_window(self, new_window: Window) -> None:
        self.__window = new_window

    def draw(self, display_file: List[Objetos]):
        # TODO: not redraw all every time
        self.__canvas.delete('all')
        drawableObject = self.__window.coord_to_window_system(display_file)
        for linha in drawableObject.linhas:
            self.__draw_line(linha[0], linha[1], cor='#000')

        for p in drawableObject.pontos:
            self.__draw_point(p, cor='#000') # TODO: fix colors

        self.__canvas.update()

    def get_width(self) -> int:
        return self.__canvas.winfo_width()

    def get_height(self) -> int:
        return self.__canvas.winfo_height()

    def zoom_in(self) -> None:
        self.__zoom(1/Viewport.ZOOM_AMOUNT)

    def zoom_out(self) -> None:
        self.__zoom(Viewport.ZOOM_AMOUNT)

    def navigate(self, direcao: Literal['up', 'down', 'left', 'right']):
        amount =  Viewport.NAVIGATION_SPEED
        if direcao == 'up':
            self.__window.move_up(amount)
        elif direcao == 'down':
            self.__window.move_down(amount)
        elif direcao == 'left':
            self.__window.move_left(amount)
        elif direcao == 'right':
            self.__window.move_right(amount)

    def rotate_window(self, direcao: Literal['left', 'right']):
        amount = Viewport.WINDOW_ROTATION_AMOUNT if direcao == 'left' else -Viewport.WINDOW_ROTATION_AMOUNT
        self.__window.rotate_around_point(amount, self.__window.get_window_center())