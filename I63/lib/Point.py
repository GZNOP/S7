from lib.Vecteur import *

class Point2D(Vecteur):

    def __init__(self, x, y, coul="black", ep=3):
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

    @property
    def ep(self):
        return self._ep
