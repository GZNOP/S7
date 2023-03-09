class Bezier:

    def __init__(self, pt_controle, coul="black", ep=3):
        self._controle = pt_controle

        self._coul = coul

        self._ep = ep

        @property
        def p_controle(self):
            return self._controle

        def __getitem__(self, index):
            return self._controle[index]

        def __setitem__(self, index, val):
            self._controle[index] = val

        @property
        def coul(self):
            return self._coul

        @property
        def ep(self):
            return self._ep

        def trouver_point(self,u):
            """
            Trouve le point des barycentres pour la valeur u
            """

            


        def bezier1(self):
            """
            Trace la courbe de Bézier sans l'utilisation des polynomes de Bernstein
            """
