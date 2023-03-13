from viewport import Viewport
from display_file import DisplayFile
from objetos import Objetos
from ponto import Ponto
from poligono import Poligono
from linha import Linha
from typing import List, Literal
from enum import Enum
from coordenada import Coordenada2D

class Controlador:
    TIPO_OBJETOS = Enum('TipoObjetos', 'ponto linha poligono')
    TIPO_ZOOM = Enum('TipoZoom', 'menos mais')

    __viewport: Viewport

    display_file: DisplayFile

    def __init__(self) -> None:
        self.display_file = DisplayFile()

    def __criar_interface(self) -> None:
        from gui import Gui
        self.__gui = Gui(controller=self)
        canvas = self.__gui.create_canvas()
        self.__viewport = Viewport(canvas)
        self.display_file.subscribe(self.__on_display_file_change)

    def __on_display_file_change(self, display_file: List[Objetos]) -> None:
        self.__viewport.draw(display_file)

    def run(self):
        self.__criar_interface()
        self.__gui.run()
        while True:
            self.__gui.update()

    def criar_objeto(self, name: str, object_type: TIPO_OBJETOS, coordinates: List[Coordenada2D]):
        if (object_type == Controlador.TIPO_OBJETOS.ponto.value):
            self.display_file.append(Ponto(name, coordinates))
        elif (object_type == Controlador.TIPO_OBJETOS.linha.value):
            self.display_file.append(Linha(name, coordinates))
        elif (object_type == Controlador.TIPO_OBJETOS.poligono.value):
            self.display_file.append(Poligono(name, coordinates))

    def zoom(self, direction: TIPO_ZOOM):
        if direction == Controlador.TIPO_ZOOM.menos.value:
            self.__viewport.zoom_in()
        else:
            self.__viewport.zoom_out()
        self.__viewport.draw(self.display_file.objetos())

    def navegar(self, direction: Literal['up', 'down', 'left', 'right']):
        self.__viewport.navigate(direction)
        self.__viewport.draw(self.display_file.objetos())
