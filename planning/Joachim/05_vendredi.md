# Joachim — Vendredi 6 novembre 2026

**Objectif du jour 5.** Relire les résultats et préparer l’exposé collectif.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Ce qui est fait.** Relire les explications mathématiques finales.

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
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Relis les équations, les définitions et les sources de ta partie. Vérifie que le signe de Robin et la source correspondent au code final.
2. Vérifie que les valeurs citées sont celles des figures conservées, avec les mêmes paramètres.
3. Transmets à Yann seulement les corrections nécessaires et confirme la partie relue.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le lecteur doit comprendre ce qui est imposé au modèle et ce qui a été observé dans les calculs.

**Vérification et résultat à transmettre.** Une partie mathématique relue et une courte liste de corrections éventuelles.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** contributeur.

**Ce qui est fait.** Préparer l’explication orale du modèle et de la dérivée.

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
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Prépare une explication avec le schéma du domaine : source, parois et effet attendu du matériau.
2. Décris l’énergie, puis explique le rôle de l’adjoint et du gradient à l’aide d’un petit déplacement de matériau.
3. Appuie l’interprétation sur une figure du groupe et répète ton passage. L’exposé collectif dure vingt minutes à cinq, suivi de dix minutes de questions.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** À l’oral, on doit pouvoir relier une formule à ce qu’elle représente dans le domaine.

**Vérification et résultat à transmettre.** Un passage oral compréhensible et un exemple simple en cas de question.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Ce qui est fait.** Finaliser le texte mathématique avec les figures du groupe.

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
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Fournis les paragraphes sur le modèle, ses propriétés, l’étude ouverte/réfléchissante et la dérivée. Définis les termes avant de les utiliser.
2. Associe chaque interprétation à la figure concernée et cite les paramètres réellement utilisés. Utilise les références du cours pour les résultats repris.
3. Transmets ton texte à Yann dans le modèle LaTeX commun et relis la version intégrée.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le rapport explique les étapes qui relient la source et les équations au panneau finalement choisi.

**Vérification et résultat à transmettre.** Un texte court, cohérent avec le code, les figures et la présentation.
