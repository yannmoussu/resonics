# Joachim — Mardi, 3 novembre 2026

Objectif : calculer un gradient fiable avant la première descente acoustique.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — État adjoint et contrôle par différences centrées

**Fichier à compléter :** `support/demo_control_polycopie2024.py`, en ajoutant `evaluate_density` et `check_gradient`, sans modifier les fonctions d'Antoine ni le lancement des campagnes.

**Ce qu'on fait.** On résout le système direct, puis un système adjoint complexe. Chaque face de mur contribue au gradient de sa variable de matériau. On vérifie ce gradient avec de petites perturbations du coût avant de l'utiliser pour optimiser.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, version complète contenant le critère de lundi et la projection d'Antoine
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Dirichlet_Nonhomogene.pdf`
- `context/GAllaire-OptimParam.pdf`, pages PDF 25 à 29
- `context/Sujet-EI-EXT-2026.md`


**Prompt à copier :**

```text
Ajoute uniquement dans demo_control_polycopie2024.py la fonction evaluate_density(chi, assemble, with_gradient=True), et une fonction check_gradient() non appelée automatiquement. Conserve les autres travaux du fichier. Ne crée aucun autre fichier.

chi est un vecteur réel de taille B, compris entre zéro et un. assemble est une fonction donnée par Yann : payload=assemble(chi). Elle renvoie un dictionnaire contenant A, b, cell_weights, face_rows, face_design et dA_diag. A est une matrice creuse complexe de taille MN par MN issue de l'assemblage avec élimination des conditions de bord ; b est aplati. Les poids cell_weights de taille MN valent h² à l'intérieur et zéro ailleurs. face_rows contient les indices globaux aplatis des intérieurs voisins des faces de conception, face_design les indices dans chi et dA_diag les dérivées complexes diagonales par face. Les indices peuvent se répéter. Le second membre b est indépendant de chi.

Résous A U=b avec scipy.sparse.linalg.spsolve. Calcule J=Re(vdot(U,cell_weights*U)). Si with_gradient est vrai, résous A.conj().T P=2*cell_weights*U, puis accumule pour chaque face -Re(conj(P[row])*dA_diag*U[row]) dans le gradient à l'indice face_design. Utilise numpy.add.at pour les répétitions. Le gradient est réel et euclidien, sans division par les poids de longueur. N'utilise aucune inverse explicite.

Pour les coefficients unitaires du support et f_rob nul, Yann transmet dA_diag=h*Alpha_code/(1-h*Alpha_code*chi_l)**2. Le dénominateur est un carré complexe. Vérifie les dimensions, la finitude et les indices. Les poids cellulaires peuvent être nuls hors du fluide. Le champ total est utilisé et le Dirichlet imposé figure déjà dans b.

Renvoie un dictionnaire avec value, gradient, u, state_residual et adjoint_residual. u est le vecteur complexe aplati de longueur MN. Sans gradient, les deux champs relatifs à l'adjoint valent None et aucune résolution adjointe n'est effectuée. Les résidus sont les normes des défauts de système divisées par max(norme du second membre,1e-30).

Pour check_gradient(), construis localement un petit assembleur synthétique inversible, avec une variable intervenant sur deux lignes et deux variables partageant une ligne. Vérifie la dérivée directionnelle g.dot(d) par (J(chi+t*d)-J(chi-t*d))/(2*t), pour plusieurs t entre 1e-2 et 1e-6 et une densité strictement entre zéro et un. Vérifie également le même coût avec et sans gradient et l'invariance par phase de b. Ne présente pas ces essais comme des performances de matériau.

Ajoute des commentaires en phrases françaises, sans équations. Renvoie le fichier complet, une explication courte et les tests réellement exécutés ou leurs appels si tu ne peux pas les lancer.
```

**Vérification et transmission.** On lance le test synthétique, puis le même contrôle centré avec l'assemblage réel transmis par Yann. On attend une baisse initiale de l'erreur avant la limite d'arrondi. On remet ensuite le fichier à Antoine, qui peut activer la descente uniquement après validation du gradient.
