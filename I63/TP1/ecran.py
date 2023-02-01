import tkinter as tk

LAR = 1280
HAU = 720

X,Y = 0,0

# -------------------------------- CALLBACKS --------------------------

def obtenir_xy(event):
    global X,Y

    X = event.x
    Y = event.y

def deplacer_fen(event, ca, tag):
    global X,Y

    dx = event.x - X
    dy = event.y - Y

    X = event.x
    Y = event.y

    ca.move(tag"vir", dx, dy)


# --------------------------- PARTIE TKINTER -------------------------------

def creer_root():
    """
    Créer une fenêtre principale en tkinter
    """
    root = tk.Tk()

    root.geometry(F"{LAR+10}x{HAU+10}")
    root.title("fenêtre virtuelle")

    return root

def creer_canvas(root):
    """
    Créer le canvas qui servira d'écran virtuel pour le tp
    """

    ca = tk.Canvas(root, width=LAR, height=HAU, bg="grey")

    ca.pack(padx=5, pady=5, expand=True)

    ca.tag_bind("vir","<Button-1>", lambda event: obtenir_xy(event))
    ca.tag_bind("vir","<B1-Motion>", lambda event: deplacer_fen(event, ca))


    return ca

def trace_vir(canv, x, y, long, lar):
    """
    Trace le rectange dans le canvas qui correspond à la fenêtre virtuelle
    """

    canv.create_rectangle(x, y, x+long, y+lar, fill="white", tag="vir")


# ------------------------ PARTIE PROJECTION -------------------------------








racine = creer_root()
ca = creer_canvas(racine)

trace_vir(ca, 250, 50, 500, 250)

racine.mainloop()
