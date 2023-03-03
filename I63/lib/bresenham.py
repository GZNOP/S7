if __name__ == "__main__":
    import sys
    sys.path.append("..")

import tkinter as tk

import lib.Vecteur as v
from lib.Projection import *

def definir_droite(P1, P2):
    """
    Détermine la droite y = ax+b à partir de deux points
    """
    D = v.Vecteur([0,0]) # droite y = D[0] * x + D[1]

    D[0] = (P2[1] - P1[1]) / (P2[0] - P1[0]) # On détermine la pente

    D[1] = P1[1] - D[0] * P1[0] # On détermine l'ordonnée à l'origine

    return D

def segment_naif(P1, P2):
    """
    Calcule les points pour tracer le segment [P1,P2] de manière naive
    on prend un pas de 0.01
    """

    pas = 0.01

    lp = []#liste des points du segment

    D = definir_droite(P1, P2)

    x = P1.x
    while x <= P2.x:
        y = D[0] * x + D[1]

        lp.append(v.Vecteur([x,y,1]))

        x += pas

    return lp
