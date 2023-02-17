import sys
from sys import argv

# A FAIRE : ADAPTER BRESENHAM A LA PROJECTION DE POINTS
if __name__ == "__main__":
    sys.path.append("..")

import tkinter as tk

import lib.Vecteur as v
import lib.Matrice as m

from TP2.projection import *


LON = 1280
HAU = 720

LAR = 1280
HAU = 720


WC = [(-5, -25),(5 , 25)]
DC = [(100, 100),(400, 300)]

M = calculer_matrice(WC, DC, HAU)

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
    ca.delete("point")
    ca.move("vir", dx, dy)

def maj_viewport(event, ca, liste_points):
    global DC, M
    tmp = ca.coords("vir")
    print(tmp)
    dy = tmp[3] - tmp[1]
    print(dy)
    DC[0] = [tmp[0], HAU - tmp[1] - dy ]
    DC[1] = [tmp[2], HAU - tmp[3] + dy]

    print("DC =", DC)

    M = calculer_matrice(WC, DC, HAU)
    projeter_fichier_points_ca(ca, liste_points, M)

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

def creer_canvas(root, liste_points):
    """
    Créer le canvas qui servira d'écran virtuel pour le tp
    """

    ca = tk.Canvas(root, width=LAR, height=HAU, bg="grey")

    ca.pack(padx=5, pady=5, expand=True)

    ca.tag_bind("vir","<Button-1>", lambda event: obtenir_xy(event))
    ca.tag_bind("vir","<B1-Motion>", lambda event: deplacer_fen(event, ca))
    ca.tag_bind("vir","<ButtonRelease-1>", lambda event: maj_viewport(event, ca, liste_points))

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

    ca.create_rectangle(new[0]-2, new[1]-2, new[0]+2, new[1]+2, tag='point', fill="red")


def projeter_fichier_points_ca(ca, liste, M):
    """
    Projette la liste de points de WC vers DC grace à M et l'affiche sur le canvas ca
    """

    new_liste = projeter_fichier_points(liste, M) #On est avec des obj Vecteur

    points = []# ON passe avec une vraie liste pour créer la ligne brisée

    print(WC)
    print(DC)
    for el in new_liste:
        points.append([el[0], el[1]])

    print(points)
    ca.create_line(points, tag='point', fill="red")

# -----------------------------------------------------------------------------

def creer_segment_naive(ca, P1, P2):
    """
    Créer un segment (ensemble de points) de manière naive
    """
    pas = 1

    D = definir_droite(P1, P2)

    x = P1.x
    while x <= P2.x:
        y = D[0] * x + D[1]

        ca.create_rectangle(x-2, HAU-y-2, x+2, HAU-y+2, width=0, fill="red")

        x += pas

def allumer_pixel(ca, x, y, taille_px):
    ca.create_rectangle(x-(taille_px/2), HAU-y-taille_px/2, x+taille_px/2, HAU-y+taille_px/2, width=0, fill="red") # On allume le pixel


def creer_segment_bresenham(ca, A, B):
    """
    Création d'un segment à l'aide de l'algorithme de Bresenham
    """
    taille_px = 8
    ca.create_line(A.x, HAU - A.y , B.x, HAU - B.y, width=0, fill="black")

    dx = B.x - A.x
    dy = B.y - A.y
    print(dx, dy)
    if dx >= 0 and dy >= 0: # Premier Quartant
        if dy != 0 and abs(dx) >= abs(dy): # Premier Octant
            x = A.x
            y = A.y
            dec = abs(dx) - 2*abs(dy)
            while x <= B.x:
                allumer_pixel(ca, x, y, taille_px)
                if dec < 0:
                    dec = dec +2*abs(dx)
                    y = y + taille_px
                dec = dec -2*abs(dy)
                x = x + taille_px
        elif dy != 0 and abs(dx) < abs(dy): # Deuxième Octant
            x = A.x
            y = A.y
            dec = abs(dy) - 2*abs(dx)
            while y <= B.y:
                allumer_pixel(ca, x, y,  taille_px)

                if dec < 0:
                    dec = dec +2*abs(dy)
                    x = x + taille_px
                dec = dec -2*abs(dx)
                y = y + taille_px

    elif dx < 0 and dy > 0: # Deuxième Quartant
        if dy != 0 and abs(dx) >= abs(dy): # 4e octant
            x = A.x
            y = A.y
            dec = abs(dx) - 2*abs(dy)
            while x >= B.x:
                allumer_pixel(ca, x, y, taille_px)
                if dec < 0:
                    dec = dec +2*abs(dx)
                    y = y + taille_px
                dec = dec -2*abs(dy)
                x = x - taille_px

        elif dy != 0 and abs(dx) < abs(dy): # 3e octant
            x = A.x
            y = A.y
            dec = abs(dy) - 2*abs(dx)
            while y <= B.y:
                allumer_pixel(ca, x, y,  taille_px) # On allume le pixel

                if dec < 0:
                    dec = dec +2*abs(dy)
                    x = x - taille_px
                dec = dec -2*abs(dx)
                y = y + taille_px

    elif dx < 0 and dy < 0: # 3e Quartant
        print("ici")
        if dy != 0 and abs(dx) >= abs(dy): # 5e octant
            x = A.x
            y = A.y
            dec = abs(dx) - 2*abs(dy)
            while x >= B.x:
                allumer_pixel(ca, x, y, taille_px)
                if dec < 0:
                    dec = dec +2*abs(dx)
                    y = y - taille_px
                dec = dec -2*abs(dy)
                x = x - taille_px

        elif dy != 0 and abs(dx) < abs(dy): # 6e octant
            print("6e oct")
            x = A.x
            y = A.y
            dec = abs(dy) - 2*abs(dx)
            while y >= B.y:
                allumer_pixel(ca, x, y,  taille_px) # On allume le pixel

                if dec < 0:
                    dec = dec +2*abs(dy)
                    x = x - taille_px
                dec = dec -2*abs(dx)
                y = y - taille_px
    elif dx > 0 and dy < 0: # 4e Quartant
        print("coucou")
        if dy != 0 and abs(dx) >= abs(dy): # 8e octant
            x = A.x
            y = A.y
            dec = abs(dx) - 2*abs(dy)
            while x <= B.x:
                print(x,y)
                allumer_pixel(ca, x, y, taille_px)
                if dec < 0:
                    dec = dec +2*abs(dx)
                    y = y - taille_px
                dec = dec -2*abs(dy)
                x = x + taille_px

        elif dy != 0 and abs(dx) < abs(dy): # 7e octant
            x = A.x
            y = A.y
            dec = abs(dy) - 2*abs(dx)
            while y >= B.y:
                allumer_pixel(ca, x, y,  taille_px) # On allume le pixel

                if dec < 0:
                    dec = dec +2*abs(dy)
                    x = x + taille_px
                dec = dec -2*abs(dx)
                y = y - taille_px





if __name__ == "__main__":


    Centre = v.Vecteur([LON//2, HAU//2])



    root = creer_fenetre()

    ca = creer_ca(root)

    creer_segment_bresenham(ca, Centre, v.Vecteur([1000,450]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([800,600]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([50,450]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([500,600]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([1000,250]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([800,10]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([50,200]))
    creer_segment_bresenham(ca, Centre, v.Vecteur([500,50]))



    root.mainloop()
