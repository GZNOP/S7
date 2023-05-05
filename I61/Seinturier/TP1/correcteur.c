#include <stdio.h>
#include <stdlib.h>

#include "correcteur.h"


unsigned int pow2(uint n){
  return 1 << n;
}

vecteur vecteur_vide(uint n){
  if (n == 0)return NULL;

  vecteur vec = calloc(n, sizeof(int));
  return vec;
}

void affiche_vecteur(vecteur v, uint n){
  if (v == NULL){
    printf("()\n");
    return;
  }

  printf("(");
  uint i = 0;
  
  if (n > 0){
    printf("%d",v[i++]);

    while (i < n){
      printf(", %d",v[i++]);
    }
    
  }

  printf(")\n");
  
}

vecteur init_vecteur(uint n, uint valeur){
  if (valeur >= pow2(n) || n<=0){
    fprintf(stderr, "Erreur Init vecteur\n");
    return NULL;
  }
    
  vecteur vec = vecteur_vide(n);

  uint i = 0;
  while (valeur > 0){
    vec[i] = valeur % 2;

    valeur >>= 1;
    i++;
  }

  return vec;
}

int valeur(vecteur v, uint n){
  if (v == NULL) return 0;

  
  int val = 0;

  int pui = 1;
  
  for (uint i = 0; i < n; i++){
    val += (v[i]*pui);
    pui <<= 1;
  }

  return val;
  
}

vecteur * mots(uint k){
  if (k == 0)return NULL;

  
  uint nbmots = pow2(k);
  vecteur * V = (vecteur *) malloc(sizeof(vecteur) * nbmots);

  for (uint i = 0; i < nbmots; i++){
    V[i] = init_vecteur(k+1, i);  
  }

  return V;
  
}

void affiche_mots(vecteur * V, uint n){

  printf("Tous les mots sur %u bits : \n",n);
  for (uint i = 0; i < pow2(n); i++){
    affiche_vecteur(V[i], n);
  }
  
}

uint poids(vecteur v, uint n){
  uint p = 0;

  for (uint i = 0; i < n; i++){
    p += v[i];
  }

  return p;
  
}


vecteur diff(vecteur u, vecteur v, uint n){
  if (u == NULL || v == NULL || n == 0) return NULL;
  
  vecteur d = vecteur_vide(n);

  for (uint i = 0; i < n; i++){
    d[i] = u[i] ^ v[i];
  }

  return d;
}

uint hamming(vecteur u, vecteur v, uint n){
  if (u == NULL || v == NULL || n == 0) return 0;
  
  vecteur d = diff(u,v,n);
  return poids(d, n);
}

matrice init_matrice(uint l, uint c){

  matrice m = malloc(sizeof(vecteur) * l);

  for (uint i = 0; i < l; i++){
    m[i] = vecteur_vide(c);
  }

  return m;
}

void affiche_matrice(matrice mat, uint l, uint c){

  for (uint i = 0; i < l; i++){
    printf("[ ");
    for (uint j = 0; j < c; j++){
      printf("%d\t", mat[i][j]);
    }
    printf("]\n");
  }
  
}

vecteur encode(vecteur v, matrice m, uint k, uint n){
  // v de taille k
  if (v == NULL || m == NULL) return NULL;

  vecteur res = vecteur_vide(n);
  
  for (uint j = 0; j < n; j++){
    for (uint i = 0; i < k; i++){
      res[j] ^= (v[i] & m[i][j]);
    }
  }

  return res;
  
}

void encoder_mots(vecteur * les_mots, matrice m, uint l, uint c){
  // il y a 2^l mots 
  
  uint nbmots = 1 << l;

  for (uint i = 0; i < nbmots; i++){
    printf("-----------\n");
    affiche_vecteur(les_mots[i], l);
    affiche_vecteur(encode(les_mots[i], m, l, c), c);
    printf("-----------\n");
  }
  
}

void les_mots_taille_4(void){

  matrice G = malloc(sizeof(vecteur)*4);
  G[0] = init_vecteur(7, 81);
  G[1] = init_vecteur(7, 114);
  G[2] = init_vecteur(7, 52);
  G[3] = init_vecteur(7, 104);

  
  vecteur * m = mots(4);

  encoder_mots(m, G, 4, 7);
}


uint dist_min(vecteur * vecteurs, uint n, uint nb_vect){
  if (vecteurs == NULL || n < 2) return 0;

  uint mini = hamming(vecteurs[0], vecteurs[1], n);
  uint tmp;
  
  for (uint i = 0; i < nb_vect; i++){
    for (uint j = 0; j < i; j++){
      tmp = hamming(vecteurs[i], vecteurs[j], n);

      if (tmp < mini){
	mini = tmp;
      }
      
    }
  }

  return mini;
  
}

float efficacite(uint d){
  return (d-1)>>1;
}

int main(int argc, char * argv[]){


  
}
