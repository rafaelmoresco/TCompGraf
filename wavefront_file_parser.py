import re
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple
from coordenada import Coordenada2D, Coordenada3D
from objetos.objetos import Objetos
from objetos.ponto import Ponto
from objetos.wireframe import Wireframe
from objetos.linha import Linha
from objetos.janela import Window

@dataclass
class MaterialObject:
    name: str
    diffuse_color: Tuple[float, float, float]

    def __post_init__(self):
        if self.diffuse_color is None:
            self.diffuse_color = tuple(0, 0, 0)

@dataclass
class WavefrontObject:
    name: str
    vertices: List[Coordenada3D]
    material: MaterialObject
    vertices_idx: List[int]

class WavefrontFileParser:
    @staticmethod
    def __parse_displayables(displayables: List[Objetos]) -> Tuple[List[WavefrontObject], List[MaterialObject]]:
        # gera material objects
        materials_dict = dict.fromkeys([displayable.get_cor() for displayable in displayables])
        for hex_color in materials_dict:
            materials_dict[hex_color] = MaterialObject(
                hex_color,
                WavefrontFileParser.__rgb_hex_to_float(hex_color)
            )
        # gera wavefront objects
        w_objects = []
        for displayable in displayables:
            coords = displayable.get_coordinates()
            w_objects.append(
                WavefrontObject(
                    name=displayable.get_nome(),
                    vertices=[Coordenada3D(coord.x, coord.y, 0) for coord in coords],
                    material=materials_dict[displayable.get_cor()],
                    vertices_idx=[]
                )
            )
        return w_objects, materials_dict.values()

    @staticmethod
    def __dump_material_file(materials: List[MaterialObject]) -> str:
        filename = 'materials.mtl'
        filepath = f'exported/{filename}'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as material_file:
            for material in materials:
                material_file.write(f'newmtl {material.name}\n')
                material_file.write(f'Kd {" ".join(map(str, material.diffuse_color))}\n')
        return filename

    @staticmethod
    def __dump_wavefront_file(objects: List[WavefrontObject], mtllib: str) -> None:
        vertices_str = []
        obj_descriptions = []
        for obj in objects:
            cur_idx = len(vertices_str)
            last_idx = cur_idx + len(obj.vertices)
            obj.vertices_idx = list(range(cur_idx+1, last_idx+1))
            vertices_str.extend([f'v {" ".join(map(str, coord))}\n' for coord in obj.vertices])
            
            obj_descriptions.append(f'o {obj.name}\n')
            obj_descriptions.append(f'usemtl {obj.material.name}\n')
            obj_descriptions.append(f'{"p" if len(obj.vertices) == 1 else "l"} {" ".join(map(str, obj.vertices_idx))}\n')

        filename = 'drawables.obj'
        filepath = f'exported/{filename}'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as wavefront_file:
            wavefront_file.writelines(vertices_str)
            wavefront_file.write(f'mtllib {mtllib}\n')
            wavefront_file.writelines(obj_descriptions)

    @staticmethod
    def __rgb_hex_to_float(hex_str: str) -> Tuple[float, float, float]:
        if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hex_str):
            div = 255.0
            if len(hex_str) <= 4:
                return tuple(int(hex_str[i]*2, 16) / div for i in (1, 2, 3))
            return tuple(int(hex_str[i:i+2], 16) / div for i in (1, 3, 5))
        raise ValueError(f'"{hex_str}" is not a valid HEX code.')

    @staticmethod
    def __rgb_float_to_hex(rgb_vals: Tuple[float, float, float]) -> str:
        int_rgb_vals = [max(0, min(int(val*255), 255)) for val in rgb_vals]
        return '#%02x%02x%02x' % tuple(int_rgb_vals)

    @staticmethod
    def __load_wavefront_file(filepath: str) -> Tuple[List[Coordenada3D], List[MaterialObject], List[List[str]]]:
        wavefront_file = open(filepath, 'r')
        content = wavefront_file.readlines()
        wavefront_file.close()
        V: List[str] = []
        materials = None
        obj_descriptions = []
        for i in range(len(content)):
            content[i] = content[i].strip()
            splitted_line = content[i].split()
            if splitted_line[0] == 'v':
                V.append(content[i])
            elif splitted_line[0] == 'mtllib':
                mtllib = f'{os.path.dirname(filepath)}/{splitted_line[1]}'
                materials = WavefrontFileParser.__load_materials_from_file(mtllib)
            elif splitted_line[0] == 'o':
                obj_desc = [content[i]]
                while True:
                    if i+1 >= len(content): break
                    nextline = content[i+1].split()
                    if nextline[0] == 'o':
                        break
                    else:
                        i += 1
                        obj_desc.append(content[i].strip())
                obj_descriptions.append(obj_desc)
        vertices = [Coordenada3D(list(map(float, v.split()[1:4]))) for v in V]
        return vertices, materials, obj_descriptions

    @staticmethod
    def __load_materials_from_file(filepath: str) -> List[MaterialObject]:
        materials_file = open(filepath, 'r')
        content = materials_file.readlines()
        materials_file.close()
        materials = []
        for i in range(len(content)):
            content[i] = content[i].strip()
            splitted_line = content[i].split()
            if splitted_line[0] == 'newmtl':
                mat_name = splitted_line[1]
                diffuse_color = None
                while True:
                    if i+1 >= len(content): break
                    nextline = content[i+1].split()
                    if nextline[0] == 'newmtl':
                        break
                    else:
                        i += 1
                        if nextline[0] == 'Kd':
                            diffuse_color = tuple(map(float, nextline[1:4]))
                materials.append(MaterialObject(mat_name, diffuse_color))
        return materials

    @staticmethod
    def __parse_wavefront(filepath: str) -> List[WavefrontObject]:
        vertices, materials, obj_descriptions = WavefrontFileParser.__load_wavefront_file(filepath)
        materials = { mat.name: mat for mat in materials }
        objects = []
        for obj_desc in obj_descriptions:
            name = obj_desc[0].split()[1]
            mat = None
            obj_vertices = []
            for i in range(1, len(obj_desc)):
                desc = obj_desc[i].split()
                directive = desc[0]
                arguments = desc[1::]
                if directive == 'p' or directive == 'l':
                    for p in arguments:
                        obj_vertices.append(vertices[int(p) - 1])
                elif directive == 'usemtl':
                    mat = materials[arguments[0]]
            objects.append(WavefrontObject(name, obj_vertices, mat, None))
        return objects
        

    @staticmethod
    def __wavefront_obj_to_displayable(obj: WavefrontObject) -> Objetos:
        color = WavefrontFileParser.__rgb_float_to_hex(obj.material.diffuse_color)
        coords = [Coordenada2D(v.x, v.y) for v in obj.vertices]
        if len(obj.vertices) == 1:
            return Ponto(obj.name, color, coords)
        elif len(obj.vertices) == 2:
            return Linha(obj.name, color, coords)
        elif len(obj.vertices) >= 3:
            return Wireframe(obj.name, color, coords)
    
    @classmethod
    def import_file(cls, filepath: str) -> Tuple[List[Objetos], Optional[Window]]:
        objects = cls.__parse_wavefront(filepath)
        return [cls.__wavefront_obj_to_displayable(obj) for obj in objects], None

    @classmethod
    def export_file(cls, displayables: List[Objetos], window: Window) -> None:
        objects, materials = cls.__parse_displayables(displayables)
        mtllib_filename = cls.__dump_material_file(materials)
        cls.__dump_wavefront_file(objects, mtllib_filename)