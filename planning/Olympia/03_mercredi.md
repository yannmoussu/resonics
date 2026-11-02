# Olympia — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser les premiers calculs pour une optimisation sur plusieurs fréquences et quelques quantités de matériau. Les ajouts servent uniquement aux comparaisons nécessaires.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## Analyze the obtained results to compare to the efficient performances on the fixed range of frequencies ; to compare to a fully absorbing wall ;

**Repère :** J3.1. **Rôle :** responsable.

**Ce qui est fait.** Comparer les réponses sur la bande.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

Trace initial, optimisé à une fréquence et entièrement recouvert pour le même scénario. Donne le maximum parmi les fréquences calculées et une moyenne sur la bande obtenue avec la méthode des trapèzes, en tenant compte de l’espacement des fréquences. Signale les augmentations entre les points d’optimisation.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une courbe et quelques valeurs suffisent pour analyser le résultat.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Ce qui est fait.** Ajouter le résultat optimisé à plusieurs fréquences.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

Sur les mêmes courbes, ajoute la répartition obtenue avec le coût de bande. Indique les fréquences utilisées pour optimiser. Utilise les mêmes références et les mêmes poids pour comparer les moyennes. Garde les tableaux simples de fréquences et d’énergies.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le gain apporté par l’optimisation de bande est lisible.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Ce qui est fait.** Montrer le compromis entre matériau et performance.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

Trace le coût moyen sur la bande en fonction de la quantité de matériau effectivement utilisée. Indique les unités et la forme du mur. Quelques quantités suffisent pour la première étude. Conserve le recouvrement complet comme référence avec sa quantité propre.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une courbe de compromis issue des calculs du groupe.
