import lib.Point as p

class Segment:

    def __init__(self, A, B, coul="black", ep=3):

        self._coul = coul

        self._P1 = A

        self._P2 = B

        self._ep = ep

    @property
    def P1(self):
        return self._P1

    @P1.setter
    def P1(self, val):
        self._P1 = val

    @property
    def P2(self):
        return self._P2

    @P2.setter
    def P2(self, val):
        self._P2 = val

    @property
    def coul(self):
        return self._coul

    @property
    def ep(self):
        return self._ep

    def intersection(S1, S2):
        """ Calcule le point d'intersection entre deux segments """

        A = S1.P1
        B = S1.P2
        C = S2.P1
        D = S2.P2

        det = (B.x - A.x) * (C.y - D.y) - (C.x - D.x) * (B.y - A.y)
        if det == 0:
            return None # Segment parallèle

        else:
            t1 = ((C.x - A.x) * (C.y - D.y) - (C.x - D.x) * (C.y - A.y)) / det
            t2 = ((B.x - A.x) * (C.y - A.y) - (C.x - A.x) * (B.y - A.y)) / det
            
            if 0 <= t1 <= 1 and 0 <= t2 <= 1:
                
                if t1 == 0:
                    x,y = A.x,A.y
                elif t1 == 1:
                    x,y = B.x,B.y
                elif t2 == 0:
                    x,y = C.x,C.y
                elif t2 == 1:
                    x,y = D.x, D.y
                else:
                    x = A.x + t1 * (B.x - A.x)
                    y = A.y + t1 * (B.y - A.y)

                return p.Point2D(x,y)
            
            else:
                # Pas d'intersection
                return None
