from math import log2
from random import randrange

def regle_chaine(OBS):
    """ Cette fonction va calculer l'entropie des sequences donnees par OBS
    OBS est une matrice ou les lignes sont les realisations des sequences de longueur
    n (OBS_1 à OBS_n)
    Pour cela on utilise la formule : H(OBS) = Sum_1^n ( H(OBS_i, OBS^{i-1}) - H( OBS^{i-1} )
    """
   


def entropie_jointe(OBS):
    """
    Calcule l'entropie jointe de la séquence et des ses réalisations, stockée dans la matrice OBS 
    """
    somme = 0
    hcube = hypercube(OBS)

    for key in hcube.keys():

        somme += hcube[key] * log2(hcube[key])

    return - somme

    

def hypercube(OBS):
    """ Construit l'hypercube de la matrice """

    r = len(OBS) # On recupere le nombre de realisation

    dico = {} # On initialise le dictionnaire, dont les cles sont les sequences
    # Ce dictionnaire va compter les occurences des sequences.

    # Pour chaque sequence, on ajoute sa concatenation en cle du dico si
    # elle n'y est pas, sinon on ajoute 1 a la cle existente.
    for i in range(r):
        
        if tuple(OBS[i]) not in dico.keys(): # On transtype en tuple car pas de liste en cle de dictionnaire
            dico[tuple(OBS[i])] = 1
        else:
            dico[tuple(OBS[i])] += 1

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
        tup.append(randrange(0,2))

    return tup

if __name__ == "__main__":

    OBS = [alea_tup(6), alea_tup(6), alea_tup(6), alea_tup(6), alea_tup(6), alea_tup(6), alea_tup(6), alea_tup(6), alea_tup(6)]

    hcube = hypercube(OBS)

    print(entropie_jointe(OBS))
