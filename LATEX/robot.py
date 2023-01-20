from math import sqrt
from random import randint
import carte as c
import partie as p

# Le nombre d'instruction d'un robot est entre 6 et 21 (en comptant l'instruction
# de secours)
MINIMUM_INSTRUCT = 6
MAXIMUM_INSTRUCT = 21

class Robot():

    # Les listes qui vont contenir les tirs des robots dans le tour
    tir_x = []
    tir_y = []

    def __init__(self, nom):
        """ Constructeur par défaut du robot
        """
        # Le dictionnaire de méthode
        # très puissant pour appeler les instructions des robots
        self._instruction = {"DD":self.deplacement,
            "AL":self.depl_alea,
            "MI":self.pose_mine,
            "IN":self.invisibilite,
            "PS":self.poursuite,
            "FT":self.fuite,
            "TH": self.tir_horizontal,
            "TV": self.tir_vertical,
            "TT": self.test
        }

        self._vivant = True

        # Energie par défaut
        self._energie = 2000

        # Distance de repérage par défaut
        self._distance_rep = 4

        # Position sur la map
        self._x = 0
        self._y = 0

        self._visible = True

        self.nom = nom

        # La liste d'instruction du robot
        self._programme = []

        # La liste des mines qu'il a posé
        self._mine = []


    @classmethod
    def fichier_to_robot(cls, nom_fichier, nom):
        """Constructeur d'un robot
        On précise son énergie (vie + stamina)
        s'il est visible
        sa liste d'instruction (programme)
        la liste des mines qu'il a posé
        """

        new = Robot(nom)

        fichier = open(nom_fichier, "r")

        nb_ligne = 0
        # On rempli
        for ligne in fichier:
            # S'il y a trop d'instructions pour le robot, on ne prend pas en compte
            # celles en trop
            if ligne[0] != ';' and nb_ligne < MAXIMUM_INSTRUCT:

                tup = ligne.split()
                if (len(tup) > 3):
                    raise ValueError

                new._programme.append(tup)
                nb_ligne += 1

        # Par contre s'il y en a trop peu on doit signaler l'erreur
        if nb_ligne < MINIMUM_INSTRUCT:
            print("Erreur nombre d'instruction robot :",nb_ligne)
            raise ValueError

        return new

    @classmethod
    def copier_robot(cls, robot):
        """ Créé une instance de robot qui copie le robot passé en paramêtre
        """

        copie = Robot(robot.nom)

        copie._energie = robot._energie

        copie._x = robot._x

        copie._y = robot._y

        copie._distance_rep = robot._distance_rep

        # Ce n'est pas grave si les robots partagent la même liste d'instruction
        # Ils ne la modifient pas
        copie._programme = robot._programme

        return copie


    @property
    def visible(self):
        return self._visible

    @property
    def programme(self):
        return self._programme

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def mettre_energie(self, val):
        self._energie = val

    def mettre_distance_rep(self, val):
        self._distance_rep = val

    def placer_robot(self,map, x, y):
        """ Tente de placer le robot sur la carte 'map'
        """
        if map._matrice[x][y] == "_":
            self._x = x
            self._y = y
            map._matrice[x][y] = "R"
            return 1
        return 0


    def subit(self, pts_energie):
        """ Retire des points de vie au robot qui appelle la méthode
        """
        self._energie -= pts_energie

    def retirer_mine(liste_robot, x, y):
        """Retire la mine de la liste des mines des robots
        car celle-ci a été détruite
        """
        # On parcourt tous les robots, et on retire la mine de leur liste
        for rbt in liste_robot:
            old = rbt._mine
            rbt._mine = []
            # On garde que les mines dont les coords sont différentes de (x,y)
            for tup in old:
                if (tup[0] != x or tup[1] != y):
                    rbt._mine.append((tup[0],tup[1]))


    def deplacement(self, tup, map, liste_robot ):
        """ Réalise un deplacement du robot qui appelle la méthode dans
        la direction indiquée dans le tuple
        Retourne 1 si le Robot s'est déplacé ou non"""

        self.subit(5)
        deplace = True
        # Selon le déplacement, il faut regarder
        # Si le robot n'est pas en bordure de carte
        # S'il n'y a pas d'obstacle / robot
        # S'il marche sur une de ses mines, il la détruit sans prendre de dégats

        map._matrice[self._x][self._y] = "_"


        # Deplacement à droite
        if self._y+1 < c.NB_COLONNE and tup[1] == "D" and \
        map._matrice[self._x][self._y+1] not in 'R#':
            if (self._x,self._y+1) in self._mine:
                map._matrice[self._x][self._y+1] = '_'
                Robot.retirer_mine(liste_robot, self._x, self._y+1)
            self._y += 1

        # Deplacement en haut
        elif self._x-1 >= 0 and tup[1] == "H" and \
        map._matrice[self._x-1][self._y] not in 'R#':
            if (self._x-1,self._y) in self._mine:
                map._matrice[self._x-1][self._y] = '_'
                Robot.retirer_mine(liste_robot, self._x-1, self._y)
            self._x -= 1

        # Deplacement à gauche
        elif self._y-1 >= 0 and tup[1] == "G" and \
        map._matrice[self._x][self._y-1] not in 'R#':
            if (self._x,self._y-1) in self._mine:
                map._matrice[self._x][self._y-1] = '_'
                Robot.retirer_mine(liste_robot, self._x, self._y-1)
            self._y -= 1

        # Deplacement en bas
        elif self._x+1 < c.NB_LIGNE and tup[1] == "B" and \
        map._matrice[self._x+1][self._y] not in 'R#':
            if (self._x+1,self._y) in self._mine:
                Robot.retirer_mine(liste_robot, self._x+1, self._y)
                map._matrice[self._x+1][self._y] = '_'
            self._x += 1


        else:
            deplace = False

        if deplace :
            self._visible = True

        # On vérifie maintenant si le robot a marché sur une mine

        if (map._matrice[self._x][self._y] == 'X'):
            map._matrice[self._x][self._y] = '_'
            self.subit(200)
            Robot.retirer_mine(liste_robot, self._x, self._y)
            self.jouer_instruction(map, liste_robot, 0) # instruciton de secours
            # print("AIE UNE MINE")

        # La nouvelle position du Robot (peut être inchangée)
        map._matrice[self.x][self.y] = 'R'

        return deplace



    def depl_alea(self, tup, map, liste_robot ):
        """Meme chose que deplacement. Sauf que le robot se deplace dans une
        direction aléatoire.
        """
        self.subit(1)
        dir = randint(1,4)
        deplace = True

        map._matrice[self.x][self.y] = '_'

        # Deplacement vers la droite
        if self._y+1 < c.NB_COLONNE and dir == 1 and \
        map._matrice[self._x][self._y+1] not in '#R':
            if (self._x,self._y+1) in self._mine:
                map._matrice[self._x][self._y+1] = '_'
                Robot.retirer_mine(liste_robot, self._x, self._y+1)
            self._y += 1

        # Deplacement vers le haut
        elif self._x-1 >= 0 and dir == 2 and \
        map._matrice[self._x-1][self._y] not in 'R#':
            if (self._x-1,self._y) in self._mine:
                map._matrice[self._x-1][self._y] = '_'
                Robot.retirer_mine(liste_robot, self._x-1, self._y)
            self._x -= 1

        # Deplacement vers la gauche
        elif self._y-1 >= 0 and dir == 3 and \
        map._matrice[self._x][self._y-1] not in 'R#':
            if (self._x,self._y-1) in self._mine:
                map._matrice[self._x][self._y-1] = '_'
                Robot.retirer_mine(liste_robot, self._x, self._y-1)
            self._y -= 1

        # Deplacement vers le bas
        elif self._x+1 < c.NB_LIGNE and dir == 4 and \
        map._matrice[self._x+1][self._y] not in 'R#':
            if (self._x+1,self._y) in self._mine:
                map._matrice[self._x+1][self._y] = '_'
                Robot.retirer_mine(liste_robot, self._x+1, self._y)
            self._x += 1


        else:
            deplace = False

        # Vérification de la mine
        if (map._matrice[self._x][self._y] == 'X'):
            map._matrice[self._x][self._y] = '_'
            Robot.retirer_mine(liste_robot, self._x, self._y)
            self.subit(200)
            self.jouer_instruction(map, liste_robot, 0)
            # print("AIE UNE MINE")

        map._matrice[self.x][self.y] = 'R'

        if deplace:
            self._visible = True

        return deplace

    def pose_mine(self, tup, map, liste_robot ):
        """
        le robot pose une mine dans une des 4 directions autour de lui
        """
        dir = randint(1,4)
        # On ajoute les coordonnées de la mine posée dans self._mine pour
        # qu'il ne marche pas dessus
        # On lui retire aussi 10 pts d'énergie

        # il subit les dégats de la pose
        self.subit(10)
        mine = True


        # Pose la mine à droite
        if self._y+1 < c.NB_COLONNE and dir == 1 and \
        map._matrice[self._x][self._y+1] not in 'RX#' and (self._x,self._y+1) not in self._mine:

            map._matrice[self._x][self._y+1] = 'X'
            self._mine.append((self._x,self._y+1))

        # Pose la mine en haut
        elif self._x-1 >= 0 and dir == 2 and \
        map._matrice[self._x-1][self._y] not in 'RX#' and (self._x-1,self._y) not in self._mine:

            map._matrice[self._x-1][self._y] = 'X'
            self._mine.append((self._x-1,self._y))


        # Pose la mine à gauche
        elif self._y-1 >= 0 and dir == 3 and \
        map._matrice[self._x][self._y-1] not in 'RX#' and (self._x,self._y-1) not in self._mine:

            map._matrice[self._x][self._y-1] = 'X'
            self._mine.append((self._x,self._y-1))


        # Pose la mine à en bas
        elif self._x+1 < c.NB_LIGNE and dir == 4 and \
        map._matrice[self._x+1][self._y] not in 'RX#' and (self._x+1,self._y) not in self._mine:

            map._matrice[self._x+1][self._y] = 'X'
            self._mine.append((self._x+1,self._y))

        else:
            mine = False

        return mine

    def invisibilite(self, tup, map, liste_robot ):
        # le robot redevient visible que s'il se deplace
        self._visible = False
        self.subit(20)

    def robot_plus_proche(self, liste_robot):
        """ Retourne le robot le plus proche de l'instance
        """
        plusproche = None
        dist_mini = 500

        # On parcourt les robots
        for robot in liste_robot:
            # On regarde s'ils sont vivants et visible avant de calculer la distance
            if robot.vivant() and robot.visible and robot != self:

                dist = sqrt(pow(robot._y - self._y, 2) + pow(robot._x - self._x, 2))
                if dist < dist_mini:
                    dist_mini = dist
                    plusproche = robot

        return plusproche

    def poursuite(self, tup, map, liste_robot ):
        """ l'instance se rapproche du robot le plus proche de lui parmis les robots
        de la liste_robot
        """
        self.subit(4)
        deplace = False
        plusproche = self.robot_plus_proche(liste_robot )

        if plusproche == None:
            return

        # L'adversaire se situe sur la même ligne à droite du robot
        if (plusproche._x == self._x and plusproche._y-1 > self._y):
            deplace = self.deplacement(["DD",'D'], map, liste_robot )

        # L'adversaire se situe sur la même ligne à gauche du robot
        elif (plusproche._x == self._x and plusproche._y < self._y-1 ):
            deplace = self.deplacement(["DD",'G'], map, liste_robot )

        # L'adversaire se trouve sur la même colonne en dessous du robot
        elif (plusproche._y == self._y and plusproche._x-1 > self._x ):
            deplace = self.deplacement(["DD",'B'], map, liste_robot )

        # L'adversaire se trouve sur la même colonne au dessus du robot
        elif (plusproche._y == self._y and plusproche._x < self._x-1):
            deplace = self.deplacement(["DD", 'H'], map , liste_robot )

        # L'adversaire se situe en bas à droite du robot
        elif (plusproche._y-1 > self._y and plusproche._x-1 > self._x):
            deplace = self.deplacement(["DD", 'B'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'D'], map, liste_robot )
                deplace = self.deplacement(["DD",'B'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'D'], map, liste_robot ) or \
                deplace

        # L'adversaire se situe en haut à droite du robot
        elif (plusproche._y-1 > self._y and plusproche._x < self._x-1):
            deplace = self.deplacement(["DD", 'H'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'D'], map, liste_robot )
                deplace = self.deplacement(["DD",'H'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'D'], map, liste_robot ) or \
                deplace

        # L'adversaire se situe en haut à gauche robot
        elif (plusproche._y < self._y-1 and plusproche._x < self._x-1):
            deplace = self.deplacement(["DD", 'H'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'G'], map, liste_robot )
                deplace = self.deplacement(["DD",'H'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'G'], map, liste_robot ) or \
                deplace

        # L'adversaire se situe en bas à gauche du robot
        elif (plusproche._y < self._y-1 and plusproche._x-1 > self._x):
            deplace = self.deplacement(["DD", 'B'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'G'], map, liste_robot )
                deplace = self.deplacement(["DD",'B'], map, liste_robot ) or \
                deplace
            else:
                deplace = deplace or \
                self.deplacement(["DD",'G'], map, liste_robot )

        # Si le robot ne s'est pas déplacé, mouvement aléatoire
        if not deplace:
            self.depl_alea([], map, liste_robot )
        return deplace


    def fuite(self, tup, map, liste_robot ):
        """ l'instance s'éloigne du robot le plus proche de lui parmis les robots
        de la liste_robot
        """
        self.subit(4)
        deplace = False
        plusproche = self.robot_plus_proche(liste_robot)

        if plusproche == None:
            return

        # L'adversaire se situe sur la même ligne à droite du robot
        if (plusproche._x == self._x and plusproche._y-1 > self._y):
            deplace = self.deplacement(["DD",'G'], map, liste_robot )

        # L'adversaire se situe sur la même ligne à gauche du robot
        elif (plusproche._x == self._x and plusproche._y < self._y-1 ):
            deplace = self.deplacement(["DD",'D'], map, liste_robot )

        # L'adversaire se trouve sur la même colonne en dessous du robot
        elif (plusproche._y == self._y and plusproche._x-1 > self._x ):
            deplace = self.deplacement(["DD",'H'], map, liste_robot )

        # L'adversaire se trouve sur la même colonne au dessus du robot
        elif (plusproche._y == self._y and plusproche._x < self._x-1):
            deplace = self.deplacement(["DD", 'B'], map , liste_robot )

        # L'adversaire se situe en bas à droite du robot
        elif (plusproche._y-1 > self._y and plusproche._x-1 > self._x):
            deplace = self.deplacement(["DD", 'H'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'G'], map, liste_robot )
                deplace = self.deplacement(["DD",'H'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'G'], map, liste_robot ) or \
                deplace

        # L'adversaire se situe en haut à droite du robot
        elif (plusproche._y-1 > self._y and plusproche._x < self._x-1):
            deplace = self.deplacement(["DD", 'B'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'G'], map, liste_robot )
                deplace = self.deplacement(["DD",'B'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'G'], map, liste_robot ) or \
                deplace

        # L'adversaire se situe en haut à gauche robot
        elif (plusproche._y < self._y-1 and plusproche._x < self._x-1):
            deplace = self.deplacement(["DD", 'B'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'D'], map, liste_robot )
                deplace = self.deplacement(["DD",'B'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'D'], map, liste_robot ) or \
                deplace

        # L'adversaire se situe en bas à gauche du robot
        elif (plusproche._y < self._y-1 and plusproche._x-1 > self._x):
            deplace = self.deplacement(["DD", 'H'], map , liste_robot )
            if not deplace:
                deplace = self.deplacement(["DD",'D'], map, liste_robot )
                deplace = self.deplacement(["DD",'H'], map, liste_robot ) or \
                deplace
            else:
                deplace = self.deplacement(["DD",'D'], map, liste_robot ) or \
                deplace

        # Si le robot ne s'est pas déplacé, mouvement aléatoire
        if not deplace:
            self.depl_alea([], map, liste_robot )

        return deplace

    def tir_vertical(self, tup, map, liste_robot ):
        dir = randint(1,2)
        print(self.nom, "tire à la vertical")
        self.subit(3)

        # Tire en haut
        if (dir == 1):
            Robot.tir_x.append((self._x, self.y, "H"))

        # Tire en bas
        else :
            Robot.tir_x.append((self._x, self._y, "B"))

    def tir_horizontal(self, tup, map, liste_robot):
        print(self.nom, "tire à l'horizontal")
        dir = randint(1,2)

        self.subit(3)

        # Tire à gauche
        if (dir == 1):
            Robot.tir_y.append((self._x, self.y, "G"))

        # Tire à droite
        else :
            Robot.tir_y.append((self._x, self._y, "D"))


    def test(self, tup, map, liste_robot ):
        """ Instruction du robot qui va tester si un robot est proche
        execute la premiere instruction du tuple si c'est le cas,
        execute l'autre instruction sinon
        """
        plusproche = self.robot_plus_proche(liste_robot)
        if plusproche == None:
            return

        # print(plusproche._x , self._x,plusproche._y , self._y)
        distance = sqrt(pow(plusproche._x - self._x,2) + pow(plusproche._y - self._y,2))

        if distance <= self._distance_rep:
            # print(tup[1])
            fonc = self._instruction[tup[1]]
            fonc(tup, map, liste_robot )

        else:
            # print(tup[2])
            fonc = self._instruction[tup[2]]

            fonc(tup, map, liste_robot )


    def vivant(self):
        """ Détermine si le robot est mort
        retourne 0 s'il est mort
        1 sinon
        """
        self._energie = int(self._energie)
        if (self._energie > 0):
            self._vivant = 1
            return 1

        # On met à jour l'état du robot
        # On considère qu'il est invisible, il n'est plus considé
        self._vivant = 0
        self._energie = 0
        self._visible = 0
        return 0

    def jouer_instruction(self, map, liste_robot, index):
        """ Réalise l'instruction à l'indice i du programme du robot
        """
        if (self.vivant() == 0):
            return

        # On récupère l'instruction
        tup = self._programme[index % (len(self._programme)-1) + 1]

        # On récupère la fonction associé à l'instruction
        fonc = self._instruction[tup[0]]
        # On l'appelle
        fonc(tup,map,liste_robot)
