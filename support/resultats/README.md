# Comparaison des quatre matériaux au niveau 3

On utilise la source RER B, un maillage de 128 points en largeur et 256 en hauteur,
une bande de 50 à 3 500 Hz avec un pas de 5 Hz, soit 691 fréquences, et au plus
100 itérations de descente. Les quatre matériaux partent de la même portion
centrale garnie. Au niveau 3, elle occupe 410 des 1 024 points du contour.

Chaque coefficient de paroi est calculé à sa fréquence, avec la convention
positive du polycopié. L'amplitude de la source intervient déjà dans le champ
calculé. La moyenne sur la bande utilise les poids des trapèzes divisés par
la largeur de la bande.

## Résultats des murs binaires

Le tableau utilise la grille de contrôle au pas de 2,5 Hz, soit 1 381 fréquences.
Les fréquences intermédiaires sont recalculées, avec leurs coefficients de matériau.
Le gain est rapporté au mur initial du même matériau, sur cette même grille.

| Matériau | Itérations acceptées | Énergie J initiale moyenne | Énergie J binaire moyenne | Réduction |
|---|---:|---:|---:|---:|
| Mélamine | 100 | 4.22422 | 0.676602 | 83.98 % |
| Laine de roche | 100 | 4.86435 | 0.92415 | 81.00 % |
| Laine de verre | 100 | 4.45979 | 0.792228 | 82.24 % |
| Ouate polyester | 100 | 4.01792 | 0.47916 | 88.07 % |

| Matériau | Maximum de J sur la grille de contrôle | Fréquence du maximum | Écart de la moyenne binaire entre les pas 5 et 2,5 Hz |
|---|---:|---:|---:|
| Mélamine | 19.7769 | 732.5 Hz | +0.37 % |
| Laine de roche | 30.0833 | 735.0 Hz | -1.79 % |
| Laine de verre | 26.5845 | 735.0 Hz | -0.22 % |
| Ouate polyester | 17.0986 | 735.0 Hz | -0.12 % |

L'historique de descente concerne la densité continue utilisée pendant le calcul.
Les spectres finaux, les répartitions et les gains de ce tableau concernent
le mur binaire. Son énergie est recalculée séparément après la binarisation.

## Contrôles et interprétation

- Toutes les étapes acceptées diminuent le critère sur la grille fixe de la descente.
- Les densités restent entre zéro et un, et leur somme conserve la quantité imposée.
  Les quatre murs binaires contiennent exactement 410 points garnis.
- Le gradient a été vérifié par différences finies, avec une erreur relative
  d'environ 2,5e-9 sur un petit maillage et 2,6e-6 au niveau 3 avec 128 points en largeur.
- Les matrices du calcul préparé ont été comparées à celles de la version
  précédente du solveur. Leur différence maximale est nulle aux quatre niveaux.
- Le contrôle a révélé un pic initial à 397,5 Hz, entre les points de la grille de 5 Hz.
  Il faut donc comparer les résultats sur la grille de contrôle. Deux grilles
  ne suffisent pas à garantir la mesure exacte de toute résonance plus étroite.
- Le maillage donne environ 12,54 points par longueur d'onde à 3 500 Hz.
  Aucune étude de convergence spatiale n'a été réalisée pour cette comparaison.

Pour l'étude de quantité, on augmente la longueur d'une portion centrale garnie
avec cinq fractions par contour. La position reste fixée. Les contours des niveaux
0, 1, 2 et 3 mesurent respectivement 1, 2, 4 et 8 mètres dans cette discrétisation.
Une même fraction représente donc des longueurs garnies différentes entre niveaux.

## Fichiers

Les dossiers par matériau contiennent les paramètres, les coefficients de paroi,
les références aux quatre niveaux, l'étude de quantité, le résultat de descente,
les historiques et les spectres aux deux pas. Les NPZ conservent les tableaux
complets, tandis que les CSV donnent les valeurs des courbes.

Les PNG sont aussi copiés dans le dossier presentation. Les noms commencés par
validation utilisent les spectres au pas de contrôle de 2,5 Hz. L'optimisation
reste faite au pas de 5 Hz. Les JSON de vérification consignent les contrôles
et les paramètres réellement utilisés.

La figure `influence_geometrie_energie.png` compare les énergies moyennes des quatre matériaux en fonction du niveau de fractale. Elle utilise les murs entièrement garnis, sur la bande de 50 à 3 500 Hz au pas de 5 Hz.
