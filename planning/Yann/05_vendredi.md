# Yann — Vendredi 6 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

## To finalize everything

**Repère :** J5.1. **Rôle :** responsable.

**Fichier à modifier si nécessaire :** [support/demo_control_polycopie2024.py](../../support/demo_control_polycopie2024.py).

**Ce qui est fait.** On vérifie les imports, les appels et les paramètres sur une exécution courte, puis sur le cas retenu. Les corrections restent limitées aux erreurs d'intégration du programme principal et sont contrôlées après modification.

**Fichiers à joindre avec le prompt :**

- La démonstration actuelle, seule cible à modifier si nécessaire.
- Les quatre autres fichiers actuels de `support/`, en lecture seule.
- Les paramètres et les résultats de référence validés jeudi, et le message d'erreur complet s'il y en a un.

**Prompt à copier :**

```text
Relis la démonstration ResoniCS jointe et vérifie son exécution avec les modules joints. Modifie uniquement demo_control_polycopie2024.py si une correction d'intégration est nécessaire. Ne crée aucun nouveau fichier Python et conserve les cellules imposées. Si l'erreur se trouve dans une dépendance, indique la fonction et le problème pour une tâche séparée de son responsable au lieu de modifier plusieurs fichiers.

Vérifie les imports, les unités, les conversions de fréquence, les signatures actuelles, les dimensions, les masques, la source, le budget, les résidus et les historiques. Une exécution depuis support/ doit appeler seulement les fichiers existants et les bibliothèques prévues. Évite tout chemin absolu personnel. Vérifie qu'aucune variable fictive de l'ancien squelette n'est encore utilisée et que le cas affiché avant/après a réellement été recalculé.

Teste d'abord un cas court puis le cas final avec les paramètres validés. Donne les commandes exactes depuis le répertoire support, les dépendances importées et les résultats du contrôle. N'invente aucun succès si tu ne peux pas exécuter les calculs. Si une correction change une valeur scientifique, signale les figures à recalculer avant la soutenance.
```

**Résultat attendu.** Le programme principal appelle uniquement les modules fournis complétés. Les autres fichiers restent sous la responsabilité de leurs auteurs et toute correction scientifique est revalidée.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** responsable.

**Fichier à modifier :** aucun pour cette préparation orale. La réponse est transmise au groupe pour sa répétition.

**Ce qui est fait.** On rassemble les contributions approuvées et on vérifie qu'elles couvrent l'énoncé. On conserve les templates LaTeX du projet précédent, les légendes courtes et les figures lisibles. Yann présente le modèle et la chaîne de calcul, puis les quatre autres membres prennent leur partie.

**Fichiers à joindre avec le prompt :**

- `context/Sujet-EI-EXT-2026.md`.
- La démonstration finale en lecture seule et les figures/tableaux de résultats retenus.
- Les cinq synthèses approuvées et, lorsqu'ils existent, le rapport ou la présentation à relire. Pour une modification LaTeX ultérieure, joindre et traiter un seul fichier cible à la fois.

**Prompt à copier :**

```text
À partir de l'énoncé et des résultats joints, propose une synthèse textuelle de notre travail et un déroulé de soutenance de vingt minutes à cinq, suivi de dix minutes de questions. Ne crée et ne modifie aucun fichier dans cette tâche.

Vérifie que le modèle, les propriétés sous les hypothèses annoncées, les bandes, le matériau complexe, le budget, l'étude ouverte/réfléchissante, le gradient, la descente et les validations sont expliqués. Vérifie les références entièrement absorbantes, les pics, l'optimisation monofréquence puis multifréquence, les quantités, le raffinement et le choix du produit.

Donne pour Yann une explication orale du modèle et des fonctions de calcul, une transition vers Mathis, puis une liste des points à vérifier collectivement. Appuie chaque performance annoncée sur une figure ou un tableau joint. Si un élément manque, identifie-le sans inventer de résultat. La répartition initiale est d'environ quatre minutes par personne et sera ajustée lors de la répétition.
```

**Résultat attendu.** Les cinq membres valident leur portion, les légendes et les nombres correspondent aux calculs et l'exposé respecte la durée prévue.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** responsable.

**Contribution de Yann.** On vérifie collectivement le texte final et la concordance entre le rapport, les figures et les calculs.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md`, version actuelle.
- `support/demo_control_polycopie2024.py`, version actuelle.

### Prompt à copier

```text
À partir de l'énoncé, du rapport actuel et des résultats validés joints, fais une relecture de finalisation dans ta réponse, sans créer de fichier et sans modifier de code.
Vérifie que chaque tiret du sujet a une réponse, que toutes les valeurs utilisées sont annoncées et que les figures ont une interprétation appuyée sur leurs données. Vérifie les unités, les sources, les budgets, les conventions de Robin, l'étude selon la forme, l'optimisation et les contrôles. Conserve les formulations personnelles correctes et corrige les fautes de langue.
Regroupe les remarques par partie et donne les corrections ponctuelles proposées pour que chaque membre valide sa contribution. La compilation et les modifications LaTeX ultérieures se font sur un seul fichier cible à la fois et reprennent le template du projet précédent. Si un fichier de rapport n'est pas joint, indique ce qui est nécessaire à la relecture, sans inventer son contenu.
```

**Contrôle et transmission.** Joindre le rapport actuel et les contributions approuvées. Les cinq membres valident leur texte, les chiffres et les figures avant le rendu.

**Passage de main du programme principal :** Joachim → Antoine → Yann. Les résultats sont ensuite transmis à Olympia et aux autres responsables pour validation.
