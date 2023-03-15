from tkinter import *
from tkinter.ttk import Notebook
from typing import Callable, Final, List, Literal, Tuple
from controlador import Controlador
from coordenada import Coordenada2D
from objetos import Objetos

# Toda a interface de usuário
class Gui:
    FONT_SIZE_DEFAULT: Final[int] = 13
    FONT_SIZE_TITLE: Final[int] = 18

    WIDTH: Final[int] = 1280
    HEIGHT: Final[int] = 720

    CANVAS_WIDTH: Final[int] = WIDTH*3/4
    CANVAS_HEIGHT: Final[int] = HEIGHT*4/6

    __root: Tk
    __controller: Controlador
    __obj_varlist: Variable

    def __init__(self, controller: Controlador) -> None:
        self.__controller = controller
        self.__root = Tk()
        self.__root.title("Sistema Gráfico Interativo")
        self.__root.resizable(width=False, height=False)
        self.__obj_varlist = Variable(value=[])
        controller.display_file.subscribe(self.update_obj_varlist)

    def __create_label(self, parent_frame: Frame, text: str, pady: int = 0, padx: int = 0,
                       font_size: int = FONT_SIZE_DEFAULT, align=TOP, anchor=None, pack=True) -> Label:
        label = Label(parent_frame, text=text, font=('Helvetica', font_size))
        label.pack(pady=pady, padx=padx, side=align, anchor=anchor)
        return label

    def __create_input(self, parent_frame: Frame, placeholder: str = "", pady: int = 0,
                       padx: int = 0, align=TOP, anchor=None, pack=True) -> Entry:
        input = Entry(parent_frame, textvariable=StringVar(value=placeholder))
        if pack:
            input.pack(ipady=3, pady=pady, padx=padx, side=align, anchor=anchor)
        return input

    def __create_button(self, parent_frame: Frame, text: str, handler: Callable, *handler_args,
                        pady: int = 0, padx: int = 0, align=TOP, anchor=None) -> Button:
        btn = Button(parent_frame, text=text, command=lambda: handler(*handler_args))
        btn.pack(pady=pady, padx=padx, side=align, anchor=anchor)
        return btn

    def __create_main_frame(self) -> Frame:
        main_frame = Frame(self.__root, width=self.WIDTH/4, height=self.HEIGHT)
        main_frame.grid(row=0,column=0,rowspan=5)
        main_frame.pack_propagate(False)
        return main_frame

    def __create_obj_list_frame(self, main_frame: Frame) -> Frame:
        obj_list_frame = LabelFrame(main_frame, text="Display File", font=('Helvetica', self.FONT_SIZE_DEFAULT),
            width=self.WIDTH/4, height=self.HEIGHT*4/6, borderwidth=2, relief=GROOVE)
        obj_list_frame.pack(padx=10, pady=10, side=TOP, anchor=NW, fill=Y, expand=True)
        obj_list_frame.pack_propagate(False)

        list_box = Listbox(obj_list_frame, listvariable=self.__obj_varlist, selectmode=SINGLE, bg="#fff")
        list_box.pack(pady=1, padx=4, side=TOP, anchor=NW, fill=BOTH, expand=True)
        
        self.__create_button(obj_list_frame, "Remover Objeto", self.__handle_remove_obj_btn, list_box, padx=4, pady=2, align=LEFT)
        self.__create_button(obj_list_frame, "Adicionar Objeto", self.__handle_add_obj_btn, padx=4, pady=2, align=RIGHT)
        
        return obj_list_frame

    def __create_navigation_frame(self, main_frame: Frame) -> Frame:
        navigation_frame = LabelFrame(main_frame, text="Navegação", font=('Helvetica', self.FONT_SIZE_DEFAULT), 
            width=self.WIDTH/4, height=self.HEIGHT*2/6, borderwidth=2, relief=GROOVE)
        navigation_frame.pack(padx=10, pady=10, side=TOP, anchor=NW)
        navigation_frame.grid_propagate(False)

        for i in range(3):
            navigation_frame.rowconfigure(i, weight=1, uniform='r')
            navigation_frame.columnconfigure(i, weight=1, uniform='c')
        navigation_frame.columnconfigure(3, weight=1, uniform='c')
        
        Button(navigation_frame, text="Zoom Out", command=lambda: self.__handle_zoom('out')).grid(row=0, column=3,padx=2)
        Button(navigation_frame, text="Zoom In", command=lambda: self.__handle_zoom('in')).grid(row=2, column=3,padx=2)
        
        Button(navigation_frame, text="↑", command=lambda: self.__handle_nav('up')).grid(row=0, column=1)
        Button(navigation_frame, text="←", command=lambda: self.__handle_nav('left')).grid(row=1, column=0)
        Button(navigation_frame, text="→", command=lambda: self.__handle_nav('right')).grid(row=1, column=2)
        Button(navigation_frame, text="↓", command=lambda: self.__handle_nav('down')).grid(row=2, column=1)
        
        return navigation_frame
    
    def __create_output_frame(self, main_frame: Frame) -> Frame:
        output_frame = LabelFrame(self.__root, text="Console", font=('Helvetica', self.FONT_SIZE_DEFAULT), 
            width=self.WIDTH*3/4, height=self.HEIGHT*2/6, borderwidth=2, relief=GROOVE)
        output_frame.grid(row=4,column=1,rowspan=5,sticky=NW,padx=10, pady=10)
        output_frame.pack_propagate(False)
        self.output = Text(output_frame, width=940, height=220, bg="white",fg="black")
        self.output.pack(padx=4, pady=2, fill=BOTH)
        return output_frame

    def __create_add_obj_form(self) -> None:
        form = Toplevel(self.__root)
        form.title("Adicionar Objeto")
        
        form_frame = Frame(form, width=400, height=600)
        form_frame.pack(fill=BOTH, expand=True)
        form_frame.pack_propagate(False)

        self.__create_label(form_frame, "Nome do novo objeto:", pady=6, padx=10, anchor=NW)
        obj_name_input = self.__create_input(form_frame, padx=7, anchor=NW)

        tabs = Notebook(form_frame)
        tabs.pack(pady=10, fill=BOTH, expand=True)
        tabs_coords_inputs = []
        for i, tab_name in enumerate(['Ponto', 'Linha', 'Wireframe']):
            tab_frame = Frame(tabs)
            tab_frame.pack(fill=BOTH, expand=True)
            self.__create_label(tab_frame, "Coordenadas:", pady=4, padx=10, anchor=NW)
            coords_inputs = []
            for _ in range(i+1):
                coords_inputs = self.__add_coord_inputs(tab_frame, coords_inputs)
            tabs_coords_inputs.append(coords_inputs)

            if tab_name == 'Wireframe':
                self.__create_button(tab_frame, "+", self.__add_coord_inputs, tab_frame, tabs_coords_inputs[2], align=RIGHT)
                self.__create_button(tab_frame, "–", self.__remove_last_coords_input, tabs_coords_inputs[2], align=RIGHT)
            
            tabs.add(tab_frame, text=tab_name)
        
        self.__create_button(form_frame, "Adicionar", self.__handle_add_obj_form, form, tabs, obj_name_input, tabs_coords_inputs, pady=10, align=BOTTOM)
    

    def __create_gui(self) -> None:
        main_frame = self.__create_main_frame()
        self.__create_obj_list_frame(main_frame)
        self.__create_navigation_frame(main_frame)
        self.__create_output_frame(main_frame)

    def __handle_remove_obj_btn(self, list_box: Listbox) -> None:
        if list_box.curselection() == (): return
        selected_idx, = list_box.curselection()
        self.__controller.display_file.remove_at(selected_idx)

    def __handle_add_obj_btn(self) -> None:
        self.__create_add_obj_form()

    def __handle_add_obj_form(self, form: Toplevel, tabs: Notebook, obj_name_input: Entry,
            tabs_coords_inputs: List[List[Tuple[Entry, Entry]]]) -> None:
        if not obj_name_input.get(): return
        obj_coords = [Coordenada2D(float(x.get()), float(y.get()))
                      for (x, y) in tabs_coords_inputs[tabs.index(tabs.select())]]
        self.__controller.criar_objeto(obj_name_input.get(), tabs.index(tabs.select())+1, obj_coords)
        form.destroy()
        
    def __handle_nav(self, direcao: Literal['up', 'down', 'left', 'right']) -> None:
        self.__controller.navegar(direcao)

    def __handle_zoom(self, direcao: Literal['in', 'out']) -> None:
        self.__controller.zoom(1 if direcao == 'in' else 2)

    def __add_coord_inputs(self, parent_frame: Frame, coords_inputs: List[Tuple[Entry, Entry]]) -> List[Tuple[Entry, Entry]]:
        inputs_frame = Frame(parent_frame)
        inputs_frame.pack(pady=10, fill=X)
        x_input = self.__create_input(inputs_frame, "x", padx=5, align=LEFT)
        y_input = self.__create_input(inputs_frame, "y", padx=5, align=LEFT)
        coords_inputs.append((x_input, y_input))
        return coords_inputs
    
    def __remove_last_coords_input(self, coords_inputs: List[Tuple[Entry, Entry]]) -> List[Tuple[Entry, Entry]]:
        if len(coords_inputs) <= 3: return coords_inputs
        for input in coords_inputs.pop():
            input.master.destroy()
        return coords_inputs

    def run(self) -> None:
        self.__create_gui()

    def update(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def create_canvas(self):
        canvas = Canvas(self.__root, bg="white", width=self.WIDTH*3/4, height=self.HEIGHT*4/6-3)
        canvas.grid(row=0,column=1,sticky=NW,rowspan=3,padx=10,pady=10)
        return canvas
    
    def update_obj_varlist(self, objects: List[Objetos]) -> None:
        obj_list = [displayable.get_nome() for displayable in objects]
        self.__obj_varlist.set(obj_list)

