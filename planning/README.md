# ResoniCS — Un premier résultat dès le jour 1

Le premier jour sert à obtenir un calcul simple et à expliquer le modèle. On utilise les cinq fichiers fournis. Les titres des tâches reprennent exactement les 22 tirets de l’[énoncé](../context/Sujet-EI-EXT-2026.md).

## Ce que le groupe doit pouvoir montrer lundi

1. Le cas retenu : bruit de roulement du RER B, avec la synthèse [SOTA.md](../SOTA.md) réalisée par Mathis et Olympia.
2. Un schéma du domaine, de la source et des conditions aux limites.
3. Un tableau court : N, M, pas, niveau du contour, dimensions représentées, fréquence, célérité, coefficient et quantité de matériau.
4. Une figure du champ initial et une valeur de son énergie calculée par `your_compute_objective_function`.
5. Les choix physiques et les formules demandées au premier jour, avec les difficultés encore à résoudre clairement indiquées.

Le programme doit s’exécuter et les figures doivent être compréhensibles. L’optimisation ne sera présentée comme effectuée qu’après son implémentation et la vérification du gradient, mardi. Les calculs du lundi ne nécessitent ni nouveau générateur de géométrie, ni réorganisation du solveur, ni format général de résultats.

## Répartition du travail lundi

| Membre | Résultat concret |
|---|---|
| Yann | Choisir les paramètres dans les blocs autorisés, lancer le code existant et expliquer le modèle |
| Mathis | Confirmer le cas de bruit, choisir un matériau documenté et calculer son coefficient à la fréquence d’essai |
| Olympia | Réutiliser l’état de l’art et rendre les figures initiales compréhensibles |
| Joachim | Compléter le calcul de l’énergie et rédiger les propriétés, l’étude théorique et la formule de dérivée |
| Antoine | Écrire le problème à quantité fixée et expliquer la descente projetée avec un exemple |

Pour le fichier commun, Joachim complète d’abord le calcul d’énergie, puis Yann ajoute l’appel et l’affichage dans un bloc autorisé. Mathis travaille séparément sur le coefficient dans `preprocessing.py` si une fonction de calcul est nécessaire. Olympia peut commenter les figures existantes sans modifier `postprocessing.py` lundi.

## Choix de départ proposés

- **Application :** roulement du RER B. La plage 250–2 000 Hz donnée dans SOTA.md sert de première piste à documenter.
- **Premier essai :** 500 Hz, avec c=340 m/s si le groupe retient la valeur utilisée dans le polycopié. On calcule k=2*pi*f/c et on vérifie h<=c/(10*f).
- **Géométrie :** celle du générateur fourni. Le réglage actuel `level=1` peut être conservé ; `level=0` donne une référence plane. Les comparaisons de plusieurs profils commencent mardi.
- **Source :** Dirichlet uniforme en haut, identique dans les comparaisons. Elle sert de référence en l’absence de spectre mesuré du RER B.
- **Matériau :** un seul pour commencer. Le cas ISOREL du §3.2.4 du polycopié fournit des données documentées pour un calcul de référence. Les autres matériaux de SOTA.md seront comparés quand leurs données seront disponibles.
- **Quantité :** annoncer ce que calcule le support. `V_obj` est une fraction des points Robin, pas un volume. La mesure en longueur ou volume sera précisée avant les comparaisons à quantité physique égale entre formes.

Le programme propose aussi les courbes `fig_rer_b_spectre.png` et `fig_rer_b_energie.png`, avec un spectre hypothétique sur 100–1 500 Hz et c=343 m/s. Ce tracé constitue un essai complémentaire. Pour J1.2, un seul calcul suffit, avec les paramètres effectivement retenus indiqués à côté du résultat.

Ces valeurs sont des propositions de travail à confirmer, pas des mesures du RER B. Si le coefficient du matériau n’est pas encore prêt, `Alpha=10-10j` reste un coefficient d’exemple pour vérifier le programme. Le résultat est alors présenté comme un essai de fonctionnement. La valeur physique et son signe doivent être validés avant toute conclusion d’absorption.

## Fiches à utiliser

Chaque fiche contient, pour chaque tâche, une explication courte, le fichier à modifier, les fichiers concernés, un contexte prêt à transmettre et le résultat attendu. Une modification de code concerne un seul fichier existant. Les contributions d’analyse ne modifient aucun fichier.

| Membre | Lundi | Mardi | Mercredi | Jeudi | Vendredi |
|---|---|---|---|---|---|
| Yann | [Fiche](Yann/01_lundi.md) | [Fiche](Yann/02_mardi.md) | [Fiche](Yann/03_mercredi.md) | [Fiche](Yann/04_jeudi.md) | [Fiche](Yann/05_vendredi.md) |
| Mathis | [Fiche](Mathis/01_lundi.md) | [Fiche](Mathis/02_mardi.md) | [Fiche](Mathis/03_mercredi.md) | [Fiche](Mathis/04_jeudi.md) | [Fiche](Mathis/05_vendredi.md) |
| Olympia | [Fiche](Olympia/01_lundi.md) | [Fiche](Olympia/02_mardi.md) | [Fiche](Olympia/03_mercredi.md) | [Fiche](Olympia/04_jeudi.md) | [Fiche](Olympia/05_vendredi.md) |
| Joachim | [Fiche](Joachim/01_lundi.md) | [Fiche](Joachim/02_mardi.md) | [Fiche](Joachim/03_mercredi.md) | [Fiche](Joachim/04_jeudi.md) | [Fiche](Joachim/05_vendredi.md) |
| Antoine | [Fiche](Antoine/01_lundi.md) | [Fiche](Antoine/02_mardi.md) | [Fiche](Antoine/03_mercredi.md) | [Fiche](Antoine/04_jeudi.md) | [Fiche](Antoine/05_vendredi.md) |

## Suite de la semaine

- Mardi : boucles simples sur les fréquences, références entièrement recouvertes, puis première descente dans `your_optimization_procedure` après vérification du gradient.
- Mercredi : même descente sur plusieurs fréquences, comparaison de quelques quantités physiques et vérification sur la bande.
- Jeudi : vérifications ciblées avec un pas plus petit et quelques départs, puis choix du produit.
- Vendredi : finalisation du rapport et répétition de l’exposé de vingt minutes à cinq, suivi de dix minutes de questions.

Les fonctions du support et leurs arguments restent le point de départ. On ajoute seulement le calcul qui manque lorsque la question le demande. Les données peuvent rester dans de simples tableaux de fréquences et d’énergies ; les informations du cas sont notées avec les résultats. Aucun ensemble de fonctions génériques ni bibliothèque propre au projet n’est demandé.

L’étude théorique du premier jour reste à faire : le choix d’un premier résultat simple ne supprime aucun des dix tirets du lundi. Les développements de code plus longs sont placés au moment où ils sont utiles aux calculs du lendemain.

## Blocs protégés

Les deux blocs de `demo_control_polycopie2024.py` marqués `Do not modify this cell, these are the values that you will be assessed against.` restent intégralement inchangés. Le premier prépare coefficients, seconds membres et géométrie. Le second appelle `solve_helmholtz`, puis copie `chi0` et `u0`.

Les paramètres et appels supplémentaires sont placés dans les blocs `Fell free to modify the function call in this cell.` Les fonctions étudiantes sont complétées à leur emplacement. On conserve les fonctions fournies de `preprocessing.py` et `processing.py`. Les essais supplémentaires se font après les blocs protégés, avec leurs propres tableaux. Chaque personne compare la version rendue à celle reçue avant de transmettre le fichier commun.

## Diagramme et documents

[![Planning de la semaine](build/gantt.png)](gantt.pdf)

Le [Gantt PDF](gantt.pdf), le [CSV](build/repartition.csv) et le [JSON](repartition.json) conservent une ligne par tiret du sujet, dans l’ordre et à la bonne journée. Les repères J1.1, J1.2, etc. désignent le jour et le rang du tiret. Le point quotidien avec les enseignants est prévu dans la fenêtre de 14h30 à 17h.

Les [documents de référence](lecture_et_sources.md) permettent de retrouver les passages utiles du polycopié.

Pour compiler le Gantt depuis `planning/build/` :

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error gantt.tex
cp gantt.pdf ../gantt.pdf
```

Les sources TeX, PNG et CSV restent dans `build/`. Le rapport et la présentation reprendront les modèles LaTeX des projets précédents lorsqu’ils seront rédigés.
