# Mathis — Mardi 3 novembre 2026

**Objectif du jour 2.** Calculer les références demandées, repérer quelques pics et faire une première descente après vérification du gradient. On complète les fonctions prévues dans le support, avec des tableaux simples de fréquences et d’énergies.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** contributeur.

**Ce qui est fait.** Fournir un coefficient valide sur la bande de référence.

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

Complète la fonction de calcul du coefficient pour les fréquences réellement utilisées. Vérifie sa dépendance à la fréquence, ses unités et le signe avec Yann. Un cas simple d’onde arrivant perpendiculairement au mur permet de vérifier que le matériau ne fournit pas d’énergie. Donne les limites de validité. Ne multiplie pas les matériaux à ce stade.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le premier matériau est utilisable sur la bande retenue.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier que le changement de forme conserve la même loi de matériau.

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

Vérifie que la même fréquence donne le même coefficient pour les différentes formes. Note les paramètres à maintenir identiques et les quantités de matériau différentes lorsque toute la paroi est recouverte. Réutilise les vérifications du cas plan ; ajoute seulement ce qui manque ou corrige une erreur identifiée.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Les différences entre courbes ne proviennent pas d’un changement involontaire de matériau.
