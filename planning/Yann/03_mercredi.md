# Yann — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser les premiers calculs pour une optimisation sur plusieurs fréquences et quelques quantités de matériau. Les ajouts servent uniquement aux comparaisons nécessaires.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## Analyze the obtained results to compare to the efficient performances on the fixed range of frequencies ; to compare to a fully absorbing wall ;

**Repère :** J3.1. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier les répartitions optimisées sur toute la bande.

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

Réutilise la boucle de fréquences pour les répartitions initiales et optimisées. Ajoute des fréquences intermédiaires et des points près des pics ; garde la source et les paramètres du matériau. Transmets les tableaux et quantités à Olympia. Les cas traction et crissement restent des compléments après l’étude du roulement. La comparaison numérique ouverte/réfléchissante peut être ajoutée sur une copie du domaine si elle aide l’étude théorique.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Les gains et les dégradations entre les fréquences d’optimisation sont visibles.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Ce qui est fait.** Lancer la version à plusieurs fréquences avec la même répartition.

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

Utilise la fonction de coût sur plusieurs fréquences préparée par Joachim et la descente adaptée par Antoine. La même densité chi et la même forme servent à toutes les fréquences. Garde les poids fixés pendant une descente. Recalcule ensuite une courbe de vérification plus détaillée, puis le champ à une fréquence annoncée pour les figures.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une seule répartition optimisée pour la bande et sa courbe de vérification.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Ce qui est fait.** Calculer quelques quantités de matériau comparables.

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

Choisis avec Mathis et Antoine un petit nombre de quantités physiques réalisables. Lorsqu’on compare des profils de longueurs différentes, mesure la longueur absorbante représentée et adapte la contrainte pour conserver cette quantité, au lieu de réutiliser automatiquement le même pourcentage de points. Calcule les réponses avec les mêmes source et matériau. Transmets les longueurs ou volumes et les courbes à Olympia.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Quelques comparaisons à quantité physique annoncée, sans série exhaustive d’essais.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
