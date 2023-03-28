import lib.Point

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
