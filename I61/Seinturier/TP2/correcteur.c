#include <stdio.h>
#include <stdlib.h>

#include "correcteur.h"

#define MATRIX_ORDER_RAW_MAJOR 0
#define MATRIX_ORDER_COLUMN_MAJOR 1

unsigned int pow2(uint n){
  return 1 << n;
}

vecteur vecteur_vide(uint n){
  return 0;
}

void affiche_vecteur(vecteur v, uint n){

  printf("(");
  uint i = 0;
  
  if (n > 0){
    printf("%d", (v >> i++) & 1);

    while (i < n){
      printf(", %d", (v >> i++) & 1);
    }
    
  }

  printf(")\n");
  
}

vecteur init_vecteur(uint n, uint valeur){
  return valeur;
}

int valeur(vecteur v, uint n){

  return v;
  
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
    p += ((v >> i) & 1);
  }

  return p;
  
}


vecteur diff(vecteur u, vecteur v, uint n){

  return init_vecteur(n, u ^ v);
}

uint hamming(vecteur u, vecteur v, uint n){
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

void affiche_matrice(matrice mat, uint taille, uint nbbits, char order){

  if (order == MATRIX_ORDER_RAW_MAJOR){
    printf("Ligne majeure : \n");
    for (uint i = 0; i < taille; i++){
    printf("[ ");
    for (uint j = 0; j < nbbits; j++){
      printf("%d\t", (mat[i] >> j) & 1 );
    }
    printf("]\n");
   }
  }
  
  else{
    printf("Colonne majeure : \n");
    for (uint i = 0; i < nbbits; i++){
    printf("[ ");
    for (uint j = 0; j < taille; j++){
      printf("%d\t", (mat[i] >> j) & 1 );
    }
    printf("]\n");
   }
   
  }
  
  

  
}

vecteur encode(vecteur v, matrice m, uint k, uint n){
  // v sur k bits
  // v est en ligne
  // m est en colonne majeure de n lignes et k bits par ligne

  vecteur res = 0;
  
  for (uint i = 0; i < n; i++){
    res += ((poids(m[i] & v, k) & 1) << i );
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

syndrome trouver_syndrome(matrice h, vecteur c, uint k, uint n){
  // c sur k bits
  // c est en ligne
  // h est en ligne majeure de n lignes et k bits par ligne

  syndrome res = 0;
  
  for (uint i = 0; i < n; i++){
    res += poids((h[i] & c), k) & 1 ;
  }
  return res;
}

void trouver_syndrome_

int main(int argc, char * argv[]){

  matrice G = init_matrice(7,4);
  G[0] = 1;
  G[1] = 2;
  G[2] = 4;
  G[3] = 8;
  G[4] = 7;
  G[5] = 14;
  G[6] = 11;

  matrice H = init_matrice(3, 7);

  H[0] = 23;
  H[1] = 46;
  H[2] = 75;

  affiche_matrice(H,3,7,1);
  affiche_matrice(H,3,7,0);
  
  vecteur v = 11;
  
  affiche_vecteur(v,4);

  vecteur e = encode(v, G, 4, 7);

  vecteur s = trouver_syndrome(H, e, 7, 3);

  affiche_vecteur(e,7);
  affiche_vecteur(s,3);
  
}
