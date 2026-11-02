# Joachim — Mardi 3 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution de Joachim. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Contribution de Joachim.** On programme l’état adjoint et le gradient, puis on les vérifie avant les descentes à une fréquence problématique.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis les fréquences problématiques parmi les pics confirmés de la réponse du panneau sur la bande RER B retenue, d’abord le roulement. Identifie le régime de bruit et la fréquence de chaque descente. Recalcule ensuite la réponse sur la bande pour vérifier qu’une baisse à ce pic ne dégrade pas excessivement les autres fréquences.

Le contrôle du gradient acoustique réel utilise la source et les coefficients du scénario RER B sélectionné, après le contrôle synthétique indépendant.

Ajoute uniquement dans demo_control_polycopie2024.py la fonction evaluate_density(chi, assemble, with_gradient=True), et une fonction check_gradient() non appelée automatiquement. Conserve les autres travaux du fichier. Ne crée aucun autre fichier.

chi est un vecteur réel de taille B, compris entre zéro et un. assemble est une fonction donnée par Yann : payload=assemble(chi). Elle renvoie un dictionnaire contenant A, b, cell_weights, face_rows, face_design et dA_diag. A est une matrice creuse complexe de taille MN par MN issue de l'assemblage avec élimination des conditions de bord ; b est aplati. Les poids cell_weights de taille MN valent h² à l'intérieur et zéro ailleurs. face_rows contient les indices globaux aplatis des intérieurs voisins des faces de conception, face_design les indices dans chi et dA_diag les dérivées complexes diagonales par face. Les indices peuvent se répéter. Le second membre b est indépendant de chi.

Résous A U=b avec scipy.sparse.linalg.spsolve. Calcule J=Re(vdot(U,cell_weights*U)). Si with_gradient est vrai, résous A.conj().T P=2*cell_weights*U, puis accumule pour chaque face -Re(conj(P[row])*dA_diag*U[row]) dans le gradient à l'indice face_design. Utilise numpy.add.at pour les répétitions. Le gradient est réel et euclidien, sans division par les poids de longueur. N'utilise aucune inverse explicite.

Pour les coefficients unitaires du support et f_rob nul, Yann transmet dA_diag=h*Alpha_code/(1-h*Alpha_code*chi_l)**2. Le dénominateur est un carré complexe. Vérifie les dimensions, la finitude et les indices. Les poids cellulaires peuvent être nuls hors du fluide. Le champ total est utilisé et le Dirichlet imposé figure déjà dans b.

Renvoie un dictionnaire avec value, gradient, u, state_residual et adjoint_residual. u est le vecteur complexe aplati de longueur MN. Sans gradient, les deux champs relatifs à l'adjoint valent None et aucune résolution adjointe n'est effectuée. Les résidus sont les normes des défauts de système divisées par max(norme du second membre,1e-30).

Pour check_gradient(), construis localement un petit assembleur synthétique inversible, avec une variable intervenant sur deux lignes et deux variables partageant une ligne. Vérifie la dérivée directionnelle g.dot(d) par (J(chi+t*d)-J(chi-t*d))/(2*t), pour plusieurs t entre 1e-2 et 1e-6 et une densité strictement entre zéro et un. Vérifie également le même coût avec et sans gradient et l'invariance par phase de b. Ne présente pas ces essais comme des performances de matériau.

Ajoute des commentaires en phrases françaises, sans équations. Renvoie le fichier complet, une explication courte et les tests réellement exécutés ou leurs appels si tu ne peux pas les lancer.
```

**Contrôle et passage de main.** On vérifie d’abord le cas synthétique, puis on transmet le fichier à Antoine. Après intégration par Yann, on refait le contrôle centré sur l’assemblage acoustique réel avant le premier lancement de descente.
