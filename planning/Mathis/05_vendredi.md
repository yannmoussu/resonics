# Mathis — Vendredi 6 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution de Mathis.** On vérifie une dernière fois que les coefficients présentés sont reproductibles à partir des paramètres annoncés.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Protection du support : les cellules protégées du programme principal sont en lecture seule. Garde aussi inchangées les fonctions initialement fournies de preprocessing.py, notamment _set_coefficients_of_pde, _set_rhs_of_pde, _set_geometry_of_domain et les fonctions du motif qu’elle appelle. Ajoute les fonctions du projet à côté ; seules ces fonctions ajoutées peuvent être complétées ou corrigées. Elles travaillent sur des tableaux indépendants et ne changent pas les valeurs du cas initial par effet de bord. Compare les fonctions fournies à la version jointe avant de rendre le fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie que les paramètres, exports et figures finaux indiquent RER B, le régime, la bande, la source, le matériau, la quantité et la provenance des données. Centre les textes de restitution sur le scénario RER B retenu. Conserve les titres officiels de l’énoncé et tous les contrôles numériques.

Valide les coefficients et les sources documentaires du matériau pour les bandes RER B présentées, puis explique leurs unités et leur provenance.

Modifie uniquement support/preprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Vérifie la version finale de preprocessing.py. Limite les corrections aux erreurs avérées ou aux commentaires utiles et conserve toutes les signatures utilisées par le pilote. Contrôle la provenance, les unités, le domaine de validité et le signe de Robin. Vérifie que l’import ne déclenche ni calcul lourd ni graphique. Donne le petit appel qui reproduit les coefficients retenus, avec les paramètres réels du projet. Ne prétends pas avoir exécuté un contrôle si tu n’as pas ses sorties.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les coefficients du programme correspondent aux valeurs présentées et les petits contrôles sont exécutables sans nouveau module.

**Passage de main.** Valider le matériau auprès de Yann le matin. Une correction de valeur scientifique impose d’actualiser les résultats concernés.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** contributeur.

**Contribution de Mathis.** On prépare l’explication orale du matériau, des unités et de sa quantité, puis on répète avec les autres membres.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Présente le besoin RER B puis la chaîne qui mène du scénario choisi au panneau retenu. Attribue la synthèse d’état de l’art à Mathis et Olympia. Annonce les bandes effectivement calculées, la représentation de la source et les gains mesurés par le code, sans transformer les perspectives de SOTA.md en résultats obtenus. Garde vingt minutes d’exposé à cinq puis dix minutes de questions.

Valide les coefficients et les sources documentaires du matériau pour les bandes RER B présentées, puis explique leurs unités et leur provenance.

Prépare une explication orale du matériau à partir du code final et des valeurs retenues. Explique l’impédance, sa conversion en coefficient Robin, le contrôle de passivité et la quantité utilisée. Donne des phrases naturelles et relie les conclusions chiffrées aux résultats joints. Le groupe dispose de vingt minutes d’exposé et dix minutes de questions, avec une intervention de chacun. Ne crée aucun fichier.

```

**Contrôle attendu.** Les chiffres commentés à l’oral correspondent au code et le groupe respecte sa durée totale.

**Passage de main.** Répéter la transition depuis le modèle de Yann vers le matériau, puis vers l’objectif de Joachim.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Contribution de Mathis.** On fournit au groupe le texte final et les valeurs sur le matériau pour le rapport commun.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le rapport final porte sur le cas RER B. Il distingue les plages proposées dans SOTA.md des bandes finalement retenues, donne toutes les valeurs numériques utilisées et justifie la source et les poids fréquentiels. Les liens de l’état de l’art sont cités pour les affirmations qu’ils établissent. Les résultats de calcul, les quantités et le choix du panneau concordent avec les figures et le programme.

Valide les coefficients et les sources documentaires du matériau pour les bandes RER B présentées, puis explique leurs unités et leur provenance.

Prépare pour le rapport commun une contribution concise contenant les paramètres du matériau, leurs unités, leur provenance, la conversion du coefficient et la quantité retenue. Appuie les conclusions sur les figures et les valeurs jointes. Distingue les contrôles synthétiques des résultats physiques. Donne le texte directement dans ta réponse pour intégration au document commun, sans créer de fichier.

```

**Contrôle attendu.** Le texte, les chiffres et les conventions sont identiques à ceux des programmes et des figures approuvées.

**Passage de main.** Relire la section intégrée par Yann et donner l’approbation finale de cette partie.
