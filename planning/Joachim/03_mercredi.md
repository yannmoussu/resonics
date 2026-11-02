# Joachim — Mercredi, 4 novembre 2026

Objectif : utiliser une distribution unique de matériau pour plusieurs fréquences.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Coût multifréquence et somme des gradients

**Fichier à compléter :** `support/demo_control_polycopie2024.py`, uniquement une nouvelle fonction `evaluate_band` et ses contrôles.

**Ce qu'on fait.** On additionne des critères évalués pour la même densité, avec des poids fréquentiels fixés. La descente d'Antoine reçoit cette somme par le même mécanisme d'évaluation qu'à une fréquence. On garde les énergies brutes pour comparer les performances sur la bande.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, version complète de mardi validée
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Sujet-EI-EXT-2026.md`
- La liste des fréquences de conception, leurs poids et leurs énergies de référence validées, collée dans le message


**Prompt à copier :**

```text
Complète uniquement demo_control_polycopie2024.py en ajoutant evaluate_band(chi, frequencies_hz, frequency_weights, assemble_frequency, reference_energies=None, with_gradient=True) et un contrôle local non appelé automatiquement. Préserve evaluate_density, les fonctions d'Antoine et les cellules imposées. Ne crée pas de fichier.

assemble_frequency(chi, frequency_hz) est le callback de Yann. Il renvoie le dictionnaire déjà attendu par evaluate_density : A,b,cell_weights,face_rows,face_design,dA_diag. Pour chaque fréquence, passe à evaluate_density une fermeture assemble(chi) qui fige cette fréquence. La même densité chi est utilisée à chaque fréquence.

Les fréquences sont positives et finies. Les poids fréquentiels sont finis, positifs ou nuls, de somme un. Les références optionnelles sont strictement positives et fixées avant la descente ; à défaut, prends un vecteur de uns. Calcule F=sum(q_m*J_m/Jref_m) et son gradient avec exactement les mêmes facteurs. Garde les J_m bruts dans energies.

Renvoie value,gradient,energies,state_residuals,adjoint_residuals et u=None, car un coût de bande n'a pas un unique champ associé. Avec with_gradient=False, aucune résolution adjointe n'est faite. Toutes les données de fréquence et de normalisation restent constantes pendant une optimisation.

Construis un petit test synthétique à deux fréquences avec les assembleurs locaux déjà disponibles. Compare la somme des gradients à une différence centrée du coût total. Vérifie aussi qu'une seule fréquence de poids un redonne evaluate_density et que deux jeux de références non unitaires emploient les bons facteurs.

Explique dans la réponse que les fréquences supplémentaires ajoutées près d'un pic demandent de recalculer les poids d'intégration si l'on veut approximer une intégrale sur la bande. Une optimisation sur une liste de fréquences n'exclut pas une dégradation entre ces points, qui sera contrôlée séparément.

Renvoie le fichier complet et les résultats réellement exécutés, avec commentaires en phrases françaises sans notation mathématique.
```

**Vérification et transmission.** On transmet la version validée à Antoine. Yann branchera l'assemblage fréquentiel et Olympia comparera aussi les points de fréquence qui n'ont pas servi à la conception. Pour l'optimisation de bande, l'affichage du champ se fait après une réévaluation à une fréquence annoncée.
