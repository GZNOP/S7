import sys
sys.path.append("..")

from lib.Projection import *
from lib.bresenham import segment_naif
import lib.Vecteur as v

## BUG: PENSER À CREER UNE CLASSE POUR DIRECTEMENT PACK LA FENETRE CANVAS

P1 = v.Vecteur([0,0,1])
P2 = v.Vecteur([7,2,1])
P3 = v.Vecteur([2,7,1])
P4 = v.Vecteur([-2,7,1])
P5 = v.Vecteur([-7,2,1])
P6 = v.Vecteur([2,-7,1])
P7 = v.Vecteur([7,-2,1])
P8 = v.Vecteur([-7,-2,1])
P9 = v.Vecteur([-2,-7,1])



S1 = segment_naif(P1,P2)


# Création de la fenetre virtuelle
root = tk.Tk()
root.geometry("1290x730")
root["bg"] = "grey"
ca = tk.Canvas(root, width=1280, height=720)
ca.pack(padx=5, pady=5)


# Projection des points
WC1 = [v.Vecteur([-10,-10]), v.Vecteur([10,10])]
DC1 = [v.Vecteur([100,100]), v.Vecteur([400,300])]

DC2 = [v.Vecteur([200,200]), v.Vecteur([600,500])]
DC3 = [v.Vecteur([200,200]), v.Vecteur([400,300])]


P = Projection(ca, "naif", WC1, DC1)
C = Projection(ca, "bresenham", WC1, DC2)
B = Projection(ca, "bresenham2", WC1, DC3)

C.segment_bresenham(P1,P2)
B.segment_bresenham(P1,P2)



for p1 in S1:
    P + p1





root.mainloop()
