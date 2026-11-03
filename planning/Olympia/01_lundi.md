# Olympia — Lundi 2 novembre 2026

**Objectif du jour.** On obtient un premier champ et son énergie avec le code fourni. Chacun apporte une explication ou un petit calcul nécessaire au résultat du groupe.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

**À montrer lundi.** Les paramètres, un champ initial, sa valeur d’énergie et les explications du groupe. Les formules demandées sont étudiées lundi, puis utilisées quand la descente est programmée mardi.

## the state of the art ;

**Repère :** J1.1. **Rôle :** responsable.

**Ce qui est fait.** Présenter l’état de l’art déjà rédigé avec Mathis.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Reprends SOTA.md et sélectionne trois points utiles au RER B : besoin, solutions existantes et idée du mur irrégulier avec poreux.
2. Associe chaque information chiffrée à sa source.
3. Prépare une synthèse à montrer au premier point avec les enseignants.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le projet teste une solution acoustique dans un modèle simple. L’état de l’art explique pourquoi cette piste mérite d’être étudiée.

**Résultat à transmettre.** Une synthèse courte qui sépare les résultats publiés et les calculs à faire.

## the model to consider,

**Repère :** J1.2. **Rôle :** contributeur.

**Ce qui est fait.** Rendre la première figure de Yann compréhensible.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Repère sur le domaine la source en haut, les côtés réfléchissants et le mur du bas.
2. Lis la légende de couleur avec Yann et précise s’il s’agit de la partie réelle du champ ou de son module.
3. Ajoute une légende explicative ou un petit schéma dans ta réponse. Indique la fréquence et les paramètres du calcul.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** La partie réelle représente une composante oscillante et peut changer de signe. Le module permet de voir où l’amplitude de pression est la plus forte.

**Résultat à transmettre.** Une figure initiale annotée ou une légende qui permet de la lire.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Ce qui est fait.** Préparer les trois premières comparaisons.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Avec les paramètres de Mathis, liste les essais de mardi : mur plan entièrement recouvert, mur irrégulier entièrement recouvert et répartition initiale sur une même forme.
2. Note la source choisie et la bande retenue, identiques pour comparer les cas.
3. Demande à Yann les fréquences et les énergies de chaque essai, accompagnées du nom de la forme et de la quantité utilisée.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Changer un paramètre à la fois permet de comprendre l’effet du relief puis celui de la quantité et de la répartition du matériau.

**Résultat à transmettre.** La liste des premiers cas à tracer, sans préparation de nouveaux programmes.
