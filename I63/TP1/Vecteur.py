class Vecteur :

    def __init__(self, vec):

        self._vec = list()

        for el in vec:
            self._vec.append(el)


    def __getitem__(self,i):
        return self._vec[i]

    def __setitem__(self,i,val):
        self._vec[i] = val

    def __len__(self):
        return len(self._vec)

    def __str__(self):
        ch = "[ "
        if self._vec != []:
            ch += f"{self[0]}"

            for i in range(1,len(self)):
                ch += f", {self[i]}"

            ch += " ]"
        return ch
