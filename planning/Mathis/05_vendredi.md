# Mathis — Vendredi 6 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution de Mathis.** On vérifie une dernière fois que les coefficients présentés sont reproductibles à partir des paramètres annoncés.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers à joindre

- `support/preprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
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

- `support/preprocessing.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Prépare une explication orale du matériau à partir du code final et des valeurs retenues. Explique l’impédance, sa conversion en coefficient Robin, le contrôle de passivité et la quantité utilisée. Donne des phrases naturelles et relie les conclusions chiffrées aux résultats joints. Le groupe dispose de vingt minutes d’exposé et dix minutes de questions, avec une intervention de chacun. Ne crée aucun fichier.

```

**Contrôle attendu.** Les chiffres commentés à l’oral correspondent au code et le groupe respecte sa durée totale.

**Passage de main.** Répéter la transition depuis le modèle de Yann vers le matériau, puis vers l’objectif de Joachim.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Contribution de Mathis.** On fournit au groupe le texte final et les valeurs sur le matériau pour le rapport commun.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `support/preprocessing.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Prépare pour le rapport commun une contribution concise contenant les paramètres du matériau, leurs unités, leur provenance, la conversion du coefficient et la quantité retenue. Appuie les conclusions sur les figures et les valeurs jointes. Distingue les contrôles synthétiques des résultats physiques. Donne le texte directement dans ta réponse pour intégration au document commun, sans créer de fichier.

```

**Contrôle attendu.** Le texte, les chiffres et les conventions sont identiques à ceux des programmes et des figures approuvées.

**Passage de main.** Relire la section intégrée par Yann et donner l’approbation finale de cette partie.
