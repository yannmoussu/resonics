# Antoine — Mardi, 3 novembre 2026

Objectif : mener la première descente à une fréquence problématique.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Descente projetée et recherche de pas

**Fichier à compléter :** `support/demo_control_polycopie2024.py`, uniquement `your_optimization_procedure` et une fonction `check_optimizer` à ajouter.

**Ce qu'on fait.** On remplace la boucle incomplète par une descente qui réévalue le coût après chaque projection et ne conserve que les essais acceptés. Le calcul acoustique est reçu sous forme d'une fonction d'évaluation, ce qui permet de vérifier l'algorithme sur une petite quadratique avant la campagne.

**Avant de commencer.** On attend la version de Joachim et son contrôle du gradient. Après cette tâche, Yann adaptera l'appel dans le programme principal. La signature et le retour ci-dessous remplacent explicitement l'ancienne signature longue et son tuple.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, avec `project_density` et `evaluate_density` validées
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/GAllaire-OptimParam.pdf`, pages PDF 18 à 20
- `context/Sujet-EI-EXT-2026.md`


**Prompt à copier :**

```text
Modifie uniquement your_optimization_procedure dans demo_control_polycopie2024.py et ajoute check_optimizer() non appelé automatiquement. Préserve toutes les fonctions de Joachim, project_density et le programme principal, qui sera branché par Yann ensuite. Ne crée aucun fichier.

Nouvelle signature : your_optimization_procedure(chi0, evaluate, design_weights, material_length_m, mu=1.0, max_iter=100, feasibility_tol=1e-10, gradient_tol=1e-6, armijo=1e-4, reduction=0.5, increase=1.1, min_step=1e-12, max_backtracks=40).

evaluate(chi, with_gradient=True) renvoie un dict avec value, gradient réel euclidien, u et des résidus. Avec with_gradient=False, le gradient peut être None et aucun adjoint n'est nécessaire. Le coût et tous ses paramètres restent fixes pendant une descente. La fonction evaluate sera préparée par Yann à partir des fonctions de Joachim ; pour les contrôles, emploie un callback quadratique local.

Projette d'abord une copie de chi0 avec project_density. Calcule coût et gradient, puis r=norm(chi-project_density(chi-gradient,w,L),inf). Arrête avec converged=True seulement si ce résidu et l'erreur de budget sont sous leurs seuils. Pour un pas s, forme trial=project_density(chi-s*gradient,w,L) et d=trial-chi. Accepte si F(trial)<=F(chi)+armijo*dot(gradient,d). Le déplacement contient déjà le pas. Sinon, réduis le pas par reduction, sans changer le point courant. Après acceptation, recalcule coût et gradient et prépare s suivant par increase*s.

L'historique contient le point initial puis seulement les points acceptés, avec iteration,value,step,projected_gradient_norm,budget_error,backtracks. Ne complète pas l'historique avec des zéros. Distingue les motifs projected_gradient,max_iter,min_step,max_backtracks,numerical_stagnation. Un coût non fini à un essai peut être rejeté ; une erreur de dimensions doit être signalée. Conserve le dernier point admissible cohérent à la sortie.

Renvoie un dict avec chi,value,gradient,u,history,stop_reason,converged,n_iterations,n_evaluations,budget_error,projected_gradient_norm. u est celui de la dernière évaluation ou None pour un coût synthétique ou de bande. Vérifie les arguments, les valeurs finies et l'absence de modification des entrées.

Dans check_optimizer(), prends F(x)=0.5*(2*(x1-0.1)^2+4*(x2-0.2)^2), w=(1,2), L=1.1, x0=(0.9,0.1). La solution contrainte vaut (0.3,0.4) et son coût vaut 0.12. Vérifie la faisabilité, la baisse, le résultat final réévalué et le retour arrière avec un pas initial trop grand. Teste aussi un coût constant. Ce sont des contrôles d'algorithme sans performance acoustique.

Renvoie le fichier complet et les contrôles réellement exécutés, ou les appels à exécuter. Les commentaires et docstrings sont des phrases françaises sans notation mathématique. Décris le changement de signature pour que Yann puisse adapter son appel.
```

**Vérification et transmission.** On exécute `check_optimizer()`, puis Yann branche la fréquence retenue par Olympia. On vérifie que la quantité reste fixée et que l'historique donne des baisses réelles avant de présenter la première optimisation.
