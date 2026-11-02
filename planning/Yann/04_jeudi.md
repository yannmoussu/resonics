# Yann — Jeudi 5 novembre

**But du jour.** Vérifier que le produit retenu reste intéressant lorsque le maillage et l'initialisation changent, puis figer une campagne reproductible.

**Passage de main.** Antoine publie ses contrôles d'arrêt, Joachim relit le calcul d'objectif, puis Yann effectue les expériences ci-dessous dans la démonstration. Olympia reçoit les résultats pour le classement final.

## Tâche 1 — Contrôler le raffinement et la reproductibilité

**Fichier à modifier :** [support/demo_control_polycopie2024.py](../../support/demo_control_polycopie2024.py).

**Ce qui est fait.** On confronte le candidat retenu à une grille plus fine et à plusieurs points de départ. On conserve les paramètres physiques, la source et la quantité de matériau pour que les comparaisons répondent à la même question.

**Fichiers à joindre avec le prompt :**

- La démonstration actuelle, seule cible à modifier.
- Les quatre autres fichiers actuels de `support/`, en lecture seule.
- Le tableau des candidats et les paramètres validés mercredi, joints ou copiés dans le message.

**Prompt à copier :**

```text
Complète seulement demo_control_polycopie2024.py, sans créer d'autre module et sans modifier les cellules imposées ni les fonctions théoriques validées.

Ajoute une campagne de validation pour les meilleurs candidats déjà calculés :
1. Raffine le pas en gardant les dimensions physiques, le niveau et les sommets du profil fixes. Avec N points, la largeur réelle utilise N-1 intervalles. Vérifie les coordonnées et les masques avant le calcul. Recalcule les indices de conception et leurs poids sur chaque grille.
2. Transfère la densité le long du même contour, puis projette-la sur le budget fin avec la fonction d'Antoine. Explique la règle de transfert et distingue l'évaluation de cette densité transférée d'une éventuelle nouvelle optimisation fine. Recalcule les pics sur les deux grilles ; une fréquence de pic peut se déplacer.
3. Relance la descente depuis une distribution uniforme et quelques répartitions admissibles différentes. Pour les tirages, fixe et affiche les graines. Toutes les initialisations sont projetées sur le même budget. Conserve coût final, contrainte, gradient projeté, cause d'arrêt, nombre de résolutions et temps de calcul.
4. Vérifie aussi les fréquences de validation qui n'ont pas servi à optimiser. Compare au mur plan et au profil entièrement recouvert en indiquant leurs quantités, puis aux autres formes à budget égal.
5. Réutilise les fonctions de calcul et de tracé existantes. Ne remplace pas un arrêt sur stagnation ou sur limite d'itérations par une annonce d'optimum global. Si le classement change au raffinement, remonte ce résultat avant de choisir le produit.
6. Centralise dans les résultats la source, les dimensions, le matériau et sa provenance, le pas, les fréquences, les poids, le budget et les paramètres d'optimisation. Mets une exécution courte à disposition pour vérifier les appels, sans lancer toute la campagne à l'import.

Renvoie le fichier complet et les vérifications réellement effectuées. Les commentaires restent des phrases simples qui expliquent les étapes. Les performances annoncées proviennent des calculs validés, avec leur domaine de comparaison.
```

**Résultat attendu.** Les mêmes paramètres permettent de retrouver la campagne, et les écarts de maillage ou d'initialisation sont visibles. Le groupe peut choisir le meilleur produit de la famille étudiée en connaissant les limites de ce classement.
