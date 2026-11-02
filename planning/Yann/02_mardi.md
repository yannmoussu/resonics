# Yann — Mardi 3 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** contributeur.

**Contribution de Yann.** On intègre les fonctions communes et on calcule la courbe de référence du mur plan entièrement recouvert.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Regroupe les paramètres validés lundi dans une zone modifiable. Refuse une campagne physique si la loi complexe ou ses paramètres manquent. Conserve la source supérieure et les dimensions annoncées. Convertis les fréquences en k=2*pi*f/c et vérifie h<=c/(10*f_max), les coordonnées réelles et la résolution des reliefs. Utilise compute_material_response de preprocessing et get_design_faces qui retourne boundary_indices, face_rows, face_design et design_weights.
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

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
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

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
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

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Prends les versions validées par Joachim puis Antoine. evaluate_density(chi,assemble,with_gradient=True) renvoie value,gradient,u aplati,state_residual,adjoint_residual. L'optimiseur d'Antoine a la signature your_optimization_procedure(chi0,evaluate,design_weights,material_length_m,mu=1.0,max_iter=100,feasibility_tol=1e-10,gradient_tol=1e-6,armijo=1e-4,reduction=0.5,increase=1.1,min_step=1e-12,max_backtracks=40) et retourne un dictionnaire.
Avant toute descente, vérifie avec Joachim une différence centrée du coût sur l'assembleur acoustique réel, à petite dimension et densité intérieure aux bornes. Le test synthétique seul ne vérifie pas ce raccordement. Choisis ensuite une ou plusieurs fréquences problématiques parmi les pics confirmés avec Olympia.
Appelle l'optimiseur en conservant géométrie et budget pendant chaque descente. Recalcule le coût et le champ final, les résidus et le budget. Conserve uniquement les itérations acceptées dans l'historique. Transmets à Olympia les records state='mono', les champs remis en forme sur grille et les historiques, avec les mêmes échelles avant/après. Les zéros de bord du solveur ne sont pas des traces physiques.
Un arrêt sur limite de pas ou d'itérations est annoncé avec son motif réel. Donne les appels de contrôle et le résultat réellement exécuté, sans annoncer d'optimum global.
```

**Contrôle et transmission.** Yann et Joachim approuvent le gradient réel avant le lancement. Antoine relit l'arrêt et Olympia prépare les cartes et courbes.

**Passage de main du programme principal :** Joachim → Antoine → Yann. Les résultats sont ensuite transmis à Olympia et aux autres responsables pour validation.
