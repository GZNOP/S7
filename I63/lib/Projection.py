import sys
from sys import argv

if __name__ == "__main__":
    sys.path.append("..")

import lib.Segment as s
import lib.Vecteur as v
import lib.Matrice as m
import tkinter as tk
from lib.eval_fonc import evaluer_fonction

"""

PENSER QUE LES POINTS SONT DE DIMENSION 3 POUR L'HOMOGÉNÉITÉ DE LA MATRICE !!!!!!!!!!! 3H DE PERDUES BOUFFON

"""


class Projection:

    def __init__(self, ca, tag, WC, DC):
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

        self._seg = [] # liste d'instances de segments

        self._X = None

        self._Y = None

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
        self._canvas.delete(f"point_seg_{self._tag}")
        self._canvas.move(self._tag, dx, dy)

    def maj_viewport(self, event):
        tmp = self._canvas.coords(self._tag)
        dy = tmp[3] - tmp[1]

        self.DC0.x = tmp[0]
        self.DC0.y = self._hauteur - tmp[1] - dy
        self.DC1.x = tmp[2]
        self.DC1.y = self._hauteur - tmp[3] + dy

        self._M = self.calculer_matrice()
        self.projeter_segment()
        self.projeter_liste()

    # ---------------------------------------------------------------------
    def projeter_segment(self):
        """
        Projette tous les segments de la liste _seg de l'instance
        """
        for S in self._seg:
            self.segment_bresenham(S)

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
        self._canvas.create_rectangle(res.x-point.ep, res.y-point.ep, res.x+point.ep, res.y+point.ep,\
        width=0, fill=point.coul, tag=f"point_{self._tag}")

    def projeter_liste(self):
        """
        projette les points de la liste
        """
        for p in self._point:
            res = self._M * p
            self._canvas.create_rectangle(res.x-p.ep, res.y-p.ep, res.x+p.ep, res.y+p.ep,\
            width=0, fill=p.coul, tag=f"point_{self._tag}")

    def projeter_point_segment(self,x,y, couleur_seg, epaisseur):
        """
        Projette dans le DC directement, sans passer par la matrice
        Utilisée spécifiquement pour Bresenham
        """
        self._canvas.create_rectangle(x-epaisseur, y-epaisseur, x+epaisseur, y+epaisseur,\
        width=0, fill=couleur_seg, tag=f"point_seg_{self._tag}")


    def projeter_fichier(self, nom_fichier):
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

    def projeter_fonction(self, xmin ,xmax, nb_point, P):
        """
        Projette un polynome dans le DC
        """

        pts = evaluer_fonction(xmin, xmax, nb_point, P)

        for point in pts :
            vp = v.Vecteur([point[0], point[1], 1])
            self + vp

    def segment_bresenham(self, S):
        """
        Création d'un segment à l'aide de l'algorithme de Bresenham
        """
        # On projette d'abord les deux points du segment avant de faire l'algo
        # Sinon il y a des trous

        seg_color = S.coul
        seg_ep = S.ep
        pas = 1

        if pas == 0:
            pas = 1

        # On récupère les extrémités du segment
        A = S.P1
        B = S.P2

        # On les projette
        A = self._M * A
        B = self._M * B

        # Puis on trace le segment avec Bresenham
        dx = B.x - A.x
        dy = B.y - A.y
        if dx >= 0 and dy >= 0: # Premier Quartant
            if dy != 0 and abs(dx) >= abs(dy): # Premier Octant
                x = A.x
                y = A.y
                dec = abs(dx) - 2*abs(dy)
                while x <= B.x:
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dx)
                        y = y + (2*pas)
                    dec = dec -2*abs(dy)
                    x = x + (2*pas)
            elif dy != 0 and abs(dx) < abs(dy): # Deuxième Octant
                x = A.x
                y = A.y
                dec = abs(dy) - 2*abs(dx)
                while y <= B.y:
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dy)
                        x = x + (2*pas)
                    dec = dec -2*abs(dx)
                    y = y + (2*pas)

        elif dx < 0 and dy > 0: # Deuxième Quartant
            if dy != 0 and abs(dx) >= abs(dy): # 4e octant
                x = A.x
                y = A.y
                dec = abs(dx) - 2*abs(dy)
                while x >= B.x:
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dx)
                        y = y + (2*pas)
                    dec = dec -2*abs(dy)
                    x = x - (2*pas)

            elif dy != 0 and abs(dx) < abs(dy): # 3e octant
                x = A.x
                y = A.y
                dec = abs(dy) - 2*abs(dx)
                while y <= B.y:
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dy)
                        x = x - (2*pas)
                    dec = dec -2*abs(dx)
                    y = y + (2*pas)

        elif dx < 0 and dy < 0: # 3e Quartant
            if dy != 0 and abs(dx) >= abs(dy): # 5e octant
                x = A.x
                y = A.y
                dec = abs(dx) - 2*abs(dy)
                while x >= B.x:
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dx)
                        y = y - (2*pas)
                    dec = dec -2*abs(dy)
                    x = x - (2*pas)

            elif dy != 0 and abs(dx) < abs(dy): # 6e octant
                x = A.x
                y = A.y
                dec = abs(dy) - 2*abs(dx)
                while y >= B.y:
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dy)
                        x = x - (2*pas)
                    dec = dec -2*abs(dx)
                    y = y - (2*pas)
        elif dx > 0 and dy < 0: # 4e Quartant
            if dy != 0 and abs(dx) >= abs(dy): # 8e octant
                x = A.x
                y = A.y
                dec = abs(dx) - 2*abs(dy)
                while x <= B.x:
                    #self + v.Vecteur([x,y,1])
                    self.projeter_point_segment(x,y,seg_color, seg_ep)
                    if dec < 0:
                        dec = dec +2*abs(dx)
                        y = y - (2*pas)
                    dec = dec -2*abs(dy)
                    x = x + (2*pas)


            elif dy != 0 and abs(dx) < abs(dy): # 7e octant
                x = A.x
                y = A.y
                dec = abs(dy) - 2*abs(dx)
                while y >= B.y:
                    self.projeter_point_segment(x,y,seg_color, seg_ep) # On allume le pixel
                    if dec < 0:
                        dec = dec +2*abs(dy)
                        x = x + (2*pas)
                    dec = dec -2*abs(dx)
                    y = y - (2*pas)

    def __add__(self, other):
        """
        Ajoute le point dans la liste de points
        """

        if type(other) is v.Vecteur:
            self._point.append(other)
            self.projeter_point(other)

        elif type(other) is s.Segment:
            self._seg.append(other)
            self.segment_bresenham(other)
