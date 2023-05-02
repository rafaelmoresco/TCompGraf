from viewport import Viewport
from display_file import DisplayFile
from objetos.objetos import Objetos
from objetos.ponto import Ponto
from objetos.wireframe import Wireframe
from objetos.linha import Linha
from objetos.curva_bezier import CurvaBezier
from objetos.b_spline import BSpline
from typing import List, Literal
from enum import Enum
from coordenada import Coordenada2D
from coordenada import Coordenada3D
from wavefront_file_parser import WavefrontFileParser

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

    def set_clipping_method(self, method: Literal['liang_barsky', 'cohen_sutherland']):
        self.__viewport.set_clipping_method(method)

    def run(self):
        self.__criar_interface()
        self.__gui.run()
        while True:
            self.__gui.update()

    def criar_objeto(self, name: str, cor: str, object_type: Literal['dot', 'line', 'wireframe', 'bezier', 'spline'], coordinates: List[Coordenada3D]):
        if object_type == 'dot':
            self.display_file.append(Ponto(name, cor, coordinates))
            self.__gui.output.insert('1.0', "Ponto criado\n")
        elif object_type == 'line':
            self.display_file.append(Linha(name, cor, coordinates))
            self.__gui.output.insert('1.0', "Linha criada\n")
        elif object_type == 'wireframe':
            self.display_file.append(Wireframe(name, cor, coordinates))
            self.__gui.output.insert('1.0', "Wireframe criado\n")
        elif object_type == 'bezier':
            self.display_file.append(CurvaBezier(name, cor, coordinates))
            self.__gui.output.insert('1.0', "Curva Bezier criada\n")
        elif object_type == 'spline':
            self.display_file.append(BSpline(name, cor, coordinates))
            self.__gui.output.insert('1.0', "B-Spline criada\n")
    def zoom(self, direcao: TIPO_ZOOM):
        if direcao == Controlador.TIPO_ZOOM.menos.value:
            self.__viewport.zoom_in()
            self.__gui.output.insert('1.0', "Zoom In\n")
        else:
            self.__viewport.zoom_out()
            self.__gui.output.insert('1.0', "Zoom out\n")
        self.__viewport.draw(self.display_file.objetos())

    def navegar(self, direcao: Literal['up', 'down', 'left', 'right']):
        self.__viewport.navigate(direcao)
        self.__viewport.draw(self.display_file.objetos())

    def tilt(self, direction: Literal['up', 'down', 'left', 'right']) -> None:
        self.__viewport.tilt(direction)
        self.__viewport.draw(self.display_file.objetos())
        self.__gui.output.insert('1.0', "Tilt\n")

    def move(self, direction: Literal['forward', 'backward']) -> None:
        self.__viewport.navigate(direction)
        self.__viewport.draw(self.display_file.objetos())
        if direction == 'forward':
            self.__gui.output.insert('1.0', "Visão movida para frente\n")
        else:
            self.__gui.output.insert('1.0', "Visão movida para trás\n")

    # Translação entrega 2 
    def translate_object(self, objeto: Objetos, movement_vector: Coordenada3D) -> None:
        objeto.translate(movement_vector)
        self.__viewport.draw(self.display_file.objetos())
        self.__gui.output.insert('1.0', "Objeto transladado\n")

    # Scale entrega 2
    def scale_object(self, objeto: Objetos, scale_vector: Coordenada3D) -> None:
        scale_vector = Coordenada3D(list(scale_vector) +[0])
        objeto.scale_around_self(scale_vector)
        self.__viewport.draw(self.display_file.objetos())
        self.__gui.output.insert('1.0', "Objeto escalado\n")
        
    # Rotação entrega 2
    def rotate_object(self, objeto: Objetos, angle: float,
                      relative_to: Literal['world', 'itself', 'coordinate'], 
                      axis: Literal['x', 'y', 'z'], center: Coordenada3D = None,
                      arbitrary_axis_coord: Coordenada3D = None) -> None:
        if relative_to == 'world':
            objeto.rotate(angle=angle, axis=axis, axis_vector=arbitrary_axis_coord)
            self.__gui.output.insert('1.0', "Objeto rotacionado relativo ao mundo\n")
        elif relative_to == 'itself':
            objeto.rotate_around_self(angle=angle, axis=axis, axis_vector=arbitrary_axis_coord)
            self.__gui.output.insert('1.0', "Objeto rotacionado relativo a si mesmo\n")
        elif relative_to == 'coordinate':
            objeto.rotate_around_point(angle=angle, point=center, axis=axis, axis_vector=arbitrary_axis_coord)
            self.__gui.output.insert('1.0', "Objeto rotacionado relativo as coordenadas\n")
        self.__viewport.draw(self.display_file.objetos())
    
    def rotate_window(self, direction: Literal['left', 'right']) -> None:
        self.__viewport.rotate_window(direction)
        self.__viewport.draw(self.display_file.objetos())
        if direction == 'left':
            self.__gui.output.insert('1.0', "Mundo rotacionado para esquerda\n")
        else:
            self.__gui.output.insert('1.0', "Mundo rotacionado para direita\n")

    def import_wavefront_file(self, filepath: str) -> None:
        new_displayables, new_window = WavefrontFileParser.import_file(filepath)
        if new_window: self.__viewport.set_window(new_window)
        self.display_file.overwrite(new_displayables)
        self.__gui.output.insert('1.0', "Arquivo importado com sucesso\n")
    
    def export_wavefront_file(self) -> None:
        WavefrontFileParser.export_file(
            self.display_file.objetos(),
            self.__viewport.get_window()
        )
        self.__gui.output.insert('1.0', "Arquivo exportado com sucesso\n")

    def get_gui(self):
        return self.__gui