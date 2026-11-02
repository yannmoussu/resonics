# Yann — Lundi 2 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

## the model to consider,

**Repère :** J1.2. **Rôle :** responsable.

**Fichier à modifier :** [support/preprocessing.py](../../support/preprocessing.py).

**Ce qui est fait.** On conserve les profils fournis de niveaux zéro, un et deux. On vérifie leurs dimensions réelles et on identifie chaque contact entre un nœud Robin du mur et un nœud intérieur. Ces contacts donnent les longueurs servant à mesurer la quantité de matériau et les indices nécessaires au gradient.

**Fichiers à joindre avec le prompt :**

- `support/preprocessing.py`, version complète actuelle, à modifier.
- `support/_env.py` et `support/processing.py`, en lecture seule pour les étiquettes et le stencil.
- `context/Sujet-EI-EXT-2026.md`.

**Prompt à copier :**

```text
Je travaille sur ResoniCS, un projet d'optimisation acoustique par différences finies. Après le code, présente le modèle : Helmholtz dans l'air, source Dirichlet en haut, côtés Neumann homogènes et mur Robin avec répartition de poreux. Les dimensions, les bandes et la loi de matériau seront validées avec Mathis. Modifie uniquement preprocessing.py joint et renvoie sa version complète. Ne crée aucun autre fichier Python et conserve les fonctions existantes. Les dépendances jointes servent seulement à comprendre les interfaces.

1. Vérifie _set_geometry_of_domain et les fonctions de fractale sur les niveaux 0, 1 et 2. Le motif actuel comporte huit segments de quart à angles droits, malgré le nom create_motif_koch. Conserve ce motif.
2. Le support utilise N colonnes, donc des indices de 0 à N-1, alors que les extrémités du profil sont actuellement définies jusqu'à N. Rends le placement cohérent avec les indices disponibles et annonce les coordonnées réelles. Utilise N-1 intervalles pour une largeur L, donc h=L/(N-1) lors des futurs appels. Pour les niveaux étudiés, choisis N-1 multiple de 4**level afin de représenter les sommets. Place aussi la paroi plane à une ligne cohérente avec ce choix. Ne modifie pas les autres modules pour adapter leurs appels maintenant : indique le changement à Yann.
3. Contrôle les étiquettes, les accès aux quatre voisins, l'absence d'intérieur au bord extérieur du tableau et la connexion du fluide. Le tableau de stockage peut contenir du complémentaire et sa hauteur ne donne pas à elle seule la hauteur du fluide.
4. Ajoute get_design_faces(domain_omega, spacestep, design_mask=None). Le masque optionnel limite la conception aux Robin du mur et permettra d'exclure une ouverture latérale. Retourne un dictionnaire avec boundary_indices, face_rows, face_design et design_weights. boundary_indices contient les indices aplatis des Robin de conception qui touchent au moins un intérieur, triés et uniques. Pour chaque contact intérieur/Robin dans les quatre directions, face_rows donne l'indice aplati de l'intérieur et face_design l'indice correspondant dans boundary_indices. Conserve tous les contacts, même si plusieurs touchent le même Robin. design_weights vaut spacestep multiplié par le nombre de contacts de chaque variable. Les indices aplatis suivent i*N+j, ordre C.
5. Vérifie poids strictement positifs, indices valides, somme des poids égale au pas multiplié par le nombre de contacts, et masque excluant effectivement les Robin non modifiables. La contrainte future sera dot(design_weights,chi)=material_length_m, chi réel entre zéro et un. Il s'agit d'une longueur absorbante absolue, commune entre profils. L'aire égale à un de l'ancien devoir n'est pas une contrainte de cette EI.
6. Donne de petits contrôles exécutables à la demande dans ce même fichier, sans effet à l'import. Les commentaires sont des phrases françaises qui expliquent les étapes, sans équations dans les commentaires. Termine par une courte explication des fonctions ajoutées, de leurs entrées/sorties et des contrôles effectués.
```

**Résultat attendu.** Les trois profils sont représentables sans indice hors du tableau. La largeur et le pas sont annoncés et les poids comptent exactement les contacts du stencil. Le calcul utilise au moins dix points par longueur d'onde et résout aussi les plus petits reliefs. L'ordre de grandeur des reliefs à comparer est une demi-longueur d'onde.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Contribution de Yann.** On confronte les bandes et dimensions proposées par Mathis aux contraintes de résolution et au coût du calcul.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers à joindre

- `support/preprocessing.py`, version actuelle.
- `support/demo_control_polycopie2024.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
À partir des fichiers joints et des valeurs proposées par Mathis, vérifie la compatibilité des dimensions et des bandes avec les différences finies. Ne modifie aucun fichier.
Pour f en Hz, calcule k=2*pi*f/c et lambda=c/f. Vérifie h<=lambda_min/10 et la résolution des plus petits reliefs. Distingue la hauteur réelle du fluide de celle du tableau. Donne les subdivisions nécessaires aux niveaux 0, 1 et 2, avec N-1 multiple de 4**level et h=L/(N-1).
Garde la même excitation supérieure pour les comparaisons. Énumère les valeurs à annoncer au groupe : bande route, bande rail, dimensions, célérité, pas, nombre de points et source. Si ces valeurs ne sont pas encore fournies, donne les relations à appliquer et les informations à obtenir, sans inventer de nombres physiques.
```

**Contrôle et transmission.** Transmettre à Mathis et Olympia les dimensions et résolutions compatibles avant la validation de lundi.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** contributeur.

**Contribution de Yann.** On précise à Joachim comment le solveur distingue la paroi réfléchissante et une ouverture, en conservant la source supérieure.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers à joindre

- `support/processing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Lis le solveur fourni sans modifier les fichiers. Vérifie comment une paroi latérale Neumann peut être remplacée par une Robin de Sommerfeld, avec la source Dirichlet en haut inchangée.
Avec coefficients unitaires et second membre Robin nul, le support impose d_n u-alpha_code*u=0, donc une ouverture a alpha_code=+1j*k. Vérifie ce signe depuis l'assemblage et identifie les étiquettes et masques concernés. Les Robin d'ouverture seront exclues de la conception et du budget.
Donne un protocole de comparaison à mêmes géométrie, source et matériau, ainsi que les traces nécessaires pour calculer un flux. Les zéros renvoyés au bord par solve_helmholtz ne sont pas ces traces. Transmets cette convention à Joachim pour son étude théorique selon la forme et l'identité énergétique. Ne conclus pas à une inégalité de pression intégrée valable à toute fréquence.
```

**Contrôle et transmission.** Joachim valide la convention et la formulation ouverte/réfléchissante. Ce cadrage alimente son étude théorique, les campagnes restent distinctes.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** contributeur.

**Contribution de Yann.** On vérifie avec Mathis le passage du coefficient physique au coefficient utilisé par la condition Robin discrète.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers à joindre

- `support/processing.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Compare, sans modifier les fichiers, la loi complexe préparée par Mathis avec l'assemblage Robin du support. Convention temporelle exp(-i*omega_phys*t), normale sortante, Z_s=pression/vitesse_normale_sortante.
Le coefficient physique de d_n u+alpha_phys*u=0 vaut -1j*omega_phys*rho_air/Z_s ; le support attend alpha_code=-alpha_phys. Sa variable historique omega reçoit k=omega_phys/c. Vérifie les dimensions et le signe par la relation de reconstruction u_B=u_I/(1-h*alpha_code) pour les coefficients unitaires.
Liste les contrôles synthétiques et de passivité à faire avec Mathis. La constante 10-10j de la démonstration n'identifie aucun matériau. Transmets les incohérences éventuelles et les appels attendus, sans annoncer de performance réelle avant validation des données complexes.
```

**Contrôle et transmission.** Mathis reste responsable de l'implémentation dans preprocessing.py ; Yann valide les unités et le signe côté solveur.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** contributeur.

**Fichier à modifier :** [support/processing.py](../../support/processing.py).

**Ce qui est fait.** On sépare l'assemblage de la résolution, afin que Joachim puisse employer exactement la même matrice pour l'état et l'adjoint. On garde le comportement du solveur fourni.

**Fichiers à joindre avec le prompt :**

- `support/processing.py`, version complète actuelle, à modifier.
- `support/_env.py`, `support/preprocessing.py` et `support/demo_control_polycopie2024.py`, en lecture seule.
- `context/Sujet-EI-EXT-2026.md`.

**Prompt à copier :**

```text
Modifie uniquement processing.py joint et renvoie le fichier complet, sans créer de nouveau module. Je veux réutiliser le solveur de Helmholtz fourni et donner sa matrice à un calcul adjoint.

Ajoute assemble_helmholtz_system avec exactement les arguments de solve_helmholtz. Cette fonction reprend l'assemblage actuel, les conditions de Dirichlet, Neumann et Robin, dans le même ordre, puis retourne A au format CSR et b comme vecteur complexe aplati. Garde la matrice complète de taille M*N, avec les lignes identité déjà prévues hors intérieur. Conserve les équations et les coefficients du support. solve_helmholtz appelle ce helper et renvoie toujours le champ de forme (M,N), rempli uniquement à l'intérieur comme auparavant. Ne change pas ses arguments ni la convention d'aplatissement i*N+j.

Le paramètre historique omega reçoit le nombre d'onde k et non les hertz. Avec les coefficients imposés égaux à un et f_rob nul, le Robin actuel reconstruit u_B=u_I/(1-h*alpha_code). Il représente donc d_n u-alpha_code*u=0. Documente ce signe dans l'explication de ta réponse et vérifie la formule depuis le code. Les valeurs nulles que solve_helmholtz renvoie au bord ne représentent pas la trace physique.

Ajoute des contrôles exécutables à la demande dans ce même fichier. Sur une petite grille plane puis irrégulière, compare le champ au comportement initial et vérifie le résidu norm(A@U-b)/max(norm(b),1e-30). Contrôle aussi les dimensions et le type complexe. N'appelle pas les anciennes fonctions non utilisées qui font référence à des étiquettes absentes de _env.py.

Conserve les fonctions existantes. Les commentaires sont de courtes phrases françaises expliquant les étapes. Termine par la signature exacte du helper et les résultats des contrôles, en séparant les contrôles synthétiques des futurs résultats physiques.
```

**À transmettre.** `processing.py` à Joachim et les deux versions courantes au groupe. Pour le cadrage, annoncer le modèle, la source de Dirichlet en haut, les côtés réfléchissants et le mur Robin. Mathis complète les unités et les données physiques, Joachim les propriétés du problème et sa formulation variationnelle. Aucun résultat de matériau n'est annoncé avant validation de sa loi complexe.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.
