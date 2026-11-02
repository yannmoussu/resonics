# Joachim — Jeudi 5 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution de Joachim. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Contribution de Joachim.** On relit le gradient et l’étude ouverte/réfléchissante, puis on vérifie les interprétations sur les données affinées.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- Les contrôles, courbes ouverte/réfléchissante et résultats de raffinement obtenus par le groupe
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
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

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Le tableau des candidats et les figures finales d’Olympia, avec les paramètres de calcul
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Relis les conclusions du choix de produit à partir des courbes et tableaux fournis. Vérifie que les comparaisons annoncent la source, la bande, le matériau, la quantité et la résolution. Distingue le critère de pression d’une puissance dissipée, et les résultats de l’optimisation de densité d’une preuve d’optimalité sur toutes les formes.

Rapproche les résultats ouverte/réfléchissante des hypothèses de l’étude théorique, puis vérifie les conclusions sur les fréquences qui n’ont pas servi à optimiser. Propose quelques phrases justifiées permettant au groupe de retenir un candidat dans la famille étudiée.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On valide avec Yann et Olympia les conclusions à conserver et les éventuels points qui nécessitent encore un calcul.
