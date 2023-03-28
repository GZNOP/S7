import sys
from sys import argv

if __name__ == "__main__":
    sys.path.append("..")

import lib.Segment as s
import lib.Vecteur as v
import lib.Matrice as m
import tkinter as tk
from lib.eval_fonc import evaluer_fonction
from lib.Point import *
from lib.Bezier import *

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

        self._tr = m.Matrice(3,3)
        self._tr[0] = [1,0,0]
        self._tr[1] = [0,1,0]
        self._tr[2] = [0,0,1]


        self._point = [] # Une liste de points

        self._seg = [] # liste d'instances de segments

        self._courbe = [] # liste de courbes de bézier

        self._X = None

        self._Y = None

        self._tmp = Bezier([],ep=1) # la courbe temporaire

        self._canvas.create_rectangle(self.DC0.x, self._hauteur - self.DC0.y, self.DC1.x,\
        self._hauteur - self.DC1.y, fill="grey", tag=self._tag)

        self._canvas.tag_bind(self._tag,"<Button-1>", lambda event: self.obtenir_xy(event))
        self._canvas.tag_bind(self._tag,"<B1-Motion>", lambda event: self.deplacer_fen(event))
        self._canvas.tag_bind(self._tag,"<ButtonRelease-1>", lambda event: self.maj_viewport(event))

        self._canvas.tag_bind(self._tag,"<Button-3>", lambda event: self.sur_clique_droit(event))

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

    def sur_clique_droit(self,event):
        """
        Créer un point de controle quand l'utilisateur fait un clique droit
        """
        P = Point2D(event.x, event.y)
        self._tmp._controle.append(P)

        self._canvas.create_rectangle(P.x-P.ep, P.y-P.ep, P.x+P.ep, P.y+P.ep,\
        width=0, fill=P.coul, tag=(f"tmp_{self._tag}",f"{self._tag}"))

        self.verifie_tmp() # si c'est le 4e point, on le trace


    def obtenir_xy(self,event):
        """
        met à jour les coordonnées X et Y quand l'utilisateur fait un clique gauche
        """
        self._X = event.x
        self._Y = event.y

    def deplacer_fen(self,event):
        """
        Déplace la fenêtre en même temps que la souris de l'utilisateur s'il est en mouvement
        """
        dx = event.x - self._X
        dy = event.y - self._Y

        self._X = event.x
        self._Y = event.y

        self._canvas.delete(f"point_{self._tag}")
        self._canvas.delete(f"point_seg_{self._tag}")
        self._canvas.move(self._tag, dx, dy)

    def maj_viewport(self, event):
        """
        Lorsque l'utilisateur lache le clique gauche, les points sont recalculés
        et de nouveau projetés
        """
        tmp = self._canvas.coords(self._tag) # on récupère les coord du rect
        # point en haut à gauche et en bas à droite
        hau = tmp[3] - tmp[1] # la hauteur de la fenêtre

        # distance entre les 2 positions de la fenetre
        dx = tmp[0] - self.DC0.x
        dy = tmp[3] - (self._hauteur - self.DC0.y)

        self.DC0.x = tmp[0]
        self.DC0.y = self._hauteur - tmp[1] - hau
        self.DC1.x = tmp[2]
        self.DC1.y = self._hauteur - tmp[3] + hau

        # Lorsque l'on déplace la fenêtre, tous les points courants seront
        # déplacés via la matrice de translation


        self._tr[0][2] = dx
        self._tr[1][2] = dy

        self._M = self.calculer_matrice()

        self.translater()

        self.projeter_segment()
        self.projeter_liste()
        self.projeter_liste_courbe()

    # ---------------------------------------------------------------------
    def verifie_tmp(self):
        """
        Vérifie la liste tmp et trace la courbe quand il y a 4 points
        """
        if len(self._tmp._controle) == 4:
            # On trace la courbe puis on remet la liste à vide

            self._courbe.append(self._tmp)

            self.projeter_courbe(self._tmp)

            self._tmp = Bezier([], ep=1)
            self._canvas.delete(f"tmp_{self._tag}")

    def translater(self):
        """
        Translate tous les points de la fenêtre
        """
        # points
        nouveau_point = []
        for point in self._point:
            point = self._tr * point
            nouveau_point.append(point)

        self._point = nouveau_point


        # segments
        nouveau_seg = []
        for S in self._seg:
            S.P1 = self._tr * S.P1
            S.P2 = self._tr * S.P2

            nouveau_seg.append(S)

        self._seg = nouveau_seg

        # courbe

        nouvelle_courbe = []

        for C in self._courbe:
            Cp = Bezier([], C.coul, C.ep, C._interpolation)
            for el in C:
                el = self._tr * el
                Cp._controle.append(el)

            nouvelle_courbe.append(Cp)

        self._courbe = nouvelle_courbe

    def projeter_courbe(self, courbe):
        """
        Affiche la courbe dans le canvas
        """

        pt = courbe.bezier_polynome()
        # On relie les points de la courbe
        for i in range(len(pt)-1):
            self.segment_bresenham(s.Segment(pt[i],pt[i+1],courbe.coul, courbe.ep))


    def projeter_liste_courbe(self):
        """
        Affiche les courbes de bézier de l'instance
        """
        for C in self._courbe:
            self.projeter_courbe(C)


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

        return res

    def afficher_point(self, point):
        """
        Affiche le point dans le canvas une fois qu'il a été projeté
        Projette dans le DC directement, sans passer par la matrice.
        """

        self._canvas.create_rectangle(point.x-point.ep, point.y-point.ep, point.x+point.ep, point.y+point.ep,\
        width=0, fill=point.coul, tag=(f"point_{self._tag}",f"{self._tag}"))

    def projeter_liste(self):
        """
        projette les points de la liste
        """
        for p in self._point:
            self.afficher_point(p)

    def afficher_point_segment(self,x,y, couleur_seg, epaisseur):
        """
        Projette dans le DC directement, sans passer par la matrice
        Utilisée spécifiquement pour les segments
        """
        self._canvas.create_rectangle(x-epaisseur, y-epaisseur, x+epaisseur, y+epaisseur,\
        width=0, fill=couleur_seg, tag=(f"point_seg_{self._tag}",f"{self._tag}"))


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

                point = Point2D(x,y)

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
            vp = Point2D(point[0], point[1])
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
        #A = self._M * A
        #B = self._M * B

        # Puis on trace le segment avec Bresenham
        dx = B.x - A.x
        dy = B.y - A.y
        if dx >= 0 and dy >= 0: # Premier Quartant
            if dy != 0 and abs(dx) >= abs(dy): # Premier Octant
                x = A.x
                y = A.y
                dec = abs(dx) - 2*abs(dy)
                while x <= B.x:
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep)
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
                    self.afficher_point_segment(x,y,seg_color, seg_ep) # On allume le pixel
                    if dec < 0:
                        dec = dec +2*abs(dy)
                        x = x + (2*pas)
                    dec = dec -2*abs(dx)
                    y = y - (2*pas)

    def __add__(self, other):
        """
        Ajoute le point dans la liste de points
        """

        # Projection d'un point seul
        if type(other) is Point2D:
            # On projette d'abord le point, puis on l'affiche
            res = self.projeter_point(other)
            self._point.append(res)
            self.projeter_point(res)
            self.afficher_point(res)

        # Projection d'un segment
        elif type(other) is s.Segment:
            # On projette d'abord les points
            P1 = self.projeter_point(other.P1)
            P2 = self.projeter_point(other.P2)
            S = s.Segment(P1, P2, other.coul, other.ep)
            self._seg.append(S)
            self.segment_bresenham(S)

        # Projection d'une liste de points
        elif type(other) is list and type(other[0]) is Point2D:
            for el in other:
                if type(el) is Point2D:
                    res = self.projeter_point(el)
                    self._point.append(res)
                    self.projeter_point(res)
                    self.afficher_point(res)

        # Projection d'une courbe de Bézier
        elif type(other) is Bezier:
            M = [] # points de contrôle projetés

            for el in other:
                M.append(self.projeter_point(el))

            B = Bezier(M,other.coul, other.ep)
            self._courbe.append(B)
            self.projeter_courbe(B)
