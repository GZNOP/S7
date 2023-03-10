from lib.Vecteur import *

class Point2D(Vecteur):

    def __init__(self, x=0, y=0, coul="black", ep=3):
        """
        Constructeur d'un point dans un plan
        """

        Vecteur.__init__(self,[x,y,1])

        # Nouvel attribut qui correspond à la couleur du point
        self._coul = coul
        self._ep = 3

    @property
    def coul(self):
        return self._coul

    @coul.setter
    def coul(self, val):
        self._coul = val

    @property
    def ep(self):
        return self._ep

    @ep.setter
    def ep(self, val):
        self._ep = val

    def __mul__(self,k):
        res = Point2D()
        res.x = self.x * k
        res.y = self.y * k
        return res

    def __rmul__(self,k):
        res = Point2D()
        res.x = self.x * k
        res.y = self.y * k
        return res

    def __add__(self, vec):
        res = Point2D()
        res.x = self.x + vec.x
        res.y = self.y + vec.y
        return res


    def __radd__(self, vec):
        res = Point2D()
        res.x = self.x + vec.x
        res.y = self.y + vec.y
        return res
