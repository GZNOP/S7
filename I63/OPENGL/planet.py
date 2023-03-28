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
year, day = 0, 0
quadric = None

###############################################################
# 

def init():
    global quadric
    glClearColor (0.0, 0.0, 0.0, 0.0) # Initialisation de la couleur
    glShadeModel (GL_FLAT) # Ombre simple
    quadric = gluNewQuadric() # Forme sphere
    gluQuadricDrawStyle(quadric, GLU_LINE)

def display():
    glClear (GL_COLOR_BUFFER_BIT) # On supprime tout
    glColor4f (1.0, 1.0, 1.0, 0.5) # On initialise la couleur 

    glPushMatrix() # On sauvegarde la matrice de transformation courante
    gluSphere(quadric, 1.0, 20, 16) # On créé une sphere dans le quadric (le soleil)
    glRotatef(year, 0.0, 1.0, 0.0) # On la fait se deplacer de year
    glTranslatef(2.0, 0.0, 0.0) # On la translate
    glRotatef(day, 0.0, 1.0, 0.0) # On effectue une rotation de jour à la Terre
    gluSphere(quadric, 0.2, 10, 8) # On créé la Terre
    glPopMatrix() # On revient à la matrice initiale

    glutSwapBuffers() # On met à jour les buffers

def reshape(width, height):
    glViewport(0, 0, width, height) # Definition de la VP
    glMatrixMode(GL_PROJECTION) # Definition de la matrice en mode projection
    glLoadIdentity() # On insère la matrice identité dans la pile de matrice
    if width <= height: # On trace le repère
        glOrtho(-2.5, 2.5, -2.5*height/width, 2.5*height/width, -10.0, 10.0)
    else:
        glOrtho(-2.5*width/height, 2.5*width/height, -2.5, 2.5, -10.0, 10.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global day, year
    key = key.decode('utf-8')
    if key == 'd':
        day = (day + 10) % 360
    elif key == 'D':
        day = (day - 10) % 360
    elif key == 'y':
        year = (year + 5) % 360
    elif key == 'Y':
        year = (year - 5) % 360
    elif key == '\033':
        # sys.exit( )  # Exception ignored
        glutLeaveMainLoop()
    glutPostRedisplay()  # indispensable en Python

###############################################################
# MAIN

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

glutCreateWindow('planet')
glutReshapeWindow(512,512)

glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

init()

glutMainLoop()
