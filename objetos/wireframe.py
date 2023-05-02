from objetos.objetos import Objetos

# Poligono
class Wireframe(Objetos):
    def _constraint_check(self):
        if len(self._coordinates) < 2 and len(self._coordinates) % 2 != 0:
            raise Exception("A wireframe must have at least 2 coordinates")
    
    def _get_drawable_lines(self):
        lines = [[self._coordinates[i], self._coordinates[i+1]] for i in range(0, len(self._coordinates), 2)]
        return lines

    def _get_drawable_points(self):
        return self._coordinates