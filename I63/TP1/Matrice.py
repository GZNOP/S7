from Vecteur import *

class Matrice:

    def __init__(self, n, m):

        self._mat = [0] * n

        for i in range(n):

            self._mat[i] = Vecteur([0] * m)


    def __getitem__(self, i):
        return self._mat[i]

    def __setitem__(self,i, val):
        self._mat[i] = val

    def __len__(self):
        return len(self._mat)

    def __str__(self):
        ch = ""
        for v in self:
            for el in v:
                ch += f"{el}  "

            ch += "\n"
        ch += "\n"

        return ch

    def __mul__(self, other):
        """
        produit matricielle ou produit scalaire
        """

        if type(other) is Vecteur:

            res = Vecteur([0] * len(other))

            for i in range(len(other)):
                for j in range(len(other)):

                    res[i] += other[j] * self[i][j]

            return res

        elif type(other) is Matrice:

            res = Matrice(len(self),len(other[0]))

            for i in range(len(self)):

                for j in range(len(other[0])):

                    for s in range(len(other)):

                        res[i][j] += self[i][s] * other[s][j]

            return res
