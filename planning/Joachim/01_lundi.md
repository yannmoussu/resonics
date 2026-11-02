# Joachim — Lundi 2 novembre 2026

**Objectif du jour 1.** Obtenir un premier calcul compréhensible avec le code fourni : un cas RER B, ses paramètres, une figure du champ initial et son énergie. Le groupe présente aussi les choix physiques et les formules demandées. La descente et l’adjoint seront programmés mardi. Aucune nouvelle organisation générale du code n’est à construire lundi.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

**Résultat attendu avant le point quotidien.** Une liste de paramètres, une figure initiale, une valeur d’énergie et les explications de chaque membre. Le coefficient d’exemple du code reste identifié comme tel tant que le matériau n’est pas validé.

## the model to consider,

**Repère :** J1.2. **Rôle :** contributeur.

**Ce qui est fait.** Écrire le modèle mathématique correspondant au programme.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Présente l’équation de Helmholtz et les conditions Dirichlet, Neumann et Robin. Définis u, chi, k et alpha. Utilise le §7.3 du polycopié, en adaptant la position du bord source au programme fourni. Explique que la forme du mur est fixée pendant une optimisation de chi. Donne les équations et une courte interprétation physique, sans écrire de code pour cette contribution.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Un modèle écrit avec des notations définies et cohérentes avec le support.

## formulate the properties of the chosen model, what is known about its solution ;

**Repère :** J1.4. **Rôle :** responsable.

**Ce qui est fait.** Énoncer les propriétés du modèle utiles au premier jour.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

À partir du polycopié, indique les hypothèses qui donnent une solution unique et le rôle de la partie absorbante du coefficient Robin. Distingue le cas physique validé du coefficient d’exemple utilisé pour vérifier le code. Explique les limites d’un argument de coercivité pour Helmholtz, en définissant cette notion si elle est utilisée. Une présentation des hypothèses et du résultat du cours suffit ; ne recopie pas toutes les preuves du polycopié.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Les propriétés annoncées ont leurs hypothèses et leur référence dans le cours.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** contributeur.

**Ce qui est fait.** Calculer simplement l’énergie du champ initial.

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
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Conserve intégralement les deux blocs marqués « Do not modify this cell, these are the values that you will be assessed against. », leurs lignes, commentaires et espaces en début de ligne. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Les modifications du lancement se font seulement dans les blocs « Fell free to modify the function call in this cell. », et les ajouts de fonctions se placent à côté des fonctions étudiantes. Les calculs supplémentaires se font après les blocs protégés, sans modifier leurs tableaux par effet de bord.

Complète seulement your_compute_objective_function(domain_omega,u,spacestep) dans la démonstration. Renvoie un float égal à spacestep**2 multiplié par la somme de abs(u)**2 aux points domain_omega == _env.NODE_INTERIOR. Vérifie que le résultat est réel, positif ou nul. Sur un tableau d’essai portant un champ constant, compare à la formule calculée à la main. Transmets le fichier à Yann pour qu’il ajoute l’affichage de cette valeur après la résolution initiale. Aucun calcul d’adjoint n’est demandé dans cette fonction.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** La fonction du support renvoie réellement l’énergie et le premier champ a une valeur numérique associée.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** responsable.

**Ce qui est fait.** Faire l’étude ouverte/réfléchissante demandée par le sujet.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Établis l’identité énergétique avec la source de Dirichlet conservée. Compare une paroi latérale Neumann à une condition de Sommerfeld et identifie le terme de flux sortant. Pour la variation selon la forme, utilise le cadre régulier du chapitre 5 : source fixe, déplacement du mur et hypothèses annoncées. Distingue cette variation de celle de la répartition chi. Explique ce que l’on peut comparer et ne déduis pas une inégalité universelle entre les énergies intérieures. Cette étude est rendue dans le texte ; aucun deuxième programme de résolution n’est demandé lundi.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une analyse théorique concise répondant au tiret du sujet, avec ses hypothèses et références.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** responsable.

**Ce qui est fait.** Établir la formule du gradient avant de la programmer.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

À partir du §7.5 du polycopié et de la note sur Dirichlet non homogène, écris l’adjoint et la dérivée du critère par rapport à chi. Définis les fonctions et les conjugaisons employées. Vérifie avec Yann le signe de Robin réellement assemblé et le rôle du champ total. Donne les étapes de calcul et le principe d’un contrôle par petites perturbations de chi. L’implémentation et ce contrôle numérique sont prévus mardi. Aucun accès supplémentaire à la matrice n’est à programmer lundi.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une formule expliquée et un algorithme de calcul, prêts à être utilisés le lendemain.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.

**Ordre des modifications du fichier commun.** Joachim complète le coût, puis Yann ajoute les paramètres et l’affichage du premier résultat. Antoine prépare la méthode dans le texte.
