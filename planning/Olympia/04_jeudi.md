# Olympia — Jeudi 5 novembre 2026

**Objectif du jour.** On vérifie le résultat retenu et on choisit le panneau à présenter.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[-50, 50]`. Le coefficient suit la convention `d_n u - alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** responsable.

**Ce qui est fait.** Sélectionner les figures qui soutiennent le choix final.

**Fichier à modifier :** `support/postprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures demandées. Conserve les noms et arguments utilisés par les appels existants. Les fonctions fournies, les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Compare le résultat retenu à la référence et à la vérification sur grille plus fine transmise par Yann.
2. Vérifie les mêmes source et quantité, puis note si les principaux pics restent comparables.
3. Retiens les figures utiles à la décision et rassemble les valeurs décisives dans un tableau court.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Un choix reste crédible si son avantage se retrouve lorsque l’on améliore la description numérique du même cas.

**Résultat à transmettre.** Quelques figures cohérentes et un tableau de décision court.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** responsable.

**Ce qui est fait.** Expliquer le compromis retenu par le groupe.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Choisis la figure qui compare le mieux les formes et les quantités étudiées.
2. Explique avec les valeurs obtenues pourquoi le panneau retenu paraît intéressant pour la bande calculée.
3. Fais valider avec le groupe la forme, le matériau et la quantité annoncés.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le produit proposé résulte d’un compromis entre la diminution des oscillations et la quantité de matériau, pour le scénario étudié.

**Résultat à transmettre.** Une conclusion commune accompagnée d’une figure lisible.
