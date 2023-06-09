from __future__ import annotations
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import askyesno, showinfo
from tkinter.ttk import Notebook
from turtle import width
from typing import Callable, Final, List, Literal, Tuple
from controlador import Controlador
from coordenada import Coordenada3D
from objetos.objetos import Objetos
import re

# Toda a interface de usuário
class Gui:
    FONT_SIZE_DEFAULT: Final[int] = 13
    FONT_SIZE_TITLE: Final[int] = 18

    WIDTH: Final[int] = 1280
    HEIGHT: Final[int] = 900

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
                       padx: int = 0, align=TOP, anchor=None, pack=True, width: int = None) -> Entry:
        input = Entry(parent_frame, textvariable=StringVar(value=placeholder), width=width)
        if pack:
            input.pack(ipady=3, pady=pady, padx=padx, side=align, anchor=anchor)
        return input

    def __create_button(self, parent_frame: Frame, text: str, handler: Callable, *handler_args,
                        pady: int = 0, padx: int = 0, align=TOP, anchor=None) -> Button:
        btn = Button(parent_frame, text=text, command=lambda: handler(*handler_args))
        btn.pack(pady=pady, padx=padx, side=align, anchor=anchor)
        return btn

    def __is_valid_color(self, color_str: str) -> bool:
        # REGEX para ver se a cor é válida
        regex_hex_color = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        return True if re.search(regex_hex_color, color_str) else False

    def __create_main_frame(self) -> Frame:
        main_frame = Frame(self.__root, width=self.WIDTH/4, height=self.HEIGHT)
        main_frame.grid(row=0,column=0,rowspan=5)
        main_frame.pack_propagate(False)
        return main_frame

    def __create_obj_list_frame(self, main_frame: Frame) -> Frame:
        obj_list_frame = LabelFrame(main_frame, text="Display File", font=('Helvetica', self.FONT_SIZE_DEFAULT),
                                    width=self.WIDTH / 4, height=self.HEIGHT * 3 / 6, borderwidth=2, relief=GROOVE)
        obj_list_frame.pack(padx=10, pady=10, side=TOP, anchor=W, fill=Y, expand=True)
        obj_list_frame.pack_propagate(False)

        import_export_frame = Frame(obj_list_frame)
        import_export_frame.pack(side=TOP, fill=X)
        import_export_frame.grid_propagate(0)
        import_btn = self.__create_button(import_export_frame, "Importar", self.__handle_import_btn, pady=6, padx=4, align=LEFT)
        export_btn = self.__create_button(import_export_frame, "Exportar", self.__handle_export_btn, pady=6, padx=4, align=RIGHT)

        list_box = Listbox(obj_list_frame, listvariable=self.__obj_varlist, selectmode=SINGLE, bg="#fff")
        list_box.pack(pady=1, padx=4, side=TOP, anchor=W, fill=BOTH, expand=True)

        btns_frame = Frame(obj_list_frame, height=self.HEIGHT / 8)
        btns_frame.pack(side=TOP, fill=X)
        btns_frame.grid_propagate(0)
        for i in range(2):
            btns_frame.rowconfigure(i, weight=1, uniform='r')
            btns_frame.columnconfigure(i, weight=1, uniform='c')

        action_btn = Button(btns_frame, text="Ações", command=lambda: self.__handle_actions_obj_btn(list_box),
                            state=DISABLED)
        action_btn.grid(row=0, column=1)
        remove_btn = Button(btns_frame, text="Remover", command=lambda: self.__handle_remove_obj_btn(list_box),
                            state=DISABLED)
        remove_btn.grid(row=1, column=0)
        add_btn = Button(btns_frame, text="Adicionar", command=lambda: self.__handle_add_obj_btn())
        add_btn.grid(row=1, column=1)

        list_box.bind('<<ListboxSelect>>', lambda evt: self.__on_obj_list_select(evt, [action_btn, remove_btn]))

        return obj_list_frame

    def __create_navigation_frame(self, main_frame: Frame) -> Frame:
        navigation_frame = LabelFrame(main_frame, text="Navegação", font=('Helvetica', self.FONT_SIZE_DEFAULT), 
            width=self.WIDTH / 4, height=self.HEIGHT * 1 / 5, borderwidth=2, relief=GROOVE)
        navigation_frame.pack(padx=10, pady=10, side=TOP, anchor=W, fill=X, expand=True)
        navigation_frame.grid_propagate(False)

        for i in range(5):
            navigation_frame.rowconfigure(i, weight=1, uniform='r')
            navigation_frame.columnconfigure(i, weight=1, uniform='c')
        navigation_frame.columnconfigure(3, weight=1, uniform='c')
        
        Button(navigation_frame, text="↶", command=lambda: self.__handle_rotate('left')).grid(row=0, column=0)
        Button(navigation_frame, text="↷", command=lambda: self.__handle_rotate('right')).grid(row=0, column=4)

        Button(navigation_frame, text="↑", command=lambda: self.__handle_nav('up')).grid(row=0, column=2)
        Button(navigation_frame, text="←", command=lambda: self.__handle_nav('left')).grid(row=2, column=0)
        Button(navigation_frame, text="→", command=lambda: self.__handle_nav('right')).grid(row=2, column=4)
        Button(navigation_frame, text="↓", command=lambda: self.__handle_nav('down')).grid(row=4, column=2)

        Button(navigation_frame, text="⮝", command=lambda: self.__handle_tilt('up')).grid(row=1, column=2)
        Button(navigation_frame, text="⮜", command=lambda: self.__handle_tilt('left')).grid(row=2, column=1)
        Button(navigation_frame, text="⮞", command=lambda: self.__handle_tilt('right')).grid(row=2, column=3)
        Button(navigation_frame, text="⮟", command=lambda: self.__handle_tilt('down')).grid(row=3, column=2)

        Button(navigation_frame, text="↥", command=lambda: self.__handle_move('forward')).grid(row=4, column=4)
        Button(navigation_frame, text="↧", command=lambda: self.__handle_move('backward')).grid(row=4, column=3)

        Button(navigation_frame, text="+", command=lambda: self.__handle_zoom('in')).grid(row=4, column=1)
        Button(navigation_frame, text="–", command=lambda: self.__handle_zoom('out')).grid(row=4, column=0)
        
        return navigation_frame
    
    def __create_clipping_frame(self, main_frame: Frame) -> Frame:
        clipping_frame = LabelFrame(main_frame, text='Técnica de Clipping', font=('Helvetica', self.FONT_SIZE_DEFAULT),
                                    width=self.WIDTH / 4, height=self.HEIGHT * 1 / 6, borderwidth=2, relief=GROOVE)
        clipping_frame.pack(padx=10, pady=10, side=TOP, anchor=W, fill=X, expand=True)
        clipping_frame.grid_propagate(0)

        clipping_method = StringVar()
        clipping_method.set('cohen_sutherland')
        Radiobutton(clipping_frame, text='Cohen-Sutherland', variable=clipping_method, value='cohen_sutherland',
                        command=lambda: self.__on_clipping_method_change(clipping_method.get())).pack(anchor=W, pady=6)
        Radiobutton(clipping_frame, text='Liang-Barsky', variable=clipping_method, value='liang_barsky',
                        command=lambda: self.__on_clipping_method_change(clipping_method.get())).pack(anchor=W, pady=6)

        self.__on_clipping_method_change(clipping_method.get())
    
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

        self.__create_label(form_frame, "Cor do novo objeto:", pady=6, padx=10, anchor=NW)
        obj_color_input = self.__create_input(form_frame, padx=7, anchor=NW, placeholder="#000")

        tabs = Notebook(form_frame)
        tabs.pack(pady=10, fill=BOTH, expand=True)
        tabs_coords_inputs = []
        for i, tab_name in enumerate(['Ponto', 'Linha', 'Wireframe', 'Bezier', 'B Spline']):
            tab_frame = Frame(tabs)
            tab_frame.pack(fill=BOTH, expand=True)
            self.__create_label(tab_frame, "Coordenadas:", pady=4, padx=10, anchor=NW)
            coords_inputs = []
            if tab_name == 'Bezier' and tab_name == 'B Spline':
                coords_inputs = self.__add_coord_inputs(tab_frame, coords_inputs, 4)
            else:
                for _ in range(i + 1):
                    coords_inputs = self.__add_coord_inputs(tab_frame, coords_inputs, 2 if tab_name == 'Wireframe' else 1)
            tabs_coords_inputs.append(coords_inputs)

            if tab_name == 'Wireframe' or tab_name == 'Bezier' or tab_name == 'B Spline':
                self.__create_button(tab_frame, "+", self.__add_coord_inputs, tab_frame, tabs_coords_inputs[i],
                                     4 if tab_name == 'Bezier' else 2 if tab_name == 'Wireframe' else 1, align=RIGHT)
                self.__create_button(tab_frame, "–", self.__remove_last_coords_input, tabs_coords_inputs[i],
                                    4 if tab_name == 'Bezier' else 2 if tab_name == 'Wireframe' else 1, align=RIGHT)

            tabs.add(tab_frame, text=tab_name)

        self.__create_button(form_frame, "Adicionar", self.__handle_add_obj_form, form, tabs, obj_name_input,
                             obj_color_input, tabs_coords_inputs, pady=10, align=BOTTOM)
    
    def __create_action_obj_form(self, obj: Objetos) -> None:
        form = Toplevel(self.__root)
        form.title("Ações")
        form_frame = Frame(form, width=500, height=600)
        form_frame.pack(fill=BOTH, expand=True)
        form_frame.pack_propagate(False)
        self.__create_label(form_frame, f'Objeto selecionado: {obj.get_nome()}', pady=25, padx=25, anchor=NW)

        tabs = Notebook(form_frame)
        tabs.pack(fill=BOTH, expand=True)
        tabs.add(self.__create_translate_frame(tabs, obj), text='Translação')
        tabs.add(self.__create_scale_frame(tabs, obj), text='Escalonamento')
        tabs.add(self.__create_rotate_frame(tabs, obj), text='Rotação')

    def __create_translate_frame(self, tabs: Notebook, obj: Objetos) -> Frame:
        frame = Frame(tabs)
        frame.pack(fill=BOTH, expand=True)
        self.__create_label(frame, "Vetor de Movimento")
        coords_frame = Frame(frame)
        x_input = self.__create_input(coords_frame, "x", padx=40, width=8)
        y_input = self.__create_input(coords_frame, "y", padx=40, width=8)
        z_input = self.__create_input(coords_frame, "z", padx=40, width=8)
        coords_frame.pack(pady=10, fill=X)
        def handle_apply_btn(objeto: Objetos, x_inp: Entry, y_inp: Entry, z_inp: Entry) -> None:
            movement_vector = Coordenada3D(float(x_inp.get()), float(y_inp.get()), float(z_inp.get()))
            self.__controller.translate_object(objeto, movement_vector)

        self.__create_button(frame, 'Aplicar', handle_apply_btn, obj, x_input, y_input, z_input, align=BOTTOM)
        return frame

    def __create_scale_frame(self, tabs: Notebook, obj: Objetos) -> Frame:
        frame = Frame(tabs)
        frame.pack(fill=BOTH, expand=True)
        self.__create_label(frame, "Vetor de Escala")
        coords_frame = Frame(frame)
        x_input = self.__create_input(coords_frame, "x", padx=40, width=8)
        y_input = self.__create_input(coords_frame, "y", padx=40, width=8)
        z_input = self.__create_input(coords_frame, "z", padx=40, width=8)
        coords_frame.pack(pady=10, fill=X)
        def handle_apply_btn(objeto: Objetos, x_inp: Entry, y_inp: Entry, z_inp: Entry) -> None:
            scale_vector = Coordenada3D(float(x_inp.get()), float(y_inp.get()), float(z_inp.get()))
            self.__controller.scale_object(objeto, scale_vector)

        self.__create_button(frame, 'Aplicar', handle_apply_btn, obj, x_input, y_input, z_input, align=BOTTOM)
        return frame

    def __create_rotate_frame(self, tabs: Notebook, obj: Objetos) -> Frame:
        frame = Frame(tabs)
        frame.pack(fill=BOTH, expand=True)

        relative_to_frame = Frame(frame)
        relative_to_frame.pack(pady=20)
        coords_frame = Frame(relative_to_frame)
        x_input = self.__create_input(coords_frame, "x", padx=40, align=LEFT, width=8)
        y_input = self.__create_input(coords_frame, "y", padx=40, align=LEFT, width=8)
        z_input = self.__create_input(coords_frame, 'z', padx=40, align=LEFT, width=8)
        coords_inputs = [x_input, y_input, z_input]
        [inp.config(state=DISABLED) for inp in coords_inputs]

        relative_to = StringVar()
        relative_to.set('world')
        Radiobutton(relative_to_frame, text="Em torno do centro do mundo", variable=relative_to, value='world',
                    command=lambda: [inp.config(state=DISABLED) for inp in coords_inputs]) \
            .pack(anchor=W, pady=8)
        Radiobutton(relative_to_frame, text="Em torno do centro do objeto", variable=relative_to, value='itself',
                    command=lambda: [inp.config(state=DISABLED) for inp in coords_inputs]) \
            .pack(anchor=W, pady=8)
        Radiobutton(relative_to_frame, text="Em torno de uma coordenada", variable=relative_to, value='coordinate',
                    command=lambda: [inp.config(state=NORMAL) for inp in coords_inputs]) \
.pack(anchor=W, pady=4)
        coords_frame.pack(pady=4)

        axis_frame = Frame(frame)
        axis_frame.pack(pady=20)
        self.__create_label(axis_frame, "Em relação ao eixo")
        axis_coords_frame = Frame(axis_frame)
        a_x_input = self.__create_input(axis_coords_frame, "x", padx=40, align=LEFT, width=8)
        a_y_input = self.__create_input(axis_coords_frame, "y", padx=40, align=LEFT, width=8)
        a_z_input = self.__create_input(axis_coords_frame, 'z', padx=40, align=LEFT, width=8)
        axis_coords_inputs = [a_x_input, a_y_input, a_z_input]
        [inp.config(state=DISABLED) for inp in axis_coords_inputs]
        axis = StringVar()
        axis.set('z')
        radio_frame = Frame(axis_frame)
        Radiobutton(radio_frame, text="x", variable=axis, value='x',
                    command=lambda: [inp.config(state=DISABLED) for inp in axis_coords_inputs]) \
            .pack(side=LEFT, padx=4)
        Radiobutton(radio_frame, text="y", variable=axis, value='y',
                    command=lambda: [inp.config(state=DISABLED) for inp in axis_coords_inputs]) \
            .pack(side=LEFT, padx=4)
        Radiobutton(radio_frame, text="z", variable=axis, value='z',
                    command=lambda: [inp.config(state=DISABLED) for inp in axis_coords_inputs]) \
            .pack(side=LEFT, padx=4)
        Radiobutton(radio_frame, text="Arbitrário", variable=axis, value='arbitrary',
                command=lambda: [inp.config(state=NORMAL) for inp in axis_coords_inputs]) \
            .pack(side=LEFT, padx=4)
        radio_frame.pack()
        axis_coords_frame.pack(pady=4)

        angle_frame = Frame(frame)
        angle_frame.pack(pady=20)
        self.__create_label(angle_frame, "Ângulo")
        angle_input = self.__create_input(angle_frame)

        def handle_apply_btn(objeto: Objetos, var_rel_to: StringVar, angle_inp: Entry,
                             x_inp: Entry, y_inp: Entry, z_inp: Entry, var_axis: StringVar,
                             a_x_inp: Entry, a_y_inp: Entry, a_z_inp: Entry) -> None:
            local_relative_to = var_rel_to.get()
            local_axis = var_axis.get()
            angle = float(angle_inp.get())
            center = None
            arbitrary_axis = None
            if local_relative_to == 'coordinate':
                center = Coordenada3D(float(x_inp.get()), float(y_inp.get()), float(z_inp.get()))
            if local_axis == 'arbitrary':
                arbitrary_axis = Coordenada3D(float(a_x_inp.get()), float(a_y_inp.get()), float(a_z_inp.get()))
                local_axis=None
            self.__controller.rotate_object(displayable=objeto,
                                            angle=angle,
                                            relative_to=local_relative_to,
                                            axis=local_axis,
                                            center=center,
                                            arbitrary_axis_coord=arbitrary_axis)

        self.__create_button(frame, 'Aplicar', handle_apply_btn, obj, relative_to, angle_input,
                            x_input, y_input, z_input, axis, a_x_input, a_y_input, a_z_input, align=BOTTOM)
        return frame

    def __create_gui(self) -> None:
        main_frame = self.__create_main_frame()
        self.__create_obj_list_frame(main_frame)
        self.__create_navigation_frame(main_frame)
        self.__create_output_frame(main_frame)
        self.__create_clipping_frame(main_frame)

    def __handle_import_btn(self) -> None:
        if askyesno(title="Atenção!", message="Essa ação sobrescreverá o Display File atual.\nProsseguir?"):
            showinfo(title="Importante!", message="Certifique-se de que o arquivo de descrição de material (.mtl) está no mesmo diretório que o de objetos (.obj)")
            filepath = filedialog.askopenfilename(title="Importar arquivo", initialdir='./', filetypes=[("Wavefront", ".obj")])
            self.__controller.import_wavefront_file(filepath)

    def __handle_export_btn(self) -> None:
        self.__controller.export_wavefront_file()
        showinfo(title="Exportado com sucesso!", message="Arquivo exportado com sucesso!\nDisponível em ./export/")
    
    def __handle_remove_obj_btn(self, list_box: Listbox) -> None:
        if list_box.curselection() == (): return
        selected_idx, = list_box.curselection()
        self.__controller.display_file.remove_at(selected_idx)

    def __handle_add_obj_btn(self) -> None:
        self.__create_add_obj_form()

    def __handle_add_obj_form(self, form: Toplevel, tabs: Notebook, obj_name_input: Entry, obj_color_input: Entry,
                              tabs_coords_inputs: List[List[Tuple[Entry, Entry, Entry]]]) -> None:
        if not obj_name_input.get(): return
        if not self.__is_valid_color(obj_color_input.get()): return
        selected_tab = tabs.index(tabs.select())
        obj_coords = [Coordenada3D(float(x.get()), float(y.get()), float(z.get()))
                      for (x, y, z) in tabs_coords_inputs[selected_tab]]
        obj_type = ['dot', 'line', 'wireframe', 'bezier', 'spline']
        obj_type = obj_type[selected_tab]
        self.__controller.criar_objeto(obj_name_input.get(), obj_color_input.get(), obj_type, obj_coords)
        form.destroy()

    def __handle_actions_obj_btn(self, list_box: Listbox) -> None:
        if list_box.curselection() == (): return
        selected_idx, = list_box.curselection()
        # TODO: this is pattern breaking, we should rethink how to do this
        selected_obj = self.__controller.display_file[selected_idx]
        self.__create_action_obj_form(selected_obj)

    def __handle_rotate(self, direction: Literal['left', 'right']) -> None:
        self.__controller.rotate_window(direction)
        
    def __handle_nav(self, direcao: Literal['up', 'down', 'left', 'right']) -> None:
        self.__controller.navegar(direcao)

    def __handle_tilt(self, direction: Literal['up', 'down', 'left', 'right']) -> None:
        self.__controller.tilt(direction)

    def __handle_move(self, direction: Literal['forward', 'backward']) -> None:
        self.__controller.move(direction)

    def __handle_zoom(self, direcao: Literal['in', 'out']) -> None:
        self.__controller.zoom(1 if direcao == 'in' else 2)

    def __add_coord_inputs(self, parent_frame: Frame, coords_inputs: List[Tuple[Entry, Entry, Entry]], n_coords: int = 1) -> List[Tuple[Entry, Entry, Entry]]:
        inputs_frame = Frame(parent_frame)
        inputs_frame.pack(pady=10, fill=X)
        for _ in range(n_coords):
            x_input = self.__create_input(inputs_frame, "x", padx=5, align=LEFT, width=5)
            y_input = self.__create_input(inputs_frame, "y", padx=5, align=LEFT, width=5)
            z_input = self.__create_input(inputs_frame, "z", padx=5, align=LEFT, width=5)
            coords_inputs.append((x_input, y_input, z_input))
        return coords_inputs
    
    def __remove_last_coords_input(self, coords_inputs: List[Tuple[Entry, Entry, Entry]], n_coords: int = 1) -> List[Tuple[Entry, Entry]]:
        if len(coords_inputs) <= n_coords: return coords_inputs
        for _ in range(n_coords):
            for input in coords_inputs.pop():
                input.forget()
                input.master.destroy()
        return coords_inputs

    def __on_obj_list_select(self, event: Event[Listbox], buttons: List[Button]) -> None:
        if event.widget.curselection():
            for button in buttons:
                button['state'] = NORMAL
        else:
            for button in buttons:
                button['state'] = DISABLED

    def __on_clipping_method_change(self, method: str):
        self.__controller.set_clipping_method(method)

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

