import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import entropie as e


# pour lena.jpeg
Im = Image.open('lena.jpeg')
Imarray = np.asarray(Im)

plt.figure()
plt.imshow(Imarray, cmap='gray')

# Calculer et afficher la densité de probabilité de l'image
xe = np.asarray(range(np.amax(Imarray[:])+2)) # Nb de valeur possible (i)
H1, xe = np.histogram(Imarray.reshape(-1), bins=xe) # H1[i] c'est le nombre d'occurence de cette valeur de i
P1 = H1/Imarray.size # P1[i] est la probabilité de la valeur i
plt.figure()
plt.plot(P1)

# pour lena4.jpeg

Im2 = Image.open("lena4.jpeg")
Imarray2 = np.asarray(Im2)

plt.figure()
plt.imshow(Imarray2, cmap='gray')

xe = np.asarray(range(np.amax(Imarray2[:])+2)) # Nb de valeur possible (i)
H2, xe = np.histogram(Imarray2.reshape(-1), bins=xe) #H2[i] c'est le nombre d'occurence de cette valeur de i
P2 = H2/Imarray2.size

plt.figure()
plt.plot(P2)


Pc = e.proba_jointes(Imarray, Imarray2, 256)
print(e.entropie(Pc))

print(e.NMI(Imarray, Imarray2))
#plt.show()
