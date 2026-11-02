# Joachim — Lundi 2 novembre 2026

**Objectif du jour 1.** Expliquer le modèle et obtenir un premier champ avec son énergie. La dérivée et la descente sont expliquées à la main.

**Cas de départ.** RER B, source uniforme unitaire en haut et c=343 m/s. Le premier essai est proposé à 500 Hz. La bande 250–2 000 Hz vient de SOTA.md. Avec le maillage actuel, on commence au plus à 1 500 Hz et on vérifie les dix points par longueur d’onde. Les trois gaussiennes restent un essai de sensibilité facultatif.

## the model to consider,

**Repère :** J1.2. **Rôle :** contributeur.

**Ce qui est fait.** Écrire les équations du modèle et expliquer chaque paroi.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Reprends Helmholtz au §7.3 du polycopié. Définis la pression complexe u, le nombre d’onde k=2*pi*f/c et la répartition de matériau chi. Prends c=343 m/s comme dans le code actuel et annonce cette valeur.
2. Sur un schéma, place la source de Dirichlet uniforme unitaire en haut, les côtés Neumann réfléchissants et le mur Robin en bas. Une valeur uniforme impose aussi la même phase sur toute la source.
3. Explique que l’on fixe une forme, puis que l’on déplace le matériau sur cette forme. Vérifie la convention du coefficient Robin avec Yann avant de relier le coefficient du cours à Alpha dans le code.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** La source excite le domaine. Les côtés renvoient les ondes et la partie poreuse du mur permet de les dissiper.

**Vérification et résultat à transmettre.** Un schéma et les équations avec leurs grandeurs définies.

## formulate the properties of the chosen model, what is known about its solution ;

**Repère :** J1.4. **Rôle :** responsable.

**Ce qui est fait.** Retrouver les propriétés du problème dans le cours.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Retrouve dans le §7.3 les hypothèses sur le domaine, les conditions aux limites et le coefficient du matériau.
2. Énonce simplement le résultat d’existence et d’unicité sous ces hypothèses. Explique qu’il garantit un champ déterminé pour une source et une paroi données.
3. Relie l’absorption à la partie dissipative du coefficient, avec la convention temporelle du cours. Distingue le coefficient de matériau validé du nombre d’exemple Alpha=10-10j.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Les résonances peuvent produire un champ important. Un matériau dissipatif absorbe une partie de l’énergie qui atteint la paroi.

**Vérification et résultat à transmettre.** Quelques propriétés sourcées, avec leurs hypothèses et leur sens physique.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** contributeur.

**Ce qui est fait.** Compléter la fonction qui calcule l’énergie du champ.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », leurs commentaires et leur indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les fonctions fournies restent inchangées et les ajouts restent dans ce seul fichier.

1. Complète your_compute_objective_function(domain_omega,u,spacestep). Sélectionne les points étiquetés NODE_INTERIOR, puis additionne abs(u)**2 sur ces points et multiplie par spacestep**2. Renvoie ce nombre réel.
2. Explique le calcul : chaque point intérieur représente une petite aire et abs(u)**2 mesure l’amplitude de pression au carré. Ce critère correspond à l’intégrale de |u|² du chapitre 7.
3. Vérifie un seul exemple à la main : quatre points intérieurs, u=2 et h=0.5 donnent 4. Transmets ensuite le fichier à Yann pour afficher la valeur du premier calcul.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Une valeur plus petite traduit un champ de pression globalement moins intense dans le domaine observé. Les unités du modèle doivent être précisées avant de parler de joules.

**Vérification et résultat à transmettre.** La fonction complétée, un exemple vérifié et l’énergie du champ initial.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** responsable.

**Ce qui est fait.** Comparer une paroi réfléchissante à une paroi ouverte.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Conserve la même source en haut. Écris les deux modèles en remplaçant seulement une paroi latérale Neumann par la condition de Sommerfeld donnée dans la note de l’énoncé.
2. Multiplie Helmholtz par le conjugué de u et intègre par parties. Définis chaque terme de l’identité obtenue, en gardant le terme de la source et celui du bord ouvert. Le flux représente l’énergie qui traverse ce bord.
3. Écris le critère J(Omega)=int_Omega |u|² et explique comment la forme du mur et les réflexions interviennent dans u, à l’aide du chapitre 5. Présente les hypothèses de l’étude et ce que l’identité permet de comparer. Une inégalité entre les deux énergies intérieures demande une justification supplémentaire.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Une paroi réfléchissante renvoie les ondes dans le domaine, alors qu’une paroi ouverte permet à une partie de l’onde de sortir. Les interférences peuvent modifier les pics.

**Vérification et résultat à transmettre.** Les deux modèles, l’identité d’énergie et une comparaison physique expliquée.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** responsable.

**Ce qui est fait.** Expliquer comment le déplacement du matériau modifie l’énergie.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Reprends le §7.5 et la note sur Dirichlet non homogène. Définis une petite variation de chi et la variation d’énergie qu’elle produit, à source fixée.
2. Présente l’adjoint comme un deuxième champ calculé pour déterminer cette variation, puis donne son équation et la formule de dérivée du cours. Définis les conjugaisons et utilise le champ total avec la source imposée.
3. Explique à Antoine le signe de la dérivée : une variation dans une direction où elle est négative devrait diminuer l’énergie. Écris les étapes à programmer mardi et prépare avec Yann la correspondance de signe du coefficient Robin.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le gradient indique où modifier le matériau pour diminuer le champ global, à condition de garder la quantité choisie.

**Vérification et résultat à transmettre.** La dérivée, l’équation de l’adjoint et leur interprétation, sans code supplémentaire lundi.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.

**Fichier commun.** Joachim complète le coût, puis Yann lance le premier calcul. Antoine transmet la méthode expliquée à la main.
