import sys
if __name__ == "__main__":
    sys.path.append("..")

from sys import argv

import tkinter as tk

from projection import *
import lib.Vecteur as v
import lib.Matrice as m

LAR = 1280
HAU = 720


WC = [(0, 0),(10 , 10)]
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

def maj_viewport(event,canvas, liste_points):
    tmp = ca.coords("vir")
    dy = tmp[3] - tmp[1]
    DC[0] = [tmp[0], HAU - tmp[1] - dy ]
    DC[1] = [tmp[2], HAU - tmp[3] + dy]
    M = calculer_matrice(WC, DC, HAU)
    projeter_fichier_points_ca(ca, liste_points, M)




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

    print(new)

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



# ------------------------ PARTIE PROJECTION ----------------------------
xmin = float(argv[1])
xmax = float(argv[2])
nb_point = int(argv[3])
coef =  argv[4:]

for i in range(len(coef)):
    coef[i] = float(coef[i])

p = evaluer_fonction(xmin,xmax,nb_point,coef)

V = v.Vecteur([2,2])


ecrire_points_fichier(p, "/tmp/courbe.dat")
liste = lecture_fichier_points("/tmp/courbe.dat")

racine = creer_root()
ca = creer_canvas(racine, liste)
trace_vir(ca, DC[0][0], HAU - DC[1][1] , DC[1][0]-DC[0][0], DC[1][1]-DC[0][1])

projeter_point_ca(ca,V,M)
projeter_fichier_points_ca(ca, liste, M)


racine.mainloop()
