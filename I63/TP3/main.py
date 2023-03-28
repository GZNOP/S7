import sys
if __name__ == "__main__":
    sys.path.append("..")

import tkinter as tk

from lib.fenetre import creer_fenetre
from lib.Point import *
from lib.Segment import *
from lib.Bezier import *
from lib.Projection import *


# Création de la fenetre virtuelle
root, ca = creer_fenetre(1280,720)


# On bind le fait de pouvoir placer des points de controle

# Projection
WC1 = [Point2D(0,0), Point2D(1,1)]
DC2 = [Point2D(200,200), Point2D(1000,700)]

P = Projection(ca, "bezier", WC1, DC2)


root.mainloop()
