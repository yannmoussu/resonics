# Yann — Jeudi 5 novembre 2026

**Objectif du jour 4.** Vérifier les meilleurs résultats et choisir un produit. On limite les nouveaux essais à ceux qui peuvent changer la conclusion.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Ce qui est fait.** Faire quelques vérifications décisives sur les meilleurs cas.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Conserve intégralement les deux blocs marqués « Do not modify this cell, these are the values that you will be assessed against. », leurs lignes, commentaires et espaces en début de ligne. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Les modifications du lancement se font seulement dans les blocs « Fell free to modify the function call in this cell. », et les ajouts de fonctions se placent à côté des fonctions étudiantes. Les calculs supplémentaires se font après les blocs protégés, sans modifier leurs tableaux par effet de bord.

Recalcule les meilleurs cas avec un pas plus petit, le même niveau géométrique et les mêmes dimensions de référence. Annonce les dimensions discrètes réellement obtenues et les éventuels arrondis du contour. Vérifie les fréquences entre les points d’optimisation. Reprends deux ou trois répartitions de départ si le temps le permet. Réutilise les boucles existantes et conserve les paramètres permettant de refaire le calcul.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le classement des meilleurs cas est vérifié sans multiplier inutilement les essais.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Ce qui est fait.** Contribuer au choix du panneau avec les calculs reproductibles et les dimensions du panneau.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

À partir des résultats fournis, propose une conclusion courte sur les calculs reproductibles et les dimensions du panneau. Le choix concerne un panneau pour le scénario RER B et la bande réellement calculés. Cite les valeurs décisives, les quantités et les formes comparées. Distingue les résultats obtenus des perspectives de SOTA.md. Fais valider la conclusion par le groupe sans inventer de performance manquante.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une décision appuyée sur une figure et quelques valeurs vérifiables.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
