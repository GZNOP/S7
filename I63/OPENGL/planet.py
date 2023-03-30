#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c

from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

###############################################################
# variables globales
year, day, sat, rev , angh, angv = 0, 0, 0, 0, 0, 0
X , Z = 0, 0
quadric = None

###############################################################
#

def creer_soleil():
    """Création du soleil"""

   # glDisable(GL_LIGHTING)

   # glColor4f (0.7, 0.5, 0.0, 1.0)
    
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (1.0, 1.0, 0.3, 1.0) )
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.7, 0.7, 0.0, 1.0) )
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.7, 0.7, 0.0, 1.0) )
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.7, 0.7, 0.0, 1.0) )
    
    gluSphere(quadric, 1.0, 20, 16) # On créé une sphere (le soleil)

    #glEnable(GL_LIGHTING)

def creer_terre():
    """Création de la Terre"""

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0) )
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.0, 0.0, 0.3, 1.0) )
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.1, 0.1, 0.6, 1.0) )
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0) )
    
    glRotatef(year, 0.0, 1.0, 0.0) # On la fait se deplacer de year
    glTranslatef(2.0, 0.0, 0.0) # On la translate
    glRotatef(day, 0.0, 1.0, 0.0) # On effectue une rotation de jour à la Terre
    
    gluSphere(quadric, 0.2, 10, 8) 

def creer_lumiere():
    """
    Création de la lumière du Soleil
    """
    pos = (0.0, 0.0, 0.0, 1.0)
    diffuse = (0.8, 0.8, 0.8, 1.0)
    
    glLightfv(GL_LIGHT0, GL_POSITION, pos) # On place la lumière
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse ) # On met les paramètres de la lumière

def creer_satellite():
    """
    Création d'un satellite autour de la Terre
    """

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.3, 0.3, 0.3, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
    
    glRotatef(sat, 1.0, 0.0, 0.0)
    glTranslatef(0.5, 0.0, 0.0)
    glRotatef(sat, 0.0, 1.0, 0.0)
    gluSphere(quadric, 0.1, 8, 6) # Création de la lune
    

def init():
    global quadric
    glClearColor (0.0, 0.0, 0.0, 0.0) # Initialisation de la couleur

    
    # glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH) # Ombre réaliste
    quadric = gluNewQuadric() # Forme sphere
    gluQuadricDrawStyle(quadric, GLU_FILL)


def creer_camera():
    """
    Créer une perspective qui représente la caméra de la scene
    """

    glRotatef(angv, 0.0, 1.0, 0.0)
    glRotatef(angh, 1.0, 0.0 ,0.0)
    glTranslatef(X, 0.0 , Z)
    glTranslatef(0.0, 0.0, -5.0)


    

    
    
def display():
    glClear (GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT) # On supprime tout
    # glColor4f (1.0, 1.0, 0, 1.0) # On initialise la couleur 

    
    glPushMatrix() # On sauvegarde la matrice de transformation courante
    
    creer_camera()
    
    creer_soleil()
    
    creer_lumiere()

    creer_terre()

    creer_satellite()
    
    glPopMatrix() # On revient à la matrice initiale

    
    glutSwapBuffers() # On met à jour les buffers

def reshape(width, height):
    glViewport(0, 0, width, height) # Definition de la VP

    
    glMatrixMode(GL_PROJECTION) # Definition de la matrice en mode projection
    glLoadIdentity() # On insère la matrice identité dans la pile de matrice
    gluPerspective(60, width / height, 0.1, 100) # On définit la perspective

    # if width <= height: # On recadre la fenêtre
    #     glOrtho(-2.5, 2.5, -2.5*height/width, 2.5*height/width, -10.0, 10.0)
    # else:
    #     glOrtho(-2.5*width/height, 2.5*width/height, -2.5, 2.5, -10.0, 10.0)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    


    
def keyboard(key, x, y):
    global day, year, sat, rev, X, Z, angh, angv
    key = key.decode('utf-8')
    if key == 'j':
        day = (day + 10) % 360
        sat = (sat + 28) % 360
    elif key == 'a':
        year = (year + 5) % 360
        sat = (sat + 28) % 360
        day = (day + 10) % 360
        rev = (rev + 10) % 360
    elif key == 'z':
        Z += 0.5 
    elif key == 'q':
        X += 0.5
    elif key == 's':
        Z -= 0.5
    elif key == 'd':
        X -= 0.5
    elif key == 'o':
        angh = (angh - 10) % 360
    elif key == 'k':
        angv = (angv - 10) % 360
    elif key == 'l':
        angh = (angh + 10 ) % 360
    elif key == 'm':
        angv = (angv + 10 ) % 360
    elif key == '\033':
        # sys.exit( )  # Exception ignored
        glutLeaveMainLoop()
    glutPostRedisplay()  # indispensable en Python

###############################################################
# MAIN

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

glutCreateWindow('planet')
glutReshapeWindow(512,512)

glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

init()

glutMainLoop()
