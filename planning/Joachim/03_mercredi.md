# Joachim — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser les premiers calculs pour une optimisation sur plusieurs fréquences et quelques quantités de matériau. Les ajouts servent uniquement aux comparaisons nécessaires.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Ce qui est fait.** Étendre le coût et le gradient à plusieurs fréquences.

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

Pour une même chi, additionne les coûts des fréquences choisies avec des poids fixes, puis additionne leurs gradients avec les mêmes poids. Sans spectre mesuré, utilise des poids de la méthode des trapèzes normalisés pour que leur somme vaille un. Si des fréquences supplémentaires sont ajoutées, recalcule les poids avant une nouvelle descente. Ajoute la boucle dans la fonction de calcul déjà utilisée mardi, sans créer un système de fonctions reçues en argument. Vérifie la dérivée du coût total par différences centrées. Le champ représenté sur une figure est recalculé à une fréquence précise.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le même calcul de gradient fonctionne pour une fréquence ou une bande.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
