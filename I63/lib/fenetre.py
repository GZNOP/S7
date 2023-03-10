import tkinter as tk
def creer_fenetre(largeur=1280, hauteur=720):
    """
    Créer une root avec un canvas (qui joue le role de window)
    """

    root = tk.Tk()
    root.geometry(f"{largeur+10}x{hauteur+10}")
    root.title("Fenêtre de projection")
    root["bg"] = "grey"
    ca = tk.Canvas(root, width=largeur, height=hauteur)
    ca.pack(padx=5, pady=5)

    return root, ca
