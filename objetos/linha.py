from objetos.objetos import Objetos

class Linha(Objetos):

    def _constraint_check(self):
        if len(self._coordinates) != 2:
            raise Exception("A linha precisa de duas coordenadas")
    
    def _get_drawable_lines(self):
        return [self._coordinates]

    def _get_drawable_points(self):
        return self._coordinates