# Joachim — Vendredi, 6 novembre 2026

Objectif : expliquer le critère, le gradient et le rôle des conditions de bord pendant la soutenance.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Réception du code et préparation de l'intervention

**Fichier concerné :** `support/demo_control_polycopie2024.py`, en lecture pour les fonctions de Joachim. On ne crée pas de document ou de programme supplémentaire dans cette tâche.

**Ce qu'on fait.** On refait les petits contrôles, puis on prépare une explication orale courte et des réponses aux questions sur les mathématiques. Le groupe garde vingt minutes de présentation, puis dix minutes de questions, avec une intervention de chacun.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, version finale partagée
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Sujet-EI-EXT-2026.md` et `context/Dirichlet_Nonhomogene.pdf`
- Les figures et valeurs retenues par le groupe, sous leur forme actuelle


**Prompt à copier :**

```text
À partir du fichier final demo_control_polycopie2024.py et des résultats fournis, prépare une explication orale des fonctions your_compute_objective_function, evaluate_density et evaluate_band. Ne modifie aucun fichier et ne crée aucun nouveau fichier.

Explique pour chaque fonction les entrées, les étapes et les sorties. Présente le critère de pression, le système direct et l'adjoint, puis montre pourquoi le gradient coûte deux résolutions par fréquence au lieu d'une résolution par variable de conception. Donne un exemple simple de module au carré pour un nombre complexe et un exemple de perturbation pour vérifier une dérivée.

Rappelle la nécessité du champ total avec la source Dirichlet non homogène et la comparaison entre réflexion et ouverture. Relie chaque conclusion aux résultats réellement fournis. Prépare des réponses courtes sur la conjugaison, le facteur deux, le contrôle par différences centrées et la distinction entre pression intégrée et puissance dissipée.

Liste les appels de contrôles déjà présents dans ce même fichier et les résultats à vérifier avant la soutenance. Ne dis pas qu'un calcul a réussi si ses sorties ne sont pas jointes. Donne la réponse directement dans le message pour qu'elle puisse être reprise par Yann dans les documents communs.
```

**Validation collective.** On confirme avec Yann que les équations, les chiffres, les figures et le code final emploient les mêmes conventions. Pendant la répétition, on mesure la durée totale de l'équipe et on ajuste son intervention.
