# Yann — Jeudi 5 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Fichier à modifier :** [support/demo_control_polycopie2024.py](../../support/demo_control_polycopie2024.py).

**Ce qui est fait.** On confronte le candidat retenu à une grille plus fine et à plusieurs points de départ. On conserve les paramètres physiques, la source et la quantité de matériau pour que les comparaisons répondent à la même question.

**Fichiers à joindre avec le prompt :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- La démonstration actuelle, seule cible à modifier.
- Les quatre autres fichiers actuels de `support/`, en lecture seule.
- Le tableau des candidats et les paramètres validés mercredi, joints ou copiés dans le message.

**Prompt à copier :**

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie la robustesse du classement pour les régimes RER B effectivement calculés. Le maillage est dimensionné sur la fréquence maximale du cas comparé, y compris 4 000 Hz si le crissement est finalement inclus, et sur les reliefs. Recalcule la loi complexe et les poids du mur au raffinement, avec les mêmes dimensions et source. Les performances retenues restent celles du modèle de panneau et de sa bande validée.

Conserve une exécution courte à petite dimension et annonce le coût réel des campagnes RER B. Une campagne de validation à fréquence plus haute doit satisfaire sa propre contrainte de maillage.

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

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Contribution de Yann.** On rassemble les résultats validés pour décider collectivement quel produit retenir.

**Fichier à modifier :** aucun, cette contribution est une analyse à transmettre au groupe.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.
- `support/demo_control_polycopie2024.py`, version actuelle.

### Prompt à copier

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis le produit pour le cas d’usage RER B en reliant la bande et le régime visés, la forme du panneau, le matériau, la quantité et les performances réellement calculées. Examine le concept de cartouches amovibles de SOTA.md et documente les contraintes d’entretien et d’encombrement. Présente le compromis retenu et distingue les critères de calcul des hypothèses de réalisation.

Conserve une exécution courte à petite dimension et annonce le coût réel des campagnes RER B. Une campagne de validation à fréquence plus haute doit satisfaire sa propre contrainte de maillage.

À partir du tableau des candidats et des figures validées joints au message, propose une conclusion de produit pour ResoniCS, sans modifier ni créer de fichier.
Compare les géométries, le matériau, la quantité, le critère moyen sur bande, les pics échantillonnés et la stabilité au raffinement et aux initialisations. Cite les résultats disponibles et distingue les références entièrement recouvertes des comparaisons à budget égal.
Donne le produit retenu dans la famille effectivement testée et les chiffres qui motivent le choix. Si les données ne suffisent pas à départager les candidats, précise le calcul complémentaire nécessaire sans inventer de classement. Prépare une synthèse courte à faire approuver par les cinq membres.
```

**Contrôle et transmission.** Chaque membre approuve sa portion. Le choix final s'appuie sur les résultats d'Olympia et les validations de Mathis, Joachim et Antoine.

**Passage de main du programme principal :** Joachim → Antoine → Yann. Les résultats sont ensuite transmis à Olympia et aux autres responsables pour validation.
