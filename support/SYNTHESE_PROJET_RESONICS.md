# Études numériques ResoniCS pour le RER B

On compare les formes de murs et les répartitions d'absorbant avec trois matériaux : **MELAMINE, LAINE_VERRE et OUATE_POLYESTER**. Aucun matériau n'est désigné comme produit final.

## Exécuter les calculs

Avec Python, NumPy, SciPy et Matplotlib installés, depuis la racine du projet :

```sh
python support/demo_control_polycopie2024.py
```

Les paramètres se règlent au début de ce fichier. `ETUDE` détermine les calculs :

| Valeur | Étude |
| --- | --- |
| `"demo"` | Exemple à une fréquence, avec la mélamine |
| `"materiaux_validation"` | Coefficients, énergies des sept matériaux disponibles, cas ouvert et contrôle du gradient |
| `"monofrequence"` | Spectres et placements à une fréquence, pour chacun des trois matériaux retenus |
| `"multifrequence"` | Placements communs à plusieurs fréquences et étude des quantités, pour les trois matériaux |
| `"comparaison_dispositifs"` | Neuf couples forme–matériau à quantité totale identique |
| `"tous"` | Toutes ces études, dans cet ordre |

Les figures, CSV et NPZ actuels sont enregistrés dans `support/resultats_comparaison_materiaux/`. Les études de placement sont séparées par matériau, puis par étude (`monofrequence`, `multifrequence`). `budget_identique/` contient les comparaisons à quantité totale imposée. La démonstration conserve ses figures dans `support/`.

Les figures originales `fig_energy_frequency_level0.jpg`, `fig_energy_frequency_level1.jpg` et `fig_energy_frequency_level2.jpg` d'Antoine sont conservées. Les nouveaux tracés reprennent cette comparaison avec des données numériques enregistrées et des panneaux séparés pour améliorer la lecture. Les anciens dossiers `resultats_monofrequence/`, `resultats_multifrequence/`, `resultats_materiaux_validation/` et `resultats_comparaison_dispositifs/` conservent les calculs antérieurs avec la laine de roche. Ils ne décrivent pas la comparaison actuelle des trois candidats.

## Paramètres

| Paramètre | Valeur et rôle |
| --- | --- |
| `SOURCE` | `preprocessing.source_rer_b`, remplaçable par `preprocessing.source_constant` |
| `CAR_MAT` | `MATERIAUX["MELAMINE"]` pour la démonstration et les contrôles illustratifs |
| `MATERIAUX_A_COMPARER` | `MELAMINE`, `LAINE_VERRE`, `OUATE_POLYESTER`, sans sélection finale |
| `ALPHA0` | `[50.0, -50.0]`, point initial de l'identification du coefficient |
| `C` | 343 m/s |
| `OMEGA` | 3 430 rad/s pour la démonstration et le contrôle du gradient |
| `N_POINTS` | 128, soit une grille de 256 × 128 points et un pas de 1/128 m |
| `FREQUENCES_HZ` | 50 à 3 500 Hz, par pas de 50 Hz, pour les optimisations et leur évaluation |
| `FREQUENCES_DETAILLEES_HZ` | 50 à 3 500 Hz, par pas de 10 Hz, pour les murs entièrement garnis |
| `N_ITERATIONS` | 80 itérations au maximum pour les études de placement |
| `FRACTION_GARNIE` | 0,30 sur une forme donnée |
| `QUANTITES` | 0,10 ; 0,30 ; 0,50 ; 0,70 ; 1,00 |

La démonstration conserve les étapes et les affichages imposés du support, avec 100 itérations au maximum et la quantité de sa répartition initiale. La mélamine y illustre le fonctionnement du programme. Les modes d'étude répètent les recherches pour les trois candidats.

## Source et convention de Robin

Les fonctions de source prennent `(y, omega)` en arguments. La source RER B est uniforme le long de l'entrée. Son amplitude est une somme de trois gaussiennes en fréquence, centrées sur 200, 800 et 2 500 Hz, d'écarts-types 100, 350 et 150 Hz et de poids 1, 0,8 et 0,5. Il s'agit d'un spectre simplifié.

`compute_alpha` reçoit la pulsation en radians par seconde. Le solveur reçoit le nombre d'onde, obtenu en divisant cette pulsation par la célérité. Le paramètre nommé `omega` dans les fonctions initiales du solveur désigne ce nombre d'onde.

On utilise partout la convention du polycopié : dérivée normale plus coefficient de Robin multiplié par la densité et le champ. Le coefficient identifié a une partie réelle positive et une partie imaginaire négative. On l'applique directement par `alpha_rob = Alpha*chi`. La sortie ouverte utilise `Alpha = -1j*k`.

## Lecture des résultats

**Énergie J** désigne l'intégrale discrète du module au carré de la pression dans l'air. Les unités sont celles du modèle et ne constituent pas une mesure étalonnée en joules ou en décibels. L'amplitude de la source est déjà incluse dans le champ.

La descente optimise une densité comprise entre zéro et un, avec une quantité fixée. On projette chaque proposition pour respecter cette contrainte, puis on la conserve si son énergie diminue. Le tri final donne une répartition binaire, dont on recalcule l'énergie. Cette dernière peut être supérieure à celle de la densité continue.

L'optimisation multifréquence minimise la moyenne de trois fréquences cibles. On évalue ensuite le placement sur toute la bande. La moyenne sur la bande est calculée par la méthode des trapèzes divisée par la largeur de bande. Les pics sont ceux de la grille fréquentielle utilisée.

Une même fraction garnie ne représente pas la même quantité totale sur des murs de longueurs différentes. La comparaison supplémentaire impose donc 38 points garnis pour chaque forme et chaque matériau. Cette quantité nodale est une approximation de la longueur garnie.

À 3 500 Hz, le maillage compte environ 12,5 pas par longueur d'onde. Les très petits reliefs et les portions garnies demandent aussi un contrôle de résolution. Les comparaisons concernent les cas effectivement calculés et servent à discuter les compromis, sans désigner de produit gagnant.

## Organisation du code

- `demo_control_polycopie2024.py` contient les réglages, les fonctions étudiantes imposées et l'enchaînement des études.
- `preprocessing.py` définit le domaine, les sources et les répartitions, puis effectue la projection et la sélection binaire.
- `processing.py` assemble et résout les systèmes, calcule le gradient et réalise les études comparatives.
- `postprocessing.py` produit les figures et enregistre les tableaux.
- `compute_alpha.py` contient les caractéristiques des matériaux et l'identification du coefficient complexe.

Le [rapport](../report/report.pdf) et la [présentation](../presentation/presentation.pdf) suivent les consignes de l'énoncé dans leur ordre. Les fonctions associées sont indiquées au fil de l'analyse.
