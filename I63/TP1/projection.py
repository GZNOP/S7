def produit_mat_vec(M, V):
    """Fonction qui calcule le produit d'une matrice avec un vecteur
    On supposera que len(M[0]) = len(V)
    """

    res = [0] * len(V)

    for i in range(len(M)):
        for j in range(len(V)):

            res[i] += M[i][j]*V[j]

    return res

def calculer_matrice(WC, DC, hauteur):
    """
    Calcule la matrice de transformation

        WC est le world coordinate [(x_w1, y_w1),(x_w2, y_w2)]
        DC est le device coordinate [(x_v1, y_v1),(x_v2, y_v2)]

    """
    dx_v = (DC[1][0] - DC[0][0])
    dx_w = (WC[1][0] - WC[0][0])

    dy_v = (DC[1][1] - DC[0][1])
    dy_w = (WC[1][1] - WC[0][1])

    # Calcule de la matrice
    M = [[ dx_v / dx_w  , 0 , (dx_v * DC[0][0])- WC[0][0] ]\
        ,[ 0 , - (dy_v / dy_w) , -WC[0][1] + ( dy_v * (DC[0][1] + hauteur) / dy_w ) ]\
        ,[ 0 , 0 , 1 ]]

    return M



def projeter_point(point, M):
    """
    projette un point de l’espace euclidien (WC) dans l’espace écran DC
    (en passant par l’espace normalisé NC)

    point est un tuple de (x_p, y_p)

    """

    print(point)

    res = produit_mat_vec(M, point)

    print(res)

if __name__ == "__main__":

    WC = [(2.0, 2.0),(6.0 ,6.0)]

    DC = [(750, 750//2),(1400, 700)]

    M = calculer_matrice(WC, DC, 750)

    print(M)

    projeter_point([4,4,1], M)
