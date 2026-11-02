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

## Comment utiliser une fiche

1. Récupérer les versions actuelles des fichiers partagés, puis ouvrir la fiche du jour.
2. Joindre les fichiers indiqués et copier le prompt de la tâche. Un seul fichier cible est modifié ; les dépendances sont fournies en lecture seule.
3. Vérifier le résultat, puis transmettre le fichier complet au membre suivant avant sa modification.

Les résultats et paramètres produits les jours précédents sont joints lorsqu'une tâche les utilise. Une donnée encore manquante est signalée et aucun résultat physique n'est inventé pour la remplacer.

## Fichiers partagés

| Fichier existant | Contributions prévues |
|---|---|
| `support/preprocessing.py` | Yann prépare la géométrie et les poids du mur, puis Mathis ajoute la loi de matériau |
| `support/processing.py` | Yann rend l'assemblage accessible pour le calcul de l'état et de l'adjoint |
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
