# Antoine — Lundi 2 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** responsable.

**Contribution d’Antoine.** On formule les variables de conception, le critère à minimiser et la contrainte de quantité de matériau.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Formule le problème d’optimisation ResoniCS à partir du critère défini par Joachim. La densité chi est réelle, vaut entre zéro et un aux nœuds Robin de conception et reste nulle hors du mur modifiable. À géométrie fixée, le coût est l’intégrale intérieure de pression au carré obtenue après résolution de Helmholtz.

Le poids d’une variable est la longueur discrète fournie par Yann, égale au pas multiplié par le nombre de contacts avec un intérieur. Imposer dot(design_weights,chi)=material_length_m conserve une longueur absorbante absolue. Les Robin d’ouverture sont exclues de la conception. À épaisseur et profondeur constantes, le volume est proportionnel à cette longueur. Précise les conditions de faisabilité et l’ensemble admissible. La comparaison des formes utilise des optimisations séparées et n’impose pas l’aire unité de l’ancien devoir.

Explique le cas entièrement recouvert comme référence demandée par l’énoncé, avec sa quantité propre, et non comme une borne minimale assurée. Présente les données à fixer avant la descente : source, matériau, fréquence, géométrie, budget et éventuelle normalisation du coût.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On fait valider le problème à quantité fixée avec Joachim, Mathis et Yann avant de programmer la projection.

## to choose porous material(s) and its quantity ;

**Repère :** J1.7. **Rôle :** contributeur.

**Contribution d’Antoine.** On exprime le budget physique choisi par Mathis avec les longueurs représentées par le maillage.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Le matériau, l’épaisseur, la profondeur et la quantité proposés par Mathis, puis les poids du mur calculés par Yann
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Vérifie la quantité proposée par Mathis pour le mur. Donne le lien entre longueur absorbante pondérée, épaisseur, profondeur et volume de poreux. Vérifie les unités et la faisabilité du budget sur tous les profils retenus. Une même fraction du nombre de nœuds Robin ne conserve pas forcément la même quantité physique entre des contours de longueurs différentes.

Prépare les valeurs et les hypothèses de quantité à transmettre au groupe. Si un paramètre manque, identifie-le. Ne choisis pas de quantité physique arbitraire pour rendre un test faisable. Les budgets synthétiques de contrôle seront séparés des budgets réels.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On remet à Mathis et Yann la règle de mesure du budget, puis on utilise cette même règle dans la projection.

## formulate/consider the numerical gradient descent method.

**Repère :** J1.10. **Rôle :** responsable.

**Contribution d’Antoine.** On formule la descente projetée et on programme la projection qui conserve le budget de matériau.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Complète uniquement demo_control_polycopie2024.py en ajoutant project_density(z, design_weights, material_length_m, tol=1e-10, max_iter=100) et une fonction check_projection() non appelée automatiquement. Ne crée aucun fichier et préserve les fonctions de Joachim ainsi que les cellules imposées.

z est un vecteur réel de densités d'essai. design_weights contient des longueurs positives de même taille, fournies par Yann : le pas de grille multiplié par le nombre de faces intérieures de chaque nœud de conception. material_length_m est la longueur absorbante absolue imposée. On cherche la projection euclidienne sur 0<=chi<=1 avec dot(design_weights,chi)=material_length_m.

Utilise chi=clip(z-lambda*design_weights,0,1). Le gradient de coût sera euclidien, donc un décalage uniforme ne convient pas quand les poids diffèrent. Trouve lambda par dichotomie entre min((z-1)/w) et max(z/w). Si la quantité calculée est trop grande, augmente lambda. Traite directement les budgets nul et maximal. Vérifie les bornes et l'erreur de budget avant de renvoyer le vecteur, et signale l'échec de la dichotomie si la tolérance n'est pas atteinte.

Vérifie les dimensions, les valeurs réelles finies, les poids strictement positifs et un budget compris entre zéro et sum(w). Préserve les entrées. Dans check_projection(), teste les budgets extrêmes, les poids différents, l'idempotence et le cas w=(1,1), L=1, z=(0.8,0.6), dont la projection vaut (0.6,0.4). Les tests restent dans ce même fichier.

Après le code, explique le futur algorithme de gradient projeté : évaluation du coût et du gradient, essai projeté, recalcul du coût, réduction du pas si la baisse est insuffisante. Le comptage de nœuds V_obj du démo sera remplacé par le budget physique lors de l'intégration de Yann. Les nœuds d'ouverture ne font pas partie de la conception.

Renvoie le fichier complet avec de courts commentaires français sans équations, puis les contrôles réellement exécutés ou leurs appels si tu ne peux pas les exécuter. Ne modifie pas encore your_optimization_procedure.
```

**Contrôle et passage de main.** Après la version de Joachim, on lance check_projection() puis on transmet le fichier complet à Yann. On présente le schéma de descente au point collectif avant son activation mardi.
