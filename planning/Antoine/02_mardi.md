# Antoine — Mardi 3 novembre 2026

**Objectif du jour 2.** Calculer les références demandées, repérer quelques pics et faire une première descente après vérification du gradient. On complète les fonctions prévues dans le support, avec des tableaux simples de fréquences et d’énergies.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** contributeur.

**Ce qui est fait.** Préparer une répartition initiale qui respecte la quantité choisie.

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

Vérifie les bornes de chi et la valeur de V_obj sur les points Robin. Conserve la même quantité pendant la descente d’une forme donnée. Annonce séparément la quantité du mur entièrement recouvert. Donne à Yann les valeurs initiales et les paramètres ; aucun nouveau programme de lancement n’est nécessaire.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une répartition initiale et une quantité clairement annoncées.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** responsable.

**Ce qui est fait.** Compléter la descente dans la fonction prévue par le professeur.

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

Complète your_optimization_procedure avec sa liste d’arguments et son retour chi,energy,u,grad. Utilise le calcul de coût et gradient reçu de Joachim. Pour une forme fixe et la fraction nodale du support, projette les valeurs Robin sur 0<=chi<=1 et sum(chi)=V_obj*S, avec S le nombre de points Robin : un décalage scalaire choisi par dichotomie suivi d’un clip suffit. Les autres points restent à zéro. Essaie chi-step*grad, projette, recalcule le coût et réduis le pas si la diminution est insuffisante. Un essai refusé ne remplace jamais la dernière répartition acceptée. Arrête selon le gradient projeté, un nombre maximal d’itérations ou un pas trop petit, puis annonce la raison. Conserve seulement l’énergie initiale et celles des étapes acceptées. Vérifie d’abord la projection sur un exemple à deux valeurs, puis la diminution du coût. La mesure physique commune sera ajoutée quand les comparaisons entre formes l’exigeront.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** La descente fonctionne dans la fonction du support et respecte la quantité définie pour cette forme.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
