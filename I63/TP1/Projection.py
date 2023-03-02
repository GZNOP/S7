import sys
from sys import argv

if __name__ == "__main__":
    sys.path.append("..")

import lib.Vecteur as v
import lib.Matrice as m
import tkinter as tk
from lib.eval_fonc import evaluer_fonction

"""

PENSER QUE LES POINTS SONT DE DIMENSION 3 POUR L'HOMOGÉNÉITÉ DE LA MATRICE !!!!!!!!!!! 3H DE PERDUES BOUFFON

"""


class Projection:

    def __init__(self, ca, tag, WC, DC, coul="red"):
        if len(WC) + len(DC) != 4 and type(WC[0]) is not v.Vecteur and type(DC[0]) is not v.Vecteur:
            raise ValueError
        # On associe tout de suite notre projection à un canvas
        self._canvas = ca

        # On associe un tag à tous les objets de la viewport
        self._tag = tag

        self._hauteur = int(self._canvas["height"])

        self._WC = WC # liste de deux points

        self._DC = DC # liste de deux points

        self._M = self.calculer_matrice() # La matrice de projection

        self._point = [] # Une liste de points

        self._coul = coul

        self._X = None

        self._Y = None

        self._ep = 3

        self._canvas.create_rectangle(self.DC0.x, self._hauteur - self.DC0.y, self.DC1.x,\
        self._hauteur - self.DC1.y, fill="grey", tag=self._tag)

        self._canvas.tag_bind(self._tag,"<Button-1>", lambda event: self.obtenir_xy(event))
        self._canvas.tag_bind(self._tag,"<B1-Motion>", lambda event: self.deplacer_fen(event))
        self._canvas.tag_bind(self._tag,"<ButtonRelease-1>", lambda event: self.maj_viewport(event))


    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, l_point):
        if type(l_point[0]) is not v.Vecteur:
            raise ValueError

        self._point = l_point
        self.projeter_liste()

    @property
    def canvas(self):
        return self._canvas

    @property
    def tag(self):
        return self._tag

    # Premier point qui définit le WC
    @property
    def WC0(self):
        return self._WC[0]

    # Deuxieme point qui définit le WC
    @property
    def WC1(self):
        return self._WC[1]

    # Premier point qui définit le DC
    @property
    def DC0(self):
        return self._DC[0]

    # Deuxieme point qui définit le DC
    @property
    def DC1(self):
        return self._DC[1]

    # BUG: FINIR LES PROPERTIES


    # ----------------------------
    # CALLBACKS
    def obtenir_xy(self,event):

        self._X = event.x
        self._Y = event.y

    def deplacer_fen(self,event):

        dx = event.x - self._X
        dy = event.y - self._Y

        self._X = event.x
        self._Y = event.y
        self._canvas.delete(f"point_{self._tag}")
        self._canvas.move(self._tag, dx, dy)

    def maj_viewport(self, event):
        tmp = ca.coords(self._tag)
        dy = tmp[3] - tmp[1]

        self.DC0.x = tmp[0]
        self.DC0.y = self._hauteur - tmp[1] - dy
        self.DC1.x = tmp[2]
        self.DC1.y = self._hauteur - tmp[3] + dy

        self._M = self.calculer_matrice()
        self.projeter_liste()

    # ---------------------------------------------------------------------

    def calculer_matrice(self):
        """
        Calcule la matrice de projection
        """

        dxw = (self.WC1.x - self.WC0.x)
        dyw = (self.WC1.y - self.WC0.y)
        dxv = (self.DC1.x - self.DC0.x)
        dyv = (self.DC1.y - self.DC0.y)


        # Calcule de la matrice

        M = m.Matrice(3,3)
        M[0] = [ dxv/dxw  , 0 , - self.WC0.x * dxv / dxw + self.DC0.x ]
        M[1] = [ 0 , - dyv/dyw , self.WC0.y * dyv / dyw + dyv + (self._hauteur - self.DC1.y)]
        M[2] = [ 0 , 0 , 1 ]

        return M


    def projeter_point(self, point):
        """
        projette un point unique dans le DC
        """

        res = self._M * point
        self._canvas.create_rectangle(res.x-self._ep, res.y-self._ep, res.x+self._ep, res.y+self._ep,\
        width=0, fill=self._coul, tag=f"point_{self._tag}")

    def projeter_liste(self):
        """
        projette les points de la liste
        """
        for p in self._point:
            res = self._M * p
            self._canvas.create_rectangle(res.x-self._ep, res.y-self._ep, res.x+self._ep, res.y+self._ep,\
            width=0, fill=self._coul, tag=f"point_{self._tag}")

    def projetter_fichier(self, nom_fichier):
        """
        Projette les points du fichier passé en paramêtre
        """

        fic = open(nom_fichier,"r")

        for line in fic:
            try:
                tmp = line.split()
                x = float(tmp[0])
                y = float(tmp[1])

                point = v.Vecteur([x,y,1])

                self + point

            except:
                print("Err fichier")
                raise Exception

    def projetter_fonction(xmin ,xmax, nb_point, P):
        """
        Projette un polynome dans le DC
        """

        pts = evaluer_fonction(xmin, xmax, nb_point, P)

        for point in pts :
            vp = v.Vecteur([point[0], point[1], 1])
            self + vp

    def __add__(self, point):
        """
        Ajoute le point dans la liste de points
        """
        if type(point) is v.Vecteur:
            self._point.append(point)
            self.projeter_point(point)
