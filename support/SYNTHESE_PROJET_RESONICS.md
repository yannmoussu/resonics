# Études numériques ResoniCS pour le bruit du RER B

Le programme utilise les différences finies pour comparer le matériau, la forme du mur et la répartition de l'absorbant. Les études sont réparties dans les quatre fichiers du support selon leur rôle.

## Lancer une étude

Depuis la racine du projet, on lance toujours la même commande :

```sh
python support/demo_control_polycopie2024.py
```

On choisit au début de ce fichier la valeur de `ETUDE` :

| Valeur | Calculs réalisés |
| --- | --- |
| `"demo"` | Champ initial, descente du support et courbe fréquentielle de référence |
| `"materiaux_validation"` | Coefficients des matériaux, comparaison des parois et vérification du gradient |
| `"monofrequence"` | Spectres des murs, niveaux géométriques et optimisations à une fréquence |
| `"multifrequence"` | Évaluation sur la bande, optimisation à plusieurs fréquences et quantité garnie |
| `"comparaison_dispositifs"` | Répartitions continue, binaire et mixte, profils incidents et comparaison des candidats |
| `"tous"` | Exécution successive de toutes les études |

Les figures et les données sont enregistrées dans les dossiers thématiques suivants, sous `support/` :

- `resultats_materiaux_validation/` pour les matériaux et les vérifications
- `resultats_monofrequence/`, avec `data_monofrequence.npz`, pour les spectres et les placements à une fréquence
- `resultats_multifrequence/`, avec `data_multifrequence.npz`, pour les placements communs à plusieurs fréquences et l'étude de la quantité
- `resultats_comparaison_dispositifs/`, avec `data_comparaison_dispositifs.npz`, pour les configurations candidates

La démonstration conserve ses figures dans `support/`. Chaque étude recalcule ses résultats à partir des paramètres choisis.

## Paramètres communs

Les choix sont regroupés en tête de `demo_control_polycopie2024.py`, puis transmis aux fonctions de calcul et de tracé :

| Paramètre | Valeur initiale et rôle |
| --- | --- |
| `SOURCE` | `preprocessing.source_rer_b`, ou `preprocessing.source_constant` pour une amplitude unitaire |
| `CAR_MAT` | `MATERIAUX["LAINE_ROCHE"]`, pour le matériau du cas principal |
| `ALPHA0` | `[50.0, -50.0]`, pour le point de départ de l'identification du coefficient |
| `C` | `343.0` m/s, pour la célérité du son |
| `OMEGA` | `3430.0` rad/s, pour la pulsation du cas à une fréquence et de la vérification du gradient |
| `N_POINTS` | `128`, pour la largeur de grille, avec `M = 2*N_POINTS` et un pas de `1/N_POINTS` m |
| `FREQUENCES_HZ` | De 50 à 3 500 Hz par pas de 50 Hz |
| `N_ITERATIONS` | `80`, pour le maximum d'itérations des optimisations de placement |
| `FRACTION_GARNIE` | `0.30`, pour la fraction moyenne de points garnis dans les études de placement |
| `QUANTITES` | `[0.10, 0.30, 0.50, 0.70, 1.0]`, pour les fractions testées dans l'étude multifréquence |
| `MATERIAUX_A_COMPARER` | `LAINE_ROCHE`, `MELAMINE` et `LAINE_VERRE`, pour la validation des matériaux et la comparaison des dispositifs |

La démonstration conserve la descente imposée du support, limitée à 100 itérations, et la quantité de sa répartition initiale. Les paramètres `N_ITERATIONS` et `FRACTION_GARNIE` règlent les études de placement.

À 3 500 Hz, la grille par défaut comporte environ 12,5 pas par longueur d'onde. Une grille réduite et quelques fréquences permettent de vérifier rapidement l'exécution. L'interprétation physique demande ensuite de vérifier la résolution des ondes, des reliefs et des pics fréquentiels.

## Répartition du code

| Fichier | Rôle |
| --- | --- |
| `demo_control_polycopie2024.py` | Choix des paramètres, fonctions étudiantes imposées et enchaînement des calculs et des tracés |
| `preprocessing.py` | Domaine, sources, répartition initiale, projection de la densité et sélection d'une répartition binaire |
| `processing.py` | Assemblage, résolutions, adjoint, gradient, optimisations et calculs des études |
| `postprocessing.py` | Figures et enregistrement des tableaux CSV et NPZ |
| `compute_alpha.py` | Dictionnaire `MATERIAUX` et identification du coefficient complexe à partir de la source et du matériau |

`compute_state`, `compute_adjoint` et `compute_gradient` sont définies dans `processing.py`. `project_density` et `binarize_chi` sont définies dans `preprocessing.py`. Le programme principal importe les fonctions nécessaires à la descente du support. Les fonctions d'étude renvoient leurs résultats, puis les fonctions de `postprocessing.py` les tracent et les enregistrent.

Pour retrouver les calculs et leurs tracés :

- `study_spectra_and_single_frequency_placement` transmet ses résultats à `plot_spectra_and_single_frequency_placement`
- `study_multifrequency_placement_and_coverage` transmet ses résultats à `plot_multifrequency_placement_and_coverage`
- `compare_absorber_configurations` transmet ses résultats à `plot_absorber_configuration_comparison`

## Source et convention du matériau

Les deux sources proposées prennent `(y, omega)` en arguments, où `y` est la position le long du bord d'entrée et `omega` la pulsation. Elles sont uniformes sur ce bord. La source RER B est la somme de trois gaussiennes centrées sur 200, 800 et 2 500 Hz, de largeurs 100, 350 et 150 Hz et de poids 1, 0,8 et 0,5. Ce spectre simplifié est un choix de modélisation.

Pour chaque fréquence, on convertit les hertz en pulsation par `omega = 2*pi*frequency_hz`, puis en nombre d'onde par `k = omega/C`. `compute_alpha` reçoit la pulsation, alors que le solveur de Helmholtz reçoit le nombre d'onde. Le paramètre appelé `omega` dans plusieurs fonctions initiales du support conserve son nom mais désigne ce nombre d'onde.

La condition du polycopié est `d_n u + alpha*chi*u = 0`, avec une partie réelle positive et une partie imaginaire négative pour le matériau dissipatif. `compute_alpha(omega, SOURCE, CAR_MAT, ALPHA0)` fournit directement ce coefficient, puis on forme `alpha_rob = Alpha*chi`. Le calcul s'arrête si l'identification échoue. Pour la sortie ouverte, on prend `alpha = -i*k`, ce qui donne la condition de Sommerfeld.

Les matériaux sont définis par leur porosité, leur tortuosité et leur résistivité à l'air dans `MATERIAUX`. Le modèle actuel d'identification ne contient pas de paramètre d'épaisseur de couche. Le coefficient est fixé pendant une optimisation à une fréquence et recalculé pour chaque fréquence d'une étude spectrale.

## Lecture des résultats

Le coût est l'intégrale discrète du module au carré du champ sur les points intérieurs. Il permet de comparer les réponses du modèle à une excitation donnée. Les valeurs obtenues ne sont pas des mesures étalonnées en décibels. Le champ contient déjà l'amplitude de la source, donc on ne multiplie pas de nouveau son coût par le carré de cette amplitude.

La descente recherche une densité entre zéro et un à fraction moyenne fixée. Après la sélection des points les plus garnis pour former une répartition binaire, on résout à nouveau le problème et on mesure son coût. Le coût binaire peut être plus élevé que celui de la répartition continue. La répartition mixte est également évaluée séparément dans la comparaison des dispositifs.

Pour les profils uniforme, localisé et oblique de la comparaison des dispositifs, on impose la même somme d'amplitudes au carré sur le bord d'entrée. Le profil localisé correspond à une excitation sur un point du bord. On conserve le coefficient du matériau pour examiner l'effet du profil.

Une même fraction de points garnis peut employer davantage de matériau lorsque le niveau géométrique augmente. Le tableau de comparaison des dispositifs donne donc les nombres de points garnis et disponibles. Les comparaisons restent celles du modèle calculé et ne présument pas du matériau ou de la forme donnant le coût minimal.
