# Olympia — Vendredi 6 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution d’Olympia.** On homogénéise les figures finales et on vérifie leur correspondance avec les résultats retenus.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers à joindre

- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
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

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Prépare quelques phrases naturelles pour présenter les figures finales : références entièrement recouvertes, optimisation à un pic, optimisation commune de bande, quantité et choix de produit. Relie chaque conclusion aux chiffres fournis et explique les axes avant les résultats. Propose des transitions courtes entre la méthode d’Antoine et ces comparaisons. Le groupe garde vingt minutes d’exposé avec cinq interventions et dix minutes de questions. Ne crée aucun fichier.

```

**Contrôle attendu.** Les valeurs dites correspondent aux figures et le message principal de chaque graphique est explicable sans long texte sur les slides.

**Passage de main.** Participer à la répétition collective et ajuster l’intervention pour respecter la durée totale.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Contribution d’Olympia.** On prépare les légendes, les références de figures et l’analyse finale pour le rapport commun.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Prépare pour le rapport les légendes courtes des figures retenues et des paragraphes d’analyse renvoyant explicitement à ces figures. Explique les comparaisons initial/full/mono/multi, les quantités et les validations sans dupliquer les tableaux bruts. Conserve les unités, les références et les paramètres des calculs joints. Signale les résultats manquants sans les inventer. Donne cette contribution textuelle dans ta réponse pour intégration au rapport commun, sans créer de document supplémentaire.

```

**Contrôle attendu.** Chaque conclusion est rattachée à une figure ou un tableau réellement obtenu, avec un titre descriptif et des valeurs cohérentes.

**Passage de main.** Relire les figures et analyses une fois intégrées par Yann, puis approuver cette portion du rapport.
