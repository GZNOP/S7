from sys import argv
import sys
if __name__ == "__main__":
    sys.path.append("..")

import lib.Vecteur as v
import lib.Matrice as m

def calculer_matrice(WC, DC, hauteur):
    """
    Calcule la matrice de transformation

        WC est le world coordinate [(x_w1, y_w1),(x_w2, y_w2)]
        DC est le device coordinate [(x_v1, y_v1),(x_v2, y_v2)]

    """


    x_w1 = WC[0][0]
    y_w1 = WC[0][1]
    dxw = (WC[1][0] - WC[0][0])
    dyw = (WC[1][1] - WC[0][1])
    dxv = (DC[1][0] - DC[0][0])
    dyv = (DC[1][1] - DC[0][1])
    x_v1 = DC[0][0]
    y_v1 = DC[0][1]
    y_v2 = DC[1][1]

    # Calcule de la matrice

    M = m.Matrice(3,3)
    M[0] = [ dxv/dxw  , 0 , - x_w1 * dxv / dxw + x_v1 ]
    M[1] = [ 0 , - dyv/dyw , y_w1 * dyv / dyw + dyv + (hauteur - y_v2)]
    M[2] = [ 0 , 0 , 1 ]

    #M =  [[ e/c  , 0 , e*g/c - a]\
    #    ,[ 0 , (f/d) , -b + f*h/d + f*hauteur/d]\
    #    ,[ 0 , 0 , 1 ]]

    print(M)

    return M

def projeter_point(point, M):
    """
    projette un point de l’espace euclidien (WC) dans l’espace écran DC
    (en passant par l’espace normalisé NC)

    point est un tuple de (x_p, y_p)

    """
    print(point)
    res = M * point
    print(res)
    return res

def lecture_fichier_points(nom_fichier):
    """
    Lis un fichier dont chaque ligne est un point (couple) de R x R
    """
    liste_points = []

    fichier = open(nom_fichier, "r")

    for line in fichier:
        tmp = line.split()
        # On regarde s'il y a bien 1 point
        if len(tmp) != 2:
            print("err fichier: pas toutes les composantes dans le vec")
            print(tmp)
            raise ValueError

        tmp[0] = float(tmp[0])
        tmp[1] = float(tmp[1])
        tmp.append(1.0) # On passe en dimension 3 pour pouvoir utiliser la matrice homogène

        liste_points.append(v.Vecteur(tmp))

    return liste_points

def projeter_fichier_points(liste_points, M):
    """
    Projette une liste de points de WC dans DC via la matrice M
    """
    nouvelle_liste = []

    for point in liste_points:
        nouvelle_liste.append(projeter_point(point,M))

    return nouvelle_liste

def horner(P, x):
    """
    Algorithme de calcule d'un polynome avec la méthode de Horner
    """
    n = len(P)
    res = P[n-1]
    i = n-2
    while i >= 0:
        res = res * x + P[i]
        i -= 1
    return res

def evaluer_fonction(xmin, xmax, nb_point, P ):
    """
    Evalue la fonction P dans l'intervalle [xmin, xmax] en nb_point points
    """
    pas = (xmax-xmin) / nb_point

    points = []

    i = xmin
    while i <= xmax:
        points.append([i,horner(P,i)])
        i += pas

    return points

def ecrire_points_fichier(liste_points, nom_fichier):
    """
    Ecrit un fichier de points dans le fichier nom_fihcier
    """

    fic = open(nom_fichier, "w")

    for points in liste_points:
        fic.write(f"{points[0]} {points[1]}\n")


if __name__ == "__main__":
    print(argv)
    xmin = float(argv[1])
    xmax = float(argv[2])
    nb_point = int(argv[3])
    coef =  argv[4:]
    for i in range(len(coef)):
        coef[i] = float(coef[i])

    p = evaluer_fonction(xmin,xmax,nb_point,coef)
    print(p)

    ecrire_points_fichier(p, "courbe.dat")
