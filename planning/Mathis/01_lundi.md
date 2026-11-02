# Mathis — Lundi 2 novembre 2026

**Objectif du jour 1.** Obtenir un premier calcul compréhensible avec le code fourni : un cas RER B, ses paramètres, une figure du champ initial et son énergie. Le groupe présente aussi les choix physiques et les formules demandées. La descente et l’adjoint seront programmés mardi. Aucune nouvelle organisation générale du code n’est à construire lundi.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

**Résultat attendu avant le point quotidien.** Une liste de paramètres, une figure initiale, une valeur d’énergie et les explications de chaque membre. Le coefficient d’exemple du code reste identifié comme tel tant que le matériau n’est pas validé.

## the state of the art ;

**Repère :** J1.1. **Rôle :** contributeur.

**Ce qui est fait.** Exploiter la synthèse déjà rédigée avec Olympia.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Relis SOTA.md en gardant le cas RER B. Vérifie les sources des bandes de bruit, des exemples industriels et des performances chiffrées. Fournis à Olympia les corrections ou incertitudes importantes. Il suffit d’une synthèse courte : besoin, solutions existantes et choix que le projet va tester.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** La synthèse est réutilisée et ses points à confirmer sont identifiés.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** responsable.

**Ce qui est fait.** Choisir un premier cas simple de bruit du RER B.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Propose le roulement comme premier cas et 500 Hz comme fréquence d’essai, dans la plage indicative 250–2 000 Hz de SOTA.md. Fais valider ces choix par le groupe. Le polycopié utilise c=340 m/s ; indique cette valeur et sa provenance si elle est retenue. Définis une source de Dirichlet uniforme en haut pour comparer les panneaux. Si aucun spectre mesuré n’est fourni, présente cette excitation comme un essai du modèle. Donne une courte liste des dimensions et paramètres à transmettre à Yann. Les autres types de bruit seront examinés après ce premier calcul.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Un seul scénario, une fréquence d’essai et une source sont choisis pour le premier jour.

## to choose porous material(s) and its quantity ;

**Repère :** J1.7. **Rôle :** responsable.

**Ce qui est fait.** Retenir un matériau documenté et annoncer sa quantité.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Choisis d’abord un seul matériau dont le coefficient peut être calculé à partir des documents fournis. Le cas ISOREL du polycopié, §3.2.4, fournit un point de départ documenté pour le calcul ; compare-le aux matériaux de SOTA.md seulement si leurs données sont disponibles. Donne les paramètres, leur origine et les hypothèses. Pour le premier calcul, utilise la répartition chi déjà créée par le support et annonce la fraction V_obj qu’il calcule. Cette fraction de points n’est pas présentée comme un volume. La mesure physique de quantité sera précisée avant de comparer des formes différentes.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Un matériau de référence et une quantité clairement définie, sans étude comparative étendue dès lundi.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** responsable.

**Ce qui est fait.** Calculer le coefficient du matériau à la fréquence du premier essai.

**Fichier à modifier :** `support/preprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/preprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Modifie seulement preprocessing.py en ajoutant ou corrigeant la fonction du projet demandée. Garde inchangées les fonctions initialement fournies, notamment _set_coefficients_of_pde, _set_rhs_of_pde et _set_geometry_of_domain. Les blocs protégés du programme principal et les autres fichiers restent inchangés.

Utilise le §3.2.4 du polycopié pour calculer le coefficient complexe à la fréquence choisie. Le cas ISOREL et ses paramètres sont donnés page imprimée 47. Précise les paramètres complémentaires du calcul et les hypothèses, notamment la source plane si elle est retenue. Vérifie les unités, la convention temporelle et le signe avec Yann. Si une fonction est nécessaire, ajoute seulement compute_alpha dans preprocessing.py : elle reçoit la fréquence et les paramètres annoncés, puis renvoie le coefficient complexe. Donne un exemple d’appel pour une fréquence. N’ajoute pas de système général de matériaux ni de fichier Python. Si une donnée manque, indique précisément laquelle et conserve le coefficient du support seulement pour un essai de fonctionnement, clairement identifié comme tel.

Pour les coefficients unitaires et f_rob nul, le code utilise u_B=u_I/(1-h*Alpha), donc la condition d_n u-Alpha*u=0. Si le coefficient physique est défini par d_n u+alpha*u=0, on utilise Alpha=-alpha après vérification des unités.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une valeur calculée et justifiée pour le premier essai, ou la liste précise des données qui empêchent ce calcul.
