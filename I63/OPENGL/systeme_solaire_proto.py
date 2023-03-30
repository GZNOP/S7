#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c

from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
# from Image import open
from PIL import Image

###############################################################
# variables globales
year, day = 0, 0  # Terre
luna, periode = 0, 0  # Lune
quadric = None
SOLEIL, TERRE, ATERRE, LUNE = 1, 2, 3, 4  # ID astre, planete, satellite
texture_planete = [None for i in range(5)]

###############################################################
# chargement des textures

def LoadTexture(filename, ident):
    global texture_planete
    image = Image.open(filename)  # retourne une PIL.image
    
    ix = image.size[0]
    iy = image.size[1]
    # image = image.tostring("raw", "RGBX", 0, -1)
    image = image.tobytes("raw", "RGBX", 0, -1)
    
    # 2d texture (x and y size)
    # BUG (?)
    #glBindTexture(GL_TEXTURE_2D, glGenTextures(1, texture_planete[ident]))
    texture_planete[ident] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, int(texture_planete[ident]))

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # commente car alpha blinding (cf. atmosphere)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

###############################################################
# creation des composants du systeme

def CreerPlanete(rayon):
    ambient = (0.1, 0.1, 0.1, 1.0)
    diffuse = (0.8, 0.8, 0.8, 1.0)
    Black = (0.0, 0.0, 0.0, 1.0)
    sph1 = gluNewQuadric()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, Black)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, ambient)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)

    gluQuadricDrawStyle(sph1, GLU_FILL)
    gluQuadricNormals(sph1, GLU_SMOOTH)
    gluQuadricTexture(sph1, GL_TRUE)
    gluSphere(sph1, rayon, 100, 80)

def CreerSoleil(rayon):
    ambient = (0.5, 0.5, 0.5, 1.0)
    diffuse = (0.8, 0.8, 0.5, 1.0)
    Yellow = (0.5, 0.5, 0.1, 1.0)
    sph2 = gluNewQuadric()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, Yellow)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, ambient)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)

    gluQuadricDrawStyle(sph2, GLU_FILL)
    gluQuadricNormals(sph2, GLU_SMOOTH)
    gluQuadricTexture(sph2, GL_TRUE)
    gluSphere(sph2, rayon, 100, 80)

###############################################################
# affichage

def display_sun():
    pass

def display_earth():
    pass

def display_atmosphere():
    pass

def display_moon():
    pass

###############################################################
# 

def init_texture():
    pass

def init():
    global quadric
    glClearColor (0.0, 0.0, 0.0, 0.0) # Initialisation de la couleur

    
    # glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH) # Ombre réaliste
    quadric = gluNewQuadric() # definition d'une Forme 
    gluQuadricDrawStyle(quadric, GLU_FILL)

def display():
    pass

def reshape(width, height):
    pass

def keyboard(key, x, y):
    pass

###############################################################
# MAIN

glutInit(sys.argv)

glutMainLoop()
