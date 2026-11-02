# Antoine — Vendredi 6 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution d’Antoine.** On réceptionne les fonctions de projection et de descente et leurs contrôles.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- support/_env.py, support/preprocessing.py et support/postprocessing.py en lecture seule
- Les sorties de check_projection, check_optimizer et les résumés finaux de convergence
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Vérifie dans la démonstration finale les fonctions project_density et your_optimization_procedure et les sorties des contrôles fournies. Ne modifie aucun fichier dans cette vérification. Contrôle les bornes, le budget, le retour arrière, les itérations acceptées et la cohérence de la dernière évaluation. Confirme les signatures utilisées par Yann et l’absence de variable fictive du squelette initial. Liste les appels à refaire avant validation. Si une correction est nécessaire, signale la fonction et le test à reprendre pour une intervention séparée dans ce seul fichier.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On transmet à Yann l’approbation du lot ou les corrections encore nécessaires avant l’exécution finale.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** contributeur.

**Contribution d’Antoine.** On prépare l’explication orale de la projection, de la recherche du pas et du résultat de convergence.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Les historiques et valeurs finales retenus par le groupe et le plan de soutenance
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
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

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Les paramètres d’optimisation, historiques et paragraphes de rapport déjà rédigés, s’ils existent
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Prépare dans le message la contribution finale au rapport sur la projection et la descente, sans créer ni modifier de fichier. Décris l’ensemble admissible, la projection pondérée, la recherche du pas, les critères d’arrêt et les contrôles d’algorithme. Donne les paramètres numériques réellement utilisés et relie-les aux historiques retenus. Explique l’emploi du même optimiseur pour une fréquence puis pour un critère de bande.

Relis les paragraphes déjà joints et corrige les conclusions de convergence qui dépasseraient les calculs fournis. Garde une explication courte du test de projection et de la quadratique à solution connue. Yann intégrera ensuite ces éléments dans le LaTeX commun lors d’une tâche dédiée. Les résultats absents restent signalés.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On approuve avec Yann les budgets, les tolérances, les motifs d’arrêt et les figures d’historique cités dans le rapport.
