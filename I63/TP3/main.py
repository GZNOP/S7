import sys
if __name__ == "__main__":
    sys.path.append("..")

import tkinter as tk

from lib.fenetre import creer_fenetre
from lib.Point import *
from lib.Bezier import *
from lib.Projection import *


# Création de la fenetre virtuelle
root, ca = creer_fenetre(1280,720)

# Projection
WC1 = [Point2D(0,0), Point2D(1,1)]
DC2 = [Point2D(200,200), Point2D(600,500)]

P = Projection(ca, "bezier", WC1, DC2)

# Points de controle pour le traçage de la courbe
M = [Point2D(0,0), Point2D(0,1), Point2D(1,1), Point2D(1,0)]
C = Bezier(M,ep=1,coul="red")

# Obtention des points
pt2 = C.bezier_polynome(50)

P + pt2

root.mainloop()
