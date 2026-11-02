# Antoine — Lundi 2 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** responsable.

**Contribution d’Antoine.** On formule les variables de conception, le critère à minimiser et la contrainte de quantité de matériau.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Formule le coût du scénario RER B avec une quantité physique de poreux fixée. La source unitaire en haut donne d’abord une réponse fréquentielle de référence. Si aucun spectre mesuré n’est disponible, annonce des poids d’intégration de fréquence normalisés. Si un spectre mesuré est fourni, sa provenance et sa normalisation sont fixées avant la descente et la réponse à source unitaire est pondérée sans compter deux fois l’amplitude du bruit.

La projection porte sur la longueur physique absorbante des cartouches du panneau RER B. Le pourcentage indicatif de SOTA.md ne remplace pas le budget pondéré commun entre profils.

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

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Le matériau, l’épaisseur, la profondeur et la quantité proposés par Mathis, puis les poids du mur calculés par Yann
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le concept envisagé dans SOTA.md associe un panneau rigide et des cartouches poreuses amovibles. Examine la laine de roche et la fibre de chanvre seulement si leurs données complexes sont disponibles, puis fixe épaisseur, profondeur et quantité avec provenance. Une fraction illustrative telle que 40 % n’est pas un budget absolu commun entre des murs de longueurs différentes. Les contraintes d’entretien et d’encombrement sont des critères de choix à documenter.

La projection porte sur la longueur physique absorbante des cartouches du panneau RER B. Le pourcentage indicatif de SOTA.md ne remplace pas le budget pondéré commun entre profils.

Vérifie la quantité proposée par Mathis pour le mur. Donne le lien entre longueur absorbante pondérée, épaisseur, profondeur et volume de poreux. Vérifie les unités et la faisabilité du budget sur tous les profils retenus. Une même fraction du nombre de nœuds Robin ne conserve pas forcément la même quantité physique entre des contours de longueurs différentes.

Prépare les valeurs et les hypothèses de quantité à transmettre au groupe. Si un paramètre manque, identifie-le. Ne choisis pas de quantité physique arbitraire pour rendre un test faisable. Les budgets synthétiques de contrôle seront séparés des budgets réels.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On remet à Mathis et Yann la règle de mesure du budget, puis on utilise cette même règle dans la projection.

## formulate/consider the numerical gradient descent method.

**Repère :** J1.10. **Rôle :** responsable.

**Contribution d’Antoine.** On formule la descente projetée et on programme la projection qui conserve le budget de matériau.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

La descente améliore une densité sur le panneau RER B à budget absolu fixé. Les coefficients du matériau, la source, le profil et les poids fréquentiels restent constants pendant une descente. Préserve les petits contrôles algorithmiques et distingue-les des futures performances acoustiques.

La projection porte sur la longueur physique absorbante des cartouches du panneau RER B. Le pourcentage indicatif de SOTA.md ne remplace pas le budget pondéré commun entre profils.

Complète uniquement demo_control_polycopie2024.py en ajoutant project_density(z, design_weights, material_length_m, tol=1e-10, max_iter=100) et une fonction check_projection() non appelée automatiquement. Ne crée aucun fichier et préserve les fonctions de Joachim ainsi que les cellules imposées.

z est un vecteur réel de densités d'essai. design_weights contient des longueurs positives de même taille, fournies par Yann : le pas de grille multiplié par le nombre de faces intérieures de chaque nœud de conception. material_length_m est la longueur absorbante absolue imposée. On cherche la projection euclidienne sur 0<=chi<=1 avec dot(design_weights,chi)=material_length_m.

Utilise chi=clip(z-lambda*design_weights,0,1). Le gradient de coût sera euclidien, donc un décalage uniforme ne convient pas quand les poids diffèrent. Trouve lambda par dichotomie entre min((z-1)/w) et max(z/w). Si la quantité calculée est trop grande, augmente lambda. Traite directement les budgets nul et maximal. Vérifie les bornes et l'erreur de budget avant de renvoyer le vecteur, et signale l'échec de la dichotomie si la tolérance n'est pas atteinte.

Vérifie les dimensions, les valeurs réelles finies, les poids strictement positifs et un budget compris entre zéro et sum(w). Préserve les entrées. Dans check_projection(), teste les budgets extrêmes, les poids différents, l'idempotence et le cas w=(1,1), L=1, z=(0.8,0.6), dont la projection vaut (0.6,0.4). Les tests restent dans ce même fichier.

Après le code, explique le futur algorithme de gradient projeté : évaluation du coût et du gradient, essai projeté, recalcul du coût, réduction du pas si la baisse est insuffisante. Le comptage de nœuds V_obj du démo sera remplacé par le budget physique lors de l'intégration de Yann. Les nœuds d'ouverture ne font pas partie de la conception.

Renvoie le fichier complet avec de courts commentaires français sans équations, puis les contrôles réellement exécutés ou leurs appels si tu ne peux pas les exécuter. Ne modifie pas encore your_optimization_procedure.
```

**Contrôle et passage de main.** Après la version de Joachim, on lance check_projection() puis on transmet le fichier complet à Yann. On présente le schéma de descente au point collectif avant son activation mardi.
