import sys
if __name__ == "__main__":
    sys.path.append("..")

from lib.Projection import *

if __name__ == "__main__":
    """

    ./python3 main.py -7 8 10 2 3 4

    Evaluation sur [-7, 8] en 10 points de 4x²+3x+2

    """

    xmin = float(argv[1])
    xmax = float(argv[2])
    nb_point = int(argv[3])
    coef =  argv[4:]

    for i in range(len(coef)):
        coef[i] = float(coef[i])

    WC1 = [v.Vecteur([0,0]), v.Vecteur([10,10])]
    DC1 = [v.Vecteur([100,100]), v.Vecteur([400,300])]

    WC2 = [v.Vecteur([-5,-5]), v.Vecteur([5,5])]
    DC2 = [v.Vecteur([200,200]), v.Vecteur([500,400])]

    WC3 = [v.Vecteur([xmin,0]), v.Vecteur([xmax,25])]
    DC3 = [v.Vecteur([300,300]), v.Vecteur([600,500])]


    root = tk.Tk()
    root.geometry("1290x730")
    root["bg"]="grey"

    ca = tk.Canvas(root, width=1280, height=720)
    ca.pack(padx=5, pady=5)

    P = Projection(ca,"premier", WC1, DC1)
    Q = Projection(ca,"deuxieme", WC2, DC2)
    R = Projection(ca,"trois", WC3, DC3)


    Q + v.Vecteur([2,2,1])
    Q + v.Vecteur([4,4,1])

    P.projetter_fichier("courbe.dat")

    R.projetter_fonction(xmin, xmax, nb_point, coef)

    root.mainloop()
