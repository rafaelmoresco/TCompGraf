from typing import List
from coordenada import Coordenada2D


class CurveAlgorithms:

    @staticmethod
    def forward_differences(number_of_points: int,
                            Dx: List[List[float]], Dy: List[List[float]]) -> List[List[Coordenada2D]]:
        x = Dx[0][0]
        y = Dy[0][0]
        old_x = x
        old_y = y
        lines = []
        for i in range(0, number_of_points):
            x += Dx[1][0]
            Dx[1][0] += Dx[2][0]
            Dx[2][0] += Dx[3][0]

            y += Dy[1][0]
            Dy[1][0] += Dy[2][0]
            Dy[2][0] += Dy[3][0]
            lines.append([Coordenada2D(old_x, old_y), Coordenada2D(x, y)])

            old_x = x
            old_y = y

        return lines