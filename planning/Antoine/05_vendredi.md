# Antoine — Vendredi, 6 novembre 2026

Objectif : expliquer simplement comment la répartition de matériau a été améliorée.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Validation finale et préparation de l'oral

**Fichier concerné :** `support/demo_control_polycopie2024.py`, en lecture pour les fonctions d'Antoine. Aucun nouveau fichier n'est créé.

**Ce qu'on fait.** On relance les petits contrôles, puis on prépare une explication courte de la projection, de la recherche de pas et des résultats de convergence. Tous les membres parlent dans la soutenance collective de vingt minutes, suivie de dix minutes de questions.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, version finale partagée
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Sujet-EI-EXT-2026.md`
- Les historiques et les valeurs finales retenus par le groupe, dans leur forme actuelle


**Prompt à copier :**

```text
À partir de demo_control_polycopie2024.py et des résultats joints, prépare une explication orale des fonctions project_density et your_optimization_procedure. Ne modifie aucun fichier et ne crée aucun nouveau fichier.

Explique les entrées, les étapes et les sorties de chacune. Utilise le petit exemple de projection w=(1,1), L=1 et z=(0.8,0.6), qui donne (0.6,0.4). Explique ensuite pourquoi les poids changent la translation quand la longueur représentée par chaque variable diffère.

Présente un essai de descente projetée, le recalcul du coût et la réduction du pas en cas de refus. Explique comment on vérifie la quantité, comment on lit l'historique et ce que signifie le motif d'arrêt réellement observé. Distingue la qualité locale du candidat d'une preuve d'optimum global.

Prépare des réponses courtes à ces questions : pourquoi ne pas garder un pas constant, pourquoi recalculer après projection, pourquoi utiliser le gradient projeté pour arrêter, et pourquoi comparer plusieurs départs. Relie les explications aux valeurs réellement obtenues, sans annoncer de résultat absent des données.

Liste enfin les appels des contrôles présents dans le fichier et les vérifications à faire avant la soutenance. Donne la réponse directement dans le message pour qu'elle puisse être reprise dans les documents communs.
```

**Validation collective.** On confirme avec Yann les budgets, les tolérances et les motifs d'arrêt retenus. On participe à la répétition pour garder une présentation totale de vingt minutes et des transitions claires entre le gradient de Joachim et les résultats d'Olympia.
