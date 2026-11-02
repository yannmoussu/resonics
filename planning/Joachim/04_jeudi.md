# Joachim — Jeudi 5 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution de Joachim. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Contribution de Joachim.** On relit le gradient et l’étude ouverte/réfléchissante, puis on vérifie les interprétations sur les données affinées.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- Les contrôles, courbes ouverte/réfléchissante et résultats de raffinement obtenus par le groupe
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie la robustesse du classement pour les régimes RER B effectivement calculés. Le maillage est dimensionné sur la fréquence maximale du cas comparé, y compris 4 000 Hz si le crissement est finalement inclus, et sur les reliefs. Recalcule la loi complexe et les poids du mur au raffinement, avec les mêmes dimensions et source. Les performances retenues restent celles du modèle de panneau et de sa bande validée.

Relie les conclusions théoriques aux scénarios RER B effectivement calculés et conserve la distinction entre critère de pression et puissance dissipée.

Relis uniquement les fonctions de coût, d'adjoint et de gradient de demo_control_polycopie2024.py. processing.py sert de référence mais ne doit pas être modifié. Ne crée aucun fichier. Préserve les fonctions d'Antoine et le lancement des expériences.

Vérifie la cohérence entre l'assemblage réel, sa dérivée par face, le champ total et le système adjoint à transposée conjuguée. Vérifie les répétitions d'indices, le facteur deux, les poids de volume, les poids de fréquence et les valeurs nulles permises hors du fluide. Reprends un test centré à petite dimension puis sur le maillage affiné si ses données sont fournies. N'annonce aucun résultat non exécuté.

À partir des courbes et paramètres fournis, explique la comparaison entre une paroi latérale Neumann et la même paroi Sommerfeld, avec le même bord source supérieur, matériau et géométrie. L'ouverture apporte un flux sortant, mais l'intégrale intérieure de pression dépend aussi des résonances et du flux injecté par la source. Relie les observations à l'identité de Green sans inventer une inégalité universelle sur les coûts.

Fournis une courte liste des équations et hypothèses à retenir pour le rapport et l'oral, en citant les documents joints. Vérifie aussi que l’étude de variation selon la forme de lundi a été menée sous ses hypothèses annoncées, puis rapproche-la des comparaisons numériques entre profils. Distingue cette étude géométrique de la dérivée par rapport à la répartition de matériau. Signale explicitement toute demande de l'énoncé restant non traitée.

Si une correction est nécessaire dans les fonctions de Joachim, renvoie le fichier cible complet corrigé et les vérifications proposées. Sinon, indique qu'aucune modification n'est nécessaire. Les commentaires du code restent des phrases françaises sans notation mathématique.
```

**Contrôle et passage de main.** On transmet à Yann les corrections éventuelles et les contrôles à reprendre. Une correction du gradient impose de prévenir Antoine et de relancer les optimisations concernées.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Contribution de Joachim.** On vérifie que les conclusions mathématiques du choix de produit sont justifiées par les résultats disponibles.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Le tableau des candidats et les figures finales d’Olympia, avec les paramètres de calcul
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis le produit pour le cas d’usage RER B en reliant la bande et le régime visés, la forme du panneau, le matériau, la quantité et les performances réellement calculées. Examine le concept de cartouches amovibles de SOTA.md et documente les contraintes d’entretien et d’encombrement. Présente le compromis retenu et distingue les critères de calcul des hypothèses de réalisation.

Relie les conclusions théoriques aux scénarios RER B effectivement calculés et conserve la distinction entre critère de pression et puissance dissipée.

Relis les conclusions du choix de produit à partir des courbes et tableaux fournis. Vérifie que les comparaisons annoncent la source, la bande, le matériau, la quantité et la résolution. Distingue le critère de pression d’une puissance dissipée, et les résultats de l’optimisation de densité d’une preuve d’optimalité sur toutes les formes.

Rapproche les résultats ouverte/réfléchissante des hypothèses de l’étude théorique, puis vérifie les conclusions sur les fréquences qui n’ont pas servi à optimiser. Propose quelques phrases justifiées permettant au groupe de retenir un candidat dans la famille étudiée.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On valide avec Yann et Olympia les conclusions à conserver et les éventuels points qui nécessitent encore un calcul.
