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

    def __on_display_file_change(self, display_file_change: List[Objetos]) -> None:
        self.__viewport.draw(display_file_change)
        self.__gui.output.insert('1.0', "Objetos alterados\n")

    def run(self):
        self.__criar_interface()
        self.__gui.run()
        while True:
            self.__gui.update()

    def criar_objeto(self, name: str, cor: str, object_type: Literal['dot', 'line', 'wireframe'], coordinates: List[Coordenada2D]):
        if object_type == 'dot':
            self.display_file.append(Ponto(name, cor, coordinates))
            self.__gui.output.insert('1.0', "Ponto criado\n")
        elif object_type == 'line':
            self.display_file.append(Linha(name, cor, coordinates))
            self.__gui.output.insert('1.0', "Linha criada\n")
        elif object_type == 'wireframe':
            self.display_file.append(Wireframe(name, cor, coordinates))
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

    def translate_object(self, objeto: Objetos, movement_vector: Coordenada2D) -> None:
        objeto.translate(movement_vector)
        self.__viewport.draw(self.display_file.objetos())
        self.__gui.output.insert('1.0', "Objeto transladado\n")

    def scale_object(self, objeto: Objetos, scale_vector: Coordenada2D) -> None:
        objeto.scale_around_self(scale_vector)
        self.__viewport.draw(self.display_file.objetos())
        self.__gui.output.insert('1.0', "Objeto escalado\n")
        
    def rotate_object(self, objeto: Objetos, angle: float,
                      relative_to: Literal['world', 'itself', 'coordinate'], center: Coordenada2D = None) -> None:
        if relative_to == 'world':
            objeto.rotate(angle)
            self.__gui.output.insert('1.0', "Objeto rotacionado relativo ao mundo\n")
        elif relative_to == 'itself':
            objeto.rotate_around_self(angle)
            self.__gui.output.insert('1.0', "Objeto rotacionado relativo a si mesmo\n")
        elif relative_to == 'coordinate':
            objeto.rotate_around_point(angle, center)
            self.__gui.output.insert('1.0', "Objeto rotacionado relativo as coordenadas\n")
        self.__viewport.draw(self.display_file.objetos())
    
    def get_gui(self):
        return self.__gui