# Yann — Lundi 2 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## the model to consider,

**Repère :** J1.2. **Rôle :** responsable.

**Fichier à modifier :** [support/preprocessing.py](../../support/preprocessing.py).

**Ce qui est fait.** On ajoute un helper pour les campagnes utilisant les profils fournis de niveaux zéro, un et deux, en conservant le générateur initial. On vérifie leurs dimensions réelles et on identifie chaque contact entre un nœud Robin du mur et un nœud intérieur. Ces contacts donnent les longueurs servant à mesurer la quantité de matériau et les indices nécessaires au gradient.

**Fichiers concernés avec le prompt :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py`, version complète actuelle, à modifier.
- `support/_env.py` et `support/processing.py`, en lecture seule pour les étiquettes et le stencil.
- `context/Sujet-EI-EXT-2026.md`.

**Contexte :**

```text
Protection du support : les cellules protégées du programme principal sont en lecture seule. Garde aussi inchangées les fonctions initialement fournies de preprocessing.py, notamment _set_coefficients_of_pde, _set_rhs_of_pde, _set_geometry_of_domain et les fonctions du motif qu’elle appelle. Ajoute les fonctions du projet à côté ; seules ces fonctions ajoutées peuvent être complétées ou corrigées. Elles travaillent sur des tableaux indépendants et ne changent pas les valeurs du cas initial par effet de bord. Compare les fonctions fournies à la version jointe avant de rendre le fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le modèle représente un panneau destiné au bruit du RER B dans le tunnel réfléchissant demandé par l’énoncé. Décris le domaine et ses dimensions physiques, le profil fourni et la source de Dirichlet supérieure. La paroi rigide et les côtés Neumann sont les hypothèses du modèle. Choisis un profil physique fixe pour les comparaisons en fréquence ; le motif orthogonal fourni reste celui effectivement calculé.

Vérifie en particulier que la largeur physique, les reliefs et le pas permettent les fréquences retenues et que la source supérieure conserve la convention du support.

Je travaille sur ResoniCS, un projet d'optimisation acoustique par différences finies. Après le code, présente le modèle : Helmholtz dans l'air, source Dirichlet en haut, côtés Neumann homogènes et mur Robin avec répartition de poreux. Les dimensions, les bandes et la loi de matériau seront validées avec Mathis. Modifie uniquement preprocessing.py joint et renvoie sa version complète. Ne crée aucun autre fichier Python et conserve les fonctions existantes. Les dépendances jointes servent seulement à comprendre les interfaces.

1. Lis _set_geometry_of_domain et les fonctions de fractale sur les niveaux 0, 1 et 2 sans modifier leurs lignes. Le motif fourni comporte huit segments de quart à angles droits, malgré le nom create_motif_koch. Garde ce motif et le comportement initial des fonctions fournies.
2. Ajoute prepare_geometry_of_domain(M, N, level=0) dans preprocessing.py pour les campagnes, avec le même type de retour à cinq valeurs que _set_geometry_of_domain. Elle construit ses propres tableaux et réutilise les fonctions de motif en lecture seule. Dans ce nouveau helper seulement, définis les extrémités et la paroi plane dans les indices de 0 à N-1. Pour une largeur physique L, les campagnes emploient h=L/(N-1), avec N-1 multiple de 4**level pour les niveaux étudiés. Ne remplace pas l’appel protégé à _set_geometry_of_domain et ne redéfinis pas cette fonction sous le même nom. Transmets la nouvelle signature à Yann pour ses appels de campagne.
3. Dans les tableaux du nouveau helper, contrôle les étiquettes, les accès aux quatre voisins, l’absence d’intérieur au bord extérieur et la connexion du fluide. Le tableau peut contenir du complémentaire et sa hauteur ne donne pas à elle seule la hauteur du fluide. Le cas initial fourni reste disponible avec ses coordonnées d’origine.
4. Ajoute get_design_faces(domain_omega, spacestep, design_mask=None). Le masque optionnel limite la conception aux Robin du mur et permettra d'exclure une ouverture latérale. Retourne un dictionnaire avec boundary_indices, face_rows, face_design et design_weights. boundary_indices contient les indices aplatis des Robin de conception qui touchent au moins un intérieur, triés et uniques. Pour chaque contact intérieur/Robin dans les quatre directions, face_rows donne l'indice aplati de l'intérieur et face_design l'indice correspondant dans boundary_indices. Conserve tous les contacts, même si plusieurs touchent le même Robin. design_weights vaut spacestep multiplié par le nombre de contacts de chaque variable. Les indices aplatis suivent i*N+j, ordre C.
5. Vérifie poids strictement positifs, indices valides, somme des poids égale au pas multiplié par le nombre de contacts, et masque excluant effectivement les Robin non modifiables. La contrainte future sera dot(design_weights,chi)=material_length_m, chi réel entre zéro et un. Il s'agit d'une longueur absorbante absolue, commune entre profils. L'aire égale à un de l'ancien devoir n'est pas une contrainte de cette EI.
6. Donne de petits contrôles exécutables à la demande dans ce même fichier, sans effet à l'import. Les commentaires sont des phrases françaises qui expliquent les étapes, sans équations dans les commentaires. Termine par une courte explication des fonctions ajoutées, de leurs entrées/sorties et des contrôles effectués.
```

**Résultat attendu.** Les trois profils sont représentables sans indice hors du tableau. La largeur et le pas sont annoncés et les poids comptent exactement les contacts du stencil. Le calcul utilise au moins dix points par longueur d'onde et résout aussi les plus petits reliefs. L'ordre de grandeur des reliefs à comparer est une demi-longueur d'onde.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Contribution de Yann.** On confronte les bandes et dimensions proposées par Mathis aux contraintes de résolution et au coût du calcul.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py`, version actuelle.
- `support/demo_control_polycopie2024.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Contexte

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le choix d’application est désormais le RER B. Prends le roulement de 250 à 2 000 Hz comme première plage proposée, puis considère traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz comme cas complémentaires. Ces plages viennent de SOTA.md, pas d’un spectre mesuré fourni. Fais valider le régime, la bande, le site ou la section-type, la vitesse si elle est connue, les dimensions, la source et les données de matériau. Calcule le pas nécessaire à la fréquence maximale réellement étudiée et résous les reliefs. La règle des détails de l’ordre de lambda/2 guide le choix d’un panneau fixe et ne conduit pas à redimensionner le panneau à chaque fréquence.

Vérifie en particulier que la largeur physique, les reliefs et le pas permettent les fréquences retenues et que la source supérieure conserve la convention du support.

À partir des fichiers joints et des valeurs proposées par Mathis, vérifie la compatibilité des dimensions et des bandes avec les différences finies. Ne modifie aucun fichier.
Pour f en Hz, calcule k=2*pi*f/c et lambda=c/f. Vérifie h<=lambda_min/10 et la résolution des plus petits reliefs. Distingue la hauteur réelle du fluide de celle du tableau. Donne les subdivisions nécessaires aux niveaux 0, 1 et 2, avec N-1 multiple de 4**level et h=L/(N-1).
Garde la même excitation supérieure pour les comparaisons. Énumère les valeurs à annoncer au groupe : régime de bruit RER B, bande retenue, dimensions, célérité, pas, nombre de points et source. Si ces valeurs ne sont pas encore fournies, donne les relations à appliquer et les informations à obtenir, sans inventer de nombres physiques.
```

**Contrôle et transmission.** Transmettre à Mathis et Olympia les dimensions et résolutions compatibles avant la validation de lundi.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** contributeur.

**Contribution de Yann.** On précise à Joachim comment le solveur distingue la paroi réfléchissante et une ouverture, en conservant la source supérieure.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/processing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Contexte

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Étudie le même panneau destiné au RER B avec un côté réfléchissant puis ouvert, sans changer le bord source ni le budget. Les dimensions et le profil restent identiques entre ces deux scénarios. Relie la comparaison au confinement retenu dans le modèle et conserve séparément le scénario du tunnel réfléchissant utilisé pour classer les produits.

Vérifie en particulier que la largeur physique, les reliefs et le pas permettent les fréquences retenues et que la source supérieure conserve la convention du support.

Lis le solveur fourni sans modifier les fichiers. Vérifie comment une paroi latérale Neumann peut être remplacée par une Robin de Sommerfeld, avec la source Dirichlet en haut inchangée.
Avec coefficients unitaires et second membre Robin nul, le support impose d_n u-alpha_code*u=0, donc une ouverture a alpha_code=+1j*k. Vérifie ce signe depuis l'assemblage et identifie les étiquettes et masques concernés. Les Robin d'ouverture seront exclues de la conception et du budget.
Donne un protocole de comparaison à mêmes géométrie, source et matériau, ainsi que les traces nécessaires pour calculer un flux. Les zéros renvoyés au bord par solve_helmholtz ne sont pas ces traces. Transmets cette convention à Joachim pour son étude théorique selon la forme et l'identité énergétique. Ne conclus pas à une inégalité de pression intégrée valable à toute fréquence.
```

**Contrôle et transmission.** Joachim valide la convention et la formulation ouverte/réfléchissante. Ce cadrage alimente son étude théorique, les campagnes restent distinctes.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** contributeur.

**Contribution de Yann.** On vérifie avec Mathis le passage du coefficient physique au coefficient utilisé par la condition Robin discrète.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/processing.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Contexte

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Calcule la loi complexe sur les fréquences du scénario RER B retenu, en priorité la plage de roulement proposée. Les autres plages seront calculées seulement dans la validité de cette loi. Garde séparés la bande, les paramètres du matériau et leur provenance. La synthèse SOTA.md oriente les matériaux candidats et ne fournit pas à elle seule les paramètres d’une impédance complexe.

Vérifie en particulier que la largeur physique, les reliefs et le pas permettent les fréquences retenues et que la source supérieure conserve la convention du support.

Compare, sans modifier les fichiers, la loi complexe préparée par Mathis avec l'assemblage Robin du support. Convention temporelle exp(-i*omega_phys*t), normale sortante, Z_s=pression/vitesse_normale_sortante.
Le coefficient physique de d_n u+alpha_phys*u=0 vaut -1j*omega_phys*rho_air/Z_s ; le support attend alpha_code=-alpha_phys. Sa variable historique omega reçoit k=omega_phys/c. Vérifie les dimensions et le signe par la relation de reconstruction u_B=u_I/(1-h*alpha_code) pour les coefficients unitaires.
Liste les contrôles synthétiques et de passivité à faire avec Mathis. La constante 10-10j de la démonstration n'identifie aucun matériau. Transmets les incohérences éventuelles et les appels attendus, sans annoncer de performance réelle avant validation des données complexes.
```

**Contrôle et transmission.** Mathis reste responsable de l'implémentation dans preprocessing.py ; Yann valide les unités et le signe côté solveur.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** contributeur.

**Fichier à modifier :** [support/processing.py](../../support/processing.py).

**Ce qui est fait.** On ajoute une fonction qui expose la matrice et le second membre pour l’état et l’adjoint, en reproduisant la composition du solveur fourni. Le solveur initial et les appels protégés restent inchangés.

**Fichiers concernés avec le prompt :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/processing.py`, version complète actuelle, à modifier.
- `support/_env.py`, `support/preprocessing.py` et `support/demo_control_polycopie2024.py`, en lecture seule.
- `context/Sujet-EI-EXT-2026.md`.

**Contexte :**

```text
Protection du support : conserve intégralement solve_helmholtz et les fonctions d’assemblage initialement fournies, car elles déterminent le calcul appelé par la cellule protégée. Ajoute seulement les fonctions complémentaires demandées dans processing.py, en réutilisant les fonctions existantes sans les modifier. Aucun remplacement ou redirection de solve_helmholtz. Compare les fonctions fournies à la version jointe avant de rendre le fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

La dérivée doit rester celle du système discret réellement assemblé pour la source du scénario RER B. Vérifie les conjugaisons, le signe et les poids, plutôt que d’utiliser directement la formule indicative de placement du poreux écrite dans SOTA.md. Pour un coût pondéré en fréquence, la dérivée emploie exactement les poids fixés dans le coût.

Vérifie en particulier que la largeur physique, les reliefs et le pas permettent les fréquences retenues et que la source supérieure conserve la convention du support.

Modifie uniquement processing.py joint et renvoie le fichier complet, sans créer de nouveau module. Je veux réutiliser le solveur de Helmholtz fourni et donner sa matrice à un calcul adjoint.

Ajoute assemble_helmholtz_system avec exactement les arguments de solve_helmholtz. Cette fonction reprend l'assemblage actuel, les conditions de Dirichlet, Neumann et Robin, dans le même ordre, puis retourne A au format CSR et b comme vecteur complexe aplati. Garde la matrice complète de taille M*N, avec les lignes identité déjà prévues hors intérieur. Conserve les équations et les coefficients du support. Ce nouveau helper est indépendant : il appelle les fonctions compute_stiffness_matrix, compute_mass_matrix puis compute_dirichlet_condition, compute_neumann_condition et compute_robin_condition, dans l’ordre du solveur fourni. solve_helmholtz et toutes ces fonctions restent exactement inchangées. Ne remplace pas l’appel du bloc protégé par le nouveau helper. Garde la convention d’aplatissement i*N+j et compare les solutions des deux chemins sur les mêmes données.

Le paramètre historique omega reçoit le nombre d'onde k et non les hertz. Avec les coefficients imposés égaux à un et f_rob nul, le Robin actuel reconstruit u_B=u_I/(1-h*alpha_code). Il représente donc d_n u-alpha_code*u=0. Documente ce signe dans l'explication de ta réponse et vérifie la formule depuis le code. Les valeurs nulles que solve_helmholtz renvoie au bord ne représentent pas la trace physique.

Ajoute des contrôles exécutables à la demande dans ce même fichier. Sur une petite grille plane puis irrégulière, compare le champ au comportement initial et vérifie le résidu norm(A@U-b)/max(norm(b),1e-30). Contrôle aussi les dimensions et le type complexe. N'appelle pas les anciennes fonctions non utilisées qui font référence à des étiquettes absentes de _env.py.

Conserve les fonctions existantes. Les commentaires sont de courtes phrases françaises expliquant les étapes. Termine par la signature exacte du helper et les résultats des contrôles, en séparant les contrôles synthétiques des futurs résultats physiques.
```

**À transmettre.** `processing.py` à Joachim et les deux versions courantes au groupe. Pour le cadrage, annoncer le modèle, la source de Dirichlet en haut, les côtés réfléchissants et le mur Robin. Mathis complète les unités et les données physiques, Joachim les propriétés du problème et sa formulation variationnelle. Aucun résultat de matériau n'est annoncé avant validation de sa loi complexe.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.
