from viewport import Viewport
from display_file import DisplayFile
from objetos import Objetos
from ponto import Ponto
from wireframe import Wireframe
from linha import Linha
from typing import List, Literal
from enum import Enum
from coordenada import Coordenada2D

class Controlador:
    TIPO_OBJETOS = Enum('TipoObjetos', 'ponto linha wireframe')
    TIPO_ZOOM = Enum('TipoZoom', 'menos mais')

    __viewport: Viewport

    display_file: DisplayFile

    def __init__(self) -> None:
        #Cria DisplayFile
        self.display_file = DisplayFile()

    def __criar_interface(self) -> None:
        from gui import Gui
        self.__gui = Gui(controller=self)
        canvas = self.__gui.create_canvas()
        self.__viewport = Viewport(canvas)
        self.display_file.subscribe(self.__on_display_file_change)

    def __on_display_file_change(self, display_file: List[Objetos]) -> None:
        self.__viewport.draw(display_file)
        self.__gui.output.insert('1.0', "Objetos alterados\n")

    def run(self):
        self.__criar_interface()
        self.__gui.run()
        while True:
            self.__gui.update()

    def criar_objeto(self, name: str, object_type: TIPO_OBJETOS, coordinates: List[Coordenada2D]):
        if (object_type == Controlador.TIPO_OBJETOS.ponto.value):
            self.display_file.append(Ponto(name, coordinates))
            self.__gui.output.insert('1.0', "Ponto criado\n")
        elif (object_type == Controlador.TIPO_OBJETOS.linha.value):
            self.display_file.append(Linha(name, coordinates))
            self.__gui.output.insert('1.0', "Linha criada\n")
        elif (object_type == Controlador.TIPO_OBJETOS.wireframe.value):
            self.display_file.append(Wireframe(name, coordinates))
            self.__gui.output.insert('1.0', "Wireframe criado\n")

    def zoom(self, direcao: TIPO_ZOOM):
        if direcao == Controlador.TIPO_ZOOM.menos.value:
            self.__viewport.zoom_in()
        else:
            self.__viewport.zoom_out()
        self.__viewport.draw(self.display_file.objetos())

    def navegar(self, direcao: Literal['up', 'down', 'left', 'right']):
        self.__viewport.navigate(direcao)
        self.__viewport.draw(self.display_file.objetos())

    def get_gui(self):
        return self.__gui