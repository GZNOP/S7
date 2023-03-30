from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys



def init():

    glClearColor(0.5, 0.5, 0.5, 0)

    # glEnable(GL_CULL_FACE)
    # glEnable(GL_DEPTH_TEST)


def reshape(width, height):
    # On définit la VP de 0,0 jusqu'à width et height (taille de la fenêtre)
    glViewPort(0, 0, width, height)

    # On se met en mode projection, c'est à dire qu'on va définir le mode de visualisation
    glMatrixMode(GL_PROJECTION)

    glOrtho(-2.5, -2.5, 2.5, 2.5, -10, 10)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def display():
    # Avant chaque affichage, on clear les buffer utilisés
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # On sauvegarde la matrice avant de faire tous les changements
    glPushMatrix()

    # Création du cube
    glBegin(GL_TRIANGLE_STRIP)

    # On définit la couleur 
    glColor3f(1.0, 1.0, 1.0)

    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    
    glEnd(GL_TRIANGLE_STRIP)

    glEnd(

def keybind():
    pass


glutInit() # Initialise la fenêtre racine

# GLUT_DOUBLE = On alloue 2 swaps buffers
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA )

# Création de la fenêtre planete
glutCreateWindow('moncube')
# On ajuste la taille de la fenêtre
glutReshapeWindow(1280,720)



glutMainLoop()

