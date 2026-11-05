# Comparer les matériaux et les géométries

On utilise Python 3, NumPy, SciPy et Matplotlib. Depuis la racine du projet :

```sh
python support/demo_control_polycopie2024.py
```

Les paramètres sont au début de ce fichier. La comparaison demandée utilise les quatre matériaux `MELAMINE`, `LAINE_ROCHE`, `LAINE_VERRE` et `OUATE_POLYESTER`, la source RER B, une bande de 50 à 3 500 Hz avec un pas de 5 Hz et un maximum de 100 itérations de descente. Le maillage comporte 128 points sur sa largeur.

La descente compare les quatre matériaux au niveau de fractale 3, avec la même répartition initiale. Les géométries et les quantités sont également étudiées aux niveaux 0, 1 et 2. Les étapes acceptées diminuent le critère, et les contraintes de quantité sont conservées. Les spectres finaux sont recalculés avec le matériau présent ou absent à chaque point du mur.

Pour l’étude de quantité, on augmente la longueur d’une portion centrale garnie, avec cinq fractions de chaque contour. On mesure donc l’influence de cette quantité à position fixée. Les longueurs totales des contours diffèrent selon le niveau.

Après la descente, on recalcule les spectres initial et binaire aux fréquences intermédiaires. On obtient ainsi une grille de contrôle au pas de 2,5 Hz. Cette comparaison mesure ce qui change lorsque le pas est divisé par deux. Le contrôle a notamment repéré un pic initial à 397,5 Hz, entre deux points de la grille de descente.

Les données et les figures se trouvent dans `support/resultats/`. Les PNG sont aussi copiés directement dans `presentation/`. Les calculs déjà enregistrés sont réutilisés quand leurs paramètres sont identiques. Le programme peut ainsi reprendre un calcul interrompu à la fin d’une étude déjà enregistrée.

Le système conserve tous les points de la grille et les conditions aux limites du support. Les voisinages fixes sont préparés une fois. La même factorisation est utilisée pour le champ et son adjoint à une fréquence donnée. Les matrices ont été comparées à celles du support et le gradient a été contrôlé par différences finies.

Pour compiler les slides depuis la racine :

```sh
latexmk -cd -pdf presentation/presentation.tex
```
