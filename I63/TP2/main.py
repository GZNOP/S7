import sys
sys.path.append("..")

from lib.Point import *
from lib.Segment import *
from lib.Projection import *
from lib.bresenham import segment_naif
import lib.Vecteur as v

## BUG: PENSER À CREER UNE CLASSE POUR DIRECTEMENT PACK LA FENETRE CANVAS

P1 = Point2D(0,0)
P2 = Point2D(7,2)
P3 = Point2D(2,7)
P4 = Point2D(-7,2)
P5 = Point2D(-2,7)
P6 = Point2D(7,-2)
P7 = Point2D(2,-7)
P8 = Point2D(-2,-7)
P9 = Point2D(-7,-2)


# Création de la fenetre virtuelle
root = tk.Tk()
root.geometry("1290x730")
root["bg"] = "grey"
ca = tk.Canvas(root, width=1280, height=720)
ca.pack(padx=5, pady=5)


# Projection des points
WC1 = [Point2D(-10,-10), Point2D(10,10)]

DC2 = [Point2D(200,200), Point2D(600,500)]

C = Projection(ca, "bresenham", WC1, DC2)

S1 = Segment(P1,P2,"red",5)
S2 = Segment(P1,P3, "pink",7)
S3 = Segment(P1,P4, "darkred",1)
S4 = Segment(P1,P5, "blue")
S5 = Segment(P1,P6, "cyan")
S6 = Segment(P1,P7, "yellow")
S7 = Segment(P1,P8, "purple")
S8 = Segment(P1,P9, "green")


C + S1
C + S2
C + S3
C + S4
C + S5
C + S6
C + S7
C + S8

root.mainloop()
