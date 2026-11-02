# Lecture des documents et références de travail

La préparation s'appuie sur l'énoncé EI, les trois documents complémentaires, les programmes de support et les documents des parties un, deux et trois. Les copies identiques des cours ont été regroupées pour la lecture. La note de deux pages sur le Dirichlet non homogène a été lue intégralement. Les figures de résultats des anciens projets ont été examinées dans leurs rapports et leurs présentations ; les dépendances installées et les fichiers de compilation ne constituent pas des supports scientifiques.

## Documents utiles à chaque lot

| Document | Passages utiles | Usage |
|---|---|---|
| Sujet EI extérieur 2026 | Ensemble de l'énoncé | Livrables, cinq journées, références entièrement recouvertes, quantités et soutenance |
| Allaire, optimisation paramétrique | Pages PDF 13–20 et 25–29 | Adjoint, projection, recherche du pas, gradient discret |
| Note Dirichlet non homogène | Deux pages | Relèvement et utilisation du champ total dans le gradient |
| Mur antibruit, Filoche | Pages 5–6, 17–24, 35–46, 56–70 | Impédance, pertes, formes et exemples de matériaux |
| Cours de modélisation antérieur | Pages 18–19, 33–42 et 59–66 | Conventions, conditions au bord et limites des données de matériau disponibles |
| Rapports et présentations antérieurs | Méthodes de vérification et préambules LaTeX | Tests, exports et mise en forme |
| Cinq modules de support | Fonctions d'assemblage, géométrie, stubs et affichage | Contrat numérique effectif et points à compléter |

Les nombres de pages ci-dessus désignent les pages des fichiers PDF. Pour Allaire, les pages PDF 13–20 correspondent aux pages imprimées 89–96 et les pages PDF 25–29 aux pages imprimées 101–105.

## Points effectivement constatés dans le support

Les deux fonctions pédagogiques à écrire sont des ébauches. L'objectif retourne actuellement zéro. La boucle d'optimisation contient des noms encore non définis et n'est pas branchée dans la démonstration ; les champs avant et après sont donc initialement identiques. Les cellules signalées comme imposées doivent être conservées. Le travail est réalisé dans les cinq nouveaux fichiers et leur adaptation d'appel.

Le solveur fourni assemble des matrices creuses, applique les conditions aux limites puis résout le système. Le champ retourné remplit les seuls nœuds intérieurs. Les valeurs de bord affichées à zéro ne permettent donc pas de calculer directement une dissipation : les traces sont à reconstruire avec la même convention que l'élimination de Robin.

Le paramètre historique `omega` joue le rôle du nombre d'onde. Le code ne fournit pas de modèle de matériau complexe. Le générateur utilise un motif orthogonal, des arrondis et une boîte contenant une zone complémentaire sous le profil. Les contrôles de résolution, de masques et de longueur de frontière font donc partie du lot de Yann.

## Contrôle préliminaire du gradient discret

Un petit calcul sur le support conservé a vérifié l'expression de la dérivée utilisée dans les fiches. Il emploie une grille de seize colonnes, une frontière de niveau un et un coefficient complexe de contrôle. La comparaison concerne une dérivée directionnelle, avec recalcul du coût pour les densités perturbées.

| Amplitude de la perturbation | Écart relatif de la dérivée |
|---|---|
| `0.01` | `1.81e-5` |
| `0.001` | `1.81e-7` |
| `0.0001` | `1.83e-9` |

Ces valeurs illustrent le contrôle du gradient. Les campagnes physiques et les performances du produit seront évaluées avec les paramètres de matériau validés pendant la semaine.
