# Yann — Mardi 3 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** contributeur.

**Contribution de Yann.** On intègre les fonctions communes et on calcule la courbe de référence du mur plan entièrement recouvert.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Calcule d’abord la référence du mur plan entièrement recouvert sur la plage de roulement proposée de 250 à 2 000 Hz après validation de ses paramètres. Les pics recherchés sont les pics de réponse du modèle ; ils ne constituent pas un spectre mesuré du RER B. Les cas complémentaires de traction ou de crissement sont identifiés séparément et utilisent leurs propres bandes validées.

Dans les records déjà prévus, ajoute dans metadata application='RER B', noise_regime, frequency_band_hz, band_provenance, source_model et source_spectrum_provenance. Garde le même format de records et distingue les régimes pour les comparaisons.

Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Ajoute les paramètres et le pilote run_frequency_campaign dans les parties autorisées. Appelle la campagne depuis la dernière cellule modifiable, après le bloc qui calcule u et copie chi0 et u0. Refuse une campagne physique si la loi complexe ou ses paramètres manquent. Conserve la source supérieure et les dimensions annoncées. Convertis les fréquences en k=2*pi*f/c et vérifie h<=c/(10*f_max), les coordonnées réelles et la résolution des reliefs. Pour chaque cas de campagne, utilise prepare_geometry_of_domain, compute_material_response et get_design_faces de preprocessing ; ce dernier retourne boundary_indices, face_rows, face_design et design_weights. Prépare des variables locales case_domain, case_f, case_f_dir, case_f_neu, case_f_rob, case_chi et case_alpha_rob, ainsi que des copies indépendantes des coefficients unitaires. Appelle les factories fournies pour initialiser ces tableaux de campagne sans modifier leur définition. Les valeurs u, chi0 et u0 du chemin initial conservent leurs noms et leurs copies ; les comparaisons RER B utilisent les champs mémorisés localement par la campagne.
Prépare pour Joachim assemble(chi) renvoyant A,b,cell_weights,face_rows,face_design,dA_diag. chi est le vecteur de densités aux boundary_indices. Réinjecte-le dans une grille nulle hors conception et forme alpha_rob=Alpha_code*chi. Appelle processing.assemble_helmholtz_system : A est complète de taille M*N, b est aplati et cell_weights vaut h*h à l'intérieur, zéro ailleurs. Les indices face_rows sont globaux aplatis, face_design indexe chi et les répétitions sont conservées. Pour coefficients unitaires et f_rob nul, dA_diag=h*Alpha_code/(1-h*Alpha_code*chi[face_design])**2, carré complexe. Vérifie ces hypothèses.
Calcule les réponses du profil plan entièrement recouvert sur la bande validée. Prépare des records avec case_id,frequency_hz,energy,level,state,material_length_m,spacestep_m,relative_residual,metadata. state='full' pour cette référence. L'énergie utilise h*h*sum(abs(u)**2) à l'intérieur. Donne aussi la quantité totale du mur entièrement recouvert.
Transmets la courbe à Olympia, reprends ses intervalles de maxima candidats et recalcule davantage de fréquences autour des pics. Vérifie les résidus et les coûts positifs. N'annonce pas un maximum continu à partir d'une seule grille fréquentielle.
```

**Contrôle et transmission.** Publier une courbe calculée et ses paramètres pour Olympia. Les données physiques manquantes sont signalées avant tout gain annoncé.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** contributeur.

**Contribution de Yann.** On calcule les références entièrement recouvertes pour les autres profils fournis, avec les mêmes conventions que le mur plan.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Compare au plan les profils fournis entièrement recouverts pour le même régime de bruit RER B, avec mêmes source, bande et dimensions de référence annoncées. Chaque profil reste fixe pendant le parcours de sa bande. Affiche les longueurs et quantités de matériau de chaque mur.

Dans les records déjà prévus, ajoute dans metadata application='RER B', noise_regime, frequency_band_hz, band_provenance, source_model et source_spectrum_provenance. Garde le même format de records et distingue les régimes pour les comparaisons.

Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Réutilise la chaîne intégrée pour les profils de niveaux 1 et 2 entièrement recouverts. Les niveaux changent la forme ; le pas doit résoudre la plus petite irrégularité et au moins dix points par longueur d'onde. Conserve la source et les dimensions de référence, puis annonce l'aire et la longueur du mur effectivement obtenues.
À chaque géométrie, recalcule les masques, les contacts et les poids de longueur. Le matériau est celui validé par Mathis à chaque fréquence. Calcule les courbes sur la même bande que le plan, avec state='full' et la quantité réellement utilisée. Appelle les tracés d'Olympia et affine les fréquences autour de ses nouveaux pics candidats. Ne considère pas le recouvrement intégral comme une borne minimale assurée de l'énergie.
Conserve les données brutes, les paramètres et les résidus, puis transmets les nouvelles courbes à Olympia.
```

**Contrôle et transmission.** Vérifier les dimensions physiques, la provenance du coefficient et la quantité totale de chaque référence avant la comparaison.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** contributeur.

**Contribution de Yann.** On compare les distributions initiales à quantité limitée aux références entièrement recouvertes.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Pour le même scénario RER B, compare les états initial et entièrement recouvert en indiquant leurs quantités physiques, leur bande et leur source. Le calcul doit montrer les écarts réels et ne doit pas imposer le gain ou la division de matière annoncés comme perspective dans SOTA.md.

Dans les records déjà prévus, ajoute dans metadata application='RER B', noise_regime, frequency_band_hz, band_provenance, source_model et source_spectrum_provenance. Garde le même format de records et distingue les régimes pour les comparaisons.

Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Pour chaque profil déjà calculé, prépare une densité initiale admissible sur le mur de conception. Le budget material_length_m est une longueur absolue commune entre formes ; vérifie qu'il est inférieur à la longueur totale de tous les murs. Projette l'initialisation du support avec project_density d'Antoine et les poids get_design_faces.
Recalcule les réponses sur la même bande, avec mêmes source, dimensions et matériau que les références. Utilise state='initial' et vérifie dot(design_weights,chi)=material_length_m, ainsi que les bornes. Conserve séparément les quantités des références state='full', généralement supérieures.
Transmets à Olympia les courbes et la répartition initiale. Les différences de courbe ne sont pas automatiquement attribuables à la seule quantité, puisque la répartition et la géométrie sont annoncées ensemble.
```

**Contrôle et transmission.** Antoine approuve la faisabilité des densités initiales et Olympia reçoit des références comparables avec leurs quantités.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Contribution de Yann.** On lance la première descente acoustique aux pics retenus et on calcule les champs optimisés.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis les fréquences problématiques parmi les pics confirmés de la réponse du panneau sur la bande RER B retenue, d’abord le roulement. Identifie le régime de bruit et la fréquence de chaque descente. Recalcule ensuite la réponse sur la bande pour vérifier qu’une baisse à ce pic ne dégrade pas excessivement les autres fréquences.

Dans les records déjà prévus, ajoute dans metadata application='RER B', noise_regime, frequency_band_hz, band_provenance, source_model et source_spectrum_provenance. Garde le même format de records et distingue les régimes pour les comparaisons.

Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Prends les versions validées par Joachim puis Antoine. evaluate_density(chi,assemble,with_gradient=True) renvoie value,gradient,u aplati,state_residual,adjoint_residual. L'optimiseur d'Antoine a la signature your_optimization_procedure(chi0,evaluate,design_weights,material_length_m,mu=1.0,max_iter=100,feasibility_tol=1e-10,gradient_tol=1e-6,armijo=1e-4,reduction=0.5,increase=1.1,min_step=1e-12,max_backtracks=40) et retourne un dictionnaire.
Avant toute descente, vérifie avec Joachim une différence centrée du coût sur l'assembleur acoustique réel, à petite dimension et densité intérieure aux bornes. Le test synthétique seul ne vérifie pas ce raccordement. Choisis ensuite une ou plusieurs fréquences problématiques parmi les pics confirmés avec Olympia.
Appelle l'optimiseur en conservant géométrie et budget pendant chaque descente. Recalcule le coût et le champ final, les résidus et le budget. Conserve uniquement les itérations acceptées dans l'historique. Transmets à Olympia les records state='mono', les champs remis en forme sur grille et les historiques, avec les mêmes échelles avant/après. Les zéros de bord du solveur ne sont pas des traces physiques.
Un arrêt sur limite de pas ou d'itérations est annoncé avec son motif réel. Donne les appels de contrôle et le résultat réellement exécuté, sans annoncer d'optimum global.
```

**Contrôle et transmission.** Yann et Joachim approuvent le gradient réel avant le lancement. Antoine relit l'arrêt et Olympia prépare les cartes et courbes.

**Passage de main du programme principal :** Joachim → Antoine → Yann. Les résultats sont ensuite transmis à Olympia et aux autres responsables pour validation.
