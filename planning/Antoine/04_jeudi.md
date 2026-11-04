# Antoine — Jeudi 5 novembre 2026

**Objectif du jour 4.** Interpréter les résultats calculés et choisir un panneau.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Ce qui est fait.** Lire la courbe de descente et vérifier les quantités.

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

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », leurs commentaires et leur indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les fonctions fournies restent inchangées et les ajouts restent dans ce seul fichier.

1. Reprends la courbe des étapes acceptées pour le panneau qui semble le plus intéressant. Vérifie que le coût final correspond à la répartition représentée.
2. Vérifie les bornes de chi et la quantité absorbante, puis relève la raison de l’arrêt.
3. Propose seulement une correction nécessaire ou quelques itérations supplémentaires si cela peut modifier la conclusion. Garde un seul départ de référence pour le MVP.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Une baisse à quantité constante vient du placement du matériau. Une énergie qui se stabilise décrit le résultat de cette descente, pas une preuve d’optimum global.

**Vérification et résultat à transmettre.** Une courbe interprétée et la quantité du panneau retenu vérifiée.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Ce qui est fait.** Aider le groupe à choisir avec une quantité connue.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Compare les candidats calculés en relevant la forme, la quantité de matériau et les fréquences étudiées.
2. Donne deux ou trois valeurs d’énergie utiles à la décision, ainsi que la quantité correspondante.
3. Explique le compromis retenu avec Olympia et Mathis. Appuie le choix sur les résultats, puis fais valider la conclusion par le groupe.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le choix dépend de l’énergie restante et du matériau nécessaire pour l’obtenir. Ajouter du matériau et mieux le placer sont deux effets à distinguer.

**Vérification et résultat à transmettre.** Une conclusion courte sur l’efficacité obtenue pour la quantité retenue.
