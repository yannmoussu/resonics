# Études numériques ResoniCS pour le bruit du RER B

Les fichiers de `support/` rassemblent le programme initial, le calcul du coefficient de matériau et les études des quatre journées. Les calculs emploient les différences finies et la même convention de Robin que le polycopié.

## Paramètres communs

On choisit les paramètres suivants au début de `demo_control_polycopie2024.py` :

- `SOURCE` vaut `preprocessing.source_constant` ou `preprocessing.source_rer_b`. Ces fonctions prennent la position sur le bord et la pulsation en arguments. La première renvoie une amplitude unitaire et la seconde une somme de gaussiennes représentant un spectre simplifié de RER B.
- `CAR_MAT` contient les caractéristiques du matériau dans le dictionnaire `compute_alpha.MATERIAUX`. Par défaut, il s'agit de `LAINE_ROCHE`.
- `ALPHA0` fixe le point de départ de la minimisation qui identifie le coefficient de Robin, dans la convention du polycopié.
- `C` est la célérité du son, fixée à `343 m/s`, et `OMEGA` est la pulsation du calcul à une fréquence.

Les études fréquentielles utilisent par défaut les fréquences de 50 à 3 500 Hz avec un pas de 50 Hz. On prend `N = 128`, `M = 2*N` et un pas spatial de `1/N m`. La longueur d'onde à 3 500 Hz contient ainsi environ 12,5 pas de grille. La finesse géométrique et la résolution des pics doivent également être vérifiées pour interpréter une étude donnée.

Pour chaque fréquence, on convertit les hertz en pulsation par `omega = 2*pi*frequency_hz`, puis en nombre d'onde par `k = omega/C`. `compute_alpha` reçoit la pulsation, alors que le solveur de Helmholtz reçoit le nombre d'onde. Le paramètre appelé `omega` dans plusieurs fonctions du support conserve son nom initial mais correspond au nombre d'onde dans leur système discret.

## Source et coefficient du matériau

`compute_alpha.compute_alpha(omega, SOURCE, CAR_MAT, ALPHA0)` renvoie les parties réelle et imaginaire du coefficient, le succès et le message de la minimisation. Les études arrêtent leur calcul si cette identification échoue ou si le coefficient obtenu est incompatible avec la convention attendue.

La condition de bord du polycopié s'écrit `d_n u + alpha*chi*u = 0`. On emploie directement le coefficient identifié, de partie réelle positive et de partie imaginaire négative. Pour une sortie ouverte du domaine rectangulaire, on prend `alpha = -i*k`. La densité `chi` représente la répartition du matériau sur les points de Robin.

Le dictionnaire actuel contient notamment la laine de roche, la mélamine et la laine de verre, définies par leur porosité, leur tortuosité et leur résistivité à l'air. Les comparaisons utilisent ces données. Le modèle d'identification actuel ne comporte pas de paramètre d'épaisseur de couche.

La source RER B est uniforme sur le bord d'entrée. Son amplitude spectrale est la somme de trois gaussiennes centrées sur 200, 800 et 2 500 Hz, de largeurs respectives 100, 350 et 150 Hz, avec les poids 1, 0,8 et 0,5. Ces valeurs décrivent une source simplifiée et doivent être annoncées comme des choix de modélisation.

## Contenu des fichiers

| Fichier | Rôle |
| --- | --- |
| `preprocessing.py`, `processing.py`, `postprocessing.py` | Construction du domaine, résolution du système discret et tracés du support |
| `compute_alpha.py` | Identification du coefficient de Robin à partir de la source et du matériau |
| `demo_control_polycopie2024.py` | Paramètres communs, coût, adjoint, gradient et descente projetée du programme initial |
| `fast_helmholtz.py` | Résolutions répétées sur les points intérieurs et optimisations à une ou plusieurs fréquences |
| `jour1_etude_theorique_et_materiaux.py` | Comparaison des coefficients des matériaux, frontières réfléchissante et ouverte, vérification du gradient par différences finies |
| `jour2_spectre_et_optimisation_mono.py` | Spectres, niveaux géométriques, détection des pics et optimisation à une fréquence |
| `jour3_multifrequence_et_volume.py` | Évaluation sur une bande, optimisation à plusieurs fréquences et variation de la fraction garnie |
| `jour4_analyse_performances_et_produit.py` | Comparaison continu/binaire, essai de deux matériaux, profils d'excitation et comparaison des candidats |
| `run_all_project.py` | Exécution successive des quatre journées |

## Exécution

Depuis la racine du projet, on peut lancer une seule journée :

```sh
python support/jour1_etude_theorique_et_materiaux.py
python support/jour2_spectre_et_optimisation_mono.py
python support/jour3_multifrequence_et_volume.py
python support/jour4_analyse_performances_et_produit.py
```

Pour tout recalculer :

```sh
python support/run_all_project.py
```

Cette dernière commande effectue de nombreuses résolutions et optimisations. Les fonctions d'étude acceptent une grille, des fréquences ou un nombre d'itérations réduits pour vérifier rapidement leur exécution. Une étude réduite sert à vérifier le programme et ne remplace pas les calculs nécessaires à la comparaison physique.

Chaque journée enregistre ses figures et données dans `support/resultats_jour1/` à `support/resultats_jour4/`. La quatrième journée est autonome et sélectionne ses fréquences cibles dans un spectre recalculé. Elle ne dépend pas des fichiers de résultats d'une ancienne exécution.

## Lecture des résultats

Le coût est l'intégrale discrète du module au carré du champ sur les points intérieurs. Sa comparaison renseigne sur la réponse du modèle à une excitation donnée. Les valeurs obtenues ne constituent pas une mesure acoustique étalonnée en décibels.

La descente recherche une densité continue entre zéro et un, sous une contrainte de fraction moyenne sur le bord. Après la sélection des points les plus garnis pour obtenir une densité binaire, on résout à nouveau le problème pour mesurer son coût. La répartition mixte du jour 4 est aussi évaluée séparément, car son amélioration éventuelle doit être observée dans les calculs.

Pour les profils uniforme, localisé et oblique du jour 4, on impose la même somme d'amplitudes au carré sur le bord d'entrée. Le profil localisé désigne ici une excitation imposée sur un point du bord. Le coefficient de matériau est conservé pour isoler l'effet du profil dans ce test.

La fraction de points garnis vaut généralement 30 %. Le nombre total de points de Robin dépend du niveau géométrique, donc une fraction identique peut employer davantage de matériau. Le tableau du jour 4 précise le nombre de points garnis et le nombre de points disponibles pour rendre cette différence visible.

Les anciennes valeurs de pics, de gains et de classement obtenues avec une autre source ou un autre modèle de matériau doivent être recalculées. Les figures, CSV et NPZ produits par les commandes précédentes permettront de choisir un candidat dans le cadre du modèle, sans présumer du matériau ou de la géométrie qui donnera le coût le plus faible.
