from view.viewport import Viewport
from model.display_file import ObservableDisplayFile
from model.displayable import Displayable
from model.dot import Dot
from model.wireframe import Wireframe
from model.line import Line
from typing import List, Literal
from enum import Enum
from model.coordinate import Coordinate2D


class Controller:
    ### Consts
    OBJECT_TYPES = Enum('ObjectTypes', 'dot line wireframe')
    ZOOM_TYPES = Enum('ZoomTypes', 'in_ out')

    ### Private attrs
    __viewport: Viewport

    ### Public attrs
    observable_display_file: ObservableDisplayFile

    # Constructor
    def __init__(self) -> None:
        self.observable_display_file = ObservableDisplayFile()

    ### Private methods
    def __create_interface(self) -> None:
        # TODO: Fix circular dependency injection. View cannot have controller
        #       it must communicate to controller through events
        from view.gui import Gui
        self.__gui = Gui(controller=self)
        canvas = self.__gui.create_canvas()
        self.__viewport = Viewport(canvas)
        self.observable_display_file.subscribe(self.__on_display_file_change)

    def __on_display_file_change(self, display_file: List[Displayable]) -> None:
        self.__viewport.draw(display_file)

    ### Public methods
    def run(self):
        self.__create_interface()
        self.__gui.run()
        while True:
            self.__gui.update()

    def create_object(self, name: str, object_type: OBJECT_TYPES, coordinates: List[Coordinate2D]):
        # TODO: fix typing
        if (object_type == Controller.OBJECT_TYPES.dot.value):
            self.observable_display_file.append(Dot(name, coordinates))
        elif (object_type == Controller.OBJECT_TYPES.line.value):
            self.observable_display_file.append(Line(name, coordinates))
        elif (object_type == Controller.OBJECT_TYPES.wireframe.value):
            self.observable_display_file.append(Wireframe(name, coordinates))

    def zoom(self, direction: ZOOM_TYPES):
        if direction == Controller.ZOOM_TYPES.in_.value:
            self.__viewport.zoom_in()
        else:
            self.__viewport.zoom_out()
        self.__viewport.draw(self.observable_display_file.displayables())

    def navigate(self, direction: Literal['up', 'down', 'left', 'right']):
        self.__viewport.navigate(direction)
        self.__viewport.draw(self.observable_display_file.displayables())
