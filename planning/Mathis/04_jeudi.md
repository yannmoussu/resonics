# Mathis — Jeudi 5 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Contribution de Mathis.** On vérifie que les hypothèses et les paramètres physiques restent valables pour les campagnes raffinées et les candidats encore comparés.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : les cellules protégées du programme principal sont en lecture seule. Garde aussi inchangées les fonctions initialement fournies de preprocessing.py, notamment _set_coefficients_of_pde, _set_rhs_of_pde, _set_geometry_of_domain et les fonctions du motif qu’elle appelle. Ajoute les fonctions du projet à côté ; seules ces fonctions ajoutées peuvent être complétées ou corrigées. Elles travaillent sur des tableaux indépendants et ne changent pas les valeurs du cas initial par effet de bord. Compare les fonctions fournies à la version jointe avant de rendre le fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie la robustesse du classement pour les régimes RER B effectivement calculés. Le maillage est dimensionné sur la fréquence maximale du cas comparé, y compris 4 000 Hz si le crissement est finalement inclus, et sur les reliefs. Recalcule la loi complexe et les poids du mur au raffinement, avec les mêmes dimensions et source. Les performances retenues restent celles du modèle de panneau et de sa bande validée.

Les contraintes de poussières, humidité et entretien évoquées dans SOTA.md sont des critères à documenter pour le choix du matériau ; les calculs ne leur attribuent pas de gain chiffré sans données.

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

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis le produit pour le cas d’usage RER B en reliant la bande et le régime visés, la forme du panneau, le matériau, la quantité et les performances réellement calculées. Examine le concept de cartouches amovibles de SOTA.md et documente les contraintes d’entretien et d’encombrement. Présente le compromis retenu et distingue les critères de calcul des hypothèses de réalisation.

Les contraintes de poussières, humidité et entretien évoquées dans SOTA.md sont des critères à documenter pour le choix du matériau ; les calculs ne leur attribuent pas de gain chiffré sans données.

À partir des paramètres et des comparaisons réellement fournis, rédige un paragraphe de choix du matériau : nom, épaisseur, loi complexe, quantité physique, bande de validité et raisons tirées des calculs. Précise les hypothèses qui comptent pour le produit choisi. Si une comparaison manque, identifie-la plutôt que d’inventer un classement. Donne le texte dans ta réponse sans créer de fichier.

```

**Contrôle attendu.** Le choix cite des résultats disponibles et annonce les valeurs de matériau effectivement utilisées.

**Passage de main.** Soumettre la contribution au choix collectif et transmettre le texte approuvé à Yann.
