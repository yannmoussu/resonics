# Antoine — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser la descente pour plusieurs fréquences et quelques quantités de matériau.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** responsable.

**Ce qui est fait.** Appliquer la même descente au coût de plusieurs fréquences.

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

1. Reprends la descente de mardi et le coût total préparé par Joachim. Utilise une seule répartition chi pour toutes les fréquences.
2. Remplace le coût et le gradient d’une fréquence par les sommes correspondantes. Garde les mêmes étapes de projection et de réduction du pas. Les fréquences et leurs poids restent fixes pendant ce calcul.
3. Garde la liste d’arguments et le retour initial de your_optimization_procedure. Si une liste de fréquences est nécessaire, ajoute seulement un argument facultatif en fin de liste, avec une valeur par défaut qui conserve le cas de mardi. Donne à Yann un exemple d’appel et vérifie le coût final.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Une même zone poreuse doit maintenant agir sur plusieurs pics, ce qui peut donner un placement différent de celui obtenu pour un seul pic.

**Vérification et résultat à transmettre.** La descente réutilisée et un placement commun, avec les fréquences et les poids indiqués.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Ce qui est fait.** Expliquer la contrainte de quantité pour les essais du groupe.

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

1. Avec Mathis et Yann, associe aux points Robin la longueur de mur qu’ils représentent. Écris la quantité absorbante L_abs=sum(w*chi), où w contient ces longueurs.
2. Pour chaque quantité testée, explique la projection correspondante : à partir de la proposition z, on prend clip(z-lambda*w,0,1). Le nombre lambda est choisi par dichotomie pour retrouver L_abs. Quand tous les poids sont identiques, on retrouve le décalage de mardi.
3. Vérifie un exemple chiffré avec les longueurs du mur et transmets les étapes à Yann. Compare des quantités physiques identiques entre formes, avec l’épaisseur et la profondeur annoncées par Mathis.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Cette mesure permet de distinguer l’effet d’une forme de l’effet d’une quantité plus grande de matériau.

**Vérification et résultat à transmettre.** Une contrainte de quantité expliquée et un exemple utilisable pour les essais de Yann.

**Fichier commun.** Joachim transmet son calcul à Antoine, qui complète la descente, puis Yann lance les essais. Chacun utilise la dernière version reçue.
