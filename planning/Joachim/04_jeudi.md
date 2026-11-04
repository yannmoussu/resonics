# Joachim — Jeudi 5 novembre 2026

**Objectif du jour 4.** Interpréter les résultats calculés et choisir un panneau.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[-50, 50]`. Le coefficient suit la convention `d_n u - alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Ce qui est fait.** Relier les formules aux résultats conservés.

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

1. Reprends une courbe d’énergie et une carte du champ parmi les résultats du groupe. Vérifie que leurs paramètres correspondent aux équations présentées.
2. Compare l’interprétation des pics et de la dissipation à l’étude ouverte/réfléchissante de lundi. Définis les notions utilisées dans le texte.
3. Si le calcul du gradient a changé, refais le petit essai de perturbation de mardi. Corrige uniquement une erreur identifiée dans ta partie du fichier commun.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** On explique le résultat avec les réflexions, les résonances et l’emplacement du matériau, plutôt qu’avec la seule baisse d’un nombre.

**Vérification et résultat à transmettre.** Une explication courte des figures retenues et les corrections réellement nécessaires.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Ce qui est fait.** Contribuer au choix du panneau avec les résultats du modèle.

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

1. Observe avec le groupe les courbes obtenues pour les panneaux réellement calculés, avec une source et des quantités comparables.
2. Indique la forme et la répartition qui donnent le meilleur compromis sur les fréquences retenues. Appuie la décision sur une figure et deux ou trois valeurs.
3. Explique la conclusion à partir du modèle et des hypothèses annoncées. Une pondération par le spectre hypothétique reste une variante dont on précise l’effet.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le panneau retenu doit réduire le champ pour le cas étudié, avec la quantité de matériau annoncée. Une seule fréquence favorable ne résume pas toute une bande.

**Vérification et résultat à transmettre.** Une conclusion collective qui relie le choix du panneau aux calculs.
