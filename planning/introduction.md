# Objectif et déroulement de la semaine

ResoniCS réunit Yann, Mathis et Olympia, de la voie numérique, avec Joachim et Antoine, de la voie théorique. Le projet porte sur la recherche numérique d'une forme de mur et d'une répartition d'inclusions poreuses pour réduire le critère de pression du sujet, dans les conditions défavorables d'un tunnel réfléchissant. Les applications visées sont le bruit routier et le bruit ferroviaire.

Le planning suit les journées de l'énoncé du lundi 2 au vendredi 6 novembre 2026. Ces dates constituent le calendrier prévisionnel de cette semaine. Les résultats de chaque lot doivent être présentables avant le créneau quotidien de validation, compris entre 14h30 et 17h. Le vendredi après-midi est consacré à la soutenance de vingt minutes, suivie de dix minutes de questions. Chaque personne intervient et valide la partie dont elle est responsable.

## Répartition des cinq fichiers

| Responsable | Voie | Fichier principal | Objet |
|---|---|---|---|
| Yann | Numérique | `resonics.py` | Solveur, adaptation et intégration |
| Mathis | Numérique | `materiaux.py` | Matériaux, unités et bandes |
| Olympia | Numérique | `campagnes.py` | Expériences, comparaisons et figures |
| Joachim | Théorique | `objectif.py` | Objectif, adjoint et gradient |
| Antoine | Théorique | `optimisation.py` | Projection et descente |

Les fiches individuelles sont autonomes. Chacun peut écrire et vérifier son fichier avec les seules interfaces décrites dans sa fiche. Les fonctions qui ne sont pas encore disponibles sont remplacées, pour les vérifications seulement, par de petits cas synthétiques présents dans ce même fichier. Yann effectue ensuite l'intégration. Les noms pédagogiques `your_compute_objective_function` et `your_optimization_procedure` restent attribués aux deux membres de la voie théorique.

## Jalons et dépendances

- **Lundi, Y1/M1/O1/J1/A1.** Fixer les conventions, la source, les dimensions, les bandes et le budget ; obtenir une loi de matériau documentée ; geler les signatures ; vérifier les petits cas, la projection et l'adjoint.
- **Mardi, Y2/M2/O2/J2/A2.** Calculer les références entièrement recouvertes, repérer les pics, vérifier le gradient par différences centrées, puis mener une première optimisation monofréquence.
- **Mercredi, Y3/M3/O3/J3/A3.** Optimiser une distribution commune à plusieurs fréquences, comparer plusieurs budgets, puis contrôler la bande et le raffinement.
- **Jeudi, Y4/M4/O4/J4/A4.** Vérifier la reproductibilité, la stabilité du classement et les contraintes de réalisation ; choisir le produit dans la famille étudiée ; figer les données et les figures.
- **Vendredi, Y5/M5/O5/J5/A5.** Finaliser les documents, vérifier le rendu et répéter à cinq avant la soutenance.

Les développements de lundi sont parallèles grâce aux contrats. L'optimisation acoustique dépend ensuite du solveur validé, de la loi complexe du matériau et du gradient contrôlé. La recommandation du jeudi dépend de la comparaison sur toute la bande et à quantité de poreux annoncée.

## Décisions à valider au premier point

Le sujet laisse au groupe le choix des bandes route et rail, des dimensions, de la source précise et des matériaux. La table de coefficients d'absorption réels du document Filoche ne suffit pas à reconstruire une impédance complexe. Les anciens programmes ne fournissent pas non plus de fonction `compute_alpha`. Mathis doit donc obtenir le modèle et ses paramètres, ou une table d'impédances avec sa provenance, afin de produire un coefficient physique utilisable.

Le programme de support emploie un coefficient Robin dont le signe doit être relié explicitement à celui de la condition physique. Yann et Joachim valident cette correspondance sur un cas plan. Les formules de gradient du cahier sont dérivées du système réellement assemblé, puis contrôlées par perturbations du coût.

L'EI impose une quantité de matériau, ce qui conduit ici à un budget de longueur absorbante pondérée, à épaisseur et profondeur fixées. L'aire unité conservée dans la partie trois précédente ne devient pas une contrainte de ce projet. Les comparaisons emploient une même source, des dimensions de référence annoncées et un budget absolu commun entre les formes.

Pour la comparaison théorique ouverte/réfléchissante, le premier scénario proposé conserve le bord source et ouvre une paroi latérale. Joachim fait valider le périmètre de l'étude demandée. Si une dérivée géométrique de forme est attendue, sa dérivation constitue un complément spécifique à la dérivée de densité détaillée ici.

## Ce qui est repris du travail antérieur

Nous reprenons la démarche de vérification sur un cas connu, le suivi des résidus, le raffinement à géométrie fixée et les exports de résultats. Le modèle de l'EI utilise les différences finies et une condition Robin absorbante, avec une excitation de Dirichlet non homogène en haut. Les choix de source, de nombres d'onde et de conservation d'aire du devoir précédent restent liés à leurs propres énoncés.

Le générateur fourni permet de commencer avec les niveaux zéro, un et deux. Malgré le nom `create_motif_koch`, il construit un motif orthogonal à huit segments de quart. Les descriptions et les figures doivent représenter ce contour effectif. La règle orale de détails d'ordre demi-longueur d'onde guide la conception ; l'énoncé exige au moins dix points par longueur d'onde. Ces deux contrôles ont des rôles différents.

## Documents et soutenance

Le rapport est rédigé en LaTeX dans le template récent, article A4 de onze points avec marges de deux virgule deux centimètres. La présentation reprend Beamer CambridgeUS en seize neuvièmes, un plan détaillé et des rappels de plan. Les paragraphes expliquent les choix, les figures portent des légendes nominales et les grandeurs numériques proviennent des exports.

Une première répartition orale réserve quatre minutes à chacun : modèle et calcul pour Yann, matériau et bandes pour Mathis, critère et gradient pour Joachim, optimisation pour Antoine, comparaisons et produit pour Olympia. La répétition permet d'ajuster les transitions en conservant vingt minutes au total.

Chaque membre remet son fichier, les contrôles exécutés, ses paramètres et les éléments d'analyse de son lot. Il relit et approuve les figures et les équations correspondantes avant la validation collective.
