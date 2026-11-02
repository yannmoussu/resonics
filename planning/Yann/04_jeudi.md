# Yann — Jeudi 5 novembre 2026

**Objectif du jour.** On vérifie le résultat retenu et on choisit le panneau à présenter.

**Cas de départ.** Bruit de roulement du RER B. Premier essai proposé à 500 Hz avec c=343 m/s. Les comparaisons utilisent une pression imposée unitaire avec la même phase sur le bord supérieur. La plage 250–2 000 Hz de SOTA.md reste indicative. Avec la grille actuelle, on commence sur 250–1 500 Hz avant d’élargir si nécessaire.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier simplement le résultat qui guidera le choix du produit.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », avec leurs lignes, commentaires et indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les essais supplémentaires utilisent leurs propres tableaux après les blocs protégés. Conserve les signatures et les retours du support.

1. Recalcule le meilleur cas et sa référence sur une grille un peu plus fine en conservant la forme et les dimensions visées.
2. Compare les courbes, les quantités et la position des principaux pics. Utilise quelques fréquences supplémentaires près des pics si nécessaire.
3. Explique les écarts à Olympia. Si le temps le permet, refais une seule recherche avec une autre répartition initiale pour voir si le choix reste semblable.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** La comparaison sert à vérifier que le gain observé ne vient pas principalement d’une grille trop grossière. Une deuxième répartition de départ peut montrer la dépendance à l’essai initial.

**Résultat à transmettre.** Une comparaison courte qui confirme le choix ou indique son incertitude.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Ce qui est fait.** Proposer une forme de panneau à partir des calculs effectués.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Rassemble la forme, les dimensions, la quantité et les courbes du cas retenu.
2. Explique au groupe pourquoi ce cas paraît préférable dans la bande étudiée. Donne les deux ou trois valeurs qui soutiennent le choix.
3. Annonce la source unitaire utilisée et les hypothèses encore non mesurées pour le RER B.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le panneau retenu répond au scénario calculé. La conclusion repose sur les courbes comparatives et la quantité de matériau nécessaires pour obtenir ce résultat.

**Résultat à transmettre.** Une proposition de panneau compréhensible et appuyée sur les résultats.
