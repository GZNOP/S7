import tkinter as tk

from projection import *
import Vecteur as v
import Matrice as m

LAR = 1280
HAU = 720


WC = [(0, 0),(10 ,100)]
DC = [(200, 200),(600, 400)]

M = calculer_matrice(WC, DC)

X,Y = 0,0

# -------------------------------- CALLBACKS --------------------------

def obtenir_xy(event):
    global X,Y

    X = event.x
    Y = event.y

def deplacer_fen(event, ca):
    global X,Y

    dx = event.x - X
    dy = event.y - Y

    X = event.x
    Y = event.y

    ca.move("vir", dx, dy)

def maj_viewport(event, ca):
    global DCM
    tmp = ca.coords("vir")
    DC[0] = tmp[0:2]
    DC[1] = tmp[2:]

    print(DC)

    M = calculer_matrice(WC, DC)

    print(M)




# --------------------------- PARTIE TKINTER -------------------------------

def creer_root():
    """
    Créer une fenêtre principale en tkinter
    """
    root = tk.Tk()

    root.geometry(F"{LAR+10}x{HAU+10}")
    root.title("fenêtre virtuelle")

    return root

def creer_canvas(root):
    """
    Créer le canvas qui servira d'écran virtuel pour le tp
    """

    ca = tk.Canvas(root, width=LAR, height=HAU, bg="grey")

    ca.pack(padx=5, pady=5, expand=True)

    ca.tag_bind("vir","<Button-1>", lambda event: obtenir_xy(event))
    ca.tag_bind("vir","<B1-Motion>", lambda event: deplacer_fen(event, ca))
    ca.tag_bind("vir","<ButtonRelease-1>", lambda event: maj_viewport(event, ca))

    return ca

def trace_vir(canv, x, y, long, lar):
    """
    Trace le rectange dans le canvas qui correspond à la fenêtre virtuelle
    """

    canv.create_rectangle(x, y, x+long, y+lar, fill="white", tag="vir")

def projeter_point_ca(ca, point, M):
    """
    Dessine la projection du point du WC dans la fenêtre virtuelle du canvas
    """

    new = M * point
    print(new)

    ca.create_rectangle(new[0]-2, new[1]-2, new[0]+2, new[1]+2, tag='vir', fill="red")


def projeter_fichier_points_ca(ca, liste, M):
    """
    Projette la liste de points de WC vers DC grace à M et l'affiche sur le canvas ca
    """

    new_liste = projeter_fichier_points(liste, M)

    for el in new_liste:
        ca.create_rectangle(el[0]-2, el[1]-2, el[0]+2, el[1]+2, tag='vir', fill="red")




# ------------------------ PARTIE PROJECTION ----------------------------

racine = creer_root()
ca = creer_canvas(racine)
trace_vir(ca, DC[0][0], DC[0][1], DC[1][0]-DC[0][0], DC[1][1]-DC[0][1])

liste= lecture_fichier_points("points.dat")
projeter_fichier_points_ca(ca, liste, M)


racine.mainloop()
