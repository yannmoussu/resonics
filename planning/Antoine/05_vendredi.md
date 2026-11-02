# Antoine — Vendredi 6 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution d’Antoine.** On réceptionne les fonctions de projection et de descente et leurs contrôles.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- support/_env.py, support/preprocessing.py et support/postprocessing.py en lecture seule
- Les sorties de check_projection, check_optimizer et les résumés finaux de convergence
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie que les paramètres, exports et figures finaux indiquent RER B, le régime, la bande, la source, le matériau, la quantité et la provenance des données. Centre les textes de restitution sur le scénario RER B retenu. Conserve les titres officiels de l’énoncé et tous les contrôles numériques.

Explique le budget, la descente et ses motifs d’arrêt en prenant les exemples effectivement calculés pour le RER B ; conserve les tests quadratiques comme explications d’algorithme.

Vérifie dans la démonstration finale les fonctions project_density et your_optimization_procedure et les sorties des contrôles fournies. Ne modifie aucun fichier dans cette vérification. Contrôle les bornes, le budget, le retour arrière, les itérations acceptées et la cohérence de la dernière évaluation. Confirme les signatures utilisées par Yann et l’absence de variable fictive du squelette initial. Liste les appels à refaire avant validation. Si une correction est nécessaire, signale la fonction et le test à reprendre pour une intervention séparée dans ce seul fichier.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On transmet à Yann l’approbation du lot ou les corrections encore nécessaires avant l’exécution finale.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** contributeur.

**Contribution d’Antoine.** On prépare l’explication orale de la projection, de la recherche du pas et du résultat de convergence.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Les historiques et valeurs finales retenus par le groupe et le plan de soutenance
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Présente le besoin RER B puis la chaîne qui mène du scénario choisi au panneau retenu. Attribue la synthèse d’état de l’art à Mathis et Olympia. Annonce les bandes effectivement calculées, la représentation de la source et les gains mesurés par le code, sans transformer les perspectives de SOTA.md en résultats obtenus. Garde vingt minutes d’exposé à cinq puis dix minutes de questions.

Explique le budget, la descente et ses motifs d’arrêt en prenant les exemples effectivement calculés pour le RER B ; conserve les tests quadratiques comme explications d’algorithme.

À partir de demo_control_polycopie2024.py et des résultats joints, prépare une explication orale des fonctions project_density et your_optimization_procedure. Ne modifie aucun fichier et ne crée aucun nouveau fichier.

Explique les entrées, les étapes et les sorties de chacune. Utilise le petit exemple de projection w=(1,1), L=1 et z=(0.8,0.6), qui donne (0.6,0.4). Explique ensuite pourquoi les poids changent la translation quand la longueur représentée par chaque variable diffère.

Présente un essai de descente projetée, le recalcul du coût et la réduction du pas en cas de refus. Explique comment on vérifie la quantité, comment on lit l'historique et ce que signifie le motif d'arrêt réellement observé. Distingue la qualité locale du candidat d'une preuve d'optimum global.

Prépare des réponses courtes à ces questions : pourquoi ne pas garder un pas constant, pourquoi recalculer après projection, pourquoi utiliser le gradient projeté pour arrêter, et pourquoi comparer plusieurs départs. Relie les explications aux valeurs réellement obtenues, sans annoncer de résultat absent des données.

Liste enfin les appels des contrôles présents dans le fichier et les vérifications à faire avant la soutenance. Donne la réponse directement dans le message pour qu'elle puisse être reprise dans les documents communs.
```

**Contrôle et passage de main.** On répète avec Joachim la transition depuis le gradient, puis vers les résultats d’Olympia. Les cinq interventions tiennent dans vingt minutes, suivies de dix minutes de questions.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Contribution d’Antoine.** On fournit la méthode et les paramètres approuvés pour la partie optimisation du rapport.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Les paramètres d’optimisation, historiques et paragraphes de rapport déjà rédigés, s’ils existent
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le rapport final porte sur le cas RER B. Il distingue les plages proposées dans SOTA.md des bandes finalement retenues, donne toutes les valeurs numériques utilisées et justifie la source et les poids fréquentiels. Les liens de l’état de l’art sont cités pour les affirmations qu’ils établissent. Les résultats de calcul, les quantités et le choix du panneau concordent avec les figures et le programme.

Explique le budget, la descente et ses motifs d’arrêt en prenant les exemples effectivement calculés pour le RER B ; conserve les tests quadratiques comme explications d’algorithme.

Prépare dans le message la contribution finale au rapport sur la projection et la descente, sans créer ni modifier de fichier. Décris l’ensemble admissible, la projection pondérée, la recherche du pas, les critères d’arrêt et les contrôles d’algorithme. Donne les paramètres numériques réellement utilisés et relie-les aux historiques retenus. Explique l’emploi du même optimiseur pour une fréquence puis pour un critère de bande.

Relis les paragraphes déjà joints et corrige les conclusions de convergence qui dépasseraient les calculs fournis. Garde une explication courte du test de projection et de la quadratique à solution connue. Yann intégrera ensuite ces éléments dans le LaTeX commun lors d’une tâche dédiée. Les résultats absents restent signalés.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On approuve avec Yann les budgets, les tolérances, les motifs d’arrêt et les figures d’historique cités dans le rapport.
