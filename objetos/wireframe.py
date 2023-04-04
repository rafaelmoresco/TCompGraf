from objetos.objetos import Objetos

# Poligono
class Wireframe(Objetos):
    def _constraint_check(self):
        if len(self._coordinates) < 3:
            raise Exception("Poligono precisa de no minimo 3 coordenadas")
    
    def _get_drawable_lines(self):
        lines = []
        size = (len(self._coordinates))
        for i in range(size):
            line = [self._coordinates[i], self._coordinates[(i+1)%size]]
            lines.append(line)
        return lines

    def _get_drawable_points(self):
        return self._coordinates