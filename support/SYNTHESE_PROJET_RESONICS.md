# Exécuter les études ResoniCS

On utilise les matrices et les conditions aux limites du support fourni. Le système conserve tous les points de la grille. Les matrices qui restent fixes sont préparées une fois, puis les conditions de Dirichlet et de Robin sont appliquées à chaque fréquence et à chaque placement.

On utilise Python 3 avec NumPy, SciPy et Matplotlib. Depuis la racine du projet :

```sh
python support/demo_control_polycopie2024.py
```

Les réglages sont au début du programme : `SOURCE`, `MATERIAL_NAME`, `N_POINTS`, `LEVEL`, `N_ITERATIONS` et `ETUDE`. Les trois matériaux conservés pour les comparaisons sont `MELAMINE`, `LAINE_VERRE` et `OUATE_POLYESTER`. L'ouate polyester est un exemple de calcul, sans choix de produit final.

## Les quatre modes

| Valeur de `ETUDE` | Critère |
| --- | --- |
| `mono` | Une fréquence critique repérée sur le spectre initial |
| `trois_pics` | Somme des énergies à 200, 800 et 2 500 Hz |
| `pics_resonance` | Somme des énergies à tous les maxima locaux repérés sur le spectre initial |
| `bande` | Moyenne de l'énergie sur la bande, approchée par les trapèzes |
| `complet` | Les quatre modes, les matériaux, les quantités et les contrôles |

Les pics repérés sont des maxima de la réponse à la source, pas le résultat d'un calcul de valeurs propres.

La recherche sur tous les pics et celle sur la bande peuvent partir du placement continu déjà obtenu aux trois centres. Les résultats indiquent cette succession. Les critères restent distincts et le gain ne mesure donc pas le seul effet du critère à budget identique.

## Algorithmes et code

- `your_optimization_procedure` conserve les lignes et affichages imposés pour une fréquence.
- `your_multifrequency_optimization` contient l'unique descente pour plusieurs fréquences. Les trois autres fonctions choisissent les cibles et les poids.
- `your_compute_objective_function` contient l'unique calcul de l'énergie.
- `project_density` et `binarize_chi`, dans `preprocessing.py`, sont partagées par toutes les descentes. La projection bornée, la dichotomie et le tri final suivent la section 7.6 du polycopié, pages imprimées 116–117.
- L'assemblage, l'état, l'adjoint et le gradient sont dans `processing.py`. Il n'y a aucune classe de résolution.
- Les figures et les exports sont dans `postprocessing.py`.

La source prend la position et la pulsation en arguments. Elle est évaluée à chaque fréquence, de même que le coefficient du matériau. Son amplitude est déjà incluse dans le champ et n'est pas appliquée une deuxième fois à l'énergie.

On conserve la convention avec le signe plus devant le coefficient de Robin. Le gradient est calculé à partir de l'adjoint du système complet et ses contributions sont additionnées aux coins du mur.

## Fréquences et vérification

La grille de départ couvre 50 à 3 500 Hz avec un pas de 25 Hz. Pour la descente de bande, les poids des trapèzes sont divisés par la largeur de la bande. On minimise ainsi l'énergie moyenne, qui a les mêmes minimiseurs que l'intégrale. Les indicateurs finaux donnent aussi cette intégrale sans normalisation. Des points sont ajoutés dans les intervalles où les trapèzes ou les maxima varient encore. La grille est fixée pendant chaque descente, donc la répartition courante et la proposition sont toujours comparées avec les mêmes fréquences et les mêmes poids.

Le pas fréquentiel et le pas de descente sont indépendants. Les seuils de contrôle sont 1 % pour l'indicateur d'intégrale et 5 % pour la variation du maximum entre grilles testées. Ce sont des contrôles numériques observés, sans garantie mathématique sur une résonance qui n'aurait pas été échantillonnée.

À N=128, la grille comporte environ 12,54 points par longueur d'onde à 3 500 Hz. Les petits essais servent à vérifier les calculs du programme, pas à valider la physique à haute fréquence.

## Résultats

Les nouvelles sorties se trouvent dans un sous-dossier de `support/resultats_antoine/` dont le nom précise le matériau, le maillage, l’étude et le nombre d’itérations. Cela évite de remplacer les sorties d’une autre étude. Les résultats retenus pour la présentation sont conservés directement dans `support/resultats_antoine/`. Chaque mode conserve son historique continu et son énergie après binarisation séparément. Les courbes de performance comparent uniquement des murs binaires. Le mode complet ajoute les comparaisons de matériaux et de formes, ainsi qu'une étude de quantité sur les trois centres de la source.

Les anciennes données brutes sont regroupées dans `support/archives_numeriques/`. Les figures des anciennes études retirées ne servent plus à la nouvelle présentation. Le rapport n'est pas réécrit pendant ce nettoyage ; ses anciennes références de figures devront être adaptées lors de sa reprise.
