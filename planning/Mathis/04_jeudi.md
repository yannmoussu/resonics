# Mathis — Jeudi 5 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Contribution de Mathis.** On vérifie que les hypothèses et les paramètres physiques restent valables pour les campagnes raffinées et les candidats encore comparés.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers à joindre

- `support/preprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Modifie uniquement support/preprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Relis les paramètres du matériau avec les résultats réels de la campagne joints. Vérifie unités d’impédance, coefficient Robin en inverse de mètres, épaisseur, célérité, masse volumique, domaine de validité et provenance. Un changement de matériau ou d’épaisseur doit recalculer les coefficients. Contrôle les hypothèses de la loi lorsque les données le permettent et signale les points impossibles à vérifier. Corrige preprocessing.py uniquement en cas d’erreur identifiée. Ne chiffre aucune sensibilité sans plage de paramètres justifiée et sans calcul.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les candidats sont évalués avec leurs paramètres actuels et les calculs hors validité sont identifiés.

**Passage de main.** Prévenir Yann si une correction impose de reprendre la campagne avant de figer les figures.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Contribution de Mathis.** On explique le choix physique du matériau et sa quantité à partir des comparaisons disponibles.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `support/preprocessing.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
À partir des paramètres et des comparaisons réellement fournis, rédige un paragraphe de choix du matériau : nom, épaisseur, loi complexe, quantité physique, bande de validité et raisons tirées des calculs. Précise les hypothèses qui comptent pour le produit choisi. Si une comparaison manque, identifie-la plutôt que d’inventer un classement. Donne le texte dans ta réponse sans créer de fichier.

```

**Contrôle attendu.** Le choix cite des résultats disponibles et annonce les valeurs de matériau effectivement utilisées.

**Passage de main.** Soumettre la contribution au choix collectif et transmettre le texte approuvé à Yann.
