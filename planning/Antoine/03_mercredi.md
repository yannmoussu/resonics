# Antoine — Mercredi, 4 novembre 2026

Objectif : optimiser sur plusieurs fréquences et comparer les quantités de matériau.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Réception de la descente avec le coût de bande

**Fichier concerné :** `support/demo_control_polycopie2024.py`, uniquement les contrôles de la projection et de l'optimiseur.

**Ce qu'on fait.** On vérifie que le même optimiseur accepte le coût multifréquence de Joachim. On prépare plusieurs distributions initiales et plusieurs budgets pour la campagne branchée par Yann. Une distribution unique sert à toutes les fréquences d'une descente.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, version reçue de Joachim avec `evaluate_band`
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Sujet-EI-EXT-2026.md`
- Les budgets absolus et les fréquences/poids validés par le groupe, collés dans le message


**Prompt à copier :**

```text
Complète uniquement les fonctions de contrôle de projection et d'optimisation dans demo_control_polycopie2024.py. Préserve le cœur validé sauf erreur démontrée, les fonctions de Joachim et le programme principal. Ne crée aucun fichier.

L'interface your_optimization_procedure(chi0,evaluate,design_weights,material_length_m,...) ne change pas. evaluate peut désormais fermer evaluate_band : value est une somme pondérée de coûts et gradient la somme avec les mêmes coefficients. Pour une bande, u vaut None ; l'optimiseur doit accepter cette valeur. Les fréquences, leurs poids et les références restent fixes pendant une descente.

Ajoute un contrôle à deux coûts quadratiques pondérés et vérifie que le dernier coût correspond à une réévaluation indépendante de la même somme. Reprends des poids de longueur non uniformes. Vérifie plusieurs budgets admissibles, notamment les cas nul et maximal. Tous les points acceptés doivent rester dans les bornes et respecter dot(w,chi)=L.

Prépare aussi, dans la réponse écrite, une liste simple d'initialisations à transmettre à Yann : distribution initiale du support projetée, densité uniforme L/sum(w), puis perturbations à graines fixées reprojetées. Compare toujours avec le même budget absolu sur chaque forme et annonce les motifs d'arrêt. Ces listes seront exécutées dans la campagne de Yann, sans écrire un nouveau module ni un second pilote ici.

Si les valeurs fournies ne permettent pas encore une campagne physique, limite les contrôles à l'algorithme. Ne fabrique aucun chiffre de gain acoustique. Renvoie le fichier cible complet seulement si une modification a été nécessaire, et les contrôles exécutés ou leurs appels. Les commentaires restent des phrases françaises sans équations.
```

**Vérification et transmission.** On rend le fichier à Yann pour les campagnes, puis on transmet à Olympia les coûts finaux, quantités, raisons d'arrêt et nombres d'évaluations effectivement obtenus. Elle comparera les performances sur les fréquences de validation.
