# Antoine — Jeudi 5 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Contribution d’Antoine.** On vérifie les motifs d’arrêt, les budgets et la robustesse des candidats selon leurs points de départ.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- Les historiques, budgets et résumés réels des campagnes, avec leurs initialisations
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie la robustesse du classement pour les régimes RER B effectivement calculés. Le maillage est dimensionné sur la fréquence maximale du cas comparé, y compris 4 000 Hz si le crissement est finalement inclus, et sur les reliefs. Recalcule la loi complexe et les poids du mur au raffinement, avec les mêmes dimensions et source. Les performances retenues restent celles du modèle de panneau et de sa bande validée.

Vérifie les motifs d’arrêt et les meilleurs candidats admissibles pour le régime et la bande retenus, avant d’annoncer la quantité économisée.

Relis les fonctions project_density et your_optimization_procedure ainsi que leurs contrôles dans demo_control_polycopie2024.py. Ne modifie aucun autre fichier et ne crée pas de fichier.

À partir des historiques fournis, vérifie les bornes, l'erreur absolue de budget, la condition d'acceptation avec le déplacement projeté et le motif d'arrêt. Vérifie que les essais rejetés ne remplacent jamais le point courant et qu'il n'y a pas de ligne fictive dans l'historique. Le coût, le gradient et la densité finaux doivent se rapporter à la même évaluation.

Examine plusieurs départs au même budget. Identifie le meilleur candidat admissible réellement évalué, en donnant son motif d'arrêt et son coût. Une faible baisse entre deux itérations ne suffit pas à conclure à la stationnarité. Le gradient projeté est contrôlé avec une échelle de coût annoncée et fixe. Aucune recherche locale ne prouve l'optimalité globale du produit.

Reprends les petits contrôles d'algorithme, dont les cas de budget extrême et de retour arrière. Si tu trouves une erreur dans les fonctions d'Antoine, renvoie le fichier complet corrigé en préservant les autres fonctions. Sinon, confirme qu'aucune modification n'est nécessaire. Donne les contrôles effectivement exécutés ou ceux qui restent à faire, sans inventer de résultats.

Prépare une explication courte du choix du candidat et de ses limites de calcul pour le groupe. Les campagnes au maillage affiné sont relancées par Yann et comparées par Olympia, elles ne sont pas recodées dans une autre fonction ici.
```

**Contrôle et passage de main.** On transmet les essais à conserver ou à prolonger à Yann et Olympia. Une correction de projection ou de recherche du pas impose de réévaluer les candidats concernés.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Contribution d’Antoine.** On vérifie que le candidat retenu est admissible et que son état de convergence est annoncé correctement.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Le tableau final des candidats et les historiques des essais retenus
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis le produit pour le cas d’usage RER B en reliant la bande et le régime visés, la forme du panneau, le matériau, la quantité et les performances réellement calculées. Examine le concept de cartouches amovibles de SOTA.md et documente les contraintes d’entretien et d’encombrement. Présente le compromis retenu et distingue les critères de calcul des hypothèses de réalisation.

Vérifie les motifs d’arrêt et les meilleurs candidats admissibles pour le régime et la bande retenus, avant d’annoncer la quantité économisée.

À partir du tableau et des historiques réels, identifie les candidats admissibles et leurs motifs d’arrêt. Vérifie que coût, densité, gradient projeté et budget se rapportent à la même évaluation finale. Compare les points de départ au même budget et distingue une stationnarité locale d’une limite d’itérations ou de pas.

Propose une courte conclusion pour le choix collectif du produit, en indiquant ce que l’algorithme permet d’affirmer. Le meilleur candidat évalué dans la famille testée n’est pas une preuve d’optimum global. Si le résultat jugé meilleur n’est pas suffisamment contrôlé, indique le calcul précis à reprendre avec Yann avant de le retenir.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On valide avec Olympia la façon de présenter la convergence et avec Yann les éventuels essais à relancer.
