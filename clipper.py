from typing import Tuple, Union
from coordenada import Coordenada2D

class Clipper:
   
    @staticmethod
    def liang_barsky_clip(point1: Coordenada2D, point2: Coordenada2D, 
            w_min: Coordenada2D = Coordenada2D(-1, -1), 
            w_max: Coordenada2D = Coordenada2D(1, 1)) -> Union[Tuple[Coordenada2D, Coordenada2D], None]:
       
        def parametrize_liang_barsky(p, q):
            t1, t2 = 0, 1
            if p == 0:  # parallel
                if q < 0:
                    t1 = t2 + 1
            elif p < 0:  # entering
                t1 = max(0, q / p)
            else:  # exiting
                t2 = min(1, q / p)
            return t1, t2

        x1, x2 = point1.x, point2.x
        y1, y2 = point1.y, point2.y

        p1 = lambda: -(x2 - x1)
        p2 = lambda: x2 - x1 # right
        p3 = lambda: -(y2 - y1)  # bottom
        p4 = lambda: (y2 - y1) # top

        q1 = lambda: x1 - w_min.x
        q2 = lambda: w_max.x - x1
        q3 = lambda: y1 - w_min.y
        q4 = lambda: w_max.y - y1

        ps = [p1, p2, p3, p4]
        qs = [q1, q2, q3, q4]

        for i in range(len(ps)):
            t1, t2 = parametrize_liang_barsky(ps[i](), qs[i]())
            if t1 > t2:
                return None
            x1 = x1 + t1*(x2 - x1)
            x2 = x1 + t2*(x2 - x1)
            y1 = y1 + t1 * (y2 - y1)
            y2 = y1 + t2 * (y2 - y1)

        return Coordenada2D(x1, y1), Coordenada2D(x2, y2)
    
    @staticmethod
    def cohen_sutherland_clip(point1: Coordenada2D, point2: Coordenada2D,
            w_min: Coordenada2D = Coordenada2D(-1, -1),
            w_max: Coordenada2D = Coordenada2D(1, 1)) -> Union[Tuple[Coordenada2D, Coordenada2D], None]:

        INSIDE = 0
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8

        def to_region_code(p: Coordenada2D):
            code = INSIDE
            if p.x < w_min.x:
                code |= LEFT
            elif p.x > w_max.x:
                code |= RIGHT
            if p.y < w_min.y:
                code |= BOTTOM
            elif p.y > w_max.y:
                code |= TOP

            return code

        x1, x2 = point1.x, point2.x
        y1, y2 = point1.y, point2.y

        r_code1 = to_region_code(point1)
        r_code2 = to_region_code(point2)

        accept = False

        while True:
            if not (r_code1 | r_code2): # two points inside
                accept = True
                break
            elif r_code1 & r_code2: # line outside
                break
            else:
                out_code = r_code2 if r_code2 > r_code1 else r_code1
                x, y = None, None
                if out_code & TOP:
                    x = x1 + (x2 - x1) * (w_max.y - y1) / (y2 - y1)
                    y = w_max.y
                elif out_code & BOTTOM:
                    x = x1 + (x2 - x1) * (w_min.y - y1) / (y2 - y1)
                    y = w_min.y
                elif out_code & RIGHT:
                    y = y1 + (y2 - y1) * (w_max.x - x1)/ (x2 - x1)
                    x = w_max.x
                elif out_code & LEFT:
                    y = y1 + (y2 - y1) * (w_min.x - x1) / (x2 - x1)
                    x = w_min.x

                if out_code == r_code1:
                    x1 = x
                    y1 = y
                    x1, y1 = x, y
                    r_code1 = to_region_code(Coordenada2D(x1, y1))
                else:
                    x2 = x
                    y2 = y
                    x2, y2 = x, y
                    r_code2 = to_region_code(Coordenada2D(x2, y2))

        return (Coordenada2D(x1, y1), Coordenada2D(x2, y2)) if accept else None