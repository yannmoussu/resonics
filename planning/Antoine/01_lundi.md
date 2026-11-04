# Antoine — Lundi 2 novembre 2026

**Objectif du jour 1.** Expliquer le modèle et obtenir un premier champ avec son énergie. La dérivée et la descente sont expliquées à la main.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** responsable.

**Ce qui est fait.** Écrire ce que l’on cherche à diminuer et ce qui reste fixé.

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

1. Écris le critère J=int_Omega |u|², puis définis chi comme la répartition du matériau sur le mur. La forme, la source et la fréquence sont fixées pour ce premier problème.
2. Écris les contraintes : chi reste entre zéro et un et sa quantité totale reste fixée. Dans le support, V_obj est la moyenne de chi sur les points Robin.
3. Donne un exemple : quatre points avec chi=(1,1,0,0) ont la même quantité nodale que chi=(0.5,0.5,0.5,0.5). Explique le lien avec la contrainte continue du chapitre 7.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** On cherche à mieux placer une quantité donnée de matériau, plutôt qu’à en ajouter pour obtenir une baisse d’énergie.

**Vérification et résultat à transmettre.** Le critère et les contraintes, avec un exemple compris par le groupe.

## to choose porous material(s) and its quantity ;

**Repère :** J1.7. **Rôle :** contributeur.

**Ce qui est fait.** Nommer correctement la quantité du premier essai.

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

1. Lis comment le support construit chi et calcule V_obj. Compte les points Robin et les valeurs de chi qui s’y trouvent.
2. Avec Mathis, donne la fraction utilisée pour la première forme. Un point où chi=1 est entièrement couvert et un point où chi=0 est réfléchissant dans le modèle.
3. Explique que cette fraction se transforme en longueur absorbante à partir des longueurs représentées sur le mur. Avec une épaisseur et une profondeur fixées, cette longueur permet ensuite de calculer un volume.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** À forme fixée, conserver la somme de chi conserve la quantité numérique du support. Entre deux formes, on compare les longueurs ou volumes de matériau correspondants.

**Vérification et résultat à transmettre.** La quantité du premier calcul annoncée avec son unité ou comme fraction de points.

## formulate/consider the numerical gradient descent method.

**Repère :** J1.10. **Rôle :** responsable.

**Ce qui est fait.** Expliquer la descente avec un petit exemple.

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

1. Reprends les étapes du §7.6 : calculer le champ et le gradient, déplacer chi dans le sens opposé au gradient, puis recalculer l’énergie.
2. Explique comment garder les contraintes : on décale toutes les valeurs Robin puis on les ramène entre zéro et un avec numpy.clip. On ajuste le décalage par dichotomie, en divisant l’intervalle d’essai par deux, jusqu’à retrouver la somme imposée. Par exemple, une proposition (0.9,0.5) devient (0.7,0.3) pour une somme égale à un.
3. Décris un essai accepté si l’énergie baisse et un pas divisé par deux si elle augmente. Écris ces étapes en français pour mardi. Lundi, garde l’appel de your_optimization_procedure commenté tant que le gradient est en préparation.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le gradient suggère où déplacer le matériau, puis la projection remet la quantité et les limites de couverture aux valeurs autorisées.

**Vérification et résultat à transmettre.** Une méthode expliquée à la main et un exemple de projection, sans code supplémentaire lundi.

**Fichier commun.** Joachim complète le coût, puis Yann lance le premier calcul. Antoine transmet la méthode expliquée à la main.
