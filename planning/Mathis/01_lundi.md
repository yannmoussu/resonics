# Mathis — Lundi 2 novembre 2026

**Objectif du jour.** On obtient un premier champ et son énergie avec le code fourni. Chacun apporte une explication ou un petit calcul nécessaire au résultat du groupe.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

**À montrer lundi.** Les paramètres, un champ initial, sa valeur d’énergie et les explications du groupe. Les formules demandées sont étudiées lundi, puis utilisées quand la descente est programmée mardi.

## the state of the art ;

**Repère :** J1.1. **Rôle :** contributeur.

**Ce qui est fait.** Réutiliser l’état de l’art déjà fait avec Olympia.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Relis SOTA.md et retiens les informations utiles au bruit de roulement du RER B.
2. Vérifie les sources des plages de fréquences et des performances citées.
3. Transmets à Olympia trois idées utiles au projet et les points restant à confirmer.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** L’état de l’art sert à relier le besoin ferroviaire aux grandeurs du modèle et à choisir une première étude réalisable.

**Résultat à transmettre.** Une courte synthèse sourcée, réutilisable dès lundi.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** responsable.

**Ce qui est fait.** Choisir les paramètres physiques du premier essai.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Reprends la pulsation OMEGA=3430 rad/s, soit environ 545,90 Hz, et c=343 m/s, comme dans le calcul fréquentiel actuel. Annonce ces deux choix comme des hypothèses.
2. La plage 250–2 000 Hz de SOTA.md reste indicative pour le roulement. Propose d’abord 50–3 500 Hz avec la grille actuelle et vérifie avec Yann la règle des dix points par longueur d’onde avant tout élargissement.
3. Pour les comparaisons, fixe une source Dirichlet choisie avec la même phase sur tout le bord supérieur. Note les dimensions réellement représentées et transmets les paramètres au groupe.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Une source identique permet de comparer la réponse des panneaux. Les gaussiennes existantes représentent une hypothèse de spectre et restent une vérification complémentaire.

**Résultat à transmettre.** Un tableau de paramètres pour le premier calcul et la bande envisagée.

## to choose porous material(s) and its quantity ;

**Repère :** J1.7. **Rôle :** responsable.

**Ce qui est fait.** Choisir un seul matériau documenté pour le premier calcul.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Repère un matériau dont les données sont présentes dans les documents. Le cas ISOREL du §3.2.4 du polycopié fournit un exemple documenté.
2. Rassemble ses paramètres et leur provenance dans un petit tableau. Précise les hypothèses nécessaires au coefficient.
3. Reprends la répartition initiale chi du support et annonce sa fraction V_obj. Avec Antoine, précise ensuite comment cette répartition se traduit en longueur ou volume pour les comparaisons entre formes.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le matériau impose un comportement du mur et sa quantité fixe la ressource disponible. Un seul exemple documenté permet de commencer une comparaison physique cohérente.

**Résultat à transmettre.** Un matériau de référence, ses paramètres et une première quantité annoncée.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** responsable.

**Ce qui est fait.** Calculer le coefficient du matériau à la fréquence du premier essai.

**Fichier à modifier :** `support/compute_alpha.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/compute_alpha.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Réutilise compute_alpha dans compute_alpha.py avec les paramètres du programme principal. Explique le coefficient obtenu et ses unités. Les fonctions de maillage et les blocs protégés du programme principal restent inchangés.

1. Utilise la méthode du §3.2.4 du polycopié et les paramètres du matériau retenu. Le cas ISOREL figure page imprimée 47.
2. Réutilise compute_alpha dans support/compute_alpha.py à la pulsation initiale OMEGA=3430 rad/s, puis aux pulsations correspondant aux fréquences de la courbe. La source, CAR_MAT et ALPHA0 sont fournis par le programme principal.
3. Donne la valeur, l’unité et un exemple d’appel. Vérifie le signe avec Yann en comparant la condition Robin physique à celle du solveur. Si un paramètre manque, indique lequel au groupe.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Ce coefficient relie la pression sur le mur et sa dérivée normale. Sa partie complexe traduit l’effet du matériau à la fréquence considérée.

**Résultat à transmettre.** Le coefficient à la pulsation initiale et les données permettant de le retrouver, avec la même convention que le solveur.
