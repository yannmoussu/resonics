# Joachim — Mardi 3 novembre 2026

**Objectif du jour 2.** Calculer les références demandées, repérer quelques pics et faire une première descente après vérification du gradient. On complète les fonctions prévues dans le support, avec des tableaux simples de fréquences et d’énergies.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Ce qui est fait.** Programmer et vérifier le calcul de l’adjoint et du gradient.

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

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Conserve intégralement les deux blocs marqués « Do not modify this cell, these are the values that you will be assessed against. », leurs lignes, commentaires et espaces en début de ligne. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Les modifications du lancement se font seulement dans les blocs « Fell free to modify the function call in this cell. », et les ajouts de fonctions se placent à côté des fonctions étudiantes. Les calculs supplémentaires se font après les blocs protégés, sans modifier leurs tableaux par effet de bord.

Ajoute seulement le calcul nécessaire à l’adjoint dans la démonstration, à côté des fonctions étudiantes. Réutilise les fonctions compute_stiffness_matrix, compute_mass_matrix et celles des conditions aux limites de processing.py sans modifier ce fichier. Construis le même système A U=b que le solveur fourni. Pour J=h**2*sum(abs(u)**2) à l’intérieur, l’adjoint discret peut s’écrire A.conj().T P=2*W*U avec W=h**2 aux points intérieurs et zéro ailleurs. Pour chaque voisinage intérieur/Robin, additionne à la dérivée correspondante -Re(conj(P[row])*dA_diag*U[row]) avec dA_diag=h*Alpha/(1-h*Alpha*chi_b)**2 pour les coefficients unitaires et f_rob nul. Vérifie ces hypothèses et le carré complexe. Les points peuvent être parcourus avec les quatre voisins du code existant, sans tableaux de correspondance supplémentaires. Compare le gradient à (J(chi+t*d)-J(chi-t*d))/(2*t) pour plusieurs petits t. Donne à Antoine une fonction simple renvoyant coût, champ et gradient. Conserve la signature de la fonction d’objectif fournie.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le gradient est validé sur un petit cas, puis sur le système acoustique réel avant la descente.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
