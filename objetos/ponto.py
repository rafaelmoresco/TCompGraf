from objetos.objetos import Objetos


class Ponto(Objetos):
    def _constraint_check(self):
        if len(self._coordinates) != 1:
            raise Exception("Ponto precisa de uma coordenada")
    
    def _get_drawable_lines(self):
        return []

    def _get_drawable_points(self):
        return self._coordinates
