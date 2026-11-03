# Mathis — Jeudi 5 novembre 2026

**Objectif du jour.** On vérifie le résultat retenu et on choisit le panneau à présenter.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Ce qui est fait.** Relire les données physiques du cas finalement retenu.

**Fichier à modifier :** `support/preprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/preprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Réutilise compute_alpha dans compute_alpha.py avec les paramètres du programme principal. Explique le coefficient obtenu et ses unités. Les fonctions de maillage et les blocs protégés du programme principal restent inchangés.

1. Vérifie le matériau, ses paramètres et les fréquences réellement utilisées.
2. Vérifie la quantité calculée avec la longueur, l’épaisseur et la profondeur retenues.
3. Si une erreur change les coefficients, préviens Yann avant la dernière comparaison. Garde les données de la littérature séparées des résultats du groupe.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Une courbe d’énergie ne peut être attribuée à un matériau que si son coefficient et sa quantité correspondent au cas annoncé.

**Résultat à transmettre.** Un tableau final de données physiques vérifiées.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Ce qui est fait.** Expliquer le choix du matériau et de sa quantité.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Présente les paramètres du matériau choisi et la quantité du panneau retenu.
2. Appuie le choix sur les résultats obtenus par le groupe et sur les données documentées disponibles.
3. Indique les points de SOTA.md qui restent à étudier pour une application ferroviaire réelle.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le choix final associe le comportement acoustique calculé et la ressource matérielle nécessaire pour l’obtenir.

**Résultat à transmettre.** Une conclusion courte sur le matériau et sa quantité.
