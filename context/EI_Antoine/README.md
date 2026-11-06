# Calculs à partir du programme d’Antoine

Ce dossier est la version de travail. On lance les calculs depuis ce dossier ou depuis la racine avec :

```sh
python context/EI_Antoine/demo_control_polycopie2024.py
```

NumPy, SciPy et Matplotlib sont nécessaires. Les paramètres sont au début du programme principal. On utilise quatre matériaux, les niveaux de fractale de zéro à trois et une bande de 50 à 2 000 Hz. La comparaison principale optimise les quatre matériaux au niveau trois, avec un pas fréquentiel de 5 Hz et au plus cent itérations. Le maillage comporte 128 points en largeur et 256 en hauteur. Il représente correctement le motif de niveau trois et donne environ vingt-deux points par longueur d’onde à 2 000 Hz.

Les études monofréquentielle, sur les pics détectés et sur la bande au pas de 50 Hz utilisent le même niveau trois. Les fréquences ciblées sont calculées pour chaque matériau, au lieu d’être écrites à l’avance. La bande au pas de 5 Hz constitue la comparaison principale. Toutes les répartitions finales sont binaires et leur énergie est recalculée après binarisation.

Le calcul du coefficient de paroi conserve la minimisation d’Antoine. Il utilise le profil uniforme du matériau, tandis que l’amplitude RER est imposée au champ à chaque fréquence. Le facteur d’amplitude multiplie le critère d’identification sans changer son minimiseur. La source conserve la somme des trois gaussiennes donnée dans le programme, mais les calculs portent sur la bande choisie de 50 à 2 000 Hz.

Les résultats et paramètres sont dans resultats, dans un dossier par matériau. Les PNG sont également copiés dans le dossier presentation du dépôt. Les calculs enregistrés sont réutilisés seulement si les paramètres et les fichiers de calcul correspondent. Une sauvegarde après chaque étape acceptée permet de reprendre une descente interrompue.

## Corrections apportées à la version reçue

- La condition de Robin utilise le signe positif demandé par la professeure. Les chargements non homogènes sont cohérents avec la normale sortante.
- Les contributions des différents voisins d’un même point du bord sont additionnées dans le gradient. La descente utilise un gradient de bord. Le contrôle par différences finies des composantes tient compte du pas spatial.
- La projection par écrêtage et dichotomie est celle de la méthode du cours utilisée par Antoine. La version bande conserve son réglage du pas de Barzilai–Borwein. La sigmoïde qui modifiait même une répartition sans déplacement a été remplacée par cette projection.
- Les modes mono et pics conservent l’augmentation du pas de 0,001. Le pas est réduit par deux lorsqu’une proposition augmente l’énergie. Seules les propositions acceptées comptent comme itérations.
- La définition d’énergie d’Antoine est conservée. Son solveur laisse les bords à zéro dans le tableau retourné, donc son masque incluant le bord donne la même énergie effective qu’une somme sur les points intérieurs.
- Les matrices fixes sont préparées à partir de ses fonctions d’assemblage. La même factorisation sert au champ et à son adjoint, sans classe de solveur supplémentaire.
- Les pics détectés, la source choisie et les paramètres de matériau sont utilisés réellement dans les calculs et les titres.

La quantité de matériau est étudiée en agrandissant la portion initialement garnie, à position fixée. Les contours des quatre niveaux mesurent un, deux, quatre et huit mètres dans cette discrétisation. Une même fraction garnie correspond donc à des longueurs différentes entre niveaux.

Un contrôle des champs binaires est fait sur une grille de fréquence au pas de 2,5 Hz. Ce contrôle compare deux grilles et ne constitue pas une garantie que toute résonance plus étroite est résolue. Les résultats numériques doivent être interprétés avec cette limite et avec la résolution spatiale retenue.
