# Antoine — Mercredi 4 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** responsable.

**Contribution d’Antoine.** On vérifie que la même descente accepte le critère de bande, avec une distribution unique pour toutes les fréquences.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- Les fréquences de conception, leurs poids et leurs références fixes validés par le groupe
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Optimise une distribution commune sur plusieurs fréquences de la bande RER B choisie. Sans spectre mesuré, utilise une quadrature fréquentielle normalisée explicitement annoncée. Avec un spectre de source disponible, documente les poids physiques et évite de pondérer à nouveau une amplitude déjà incluse dans la source. Les plages exploratoires se recouvrent ; leurs recouvrements ne doivent pas compter deux fois dans un coût de bande unique. Une conception couvrant plusieurs régimes est annoncée comme telle et conserve le même panneau et la même densité.

Garde les mêmes poids de coût et le même budget pendant chaque descente RER B. Des coûts de régimes différents ne sont comparés qu’avec leur normalisation annoncée.

Complète uniquement les fonctions de contrôle de projection et d'optimisation dans demo_control_polycopie2024.py. Préserve le cœur validé sauf erreur démontrée, les fonctions de Joachim et le programme principal. Ne crée aucun fichier.

L'interface your_optimization_procedure(chi0,evaluate,design_weights,material_length_m,...) ne change pas. evaluate peut désormais fermer evaluate_band : value est une somme pondérée de coûts et gradient la somme avec les mêmes coefficients. Pour une bande, u vaut None ; l'optimiseur doit accepter cette valeur. Les fréquences, leurs poids et les références restent fixes pendant une descente.

Ajoute un contrôle à deux coûts quadratiques pondérés et vérifie que le dernier coût correspond à une réévaluation indépendante de la même somme. Reprends des poids de longueur non uniformes. Vérifie plusieurs budgets admissibles, notamment les cas nul et maximal. Tous les points acceptés doivent rester dans les bornes et respecter dot(w,chi)=L.

Prépare aussi, dans la réponse écrite, une liste simple d'initialisations à transmettre à Yann : distribution initiale du support projetée, densité uniforme L/sum(w), puis perturbations à graines fixées reprojetées. Compare toujours avec le même budget absolu sur chaque forme et annonce les motifs d'arrêt. Ces listes seront exécutées dans la campagne de Yann, sans écrire un nouveau module ni un second pilote ici.

Si les valeurs fournies ne permettent pas encore une campagne physique, limite les contrôles à l'algorithme. Ne fabrique aucun chiffre de gain acoustique. Renvoie le fichier cible complet seulement si une modification a été nécessaire, et les contrôles exécutés ou leurs appels. Les commentaires restent des phrases françaises sans équations.
```

**Contrôle et passage de main.** On transmet la descente vérifiée à Yann pour les campagnes multifréquences, puis les motifs d’arrêt à Olympia pour l’analyse.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Contribution d’Antoine.** On prépare les départs admissibles et les contraintes pour comparer plusieurs quantités absolues de matériau.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Les budgets proposés par Mathis et les poids de chaque géométrie calculés par Yann
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Étudie la quantité nécessaire aux cartouches poreuses du panneau RER B avec les mêmes bandes et sources entre candidats comparables. La réduction de matière doit résulter des calculs. Les divisions par deux ou trois et la fraction de 40 % citées comme perspectives dans SOTA.md ne sont pas des résultats imposés. Compare les performances et la quantité à épaisseur et profondeur annoncées.

Garde les mêmes poids de coût et le même budget pendant chaque descente RER B. Des coûts de régimes différents ne sont comparés qu’avec leur normalisation annoncée.

Prépare les essais de quantité à partir des budgets validés, sans modifier ni créer de fichier. Vérifie pour chaque forme que le budget est compris entre zéro et la somme des poids. Décris les départs à transmettre à Yann : densité initiale du support projetée, densité uniforme, puis quelques perturbations à graines fixées reprojetées. Pour chaque comparaison, conserve le même budget absolu et les mêmes paramètres de coût.

Précise les informations à garder après chaque descente : quantité mesurée, coût final recalculé, motif d’arrêt, gradient projeté et nombre d’évaluations. Les cas de budget nul et maximal vérifient aussi le comportement de l’algorithme. Une faible baisse du coût ne constitue pas à elle seule une preuve de stationnarité.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On transmet les départs et les paramètres à Yann, qui lance les calculs. Olympia compare les performances obtenues pour chaque budget.
