# Olympia — Vendredi 6 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution d’Olympia.** On homogénéise les figures finales et on vérifie leur correspondance avec les résultats retenus.

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

Vérifie que les paramètres, exports et figures finaux indiquent RER B, le régime, la bande, la source, le matériau, la quantité et la provenance des données. Centre les textes de restitution sur le scénario RER B retenu. Conserve les titres officiels de l’énoncé et tous les contrôles numériques.

Les figures et l’oral indiquent le régime de bruit, les fréquences, la source et le budget. Les perspectives chiffrées de SOTA.md restent distinctes des résultats numériques obtenus.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Relis les fonctions de tracé finales et corrige uniquement les erreurs ou incohérences identifiées. Conserve les signatures du pilote. Vérifie axes, unités, légendes, échelles communes et noms des configurations. Les titres décrivent les figures sans annoncer une conclusion à la place du texte oral.

Vérifie les historiques sans queue de zéros, l’absence de conversion de valeurs manquantes en zéros et la séparation entre données synthétiques et résultats physiques. Permets l’enregistrement PNG et PDF lorsque le pilote le demande, sans ouverture de fenêtre en mode non interactif. Aucun calcul acoustique n’est lancé dans postprocessing.py.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les figures sont lisibles à l’écran et leurs valeurs se retrouvent dans les résultats validés.

**Passage de main.** Transmettre les figures définitives à Yann le matin et signaler celles qui nécessitent un nouveau calcul.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** contributeur.

**Contribution d’Olympia.** On prépare l’explication orale des comparaisons et du choix de produit, puis on répète avec le groupe.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Présente le besoin RER B puis la chaîne qui mène du scénario choisi au panneau retenu. Attribue la synthèse d’état de l’art à Mathis et Olympia. Annonce les bandes effectivement calculées, la représentation de la source et les gains mesurés par le code, sans transformer les perspectives de SOTA.md en résultats obtenus. Garde vingt minutes d’exposé à cinq puis dix minutes de questions.

Les figures et l’oral indiquent le régime de bruit, les fréquences, la source et le budget. Les perspectives chiffrées de SOTA.md restent distinctes des résultats numériques obtenus.

Prépare quelques phrases naturelles pour présenter les figures finales : références entièrement recouvertes, optimisation à un pic, optimisation commune de bande, quantité et choix de produit. Relie chaque conclusion aux chiffres fournis et explique les axes avant les résultats. Propose des transitions courtes entre la méthode d’Antoine et ces comparaisons. Le groupe garde vingt minutes d’exposé avec cinq interventions et dix minutes de questions. Ne crée aucun fichier.

```

**Contrôle attendu.** Les valeurs dites correspondent aux figures et le message principal de chaque graphique est explicable sans long texte sur les slides.

**Passage de main.** Participer à la répétition collective et ajuster l’intervention pour respecter la durée totale.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Contribution d’Olympia.** On prépare les légendes, les références de figures et l’analyse finale pour le rapport commun.

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

Le rapport final porte sur le cas RER B. Il distingue les plages proposées dans SOTA.md des bandes finalement retenues, donne toutes les valeurs numériques utilisées et justifie la source et les poids fréquentiels. Les liens de l’état de l’art sont cités pour les affirmations qu’ils établissent. Les résultats de calcul, les quantités et le choix du panneau concordent avec les figures et le programme.

Les figures et l’oral indiquent le régime de bruit, les fréquences, la source et le budget. Les perspectives chiffrées de SOTA.md restent distinctes des résultats numériques obtenus.

Prépare pour le rapport les légendes courtes des figures retenues et des paragraphes d’analyse renvoyant explicitement à ces figures. Explique les comparaisons initial/full/mono/multi, les quantités et les validations sans dupliquer les tableaux bruts. Conserve les unités, les références et les paramètres des calculs joints. Signale les résultats manquants sans les inventer. Donne cette contribution textuelle dans ta réponse pour intégration au rapport commun, sans créer de document supplémentaire.

```

**Contrôle attendu.** Chaque conclusion est rattachée à une figure ou un tableau réellement obtenu, avec un titre descriptif et des valeurs cohérentes.

**Passage de main.** Relire les figures et analyses une fois intégrées par Yann, puis approuver cette portion du rapport.
