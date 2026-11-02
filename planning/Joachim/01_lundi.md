# Joachim — Lundi, 2 novembre 2026

Objectif : définir le critère et expliquer sa dérivée avant le premier point.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Intégrale de pression et modèle mathématique

**Fichier à compléter :** `support/demo_control_polycopie2024.py`, uniquement `your_compute_objective_function` et une petite fonction de vérification à ajouter. Les équations et l'étude théorique sont rendues dans la réponse écrite, sans autre fichier.

**Ce qu'on fait.** On remplace le retour nul du critère par une somme des modules au carré aux seuls nœuds intérieurs. On présente ensuite le problème de Helmholtz, le rôle des bords et la dérivée qui servira au code du mardi. On conserve le bord supérieur source pour comparer un côté réfléchissant et ce même côté ouvert.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, version à jour, fichier cible complet
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Sujet-EI-EXT-2026.md`
- `context/Dirichlet_Nonhomogene.pdf`, les deux pages
- `context/GAllaire-OptimParam.pdf`, notamment les pages PDF 25 à 29 pour l'adjoint


**Prompt à copier :**

```text
Nous complétons le programme de différences finies du projet ResoniCS. Modifie uniquement le fichier demo_control_polycopie2024.py fourni, sans créer d'autre fichier. Préserve les fonctions des autres membres et les cellules explicitement imposées. Les autres pièces jointes servent à la lecture.

Complète your_compute_objective_function(domain_omega, u, spacestep) avec le critère réel J=h²*somme(|u|²) sur le masque domain_omega == _env.NODE_INTERIOR, dont le label vaut -1. Vérifie les dimensions, le pas positif fini et les valeurs intérieures finies. Utilise le module au carré, jamais le carré complexe. Renvoie un float positif ou nul. Les valeurs de bord rendues nulles par le solveur ne sont pas les traces physiques.

Ajoute une fonction check_objective() qui n'est pas appelée automatiquement. Elle vérifie le champ nul, l'invariance par une phase complexe et l'indépendance des valeurs extérieures. Sur quatre nœuds intérieurs portant chacun 3+4j avec h=0.2, le résultat attendu est 4.0. Les contrôles restent dans ce fichier.

Après le code, donne une explication courte du modèle et de ses propriétés sous les hypothèses réellement disponibles. Le paramètre historique omega du solveur représente k, alors que la fréquence f en hertz donne k=2*pi*f/c. Le critère d'intégrale de pression n'est pas directement une puissance dissipée. Ne prétends pas que Helmholtz est toujours coercif ou inversible.

Établis l'identité de Green avec la source Dirichlet non homogène en haut. Pour le scénario ouvert, garde cette source et ouvre uniquement un côté avec ∂n u-i*k*u=0. Le signe effectivement employé par le support est ∂n u-alpha_code*u=0, donc alpha_code=i*k sur l'ouverture. Explique le terme de flux sortant et compare à la paroi Neumann. Cette identité ne suffit pas à affirmer J_ouvert < J_fermé à toute fréquence.

Énonce aussi la dérivée de densité pour A(chi)U=b, J=U*WU, avec b indépendant de chi : A*P=2WU et g_l=-Re(P* (dA/dchi_l) U), où * est la transposée conjuguée. Le champ est le champ total. Distingue cette dérivée de densité de l'étude de l'énergie selon la forme du domaine demandée par le sujet et signale les hypothèses nécessaires.

Pour l’étude selon la forme demandée par l’énoncé, considère une famille de domaines obtenue en déplaçant le mur, avec la source supérieure fixe et la densité transportée avec le mur, puis définis le critère sur chaque domaine. Sur une paroi suffisamment régulière, ramène le problème au domaine de référence et différencie sa formulation variationnelle pour exprimer la variation du critère, en précisant les hypothèses et le rôle de l’adjoint. Reprends cette étude avec un côté réfléchissant puis avec Sommerfeld et identifie les termes de bord qui changent. Explique comment la comparaison numérique des profils complète cette étude pour les contours fractals discrétisés, dont le changement d’étiquette sur la grille n’est pas une dérivation continue de forme.

Les commentaires et docstrings sont de courtes phrases françaises, sans notation mathématique. Renvoie uniquement le fichier cible complet comme code, puis l'explication et les résultats de contrôles réellement exécutés. Si tu ne peux pas les exécuter, indique les appels à faire sans annoncer qu'ils ont réussi.
```

**Vérification et transmission.** On exécute `check_objective()` depuis le dossier `support`, puis on transmet la version complète à Antoine pour sa projection. On présente l'identité énergétique, la dérivée et les hypothèses au point collectif avant de choisir une fréquence d'essai.
