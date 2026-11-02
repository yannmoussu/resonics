# Antoine — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser les premiers calculs pour une optimisation sur plusieurs fréquences et quelques quantités de matériau. Les ajouts servent uniquement aux comparaisons nécessaires.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** responsable.

**Ce qui est fait.** Réutiliser la descente pour le coût de bande.

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

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Conserve intégralement les deux blocs marqués « Do not modify this cell, these are the values that you will be assessed against. », leurs lignes, commentaires et espaces en début de ligne. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Les modifications du lancement se font seulement dans les blocs « Fell free to modify the function call in this cell. », et les ajouts de fonctions se placent à côté des fonctions étudiantes. Les calculs supplémentaires se font après les blocs protégés, sans modifier leurs tableaux par effet de bord.

Garde la projection et la recherche du pas déjà vérifiées. À l’endroit où coût et gradient sont évalués, utilise maintenant la somme préparée par Joachim. Ajoute seulement les arguments de fréquence nécessaires et indique à Yann comment les passer. Vérifie les bornes, la quantité et le coût final recalculé. La densité reste commune à toutes les fréquences.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** La descente existante optimise le coût total sans deuxième algorithme.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Ce qui est fait.** Adapter la contrainte lorsque la quantité physique doit être conservée.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Avec les longueurs représentées par les points ou segments du mur, écris la contrainte sum(w*chi)=L_abs. Explique pourquoi V_obj seul ne garantit pas une quantité identique entre profils. Pour une projection avec le produit scalaire habituel, utilise clip(z-lambda*w,0,1) et trouve lambda par dichotomie. Vérifie la quantité et les bornes. Cette extension est introduite maintenant parce que la comparaison physique entre profils en a besoin ; elle n’était pas un prérequis du premier calcul.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une projection vérifiée pour les quantités physiques comparées par Yann.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
