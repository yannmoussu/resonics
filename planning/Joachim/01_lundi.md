# Joachim — Lundi 2 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution de Joachim. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## the model to consider,

**Repère :** J1.2. **Rôle :** contributeur.

**Contribution de Joachim.** On précise l’équation de Helmholtz, le champ complexe étudié, la source imposée et les conditions aux limites du tunnel.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le modèle représente un panneau destiné au bruit du RER B dans le tunnel réfléchissant demandé par l’énoncé. Décris le domaine et ses dimensions physiques, le profil fourni et la source de Dirichlet supérieure. La paroi rigide et les côtés Neumann sont les hypothèses du modèle. Choisis un profil physique fixe pour les comparaisons en fréquence ; le motif orthogonal fourni reste celui effectivement calculé.

Distingue les définitions indicatives de SOTA.md de la dérivation utilisant l’assemblage réel. Le champ total, la convention de Robin et le critère de pression restent ceux du modèle retenu.

Présente le modèle de Helmholtz du programme fourni. Définis le champ complexe, la fréquence en hertz, la pulsation physique et le nombre d’onde. Le paramètre historique omega de solve_helmholtz reçoit k=2*pi*f/c. Décris la source de Dirichlet en haut, les côtés Neumann et la paroi Robin où agit le matériau. La géométrie reste fixe pendant une optimisation de densité.

Avec la convention temporelle exp(-i*omega_phys*t), le Robin réellement assemblé s’écrit partial_n u-alpha_code*u=0. Identifie le coefficient du code et celui de la convention physique choisie par Mathis. Écris la formulation variationnelle, en tenant compte de la source Dirichlet non homogène par un relèvement. Les dimensions et les valeurs physiques seront celles validées par le groupe.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On transmet à Yann les équations et les notations communes, puis à Mathis la convention de signe à vérifier avec l’impédance.

## formulate the properties of the chosen model, what is known about its solution ;

**Repère :** J1.4. **Rôle :** responsable.

**Contribution de Joachim.** On expose les propriétés mathématiques utiles et les hypothèses qui permettent de résoudre le modèle choisi.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Énonce les propriétés sous les hypothèses du panneau et de la source harmonique retenus pour le RER B. Distingue l’approximation réfléchissante Neumann de la description d’une paroi réelle. Les résultats de solvabilité et de dissipation doivent utiliser le coefficient complexe validé, et la plage étudiée doit rester dans la validité du modèle de matériau.

Distingue les définitions indicatives de SOTA.md de la dérivation utilisant l’assemblage réel. Le champ total, la convention de Robin et le critère de pression restent ceux du modèle retenu.

À partir de l’équation et des bords du projet, explique les propriétés attendues du problème de Helmholtz. Présente les hypothèses sur le domaine, les données et le coefficient complexe. Distingue l’existence et l’unicité du problème continu, les résonances et la solvabilité du système discret. Ne prétends pas que Helmholtz est toujours coercif ou inversible.

Utilise une identité de Green pour expliquer le rôle de la partie dissipative du coefficient et les conditions nécessaires à l’unicité dans le cadre retenu. Indique quelles propriétés sont établies dans les documents joints et quelles hypothèses restent à vérifier. Présente aussi les contrôles numériques de résidu et de raffinement que Yann effectuera, en précisant ce qu’ils vérifient.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On présente les hypothèses au groupe avant la première campagne et on distingue les arguments théoriques des contrôles numériques.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** contributeur.

**Contribution de Joachim.** On définit le critère intérieur et on complète sa fonction de calcul dans la démonstration.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Formule le coût du scénario RER B avec une quantité physique de poreux fixée. La source unitaire en haut donne d’abord une réponse fréquentielle de référence. Si aucun spectre mesuré n’est disponible, annonce des poids d’intégration de fréquence normalisés. Si un spectre mesuré est fourni, sa provenance et sa normalisation sont fixées avant la descente et la réponse à source unitaire est pondérée sans compter deux fois l’amplitude du bruit.

Distingue les définitions indicatives de SOTA.md de la dérivation utilisant l’assemblage réel. Le champ total, la convention de Robin et le critère de pression restent ceux du modèle retenu.

Travaille sur la dernière version partagée de demo_control_polycopie2024.py. Modifie uniquement ce fichier et renvoie sa version complète en préservant les fonctions des autres membres et les cellules explicitement imposées. Les autres fichiers sont en lecture seule. Ne crée aucun nouveau module Python. Les commentaires et docstrings sont des phrases françaises sans notation mathématique. Donne les contrôles réellement exécutés ou leurs appels si tu ne peux pas les exécuter.

Complète your_compute_objective_function(domain_omega,u,spacestep). Le critère vaut h²*somme(|u|²) sur le masque domain_omega == _env.NODE_INTERIOR, dont le label est -1. Vérifie les dimensions, un pas positif fini et des valeurs intérieures finies. Utilise le module au carré et renvoie un float positif ou nul. Les valeurs de bord retournées nulles par le solveur ne sont pas les traces physiques.

Ajoute check_objective(), non appelée automatiquement. Vérifie le champ nul, l’invariance par une phase complexe et l’indépendance des valeurs extérieures. Avec quatre nœuds intérieurs portant chacun 3+4j et h=0.2, le résultat attendu est 4.0.

Après le code, donne à Antoine la définition du critère à minimiser et ses unités. Il s’agit d’une intégrale de pression au carré, distincte d’une puissance dissipée. La contrainte porte sur une quantité physique de matériau à confirmer avec les poids du mur fournis par Yann.
```

**Contrôle et passage de main.** On lance check_objective() depuis support, puis on transmet le fichier complet à Antoine pour ses ajouts de projection.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** responsable.

**Contribution de Joachim.** On étudie la variation de l’énergie avec la forme du mur et le changement d’une paroi réfléchissante en ouverture.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Étudie le même panneau destiné au RER B avec un côté réfléchissant puis ouvert, sans changer le bord source ni le budget. Les dimensions et le profil restent identiques entre ces deux scénarios. Relie la comparaison au confinement retenu dans le modèle et conserve séparément le scénario du tunnel réfléchissant utilisé pour classer les produits.

Distingue les définitions indicatives de SOTA.md de la dérivation utilisant l’assemblage réel. Le champ total, la convention de Robin et le critère de pression restent ceux du modèle retenu.

Établis l’identité de Green avec la source de Dirichlet non homogène en haut. Dans le scénario ouvert, conserve cette source et remplace seulement un côté latéral par partial_n u-i*k*u=0. Le support représente partial_n u-alpha_code*u=0, donc l’ouverture utilise alpha_code=1j*k. Sépare cette ouverture du mur de conception. Identifie le flux sortant et compare les termes de bord à ceux du même côté Neumann. Une ouverture ne garantit pas une intégrale de pression plus faible à chaque fréquence.

Pour l’étude selon la forme, considère une famille de domaines obtenue en déplaçant le mur, la source supérieure restant fixe et la densité étant transportée avec le mur. Définis le critère sur chaque domaine. Sur une paroi suffisamment régulière, ramène le problème au domaine de référence et différencie sa formulation variationnelle pour exprimer la variation du critère. Précise les hypothèses et le rôle de l’adjoint. Reprends cette étude dans les scénarios réfléchissant et Sommerfeld pour identifier les termes qui changent.

Explique les limites de cette dérivation pour les profils fractals discrétisés et comment les calculs sur plusieurs formes la complètent. Le changement d’étiquette sur une grille n’est pas une dérivée continue de forme. Propose à Yann les deux scénarios numériques comparables, sans remplacer l’étude de forme par le seul gradient de densité.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On présente l’étude avant le point quotidien et on transmet à Yann le scénario de contrôle. Les futures courbes ouverte/réfléchissante seront confrontées à cette identité.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** responsable.

**Contribution de Joachim.** On établit la dérivée par rapport à la répartition du matériau et le système adjoint qui évite une résolution par variable.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

La dérivée doit rester celle du système discret réellement assemblé pour la source du scénario RER B. Vérifie les conjugaisons, le signe et les poids, plutôt que d’utiliser directement la formule indicative de placement du poreux écrite dans SOTA.md. Pour un coût pondéré en fréquence, la dérivée emploie exactement les poids fixés dans le coût.

Distingue les définitions indicatives de SOTA.md de la dérivation utilisant l’assemblage réel. Le champ total, la convention de Robin et le critère de pression restent ceux du modèle retenu.

Établis la dérivée discrète du critère pour A(chi)U=b, avec b indépendant de chi, J=U*WU et * désignant la transposée conjuguée. En prenant l’adjoint A*P=2WU, montre comment obtenir g_l=-Re(P*(dA/dchi_l)U). Le gradient est réel et euclidien. Utilise le champ total, car la source de Dirichlet non homogène est déjà prise en compte dans b.

Relie cette expression à la matrice effectivement assemblée. Avec les coefficients imposés égaux à un et le second membre Robin nul, un contact apporte la dérivée diagonale h*Alpha_code/(1-h*Alpha_code*chi_l)**2. Le dénominateur est un carré complexe. Les contributions des contacts répétés doivent être additionnées. Si b dépendait de chi, sa dérivée devrait aussi être ajoutée.

Explique les entrées que Yann devra transmettre à evaluate_density mardi : A et b complets de taille M*N, cell_weights=h² à l’intérieur et zéro ailleurs, face_rows en indices globaux aplatis, face_design dans le vecteur chi, et dA_diag par contact. Propose un contrôle par différences centrées sur une densité strictement intérieure aux bornes.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On remet la formule et les hypothèses à Yann et Antoine. Le mardi, le test synthétique précède l’intégration, puis Joachim et Yann valident le gradient sur l’assemblage acoustique réel avant la descente.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.
