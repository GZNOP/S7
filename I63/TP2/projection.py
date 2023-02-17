import lib.Vecteur as v

def definir_droite(P1, P2):
    """
    Détermine la droite y = ax+b à partir de deux points
    """
    D = v.Vecteur([0,0]) # droite y = D[0] * x + D[1]

    D[0] = (P2[1] - P1[1]) / (P2[0] - P1[0]) # On détermine la pente

    D[1] = P1[1] - D[0] * P1[0] # On détermine l'ordonnée à l'origine

    return D
