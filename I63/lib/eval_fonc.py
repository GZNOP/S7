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
