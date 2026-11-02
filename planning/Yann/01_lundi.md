# Yann — Lundi 2 novembre 2026

**Objectif du jour 1.** Obtenir un premier calcul compréhensible avec le code fourni : un cas RER B, ses paramètres, une figure du champ initial et son énergie. Le groupe présente aussi les choix physiques et les formules demandées. La descente et l’adjoint seront programmés mardi. Aucune nouvelle organisation générale du code n’est à construire lundi.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

**Résultat attendu avant le point quotidien.** Une liste de paramètres, une figure initiale, une valeur d’énergie et les explications de chaque membre. Le coefficient d’exemple du code reste identifié comme tel tant que le matériau n’est pas validé.

## the model to consider,

**Repère :** J1.2. **Rôle :** responsable.

**Ce qui est fait.** Décrire le modèle et lancer un premier calcul avec le programme fourni.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Conserve intégralement les deux blocs marqués « Do not modify this cell, these are the values that you will be assessed against. », leurs lignes, commentaires et espaces en début de ligne. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Les modifications du lancement se font seulement dans les blocs « Fell free to modify the function call in this cell. », et les ajouts de fonctions se placent à côté des fonctions étudiantes. Les calculs supplémentaires se font après les blocs protégés, sans modifier leurs tableaux par effet de bord.

Utilise directement _set_geometry_of_domain et solve_helmholtz tels qu’ils sont fournis. Explique le domaine, la source de Dirichlet en haut, les côtés réfléchissants Neumann et le mur Robin. Garde une seule géométrie pour ce premier essai. Le réglage actuel level=1 peut être conservé ; level=0 sert de référence plane si nécessaire. Dans les blocs autorisés, renseigne une fréquence d’essai et la célérité, puis calcule wavenumber=2*pi*frequency_hz/c. La proposition de départ est 500 Hz et c=340 m/s, valeur utilisée dans le polycopié, à confirmer dans le tableau de paramètres. Garde N et M du support si le pas respecte h<=c/(10*frequency_hz). Relève les dimensions effectivement représentées. Lance le fichier et conserve une figure du champ initial. Le calcul d’énergie sera fourni par Joachim. Aucun nouveau générateur, aucune nouvelle méthode de rangement des données et aucune préparation de l’adjoint ne sont demandés ici.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Un schéma ou une figure du domaine, les paramètres de l’essai et une figure du champ initial.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier que le premier essai est compatible avec la grille.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Avec les choix proposés par Mathis, calcule k=2*pi*f/c et lambda=c/f. Vérifie le pas h du programme et la règle d’au moins dix points par longueur d’onde. Sépare la fréquence unique du premier essai et la bande qui sera étudiée mardi. Note N, M, h, level, les dimensions du domaine, la fréquence et la source. Lis les coordonnées produites par le code et signale un écart éventuel entre dimensions prévues et dimensions représentées. Garde la discrétisation et le générateur fournis.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le tableau de paramètres indique les unités et montre que la résolution du premier essai convient.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** contributeur.

**Ce qui est fait.** Relier les conditions aux limites du code à l’étude théorique de Joachim.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Lis les conditions Neumann et Robin dans processing.py et explique à Joachim quelle paroi réfléchissante pourrait devenir ouverte. Conserve la source supérieure. Vérifie la convention de signe employée par compute_robin_condition avant de traduire la condition de Sommerfeld. Donne cette correspondance dans ta réponse. Le lundi, cette contribution est une analyse du modèle et ne demande pas de programmer un deuxième cas.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Joachim dispose des conventions du code pour son étude ouverte/réfléchissante.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier les unités et le signe du coefficient calculé par Mathis.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Compare le coefficient physique obtenu par Mathis à la condition Robin réellement assemblée par processing.py. Vérifie les unités et les arguments reçus par solve_helmholtz. Distingue le nombre d’onde k, la pulsation et la fréquence en hertz. La valeur Alpha=10-10j du fichier initial est un coefficient d’exemple ; elle peut vérifier le fonctionnement du programme mais ne suffit pas à représenter un matériau choisi pour le RER B. Une fois la correspondance validée, Yann pourra modifier Alpha dans le bloc autorisé.

Pour les coefficients unitaires et f_rob nul, le code utilise u_B=u_I/(1-h*Alpha), donc la condition d_n u-Alpha*u=0. Si le coefficient physique est défini par d_n u+alpha*u=0, on utilise Alpha=-alpha après vérification des unités.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une valeur de coefficient a une origine et une convention de signe annoncées.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** contributeur.

**Ce qui est fait.** Comprendre les données nécessaires au futur calcul du gradient.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Avec Joachim, repère où chi intervient dans alpha_rob=Alpha*chi et comment compute_robin_condition utilise cette valeur. Écris la dépendance à conserver pour le gradient de mardi. Lis seulement les fonctions existantes. Lundi, on ne crée ni fonction d’assemblage supplémentaire ni tableau de correspondance des points du mur.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Joachim connaît la dépendance du système à chi ; aucun travail supplémentaire de préparation du code n’est requis.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.

**Ordre des modifications du fichier commun.** Joachim complète le coût, puis Yann ajoute les paramètres et l’affichage du premier résultat. Antoine prépare la méthode dans le texte.
