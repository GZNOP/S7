class Vecteur :

    def __init__(self, vec):

        self._vec = list()

        for el in vec:
            if type(el) is str:
                self._vec.append(float(el))
            else:
                self._vec.append(el)


    def __getitem__(self,i):
        return self._vec[i]

    def __setitem__(self,i,val):
        self._vec[i] = val

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, val):
        self[0] = val

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, val):
        self[1] = val

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, val):
        self[2] = val


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
