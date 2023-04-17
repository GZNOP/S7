def lire_fichier(nom_fichier):
    """ Lis le fichier nom_fichier et en retourne une matrice d'observation """

    fic = open(nom_fichier, "r")

    obs = []

    for ligne in fic:
        l = ligne.split(",")
        l[-1] = l[-1][:-1]
        obs.append(l)

    return obs

if __name__ == "__main__":

    print(lire_fichier("XN.csv"))
    
