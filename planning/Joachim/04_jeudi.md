# Joachim — Jeudi, 5 novembre 2026

Objectif : valider les équations et les conclusions effectivement soutenues par les calculs.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Relecture de l'adjoint et de la comparaison ouverte/réfléchissante

**Fichier concerné :** `support/demo_control_polycopie2024.py`, pour ses fonctions de coût et de gradient. Cette tâche est d'abord une relecture ; on corrige le fichier seulement en cas d'erreur identifiée.

**Ce qu'on fait.** On contrôle à nouveau le gradient sur une grille affinée, puis on rapproche les courbes ouverte/réfléchissante de l'identité énergétique de lundi. On prépare les équations et l'interprétation qui seront intégrées aux documents par Yann.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, dernière version complète
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Dirichlet_Nonhomogene.pdf` et `context/Sujet-EI-EXT-2026.md`
- Les sorties de contrôle et les courbes ouverte/réfléchissante obtenues par le groupe, ajoutées au message ou jointes telles qu'elles existent


**Prompt à copier :**

```text
Relis uniquement les fonctions de coût, d'adjoint et de gradient de demo_control_polycopie2024.py. processing.py sert de référence mais ne doit pas être modifié. Ne crée aucun fichier. Préserve les fonctions d'Antoine et le lancement des expériences.

Vérifie la cohérence entre l'assemblage réel, sa dérivée par face, le champ total et le système adjoint à transposée conjuguée. Vérifie les répétitions d'indices, le facteur deux, les poids de volume, les poids de fréquence et les valeurs nulles permises hors du fluide. Reprends un test centré à petite dimension puis sur le maillage affiné si ses données sont fournies. N'annonce aucun résultat non exécuté.

À partir des courbes et paramètres fournis, explique la comparaison entre une paroi latérale Neumann et la même paroi Sommerfeld, avec le même bord source supérieur, matériau et géométrie. L'ouverture apporte un flux sortant, mais l'intégrale intérieure de pression dépend aussi des résonances et du flux injecté par la source. Relie les observations à l'identité de Green sans inventer une inégalité universelle sur les coûts.

Fournis une courte liste des équations et hypothèses à retenir pour le rapport et l'oral, en citant les documents joints. Vérifie aussi que l’étude de variation selon la forme de lundi a été menée sous ses hypothèses annoncées, puis rapproche-la des comparaisons numériques entre profils. Distingue cette étude géométrique de la dérivée par rapport à la répartition de matériau. Signale explicitement toute demande de l'énoncé restant non traitée.

Si une correction est nécessaire dans les fonctions de Joachim, renvoie le fichier cible complet corrigé et les vérifications proposées. Sinon, indique qu'aucune modification n'est nécessaire. Les commentaires du code restent des phrases françaises sans notation mathématique.
```

**Vérification et transmission.** On remet à Yann les équations relues et les conclusions justifiées par les courbes. Toute modification de gradient impose de prévenir Antoine et de reprendre les optimisations concernées avant de figer le produit.
