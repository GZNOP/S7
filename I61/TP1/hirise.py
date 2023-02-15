import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import entropie as e

Im1 = Image.open('Jezero1.tif')
Im2 = Image.open('Jezero2.tif')

Im1array = np.asarray(Im1)
Im2array = np.asarray(Im2)

crop = 200

# Partie centrale de l'image 1
Im1cent = Im1array[crop:-crop,crop:-crop]
plt.figure(1)
plt.imshow(Im1cent)

# Partie centrale de l'image 2 décalé de 1 px en haut
Im2origX = Im2array[crop+100:-crop+100,crop:-crop]
plt.figure(2)
plt.imshow(Im2origX)

# Différence entre les deux images
ImdiffX = Im1cent - Im2origX
plt.figure(3)
plt.imshow(abs(ImdiffX))
plt.colorbar()

# Partie centrale de l'image 2 décalé de 1 px à droite
Im2origY = Im2array[crop:-crop,crop+100:-crop+100]
plt.figure(4)
plt.imshow(Im2origY)

ImdiffY = Im1cent - Im2origY
plt.figure(5)
plt.imshow(abs(ImdiffY))
plt.colorbar()

plt.show()
# Calcul de l'information mutuelle entre les deux parties centrales

# Décaler la partie centrale de l'image 2 d'un pixel horizontalement

# Calcul de l'information mutuelle entre Im1cent et la version décalée de Im2
