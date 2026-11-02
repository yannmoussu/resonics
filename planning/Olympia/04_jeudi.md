# Olympia — Jeudi 5 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** responsable.

**Contribution d’Olympia.** On confronte les courbes aux calculs raffinés et à plusieurs initialisations pour vérifier la stabilité des performances.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Protection du support : la cible est uniquement postprocessing.py. Les autres modules sont en lecture seule et les deux cellules « Do not modify this cell » du programme principal restent inchangées. Les corrections concernent les tracés et leurs fonctions ; elles ne modifient pas les appels protégés ni les données initiales du solveur par effet de bord.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie la robustesse du classement pour les régimes RER B effectivement calculés. Le maillage est dimensionné sur la fréquence maximale du cas comparé, y compris 4 000 Hz si le crissement est finalement inclus, et sur les reliefs. Recalcule la loi complexe et les poids du mur au raffinement, avec les mêmes dimensions et source. Les performances retenues restent celles du modèle de panneau et de sa bande validée.

Le classement et le choix du panneau RER B reposent sur les courbes réellement calculées et sur leurs quantités ; le concept de cartouches reste confronté aux données disponibles.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Prépare un comparatif à deux pas de maillage pour une même géométrie physique, une même source et un même budget. Sépare niveau géométrique et raffinement. Pour les champs, explicite une interpolation ou montre les grilles séparément sans soustraction incompatible.

Montre la dispersion des coûts finaux selon les initialisations identifiées dans metadata. Si une seule initialisation existe, demande les calculs nécessaires. Distingue une densité relaxée d’une version seuillée et exige le budget et la réponse recalculés après seuillage. Les écarts de critères sont calculés seulement sur des groupes comparables. Les données viennent de Yann, sans simulation dans postprocessing.py.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les variations de maillage et de départ sont identifiables. Le classement retenu est proportionné aux données et à l’état de convergence.

**Passage de main.** Faire relire les contrôles par Yann et Antoine avant le choix collectif du produit.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** responsable.

**Contribution d’Olympia.** On rassemble les comparaisons en une recommandation de produit à discuter et valider avec les cinq membres.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis le produit pour le cas d’usage RER B en reliant la bande et le régime visés, la forme du panneau, le matériau, la quantité et les performances réellement calculées. Examine le concept de cartouches amovibles de SOTA.md et documente les contraintes d’entretien et d’encombrement. Présente le compromis retenu et distingue les critères de calcul des hypothèses de réalisation.

Le classement et le choix du panneau RER B reposent sur les courbes réellement calculées et sur leurs quantités ; le concept de cartouches reste confronté aux données disponibles.

À partir des courbes et tableaux joints, prépare une synthèse compacte des candidats : forme, matériau, quantité physique, critère moyen pondéré, maximum échantillonné, stabilité au raffinement et état de convergence. Recommande un produit dans la famille réellement testée en citant les résultats décisifs. Distingue les différences de budget et les observations de robustesse. Ne prétends pas obtenir un optimum global de toutes les formes. Donne la recommandation dans ta réponse sans créer de fichier.

```

**Contrôle attendu.** Le produit retenu se justifie par une courbe de bande, quelques nombres vérifiables et une quantité annoncée.

**Passage de main.** Présenter la synthèse au groupe, recueillir les validations puis transmettre à Yann le choix approuvé et ses figures.
