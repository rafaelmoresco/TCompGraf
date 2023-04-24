from objetos.curva import Curva
from matriz_suporte import MatrixHelper
from algoritmos_curva import CurveAlgorithms


class BSpline(Curva):

    def _constraint_check(self):
        pass  # TODO: implement this

    def _get_drawable_points(self):
        return self._coordinates  # TODO: improve this

    def _get_method_matrix(self):
        return [
            [-1 / 6, 3 / 6, -3 / 6, 1 / 6],
            [3 / 6, -1, 3 / 6, 0],
            [-3 / 6, 0, 3 / 6, 0],
            [1 / 6, 4 / 6, 1 / 6, 0]
        ]

    def _get_drawable_lines(self):
        lines = []
        Mbs = self._get_method_matrix()

        fi = 1/self._resolution

        Efi = [
            [0, 0, 0, 1],
            [fi * fi * fi, fi * fi, fi, 0],
            [6 * fi * fi * fi, 2 * fi * fi, 0, 0],
            [6 * fi * fi * fi, 0, 0, 0]
        ]

        for i in range(-1, len(self._coordinates) -2):
            Gx = [
                [self._coordinates[i if i != -1 else 0].x],
                [self._coordinates[i+1].x],
                [self._coordinates[i+2].x],
                [self._coordinates[i+3 if i + 3 < len(self._coordinates) else i + 2].x],
                ]
            Cx = MatrixHelper.mul(Mbs, Gx)
            Dx = MatrixHelper.mul(Efi, Cx)

            Gy = [
                [self._coordinates[i if i != -1 else 0].y],
                [self._coordinates[i+1].y],
                [self._coordinates[i+2].y],
                [self._coordinates[i+3 if i + 3 < len(self._coordinates) else i + 2].y],
                ]
            Cy = MatrixHelper.mul(Mbs, Gy)
            Dy = MatrixHelper.mul(Efi, Cy)

            lines += (CurveAlgorithms.forward_differences(number_of_points=self._resolution, Dx=Dx, Dy=Dy))

        return lines