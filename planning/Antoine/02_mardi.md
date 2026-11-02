# Antoine — Mardi 3 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** contributeur.

**Contribution d’Antoine.** On fournit des distributions initiales admissibles et la quantité de matériau à afficher avec chaque référence.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Les poids de longueur et le budget validé par le groupe, puis les quantités des murs entièrement recouverts
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Pour le même scénario RER B, compare les états initial et entièrement recouvert en indiquant leurs quantités physiques, leur bande et leur source. Le calcul doit montrer les écarts réels et ne doit pas imposer le gain ou la division de matière annoncés comme perspective dans SOTA.md.

Les fréquences d’optimisation proviennent des pics confirmés de la réponse du modèle pour le régime RER B choisi et chaque descente conserve sa source et son budget.

À partir du budget et des poids fournis, prépare l’initialisation utilisée pour comparer la répartition partielle au mur entièrement recouvert. Propose de projeter la densité initiale du support avec project_density et donne la densité uniforme material_length_m/sum(design_weights) comme contrôle admissible. Vérifie bornes et budget avec les fonctions existantes, sans modifier ni créer de fichier.

Annonce séparément la quantité de la distribution initiale et celle du mur entièrement recouvert. Leur comparaison est demandée par l’énoncé même si leurs quantités diffèrent ; elle ne suffit pas à établir un gain à matériau égal. Transmets à Yann la densité initiale et ses paramètres pour le calcul des courbes, puis à Olympia les quantités à faire figurer dans les légendes.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On vérifie la faisabilité de la densité de départ et on transmet les quantités à Yann et Olympia avant l’interprétation des courbes.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** responsable.

**Contribution d’Antoine.** On remplace la boucle incomplète par une descente projetée avec recherche du pas et historique des essais acceptés.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/GAllaire-OptimParam.pdf, pages PDF 18–20 et 25–29
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis les fréquences problématiques parmi les pics confirmés de la réponse du panneau sur la bande RER B retenue, d’abord le roulement. Identifie le régime de bruit et la fréquence de chaque descente. Recalcule ensuite la réponse sur la bande pour vérifier qu’une baisse à ce pic ne dégrade pas excessivement les autres fréquences.

Les fréquences d’optimisation proviennent des pics confirmés de la réponse du modèle pour le régime RER B choisi et chaque descente conserve sa source et son budget.

Modifie uniquement your_optimization_procedure dans demo_control_polycopie2024.py et ajoute check_optimizer() non appelé automatiquement. Préserve toutes les fonctions de Joachim, project_density et le programme principal, qui sera branché par Yann ensuite. Ne crée aucun fichier.

Nouvelle signature : your_optimization_procedure(chi0, evaluate, design_weights, material_length_m, mu=1.0, max_iter=100, feasibility_tol=1e-10, gradient_tol=1e-6, armijo=1e-4, reduction=0.5, increase=1.1, min_step=1e-12, max_backtracks=40).

evaluate(chi, with_gradient=True) renvoie un dict avec value, gradient réel euclidien, u et des résidus. Avec with_gradient=False, le gradient peut être None et aucun adjoint n'est nécessaire. Le coût et tous ses paramètres restent fixes pendant une descente. La fonction evaluate sera préparée par Yann à partir des fonctions de Joachim ; pour les contrôles, emploie un callback quadratique local.

Projette d'abord une copie de chi0 avec project_density. Calcule coût et gradient, puis r=norm(chi-project_density(chi-gradient,w,L),inf). Arrête avec converged=True seulement si ce résidu et l'erreur de budget sont sous leurs seuils. Pour un pas s, forme trial=project_density(chi-s*gradient,w,L) et d=trial-chi. Accepte si F(trial)<=F(chi)+armijo*dot(gradient,d). Le déplacement contient déjà le pas. Sinon, réduis le pas par reduction, sans changer le point courant. Après acceptation, recalcule coût et gradient et prépare s suivant par increase*s.

L'historique contient le point initial puis seulement les points acceptés, avec iteration,value,step,projected_gradient_norm,budget_error,backtracks. Ne complète pas l'historique avec des zéros. Distingue les motifs projected_gradient,max_iter,min_step,max_backtracks,numerical_stagnation. Un coût non fini à un essai peut être rejeté ; une erreur de dimensions doit être signalée. Conserve le dernier point admissible cohérent à la sortie.

Renvoie un dict avec chi,value,gradient,u,history,stop_reason,converged,n_iterations,n_evaluations,budget_error,projected_gradient_norm. u est celui de la dernière évaluation ou None pour un coût synthétique ou de bande. Vérifie les arguments, les valeurs finies et l'absence de modification des entrées.

Dans check_optimizer(), prends F(x)=0.5*(2*(x1-0.1)^2+4*(x2-0.2)^2), w=(1,2), L=1.1, x0=(0.9,0.1). La solution contrainte vaut (0.3,0.4) et son coût vaut 0.12. Vérifie la faisabilité, la baisse, le résultat final réévalué et le retour arrière avec un pas initial trop grand. Teste aussi un coût constant. Ce sont des contrôles d'algorithme sans performance acoustique.

Renvoie le fichier complet et les contrôles réellement exécutés, ou les appels à exécuter. Les commentaires et docstrings sont des phrases françaises sans notation mathématique. Décris le changement de signature pour que Yann puisse adapter son appel.
```

**Contrôle et passage de main.** On valide check_optimizer() sur la quadratique, puis Yann intègre le callback acoustique. Joachim et Yann contrôlent le gradient réel avant les descentes aux pics retenus par Olympia.
