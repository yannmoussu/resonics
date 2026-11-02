# Mathis — Jeudi 5 novembre 2026

**Objectif du jour 4.** Vérifier les meilleurs résultats et choisir un produit. On limite les nouveaux essais à ceux qui peuvent changer la conclusion.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Ce qui est fait.** Valider les paramètres physiques des cas retenus.

**Fichier à modifier :** `support/preprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/preprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement preprocessing.py en ajoutant ou corrigeant la fonction du projet demandée. Garde inchangées les fonctions initialement fournies, notamment _set_coefficients_of_pde, _set_rhs_of_pde et _set_geometry_of_domain. Les blocs protégés du programme principal et les autres fichiers restent inchangés.

Vérifie le matériau, son coefficient à chaque fréquence, son épaisseur et ses limites de validité pour les calculs retenus. Si une valeur change, préviens Yann pour recalculer. Les critères d’entretien évoqués dans SOTA.md sont présentés avec leurs sources et restent distingués des résultats numériques.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Les données physiques des candidats retenus sont cohérentes.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Ce qui est fait.** Contribuer au choix du panneau avec le matériau, sa quantité et ses données physiques.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

À partir des résultats fournis, propose une conclusion courte sur le matériau, sa quantité et ses données physiques. Le choix concerne un panneau pour le scénario RER B et la bande réellement calculés. Cite les valeurs décisives, les quantités et les formes comparées. Distingue les résultats obtenus des perspectives de SOTA.md. Fais valider la conclusion par le groupe sans inventer de performance manquante.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une décision appuyée sur une figure et quelques valeurs vérifiables.
