# Bilan des calculs avec le support fourni

## Paramètres réellement utilisés

- N=128, grille de 128 × 256 points, pas spatial 0.00781250 m, mur préfractal de niveau 2 et vitesse du son de 343 m/s.
- Ouate polyester pour les optimisations, sans choix définitif de matériau pour le produit.
- Source uniforme sur l’entrée, somme de gaussiennes (centre en Hz, largeur en Hz, amplitude) : (200, 100, 1), (800, 350, 0,8), (2500, 150, 0,5).
- Quantité conservée : 204 points sur 512, soit 39.8438 % du mur.
- Budget de dix itérations par procédure. Les recherches sur les pics et sur la bande prolongent la densité continue obtenue aux trois centres. Elles ont donc bénéficié de cette première descente.
- Le signe plus de Robin est utilisé dans le système et son adjoint. Le coefficient du matériau est identifié à chaque fréquence et l’amplitude de la source est incluse une seule fois dans le champ.

## Performances des murs binaires

| Configuration | Intégrale de J sur la bande | Réduction / initial | Maximum de J | Fréquence du maximum (Hz) |
| --- | ---: | ---: | ---: | ---: |
| Mur initial | 14478.9 | 0.000 % | 7493.1 | 403.613281 |
| Entièrement garni | 1494.71 | 89.677 % | 22.8921 | 192.578125 |
| Une fréquence | 6325.94 | 56.309 % | 365.486 | 965.136719 |
| Trois centres | 1930.79 | 86.665 % | 12.5302 | 168.359375 |
| Tous les pics repérés | 1377.82 | 90.484 % | 8.86112 | 183.593750 |
| Bande entière | 1558.12 | 89.239 % | 17.6548 | 451.562500 |

Dans cet essai, le mode aux pics repérés donne le plus faible critère intégré après binarisation. Le mode de bande améliore la somme intégrée par rapport aux trois centres, mais il ne domine pas le mode aux pics. Le mode de bande conserve notamment un pic de 17,65 vers 451,56 Hz, supérieur au maximum du mode aux trois centres (12,53), alors que son énergie intégrée est plus faible de 19,3 %. La baisse de l’intégrale ne suffit donc pas à garantir la baisse de chaque pic.

Les mêmes fréquences, la même source, le même maillage et le même matériau sont employés pour toutes ces courbes. La référence entièrement garnie comporte 512 points revêtus, contre 204 pour les autres murs.

## Descente et binarisation

| Mode | Fréquences cibles | Étapes acceptées | Critère au départ | Critère continu final | Critère binaire final |
| --- | ---: | ---: | ---: | ---: | ---: |
| Une fréquence | 1 | 10 | 7493.1038 | 0.2158261 | 3.0855071 |
| Trois centres | 3 | 10 | 13.401007 | 2.9950163 | 3.7029912 |
| Tous les pics repérés | 107 | 10 | 46.647398 | 27.402249 | 39.629937 |
| Bande entière | 813 | 10 | 0.4478801 | 0.32758586 | 0.44786684 |

Ces critères diffèrent : énergie à la cible, somme aux trois centres, somme aux pics et moyenne de bande pondérée par les trapèzes. Le point après binarisation peut remonter par rapport à la dernière densité continue. Les spectres de performance emploient uniquement le mur binaire.

## Vérifications fréquentielles

- Optimisation de bande : 813 fréquences, avec des intervalles de 1.5625 à 12.5 Hz.
- Évaluation commune : 7145 fréquences entre 50 et 3500 Hz, avec des intervalles de 0.0048828125 à 5 Hz.
- Dernier indicateur relatif d’intégrale : 0.0037960593. Variation relative du maximum : 0.
- Seuils : 1 % et 5 %. Contrôle convergé : True.
- Écart relatif entre la moyenne binaire sur la grille d’optimisation et celle sur la grille de validation : 0.8329 %.
- Ce contrôle porte sur les raffinements effectivement évalués. Il ne garantit pas mathématiquement l’absence d’un pic plus étroit entre deux points.

## Autres comparaisons et limites

- Mélamine, laine de verre et ouate polyester sont comparées sur les murs entièrement garnis de niveaux 0, 1 et 2, avec un pas de 10 Hz. La longueur du mur et la quantité de matériau changent avec le niveau.
- Les cinq quantités sont optimisées et comparées uniquement aux trois centres de la source. Cette étude ne détermine pas la meilleure quantité pour l’intégrale sur toute la bande.
- Le gradient adjoint est contrôlé par différences finies, y compris pour les sommes pondérées. Les résultats sont dans les fichiers de vérification.
- Le maillage représente la plus courte longueur d’onde par 12,54 points, au-dessus du minimum demandé. Une étude de convergence spatiale n’a pas été réalisée. Les plus petites portions binaires peuvent occuper un seul point du mur, ce qui doit être distingué d’un dimensionnement validé de panneaux physiques.
- Les dix itérations constituent un budget de calcul. Elles ne prouvent ni la stationnarité de la densité finale ni un minimum global.
- Les comparaisons des critères incluent des initialisations différentes et des budgets cumulés différents.

## Reproduire les calculs

Dans `demo_control_polycopie2024.py`, les figures enregistrées correspondent à `N_POINTS = 128`, `N_ITERATIONS = 10`, `ETUDE = "complet"` et aux autres paramètres annoncés ci-dessus. Le programme utilise les systèmes complets du support. La validation enregistrée a réparti les mêmes résolutions indépendantes entre quatre processus, sans modifier les matrices ni les énergies.

Les fichiers CSV, JSON et NPZ conservent les valeurs numériques et les grilles réelles. Les anciennes données archivées ne sont pas utilisées pour ces nouvelles figures.
