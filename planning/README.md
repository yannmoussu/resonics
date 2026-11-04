# ResoniCS — Planning d’un MVP étudiant

Chaque contribution ajoute un petit résultat que les cinq membres peuvent expliquer. On reprend les fichiers de `support/`, puis on complète seulement ce qui manque pour la tâche du jour. Les 22 titres de l’[énoncé](../context/Sujet-EI-EXT-2026.md) et leur ordre sont conservés.

## Documents de suivi

Ces documents tiennent compte du code et des choix les plus récents. Les fiches individuelles conservent des propositions initiales, dont les paramètres doivent être remplacés par ceux ci-dessous :

- [Reste à faire pour le jour 1 — PDF](reste_a_faire_jour1.pdf)
- [Feuille de route du jour 2 — README](README_JOUR2.md)
- [Guide des études numériques réunies dans support](../support/SYNTHESE_PROJET_RESONICS.md)

Les études des quatre journées sont maintenant réunies dans `support/`. Elles utilisent les mêmes fonctions de source et les matériaux de `compute_alpha.MATERIAUX`. Le guide précise les commandes et les fichiers de résultats produits par chaque étude.

## Premier résultat lundi

Le groupe montre un domaine, une source, une carte du champ et une valeur d’énergie. Il explique les paramètres et les conditions aux limites. Les formules de dérivée et de descente demandées lundi sont établies sur papier, puis programmées mardi.

| Membre | Contribution du premier jour |
|---|---|
| Yann | Lancer un cas du programme fourni et expliquer où le son entre et où se trouve le matériau |
| Mathis | Réutiliser l’état de l’art, choisir la bande et calculer le coefficient d’un matériau documenté |
| Olympia | Décrire la géométrie et lire la première carte du champ |
| Joachim | Calculer l’énergie et expliquer les propriétés du modèle, la paroi ouverte et la dérivée |
| Antoine | Poser le problème à quantité fixée et expliquer une étape de descente avec un exemple |

Pour le fichier commun, Joachim complète le calcul d’énergie, puis Yann ajoute son affichage. Chaque personne repart de la dernière version transmise.

## Un cas simple pour commencer

- **Application :** bruit de roulement du RER B. La bande 250–2 000 Hz vient de [SOTA.md](../SOTA.md) et reste indicative.
- **Premier essai actuel :** k=10, soit environ 545,90 Hz avec c=343 m/s. On passe au solveur le nombre d’onde k=2*pi*f/c.
- **Grille affinée :** N=128, M=256 et h=0,0078125 m dans le support. On conserve le générateur, avec `level=2` pour le cas irrégulier actuel et `level=0` pour la référence plane.
- **Source :** `SOURCE=preprocessing.source_rer_b` par défaut, ou `preprocessing.source_constant` pour une excitation unitaire. Les deux fonctions reçoivent `(y, omega)` et le choix est commun au champ initial, à la descente et au calcul fréquentiel.
- **Matériau :** `CAR_MAT=MATERIAUX["LAINE_ROCHE"]`, avec porosité 0,97, tortuosité 1,1 et résistivité 30 000 Pa·s/m². `ALPHA0=[-50, 50]` fixe le point de départ de l’identification. Ces paramètres et `OMEGA=3430 rad/s`, `C=343 m/s` sont placés au début du programme.

À chaque fréquence, la longueur d’onde doit contenir au moins dix points de grille. Avec h=0,0078125 m et c=343 m/s, on dispose de 12,544 points par longueur d’onde à 3 500 Hz. On calcule désormais 70 fréquences de 50 à 3 500 Hz par pas de 50 Hz, ce qui couvre les trois composantes de la source. La fréquence nulle correspond à un problème statique.

Le coefficient est calculé par `compute_alpha(omega, SOURCE, CAR_MAT, ALPHA0)` à chaque pulsation. L’ensemble du projet utilise la convention `d_n u - alpha(omega)*chi*u=0`. Le résultat complexe renvoyé est utilisé directement dans `alpha_rob=Alpha*chi`. Avec cette convention dissipative, la partie réelle est négative et la partie imaginaire positive.

## Quel rôle donner au spectre RER B ?

Une source uniforme permet de comparer simplement les panneaux. Les trois gaussiennes de `source_rer_b` représentent un **spectre hypothétique**, dont les centres, largeurs et amplitudes ont été choisis pour l’illustration.

À une fréquence fixée, lorsque seule la source supérieure excite le domaine, la linéarité donne

\[
u_G=G(f)u_1,\qquad J_G=|G(f)|^2J_1
\]

Le facteur est commun à tous les panneaux. Pour G non nul, il conserve donc leur classement à cette fréquence. Le coefficient du matériau reste le même.

Sur plusieurs fréquences, les facteurs diffèrent. Ils donnent davantage de poids à certaines fréquences et peuvent ainsi changer la géométrie ou la répartition retenue. Le calcul fréquentiel actuel applique directement la source gaussienne. Un calcul unitaire complémentaire peut aider à distinguer l’effet de la source de celui du mur.

Le programme trace la réponse sur **50 à 3 500 Hz par pas de 50 Hz**, avec c=343 m/s. La source et le coefficient sont évalués à chaque fréquence. Comme l’amplitude de la source est déjà appliquée au champ, les énergies contiennent déjà son carré. La note initiale sur la source conserve des hypothèses anciennes, tandis que les paramètres exécutés sont ceux du début du programme.

## Construction progressive du résultat

| Jour | Résultat que le groupe sait expliquer |
|---|---|
| Lundi | Un premier champ, son énergie, les choix physiques et les formules demandées |
| Mardi | Les courbes des murs entièrement recouverts, puis une première répartition améliorée à une fréquence |
| Mercredi | Une répartition commune à plusieurs fréquences et l’effet de la quantité de matériau |
| Jeudi | Un choix de panneau justifié par les courbes et une vérification ciblée du résultat |
| Vendredi | Un rapport cohérent et un exposé de vingt minutes où chacun explique sa contribution |

L’optimisation de la répartition du matériau fait partie du sujet. On la programme dans la fonction prévue, avec une première étape, puis une boucle. Les tableaux et les tracés restent simples. Chaque fiche précise ce qu’on calcule, ce qu’on regarde et ce qu’on peut en conclure physiquement.

Les références entièrement recouvertes peuvent utiliser des quantités différentes selon la longueur du mur, ce qu’on indique. Pour comparer équitablement des répartitions optimisées, on fixe une même quantité physique. La fraction `V_obj` de points Robin du support permet de commencer sur une forme donnée.

## Fiches par membre et par jour

| Membre | Lundi | Mardi | Mercredi | Jeudi | Vendredi |
|---|---|---|---|---|---|
| Yann | [Fiche](Yann/01_lundi.md) | [Fiche](Yann/02_mardi.md) | [Fiche](Yann/03_mercredi.md) | [Fiche](Yann/04_jeudi.md) | [Fiche](Yann/05_vendredi.md) |
| Mathis | [Fiche](Mathis/01_lundi.md) | [Fiche](Mathis/02_mardi.md) | [Fiche](Mathis/03_mercredi.md) | [Fiche](Mathis/04_jeudi.md) | [Fiche](Mathis/05_vendredi.md) |
| Olympia | [Fiche](Olympia/01_lundi.md) | [Fiche](Olympia/02_mardi.md) | [Fiche](Olympia/03_mercredi.md) | [Fiche](Olympia/04_jeudi.md) | [Fiche](Olympia/05_vendredi.md) |
| Joachim | [Fiche](Joachim/01_lundi.md) | [Fiche](Joachim/02_mardi.md) | [Fiche](Joachim/03_mercredi.md) | [Fiche](Joachim/04_jeudi.md) | [Fiche](Joachim/05_vendredi.md) |
| Antoine | [Fiche](Antoine/01_lundi.md) | [Fiche](Antoine/02_mardi.md) | [Fiche](Antoine/03_mercredi.md) | [Fiche](Antoine/04_jeudi.md) | [Fiche](Antoine/05_vendredi.md) |

Une tâche de code concerne un seul fichier existant. Les deux blocs `Do not modify this cell` du programme principal restent inchangés, ainsi que les fonctions fournies. Les ajouts se font dans les fonctions étudiantes et les blocs autorisés. Chaque personne vérifie sa modification avant de transmettre le fichier.

## Gantt et documents utiles

[![Planning de la semaine](build/gantt.png)](gantt.pdf)

Le [Gantt](gantt.pdf), le [CSV](build/repartition.csv) et le [JSON](repartition.json) reprennent une tâche par tiret du sujet. Le [guide de lecture](lecture_et_sources.md) indique les passages utiles du cours. Le point quotidien est prévu dans la fenêtre de 14h30 à 17h.

Les sources TeX, PNG et CSV restent dans `build/`. Pour compiler le Gantt depuis ce dossier :

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error gantt.tex
cp gantt.pdf ../gantt.pdf
```
