# ResoniCS — Un mur antibruit pour le RER B

Ce projet étudie le choix du matériau, la forme d'un mur antibruit et le placement de portions absorbantes sur sa paroi. Le champ acoustique est calculé par différences finies, puis une descente de gradient permet de répartir une quantité fixée de matériau pour diminuer l'énergie J.

## Contenu des dossiers

- **[report/](report/)** contient le [rapport PDF](report/report.pdf), son fichier [LaTeX](report/report.tex) et les images utilisées dans `figures/`. Le dossier `data/` conserve des données complémentaires et des vérifications. Le script `prepare_complements.py` retrace la figure du coefficient de paroi de l'ouate à partir de ces données.
- **[support/](support/)** contient les programmes Python et les résultats numériques disponibles.

| Fichier dans `support/` | Rôle |
|---|---|
| `demo_control_polycopie2024.py` | Paramètres des études, calcul de l'énergie, descentes de gradient et lancement des comparaisons |
| `compute_alpha.py` | Caractéristiques des matériaux et calcul du coefficient complexe de paroi à chaque fréquence |
| `preprocessing.py` | Construction des géométries, répartition initiale du matériau et sources acoustiques |
| `processing.py` | Assemblage et résolution des systèmes de Helmholtz |
| `postprocessing.py` | Tracé des figures et enregistrement des bilans dans des fichiers CSV |
| `_env.py` | Identification des points intérieurs, extérieurs et des différents types de bord |

## Lire et compiler le rapport

Le fichier **[report/report.pdf](report/report.pdf)** peut être consulté directement.

Pour compiler les sources, avec une installation LaTeX comprenant `latexmk`, lancer :

```sh
cd report
latexmk -pdf report.tex
```

Le PDF est produit dans ce même dossier. Avec `pdflatex`, lancer deux fois `pdflatex report.tex` pour actualiser la table des matières et les références.

La compilation nécessite `report.tex` et le dossier `figures/`. **Le dossier `data/` et le script `prepare_complements.py` sont facultatifs pour compiler le rapport.**

## Exécuter les programmes Python

Les programmes utilisent **Python 3, NumPy, SciPy et Matplotlib**. Si ces bibliothèques ne sont pas déjà installées dans l'environnement Python utilisé :

```sh
python3 -m pip install numpy scipy matplotlib
```

Depuis la racine du projet, c'est-à-dire le dossier contenant `report/` et `support/`, lancer :

```sh
python3 support/demo_control_polycopie2024.py
```

Ce lancement calcule les références, les études de quantité et les optimisations sélectionnées, puis génère les figures. L'ensemble des calculs peut être long. Pour limiter une étude, modifier les matériaux, les modes ou le nombre d'itérations au début du programme principal.

### Paramètres du programme principal

| Paramètre | Valeur actuelle et signification |
|---|---|
| `N_POINTS` | 128 points en largeur, avec une grille de 256 points en hauteur |
| `LEVELS` | Niveaux 0, 1, 2 et 3 pour les comparaisons de géométrie |
| `LEVEL` | Niveau 3 pour les descentes de gradient |
| `MATERIALS` | `MELAMINE`, `LAINE_ROCHE`, `LAINE_VERRE`, `OUATE_POLYESTER` |
| `FREQUENCIES` | Fréquences de 50 à 2 000 Hz inclus, par pas de 5 Hz |
| `N_ITERATIONS` | Au plus 100 étapes acceptées par descente |
| `SOURCE` | Source RER B, somme de trois gaussiennes centrées à 200, 800 et 2 500 Hz |
| `C` | Célérité du son de 343 m/s |
| `RESULTS` | Dossier de sortie des nouveaux calculs |

Pour utiliser une source constante à la place de la source RER B, remplacer le réglage de `SOURCE` par :

```python
SOURCE = preprocessing.source_constant
```

`G_SOURCE`, réglé sur `compute_alpha.g1`, désigne le profil uniforme utilisé pour identifier le coefficient du matériau. `SOURCE` désigne l'excitation utilisée dans les calculs du champ acoustique.

### Études disponibles

Le paramètre `MODES` sélectionne les descentes à exécuter :

| Mode | Fréquences utilisées pour l'optimisation |
|---|---|
| `mono` | Fréquence du plus grand maximum d'énergie repéré pour le mur entièrement garni |
| `resonances` | Ensemble des maxima locaux d'énergie détectés sur ce spectre |
| `bande50` | Bande de 50 à 2 000 Hz, par pas de 50 Hz |
| `bande5` | Bande de 50 à 2 000 Hz, par pas de 5 Hz |

Le nom `resonances` correspond ici aux pics d'énergie repérés sur les courbes. La répartition finale est binaire et son énergie est recalculée après le passage aux portions garnies ou réfléchissantes.

## Résultats enregistrés

Les nouveaux calculs sont écrits dans **`support/resultats_antoine/`**, avec un sous-dossier par matériau. Ils conservent les paramètres dans `parametres.json`, les tableaux dans des fichiers `.npz`, les figures et les bilans CSV. Les spectres sont aussi contrôlés aux fréquences intermédiaires, soit un pas de 2,5 Hz avec la grille actuelle.

Les résultats et les étapes de descente déjà enregistrés sont réutilisés lorsque les paramètres correspondent. Après une modification des réglages ou des fichiers de calcul, choisir un nouveau dossier avec `RESULTS` pour conserver séparément les études. Les figures générées sont également copiées dans `presentation/`, créé si nécessaire.

### Résultats fournis et figures du rapport

Le rapport reprend les figures présentées à la soutenance, notamment les comparaisons sur la bande de 1 à 2 000 Hz et l'étude des quantités après optimisation. La configuration retenue est un mur de niveau deux, garni d'ouate de polyester sur 20 % de son contour.

Le programme actuel utilise la bande de 50 à 2 000 Hz. Son étude de quantité, définie par `VOLUMES`, agrandit une portion continue garnie à position fixée. Elle est distincte de l'étude du rapport, où le placement a été optimisé pour chaque quantité. Les descentes actuelles sont réalisées au niveau indiqué par `LEVEL`.

Le dossier **`support/resultats/`** conserve une étude antérieure sur la bande de 50 à 3 500 Hz. Ses paramètres et résultats sont décrits dans son [README](support/resultats/README.md).

Pour lire les bilans, distinguer l'énergie intégrée utilisée dans les figures du rapport et l'énergie moyenne calculée par le programme actuel. Cette moyenne est l'intégrale sur la bande divisée par la largeur de cette bande.
