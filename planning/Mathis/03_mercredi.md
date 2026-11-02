# Mathis — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser les premiers calculs pour une optimisation sur plusieurs fréquences et quelques quantités de matériau. Les ajouts servent uniquement aux comparaisons nécessaires.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** responsable.

**Ce qui est fait.** Exprimer les quantités en longueur ou volume de matériau.

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

Donne l’épaisseur et la profondeur retenues et le lien volume=longueur_absorbante*epaisseur*profondeur. Aide à mesurer la longueur avec les segments de la paroi représentée. Vérifie les unités et la faisabilité des quantités. Si un calcul de longueur manque réellement, ajoute seulement cette fonction dans preprocessing.py sans modifier les fonctions fournies. Compare un deuxième matériau seulement si ses données sont prêtes.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** La quantité est physique et comparable entre les cas annoncés.
