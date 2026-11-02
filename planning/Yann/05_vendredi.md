# Yann — Vendredi 6 novembre 2026

**Objectif du jour 5.** Finaliser les résultats et les documents, puis répéter l’exposé à cinq. Les corrections restent ciblées.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## To finalize everything

**Repère :** J5.1. **Rôle :** responsable.

**Ce qui est fait.** Vérifier la partie concernant les calculs reproductibles et les dimensions du panneau.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Conserve intégralement les deux blocs marqués « Do not modify this cell, these are the values that you will be assessed against. », leurs lignes, commentaires et espaces en début de ligne. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Les modifications du lancement se font seulement dans les blocs « Fell free to modify the function call in this cell. », et les ajouts de fonctions se placent à côté des fonctions étudiantes. Les calculs supplémentaires se font après les blocs protégés, sans modifier leurs tableaux par effet de bord.

Relis les fonctions et résultats de ta partie, puis refais les petits contrôles déjà prévus. Limite les corrections aux erreurs identifiées dans le seul fichier cible. Si l’erreur se trouve ailleurs, transmets-la à la personne concernée. Vérifie les unités, les paramètres et les figures conservées. Ne crée pas de nouveaux outils de vérification à ce stade.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Chaque membre donne son accord ou une courte liste de corrections nécessaires.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** responsable.

**Ce qui est fait.** Préparer une intervention courte et répéter avec le groupe.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Prépare une explication orale de les calculs reproductibles et les dimensions du panneau, en utilisant les figures retenues. Explique le problème, ce qui a été calculé et ce que l’on observe. Donne un exemple simple si nécessaire. La soutenance dure vingt minutes à cinq, puis dix minutes de questions. Fournis le texte dans la réponse pour les documents communs, sans nouveau fichier.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une intervention compréhensible qui tient dans la durée collective.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** responsable.

**Ce qui est fait.** Finaliser les paragraphes de sa partie du rapport.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Prépare le texte final sur les calculs reproductibles et les dimensions du panneau avec les paramètres, unités et références utilisés. Relie les résultats aux figures et donne les valeurs réellement calculées. Garde le modèle LaTeX du projet précédent. Transmets le texte à Yann puis approuve son intégration. La relecture et les éventuelles corrections du rapport sont faites sur un seul fichier à la fois.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Texte, chiffres, figures et code racontent le même résultat.

**Ordre des modifications du fichier commun.** Joachim publie ses calculs, Antoine complète la descente, puis Yann lance les essais. Chacun repart de la dernière version complète.
