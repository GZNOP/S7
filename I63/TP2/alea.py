import sys
sys.path.append("..")

from lib.Projection import *
from lib.bresenham import segment_naif
import lib.Vecteur as v
from random import randint

WC = [v.Vecteur([-1000,-1000]), v.Vecteur([1000,1000])]
DC1 = [v.Vecteur([0,0]), v.Vecteur([640,720])]
DC2 = [v.Vecteur([640,0]), v.Vecteur([1280,720])]

# Création de la fenetre virtuelle
root = tk.Tk()
root.geometry("1290x730")
root["bg"] = "grey"
ca = tk.Canvas(root, width=1280, height=720)
ca.pack(padx=5, pady=5)

 # Création d'une boucle de segments aléatoires
 
