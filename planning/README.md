# ResoniCS — Planning par personne et par jour

Chaque membre dispose de **cinq fiches**, une par jour du 2 au 6 novembre 2026. Chaque tâche indique ce qui est fait, le fichier à compléter, les fichiers à joindre, un prompt prêt à copier et les contrôles attendus.

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

Une tâche concerne **un seul fichier à la fois**, et les fichiers sont communs au groupe. Les fonctions nouvelles sont ajoutées dans ces fichiers existants. Aucun nouveau module Python n'est prévu et les programmes de `support/` n'ont pas été modifiés pendant cette préparation.

Pour éviter d'écraser des contributions, le passage de main est **Yann → Mathis** dans `preprocessing.py` le lundi, et **Joachim → Antoine → Yann** dans la démonstration. Les fonctions de calcul et les tracés peuvent avancer en parallèle dans leurs fichiers respectifs. Après l'intégration, Joachim et Yann contrôlent le gradient acoustique réel avant la première descente. Les corrections ultérieures reprennent toujours la dernière version partagée.

## Vue d'ensemble

[![Planning de la semaine](build/gantt.png)](gantt.pdf)

- **Lundi :** modèle, données physiques, étude théorique, objectif et projection.
- **Mardi :** références entièrement recouvertes, pics et première optimisation.
- **Mercredi :** optimisation commune à plusieurs fréquences, quantités et validation de bande.
- **Jeudi :** raffinement, plusieurs départs et choix du produit.
- **Vendredi :** vérifications finales et soutenance de vingt minutes à cinq, puis dix minutes de questions.

Le groupe prépare son état d'avancement avant le point quotidien prévu dans la fenêtre de **14h30 à 17h**. Les codes du Gantt associent l'initiale du membre au numéro du jour, par exemple Y1 pour Yann lundi.

Le [Gantt PDF](gantt.pdf), sa [source LaTeX](build/gantt.tex), le [CSV](build/repartition.csv) et le [JSON](repartition.json) donnent une vue synthétique. Les consignes copiables sont uniquement dans les fiches quotidiennes ; l'ancien cahier général et les anciennes fiches par module sont remplacés par cette organisation. Les [documents de référence](lecture_et_sources.md) servent à retrouver les supports utiles.

## Compiler le Gantt

Depuis `planning/build/` :

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error gantt.tex
cp gantt.pdf ../gantt.pdf
```

Les fichiers TeX, PNG et CSV restent dans `build/`. Le PDF à consulter reste dans `planning/`. Les futurs rapport et présentation reprendront les templates LaTeX du projet précédent, sans être créés à cette étape.
