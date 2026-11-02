# Yann — Mardi 3 novembre

**But du jour.** Relier les contributions dans le programme fourni, calculer les références entièrement absorbantes et lancer la première optimisation à une fréquence problématique.

**Passage de main.** Attendre les versions de `demo_control_polycopie2024.py` validées successivement par Joachim puis Antoine. Utiliser les versions de `preprocessing.py` publiées par Mathis et de `postprocessing.py` publiées par Olympia. Une seule personne modifie la démonstration à la fois.

## Tâche 1 — Intégrer les fonctions et calculer les premières références

**Fichier à modifier :** [support/demo_control_polycopie2024.py](../../support/demo_control_polycopie2024.py).

**Ce qui est fait.** On transforme la démonstration en point d'entrée du projet. On garde ses cellules imposées et on ajoute les appels de calcul dans les zones modifiables. Les modèles physiques, la résolution, le coût et les figures restent dans les fichiers où ils ont été complétés.

**Fichiers à joindre avec le prompt :**

- `support/demo_control_polycopie2024.py`, version actuelle après Joachim et Antoine, à modifier.
- `support/preprocessing.py`, `support/processing.py`, `support/postprocessing.py`, `support/_env.py`, versions actuelles en lecture seule.
- `context/Sujet-EI-EXT-2026.md`.
- Les valeurs validées lundi pour la source, la largeur, les bandes, le matériau, l'épaisseur, la profondeur et le budget, copiées dans le message. Si elles manquent, demander ces valeurs avant une campagne physique.

**Prompt à copier :**

```text
Intègre les contributions ResoniCS uniquement dans demo_control_polycopie2024.py joint et renvoie le fichier complet. Ne crée aucun module. Les autres fichiers joints sont les versions courantes à appeler sans les modifier. Conserve les cellules marquées Do not modify et les fonctions écrites par Joachim et Antoine.

1. Regroupe les paramètres physiques validés dans la zone modifiable et vérifie leur présence. La source est celle de Dirichlet en haut, identique dans toutes les comparaisons. Les côtés restent réfléchissants. Une fréquence publique est en Hz, la pulsation vaut 2*pi*f et k=2*pi*f/c. Le paramètre omega du solveur reçoit k. Emploie les dimensions réelles du générateur, avec le pas et les subdivisions annoncés par Yann. Vérifie h<=c/(10*f_max) et la représentation des petits reliefs. Ne choisis pas de nombres physiques arbitraires pour compléter des données manquantes.
2. Appelle compute_material_response de preprocessing pour la loi complexe documentée. Son alpha_code remplace le coefficient de démonstration. Utilise un seul budget absolu de longueur absorbante material_length_m entre profils, avec épaisseur et profondeur fixées. Obtiens les indices et les poids par get_design_faces. Vérifie la faisabilité du budget sur tous les profils.
3. Prépare pour Joachim un callback assemble(chi). chi est le vecteur réel aux indices boundary_indices, dans [0,1]. Réinjecte-le dans une grille nulle hors conception puis forme alpha_rob=Alpha_code*chi sur le mur. Appelle processing.assemble_helmholtz_system. Retourne un dictionnaire A, b, cell_weights, face_rows, face_design, dA_diag. A est complète M*N et b aplati. cell_weights vaut h*h à l'intérieur et zéro ailleurs. face_rows est en indices globaux aplatis, face_design indexe chi. Pour les coefficients unitaires et f_rob nul, dA_diag vaut h*Alpha_code/(1-h*Alpha_code*chi[face_design])**2, par contact. Les contacts répétés sont conservés. Vérifie ces hypothèses, sinon arrête le calcul avec une explication.
4. Branche evaluate_density de Joachim et l'optimiseur d'Antoine sans recopier leur contenu. La nouvelle signature d'Antoine commence par chi0, evaluate, design_weights, material_length_m, puis des paramètres optionnels mu, max_iter, feasibility_tol, gradient_tol, armijo, reduction, increase, min_step, max_backtracks. Elle retourne un dictionnaire contenant notamment chi, value, gradient, u, history, stop_reason et converged. Convertis le vecteur u en grille pour les tracés. Avant la première descente, compare le gradient à une différence centrée du coût avec cet assembleur acoustique réel, en présence de Joachim, sur une petite grille et une densité intérieure aux bornes. Le coût et le budget sont recalculés sur le résultat final.
5. Calcule d'abord l'énergie sur la bande validée pour les profils niveaux 0, 1 et 2 entièrement recouverts. Les fonctions de postprocessing repèrent les maxima locaux et proposent les intervalles à raffiner ; recalcule effectivement les fréquences supplémentaires avant de conclure sur un pic. Compare ensuite la répartition initiale à budget limité et celle optimisée à un pic. Le mur entièrement recouvert peut utiliser plus de matériau que le budget limité, donc affiche ses quantités.
6. Prépare pour Olympia une liste records de dictionnaires avec case_id, frequency_hz, energy, level, state ('full','initial','mono','multi'), material_length_m, spacestep_m, relative_residual et metadata. Les valeurs sont calculées et non recopiées des anciennes études. Les champs et historiques sont transmis séparément selon les signatures actuellement présentes dans postprocessing.py. Les cartes utilisent des échelles communes ; masque le complémentaire et précise que le solveur ne renvoie pas les traces physiques au bord.
7. Prévois une exécution courte de contrôle, puis une campagne explicite avec les paramètres validés. N'exécute pas toute la campagne lors d'un import. Vérifie le coût positif, les résidus, la contrainte et la décroissance des itérations acceptées. Les cas synthétiques de vérification restent distingués des résultats physiques. Explique les appels et les paramètres en français dans les commentaires, avec de simples phrases.
```

**Résultat attendu.** Une exécution depuis `support/` calcule réellement des champs différents avant et après optimisation. Olympia reçoit les courbes brutes, les intervalles de pics à préciser, les quantités et les historiques acceptés. Le groupe présente les premiers résultats avant sa validation quotidienne.

**Si une dépendance manque.** Tester la branche d'intégration sur un petit cas explicitement synthétique et indiquer la donnée manquante. Les figures de performance du produit attendent le modèle de matériau validé.
