int deg(t_graphe G, int s){
  int degre = 0;
  for (int t = 0; t < G.nbs; t++){
    degre += G.mat[s][t];
  }
  return degre;
}

char eulerien(t_graphe G){
  for (int s = 0; s < G.nbs; s++){
    if (deg(G,s) % 2){
      return 0;
    }
  }
  return 1;
}
