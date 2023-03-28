import sys
if __name__ == "__main__":
    sys.path.append("..")

from lib.Point import *
from lib.liste import copie_liste
from lib.eval_fonc import horner

class Bezier:

    def __init__(self, pt_controle, coul="black", ep=3, nb_u=10):
        self._controle = pt_controle

        self._interpolation = nb_u # le nombre de points d'interpolation

        self._coul = coul

        self._ep = ep

    @property
    def p_controle(self):
        return self._controle

    def __getitem__(self, index):
        return self._controle[index]

    def __setitem__(self, index, val):
        self._controle[index] = val

    def __iter__(self):
        self._n = len(self._controle)
        self._i = -1
        return self

    def __next__(self):
        if self._i < self._n-1:
            self._i += 1
            return self._controle[self._i]
        raise StopIteration

    @property
    def coul(self):
        return self._coul

    @property
    def ep(self):
        return self._ep

    @property
    def interpolation(self):
        return self.interpolation



    def trouver_point(self,u):
        """
        Trouve le point des barycentres pour la valeur u
        """

        M = copie_liste(self._controle) # copie des points de contrôle

        # Tant qu'il y a des + de 1 point, on calcule les barycentres des points restants
        while len(M) != 1:

            N = [] # nouvelle liste pour la génération suivante

            for i in range(len(M)-1):

                N.append((1-u)*M[i] + u*M[i+1])

            M = N

        M[0].coul = self.coul # Le point prend la couleur de la courbe
        M[0].ep = self.ep

        return M[0]



    def bezier1(self):
        """
        Trace la courbe de Bézier sans l'utilisation des polynomes de Bernstein
        """
        pts = []

        # On calcule les points avec un pas régulier pour u (i/nb_u)
        for i in range(nb_u+1):
            pts.append(self.trouver_point(i/self._interpolation))

        return pts

    def trouver_point_bernstein(self,u):
        """
        Trouver le point d'interpolation grace aux polynomes de Bernstein
        """
        B0 = [1,-3,3,-1]
        B1 = [0,3,-6,3]
        B2 = [0,0,3,-3]
        B3 = [0,0,0,1]

        M = self._controle

        point = horner(B0,u)*M[0] + horner(B1,u)*M[1] + horner(B2,u)*M[2] + horner(B3,u)*M[3]

        point.coul = self.coul # Le point prend la couleur de la courbe
        point.ep = self.ep
        return point

    def bezier_polynome(self):
        """
        Trace la courbe de bézier en utilisant les polynomes de Bernstein et donc
        la factorisation de Horner. QUE DES CUBIQUES !
        """

        pts = []

        # On calcule les points avec un pas régulier pour u (i/nb_u)
        for i in range(self._interpolation+1):
            pts.append(self.trouver_point_bernstein(i/self._interpolation))

        return pts





    def __str__(self):
        ch = ""
        for el in self._controle:
            ch += Point2D.__str__(el) + "\n"

        return ch


if __name__ == "__main__":

    M = [Point2D(0,0), Point2D(0,1), Point2D(1,1), Point2D(1,0)]

    C = Bezier(M)
    pt = C.bezier1(10)

    for el in pt:
        print(el)


    print(C)
