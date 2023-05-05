from math import log2
from random import randrange

def entropie_via_hypercube(hypercube):
    """ Calcule la formule de l'entropie jointe uniquement via l'hypercube"""

    somme = 0

    for key in hypercube.keys():
        somme += hypercube[key] * log2(hypercube[key])

    # pour éviter de retourner -0.0
    if somme == 0:
        return 0
    
    return -somme


def regle_chaine(hypercube):
    """ Cette fonction va calculer l'entropie de la sequence et ses r realisations donnee par OBS
    OBS est une matrice ou les lignes sont les realisations des sequences de longueur
    n (OBS_1 à OBS_n)
    Pour cela on utilise la formule : H(OBS) = Sum_1^n ( H(OBS_i, OBS^{i-1}) - H( OBS^{i-1} )
    """

    n = len(list(hypercube.keys())[0])
    somme = 0

    if n <= 1:
        somme += entropie_via_hypercube(hypercube)
        return somme
    
    
    for i in range(n):
        somme += entropie_via_hypercube(hypercube)

        hypercube = reduire(hypercube)

        somme -= entropie_via_hypercube(hypercube)
    return somme


def entropie_jointe(OBS):
    """
    Calcule l'entropie jointe de la séquence et des ses réalisations, stockée dans la matrice OBS 
    """
    somme = 0
    hcube = construire_hypercube(OBS, len(OBS[0]))

    for key in hcube.keys():

        somme += hcube[key] * log2(hcube[key])

    return - somme

    

def construire_hypercube(OBS, n):
    """ Construit l'hypercube de dimension n de la matrice """

    r = len(OBS) # On recupere le nombre de realisation

    dico = {} # On initialise le dictionnaire, dont les cles sont les sequences
    # Ce dictionnaire va compter les occurences des sequences.

    # Pour chaque sequence, on ajoute sa concatenation en cle du dico si
    # elle n'y est pas, sinon on ajoute 1 a la cle existente.
    for i in range(r):
        
        if tuple(OBS[i][:n]) not in dico.keys(): # On transtype en tuple car pas de liste en cle de dictionnaire
            dico[tuple(OBS[i][:n])] = 1
        else:
            dico[tuple(OBS[i][:n])] += 1

    # On calcule ensuite les probabilités jointes de nos sequences et on les stocke dans le dictionnaire        
    for k in dico.keys():
        dico[k] = dico[k] / r
    return dico


def reduire(hypercube):
    """
    Cette fonction va permettre de réduire l'hypercube de une dimension
    """

    nouveau = {} # Le nouveau dictionnaire qui va stocker les probabilites jointes de hypercube
    # Avec une dimension de moins
    
    
    for key in hypercube.keys():
        prob = hypercube[key] # On memorise la probabilite courante
        # On regarde si la nouvelle cle existe dans le nouveau dico
        if key[:-1] not in nouveau.keys():
            # si elle n'y est pas on l'ajoute
            nouveau[key[:-1]] = prob # avec la probabilite memorisee !

        else:
            # si elle y est on fait la somme des probabilites
            nouveau[key[:-1]] += prob

    return nouveau

def alea_liste(n):
    """
    Retourne une liste de taille n de nombres binaire genere aleatoirement
    """
    liste = []

    for i in range(n):
        liste.append(randrange(0,2))

    return liste

def construire_hypercube_concat2(XN, YN, indice):
    """
    Construit l'hypercube de la séquence XN de longueur indice à laquelle 
    on concatène YN de longueur indice
    """
    
    dico = {} # On initialise le dictionnaire qui va compter les occurences

    r = len(XN)# le nb de séquences (autant pour XN que pour YN)

    
    for real in range(r):
        # On concatene XN^i avec YN^i
        concat = tuple(XN[real][:indice] + YN[real][:indice])

        # On l'ajoute dans le dico
        if concat not in dico.keys():
            dico[concat] = 1
        else:
            dico[concat] += 1

    #print(dico)
    for k in dico.keys():
        dico[k] = dico[k] / r

    return dico

def probabilite(OBSXN, i):
    """
    Calcule les probabilité d'apparition de la variable aléatoire en Xi pour toutes les realisations
    """
    r = len(OBSXN) # Le nombre de realisations
    dico = {} # Le dictionnaire qui va contenir les probas

    # On compte les occurences
    for ligne in range(r):
        if OBSXN[ligne][i] not in dico.keys():
            dico[OBSXN[ligne][i]] = 1
        else:
            dico[OBSXN[ligne][i]] += 1

    # On calcule les probas
    for k in dico.keys():
        dico[k] = dico[k] / r

    return dico

def entropie(OBSXN, i):
    """ 
    Calcule l'entropie de la variable aléatoire Xi
    """

    proba = probabilite(OBSXN, i)
    somme = 0 # La somme de l'entropie
    
    for k in proba.keys():
        
        somme += proba[k] * log2(proba[k])

    return - somme

def construire_hypercube_dim2(XN, YN, i):
    """
    Construit l'hypercube des probabilités jointes des variables aléatoire Xi et Yi
    """

    dico = {} # hypercube

    r = len(XN)

    for ligne in range(r):
        # On a bien comme cle XiYi 
        cle = (XN[ligne][i],YN[ligne][i])
        
        if cle not in dico.keys():

            dico[cle] = 1

        else:

            dico[cle] += 1

    # Calcule des probas
    for k in dico.keys():

        dico[k] /= r

    return dico
    

            
def construire_hypercube_concat(XN, YN, indice):
    """
    Construit l'hypercube de la séquence XN de longueur indice à laquelle 
    on concatène YN de longueur indice-1
    """
    if indice == 0:
        return probabilite(XN,1)
    
    dico = {} # On initialise le dictionnaire qui va compter les occurences

    r = len(XN)# le nb de séquences (autant pour XN que pour YN)
    
    for real in range(r):
        # On concatene XN^i avec YN^(i-1)
        concat = tuple(XN[real][:indice] + YN[real][:indice-1])
        # On l'ajoute dans le dico
        if concat not in dico.keys():
            dico[concat] = 1
        else:
            dico[concat] += 1

    print(dico)
    for k in dico.keys():
        dico[k] = dico[k] / r

    return dico
    
def IM_conditionnelle(XN, YN, indice):
    """ Calcule l'entropie conditionnelle des deux séquences pour un indice précis"""

    XNYNI_1 = construire_hypercube_concat(XN, YN, indice)
    YNI = construire_hypercube(YN, indice)
    XNYNI = construire_hypercube_concat2(XN, YN, indice)
    YNI_1 = reduire(YNI)

    H_YNI_1 = entropie_via_hypercube(YNI_1)
    
    resultat = entropie_via_hypercube(XNYNI_1) - H_YNI_1 + entropie_via_hypercube(YNI) - entropie_via_hypercube(XNYNI)

    return resultat
    

def IM_dirigee(OBSXN, OBSYN):
    """
    Calcule l'information mutuelle dirigée des deux séquences XN et YN
    """
    
    # On suppose que les deux séquences sont de meme taille
    if len(OBSXN[0]) != len(OBSYN[0]):
        print("Erreur, les séquences doivent être de même longueur")
        exit(1)

    n = len(OBSXN[0])
    somme = 0
    
    for i in range(n):
        somme += IM_conditionnelle(OBSXN, OBSYN, i)

    return somme

def IM(OBSXN, OBSYN, i):
    """
    Calcule l'information mutuelle entre les variables à l'indice i de OBSXN et OBSYN
    """

    concat = construire_hypercube_dim2(OBSXN, OBSYN, i)
    
    res = entropie(OBSXN,i) + entropie(OBSYN, i) - entropie_via_hypercube( concat )

    return res

def hypercube_XNYi(OBSXN, OBSYN, i):
    """ 
    Calcule l'hypercube de XN et Yi concaténé ainsi que les probabilités
    """
    
    r = len(OBSXN)
    dico = {}

    for ligne in range(r):

        cle = tuple(OBSXN[ligne] + [OBSYN[ligne][i]])

        if cle not in dico.keys():

            dico[cle] = 1
        else:
            dico[cle] += 1

    for k in dico.keys():
        dico[k] /= r

    return dico
    
def IM2(OBSXN, OBSYN, i):
    """
    Calcule l'information mutuelle entre les variables XN et Yi
    """

    hcubeXNYi = hypercube_XNYi(OBSXN, OBSYN, i)
    hcubeXN = hypercube(OBSXN, len(OBSXN[0]))

    res = entropie_via_hypercube(hcubeXN) + entropie(OBSYN, i) - entropie_via_hypercube(hcubeXNYi)

    return res

def IM3(OBSXN, OBSYN):
    """
    Calcule l'information mutuelle entre toutes les variables : XN et YN
    """

    hcubeXNYN = construire_hypercube_concat2(OBSXN, OBSYN, len(OBSXN[0]))
    hcubeXN = construire_hypercube(OBSXN, len(OBSXN[0]))
    hcubeYN = construire_hypercube(OBSYN, len(OBSYN[0]))

    
    res = entropie_via_hypercube(hcubeXN) + entropie_via_hypercube(hcubeYN) - entropie_via_hypercube(hcubeXNYN)

    return res

def IM_dirigee2(OBSXN, OBSYN):
    """
    Calcule l'information mutuelle dirigée avec la formule vue en cours
    """

    somme = 0
    N =  len(OBSXN[0])

    hcubeYN = construire_hypercube(OBSYN, N)
    
    for i in range(N):

        hcubeXNYN = construire_hypercube_concat2(OBSXN, OBSYN, i)
        hcubeXNYN_1 = construire_hypercube_concat(OBSXN, OBSYN, i)

        somme += entropie_via_hypercube(hcubeXNYN_1) - entropie_via_hypercube(hcubeXNYN) + entropie_via_hypercube(hcubeYN)

        hcubeYN = reduire(hcubeYN)

    return somme
    
    
if __name__ == "__main__":

    
    
    XN = [alea_liste(4), alea_liste(4), alea_liste(4), alea_liste(4), alea_liste(4), alea_liste(4), alea_liste(4)]

    YN = [
        [0,0,1,1],
        [1,1,0,0],
        [0,1,1,1],
        [0,1,0,1],
        [0,0,1,0],
        [1,0,1,1],
        [1,0,0,0]
        ]

    print(XN)
    print(YN)
    print(construire_hypercube_concat(XN, YN, 0))
