# ResoniCS — Planning par personne et par jour

Chaque membre dispose de **cinq fiches**, une par jour du 2 au 6 novembre 2026. Les titres des tâches reprennent **mot pour mot les 22 tirets de l’[énoncé](../context/Sujet-EI-EXT-2026.md)**, dans leur ordre et à la journée prévue. Le Gantt, les fiches et les exports CSV/JSON utilisent ces mêmes intitulés.

Une tâche peut mobiliser plusieurs personnes. Sa phrase reste identique dans leurs fiches et chacune décrit sa contribution, les fichiers à joindre, un prompt prêt à copier et les contrôles attendus. Les étapes techniques sont détaillées sous le titre officiel.

| Membre | Lundi | Mardi | Mercredi | Jeudi | Vendredi |
|---|---|---|---|---|---|
| Yann | [Fiche](Yann/01_lundi.md) | [Fiche](Yann/02_mardi.md) | [Fiche](Yann/03_mercredi.md) | [Fiche](Yann/04_jeudi.md) | [Fiche](Yann/05_vendredi.md) |
| Mathis | [Fiche](Mathis/01_lundi.md) | [Fiche](Mathis/02_mardi.md) | [Fiche](Mathis/03_mercredi.md) | [Fiche](Mathis/04_jeudi.md) | [Fiche](Mathis/05_vendredi.md) |
| Olympia | [Fiche](Olympia/01_lundi.md) | [Fiche](Olympia/02_mardi.md) | [Fiche](Olympia/03_mercredi.md) | [Fiche](Olympia/04_jeudi.md) | [Fiche](Olympia/05_vendredi.md) |
| Joachim | [Fiche](Joachim/01_lundi.md) | [Fiche](Joachim/02_mardi.md) | [Fiche](Joachim/03_mercredi.md) | [Fiche](Joachim/04_jeudi.md) | [Fiche](Joachim/05_vendredi.md) |
| Antoine | [Fiche](Antoine/01_lundi.md) | [Fiche](Antoine/02_mardi.md) | [Fiche](Antoine/03_mercredi.md) | [Fiche](Antoine/04_jeudi.md) | [Fiche](Antoine/05_vendredi.md) |

## Cas d’usage retenu : le RER B

On concentre le projet sur le **bruit du RER B**. La [synthèse de l’état de l’art](../SOTA.md) a été réalisée par **Mathis et Olympia**. Elle est jointe aux prompts et sert à cadrer l’application, les matériaux et le concept de panneau. La tâche J1.1 est donc déjà amorcée par cette synthèse ; son complément porte sur les sources et sur les choix qui en découlent.

| Régime de bruit | Plage proposée dans SOTA.md | Place dans les calculs |
|---|---|---|
| Roulement | 250–2 000 Hz | Première plage de travail proposée, à valider en J1.3 |
| Traction et auxiliaires | 100–500 Hz | Cas complémentaire selon les données et les moyens de calcul |
| Crissement en courbe | 1 500–4 000 Hz | Cas complémentaire selon les données, le matériau et la résolution possible |

Ces plages sont des indications de la synthèse et doivent être documentées. L’enveloppe de 100 à 4 000 Hz ne constitue pas un spectre mesuré du RER B. En J1.3, Mathis propose au groupe le régime prioritaire, la bande finalement étudiée, le site ou la section-type, la vitesse si elle est connue, les dimensions et les données de source.

On conserve le **tunnel réfléchissant** et la **source de Dirichlet en haut** du modèle fourni. Une source unitaire permet d’abord de calculer une réponse fréquentielle comparable entre panneaux. Sans spectre mesuré, le coût de bande utilise une quadrature normalisée explicitement annoncée. Si des données de source sont obtenues, leur provenance et leur pondération sont fixées avant l’optimisation. Les gains relatifs calculés portent sur ce scénario et son critère de pression.

La forme et les dimensions du panneau restent fixes pendant une comparaison en fréquence. Yann vérifie le pas à partir de la plus haute fréquence effectivement calculée et des plus petits reliefs. Un cas à 4 000 Hz nécessite donc sa propre vérification de résolution. L’ordre de grandeur des reliefs proche de la demi-longueur d’onde guide les dimensions à tester.

Le concept à examiner est le panneau rigide avec **cartouches poreuses amovibles** décrit dans SOTA.md. Mathis documente la loi complexe des matériaux candidats, notamment laine de roche ou fibre de chanvre si leurs données sont disponibles. Antoine conserve un budget physique pondéré. Les fractions de matériau et les gains évoqués dans l’état de l’art sont des perspectives à confronter aux calculs.

Pour les exports, le dictionnaire `metadata` des `records` précise désormais `application`, `noise_regime`, `frequency_band_hz`, `band_provenance`, `source_model` et `source_spectrum_provenance`, en plus des paramètres déjà prévus. Olympia compare des configurations appartenant au même scénario et identifie les éventuels cas complémentaires. Les bandes exploratoires qui se recouvrent sont traitées séparément ou avec une pondération commune justifiée.

## Comment utiliser une fiche

1. Récupérer les versions actuelles des fichiers partagés, puis ouvrir la fiche du jour.
2. Joindre les fichiers indiqués et copier le prompt de la tâche. Un seul fichier cible est modifié ; les dépendances sont fournies en lecture seule.
3. Vérifier le résultat, puis transmettre le fichier complet au membre suivant avant sa modification.

La synthèse SOTA.md et les résultats et paramètres produits les jours précédents sont joints lorsqu’une tâche les utilise. Une donnée encore manquante est signalée et aucun résultat physique n'est inventé pour la remplacer.

## Zones protégées du programme fourni

Le programme [demo_control_polycopie2024.py](../support/demo_control_polycopie2024.py) contient **deux cellules explicitement protégées**, chacune marquée `Do not modify this cell, these are the values that you will be assessed against.` Les numéros ci-dessous sont ceux de la version initiale et peuvent se décaler lors des ajouts ; les commentaires délimitent les cellules.

| Cellule | Contenu à conserver intégralement |
|---|---|
| Initialisation, lignes 95 à 106 | Appels de `_set_coefficients_of_pde`, `_set_rhs_of_pde` et `_set_geometry_of_domain`, avec leurs affectations |
| Résolution initiale, lignes 143 à 151 | Appel de `processing.solve_helmholtz`, puis `chi0 = chi.copy()` et `u0 = u.copy()` |

Chaque cellule est conservée de son en-tête jusqu’au début de la cellule suivante, avec ses lignes, commentaires, indentation, arguments et ordre. Aucun ajout n’y est placé et leur exécution reste dans le chemin initial. Les prompts qui renvoient le fichier complet demandent de comparer ces deux cellules à leur version d’entrée avant de rendre le résultat.

Les fonctions étudiantes et les cellules signalées `Fell free to modify the function call in this cell.` accueillent les compléments. La source `f_dir`, la densité et le coefficient Robin sont définis dans la cellule modifiable prévue à cet effet. Les coefficients imposés et les factories qui les initialisent gardent leur définition fournie.

Pour préserver aussi le comportement des appels protégés, les tâches de géométrie et d’assemblage sont réalisées par **ajout de fonctions** dans les modules existants :

- `prepare_geometry_of_domain` prépare les tableaux indépendants des campagnes, puis `get_design_faces` décrit leurs contacts. `_set_geometry_of_domain` et les fonctions de motif initiales gardent leur code.
- `assemble_helmholtz_system` réutilise les fonctions d’assemblage fournies pour exposer la matrice et le second membre. `solve_helmholtz` et son appel protégé gardent leur code. Les solutions des deux chemins sont comparées sur les mêmes données.
- `run_frequency_campaign` utilise les nouveaux helpers avec des variables locales `case_*`. Son appel se place dans la dernière cellule autorisée, **après** le calcul initial et les copies protégées. Les essais de frontière ouverte et les autres géométries travaillent sur ces données indépendantes.

Les seules zones signalées comme protégées dans les cinq fichiers se trouvent dans le programme principal. La conservation des fonctions du chemin initial est une précaution supplémentaire du planning. Les fonctions nouvelles d’objectif, d’adjoint, de projection, de descente et de matériau restent à compléter dans les fichiers communs. Aucun fichier Python supplémentaire n’est demandé.

## Fichiers partagés

| Fichier existant | Contributions prévues |
|---|---|
| `support/preprocessing.py` | Yann ajoute la préparation des géométries de campagne et les poids du mur, puis Mathis ajoute la loi de matériau |
| `support/processing.py` | Yann ajoute l’accès à la matrice pour l’état et l’adjoint, en gardant le solveur initial intact |
| `support/demo_control_polycopie2024.py` | Joachim écrit le coût et le gradient, Antoine la projection et la descente, puis Yann intègre et lance les expériences |
| `support/postprocessing.py` | Olympia prépare les figures et les comparaisons à partir des calculs |
| `support/_env.py` | Constantes communes utilisées en lecture seule |

Chaque contribution de code concerne **un seul fichier à la fois**, et les fichiers sont communs au groupe. Les contributions d’analyse ou de restitution indiquent qu’aucun fichier Python n’est à modifier. Les fonctions nouvelles sont ajoutées dans ces fichiers existants. Aucun nouveau module Python n'est prévu et les programmes de `support/` n'ont pas été modifiés pendant cette préparation.

Pour éviter d'écraser des contributions, le passage de main est **Yann → Mathis** dans `preprocessing.py` le lundi, et **Joachim → Antoine → Yann** dans la démonstration. Les fonctions de calcul et les tracés peuvent avancer en parallèle dans leurs fichiers respectifs. Après l'intégration, Joachim et Yann contrôlent le gradient acoustique réel avant la première descente. Les corrections ultérieures reprennent toujours la dernière version partagée.

## Vue d'ensemble

[![Planning de la semaine](build/gantt.png)](gantt.pdf)

Le Gantt comporte **une ligne par tiret**, avec le responsable en gras, ses contributeurs et une barre dans la journée correspondante. Il est fourni en **A3 paysage** pour garder les intitulés complets lisibles.

| Journée | Nombre de tâches de l'énoncé |
|---|---|
| Lundi 2 novembre | 10 |
| Mardi 3 novembre | 4 |
| Mercredi 4 novembre | 3 |
| Jeudi 5 novembre | 2 |
| Vendredi 6 novembre | 3 |

Les repères **J1.1**, **J1.2**, etc. désignent le jour et le rang du tiret. Ils permettent de retrouver une même tâche dans le Gantt et dans les différentes fiches, sans modifier sa phrase. Le cadrage initial de la startup et la soutenance sont repris comme indications de calendrier, en dehors des 22 tirets.

Le groupe prépare son état d'avancement avant le point quotidien prévu dans la fenêtre de **14h30 à 17h**. La soutenance du vendredi après-midi dure **vingt minutes à cinq**, puis **dix minutes de questions**.

Le [Gantt PDF](gantt.pdf), sa [source LaTeX](build/gantt.tex), le [CSV](build/repartition.csv) et le [JSON](repartition.json) reprennent les 22 tâches. Les prompts sont dans les fiches quotidiennes. Les [documents de référence](lecture_et_sources.md) servent à retrouver les supports utiles.

## Compiler le Gantt

Depuis `planning/build/` :

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error gantt.tex
cp gantt.pdf ../gantt.pdf
```

Les fichiers TeX, PNG et CSV restent dans `build/`. Le PDF à consulter reste dans `planning/`. Les futurs rapport et présentation reprendront les templates LaTeX du projet précédent, sans être créés à cette étape.
