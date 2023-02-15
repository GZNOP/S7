from math import log2
import numpy as np

def entropie(P):
    """
    Calcule l'entropie de la liste de probabilité passée en paramêtre
    """

    entr = 0

    for i in range(len(P)):
        if P[i]:
            entr -= P[i] * log2(P[i])

    return entr

def proba_jointes(T1, T2, n_val):
    """
    Calcule les probabilités jointes des tableaux à deux dimensions
    en calculant la probabilité des couples.
    """
    dico = {}

    for i in range(len(T1)):
        for j in range(len(T1[0])):

            if (T1[i][j], T2[i][j]) not in dico.keys():
                dico[(T1[i][j], T2[i][j])] = 1
            else:
                dico[(T1[i][j], T2[i][j])] += 1

    prob = []
    for occ in dico.values() :
        prob.append(occ / (n_val*n_val))

    return prob

def NMI(Im1, Im2):
  # Im1: image 1 (2D np array)
  # Im2: image 2 (2D np array)

  xe = np.asarray(range(np.amax(Im1[:])+2)) # Nb de valeur possible (i)
  H1, xe = np.histogram(Im1.reshape(-1), bins=xe) # H1[i] c'est le nombre d'occurence de cette valeur de i
  P1 = H1/Im1.size # C'est la probabilité des gris dans l'image 1

  entropie1 = entropie(P1) # entropie pour l'image 1


  xe = np.asarray(range(np.amax(Im2[:])+2)) # Nb de valeur possible (i)
  H2, xe = np.histogram(Im2.reshape(-1), bins=xe) # H2[i] c'est le nombre d'occurence de cette valeur de i
  P2 = H2/Im2.size # C'est la probabilité des gris dans l'image 2

  entropie2 = entropie(P2) # entropie pour l'image 2

  # Densité de probabilité jointe et entropie jointe

  pj = proba_jointes(Im1, Im2, xe[-1])
  entropie_jointe = entropie(pj)

  # Calcul de l'information mutuelle normalisée

  nmi = (2 *( entropie1 + entropie2 - entropie_jointe) / (entropie1 + entropie2))
  return nmi
