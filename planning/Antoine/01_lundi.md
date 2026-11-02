# Antoine — Lundi, 2 novembre 2026

Objectif : conserver une quantité physique de matériau avec une projection simple.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Projection sous contrainte de quantité

**Fichier à compléter :** `support/demo_control_polycopie2024.py`, uniquement une nouvelle fonction `project_density` et ses contrôles.

**Ce qu'on fait.** On ramène une distribution d'essai entre zéro et un en conservant une longueur absorbante totale. La longueur est calculée avec les faces réellement voisines du fluide, ce qui permet de comparer des murs de longueurs différentes. On prépare ensuite le schéma de descente projetée pour le point du lundi.

**Avant de commencer.** Joachim transmet d'abord le fichier contenant son critère. On travaille sur cette version, puis on la renvoie à Yann pour l'intégration. Les ajouts restent dans le même fichier partagé.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, dernière version reçue de Joachim
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/GAllaire-OptimParam.pdf`, notamment les pages PDF 18 à 20 sur le gradient projeté
- `context/Sujet-EI-EXT-2026.md`


**Prompt à copier :**

```text
Complète uniquement demo_control_polycopie2024.py en ajoutant project_density(z, design_weights, material_length_m, tol=1e-10, max_iter=100) et une fonction check_projection() non appelée automatiquement. Ne crée aucun fichier et préserve les fonctions de Joachim ainsi que les cellules imposées.

z est un vecteur réel de densités d'essai. design_weights contient des longueurs positives de même taille, fournies par Yann : le pas de grille multiplié par le nombre de faces intérieures de chaque nœud de conception. material_length_m est la longueur absorbante absolue imposée. On cherche la projection euclidienne sur 0<=chi<=1 avec dot(design_weights,chi)=material_length_m.

Utilise chi=clip(z-lambda*design_weights,0,1). Le gradient de coût sera euclidien, donc un décalage uniforme ne convient pas quand les poids diffèrent. Trouve lambda par dichotomie entre min((z-1)/w) et max(z/w). Si la quantité calculée est trop grande, augmente lambda. Traite directement les budgets nul et maximal. Vérifie les bornes et l'erreur de budget avant de renvoyer le vecteur, et signale l'échec de la dichotomie si la tolérance n'est pas atteinte.

Vérifie les dimensions, les valeurs réelles finies, les poids strictement positifs et un budget compris entre zéro et sum(w). Préserve les entrées. Dans check_projection(), teste les budgets extrêmes, les poids différents, l'idempotence et le cas w=(1,1), L=1, z=(0.8,0.6), dont la projection vaut (0.6,0.4). Les tests restent dans ce même fichier.

Après le code, explique le futur algorithme de gradient projeté : évaluation du coût et du gradient, essai projeté, recalcul du coût, réduction du pas si la baisse est insuffisante. Le comptage de nœuds V_obj du démo sera remplacé par le budget physique lors de l'intégration de Yann. Les nœuds d'ouverture ne font pas partie de la conception.

Renvoie le fichier complet avec de courts commentaires français sans équations, puis les contrôles réellement exécutés ou leurs appels si tu ne peux pas les exécuter. Ne modifie pas encore your_optimization_procedure.
```

**Vérification et transmission.** On exécute `check_projection()` depuis `support`. On transmet la version complète à Yann, puis on présente au point collectif la conservation du budget et le schéma de descente qui sera activé après validation du gradient.
