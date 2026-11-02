# Olympia — Mercredi 4 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## Analyze the obtained results to compare to the efficient performances on the fixed range of frequencies ; to compare to a fully absorbing wall ;

**Repère :** J3.1. **Rôle :** responsable.

**Contribution d’Olympia.** On analyse les distributions retenues sur toute la bande et on les compare à la référence entièrement recouverte.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : la cible est uniquement postprocessing.py. Les autres modules sont en lecture seule et les deux cellules « Do not modify this cell » du programme principal restent inchangées. Les corrections concernent les tracés et leurs fonctions ; elles ne modifient pas les appels protégés ni les données initiales du solveur par effet de bord.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Compare les solutions sur toute la bande de roulement retenue, avec des points de validation hors des fréquences de conception. Si les cas traction ou crissement sont calculés, présente leurs bandes et leurs sources séparément. Le critère de pression du modèle et ses réductions relatives sont annoncés avec leur référence ; les valeurs de SOTA.md en dB(A) ne sont pas des performances calculées du produit.

Affiche les bandes et régimes RER B dans les axes ou légendes, distingue conception et validation, et indique si les poids viennent d’une quadrature de test ou d’un spectre documenté.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Ajoute summarize_band(records,frequency_weights=None). Pour chaque configuration comparable, retourne le maximum échantillonné, sa fréquence et un critère moyen pondéré. Sans poids fournis, utilise une quadrature trapézoïdale normalisée sur les fréquences triées. Une zone de pics raffinée ne doit pas peser davantage uniquement parce qu’elle contient plus de points. Ne prétends pas connaître le maximum continu entre les fréquences calculées. Conserve les courbes brutes pour initial, mono et full, en distinguant les quantités. Signale les groupes incompatibles ou les données manquantes.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** La comparaison inclut des fréquences qui n’ont pas servi à optimiser et utilise les mêmes références et poids entre candidats.

**Passage de main.** Transmettre au groupe les dégradations éventuelles hors du pic de conception et demander à Yann les calculs complémentaires utiles.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Contribution d’Olympia.** On montre l’effet d’une distribution commune optimisée à plusieurs fréquences sur la bande de validation.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : la cible est uniquement postprocessing.py. Les autres modules sont en lecture seule et les deux cellules « Do not modify this cell » du programme principal restent inchangées. Les corrections concernent les tracés et leurs fonctions ; elles ne modifient pas les appels protégés ni les données initiales du solveur par effet de bord.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Optimise une distribution commune sur plusieurs fréquences de la bande RER B choisie. Sans spectre mesuré, utilise une quadrature fréquentielle normalisée explicitement annoncée. Avec un spectre de source disponible, documente les poids physiques et évite de pondérer à nouveau une amplitude déjà incluse dans la source. Les plages exploratoires se recouvrent ; leurs recouvrements ne doivent pas compter deux fois dans un coût de bande unique. Une conception couvrant plusieurs régimes est annoncée comme telle et conserve le même panneau et la même densité.

Affiche les bandes et régimes RER B dans les axes ou légendes, distingue conception et validation, et indique si les poids viennent d’une quadrature de test ou d’un spectre documenté.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Réutilise les tracés et summarize_band pour comparer les états initial, mono et multi d’une même forme au même budget. Annote les fréquences de conception présentes dans metadata et distingue-les des autres fréquences de validation. Les fréquences raffinées demandent des poids de quadrature adaptés. Les cartes éventuelles utilisent une réévaluation de la densité finale à une fréquence annoncée, car le coût de bande n’a pas de champ unique. Ne compare pas une moyenne de densités indépendantes à une véritable optimisation commune.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les mêmes conventions de coût et de normalisation sont utilisées. Les gains et dégradations entre les fréquences de conception restent visibles.

**Passage de main.** Faire relire les légendes et la méthode de pondération à Joachim, puis transmettre les figures à Yann.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Contribution d’Olympia.** On représente l’évolution des performances en fonction de la quantité physique de matériau.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : la cible est uniquement postprocessing.py. Les autres modules sont en lecture seule et les deux cellules « Do not modify this cell » du programme principal restent inchangées. Les corrections concernent les tracés et leurs fonctions ; elles ne modifient pas les appels protégés ni les données initiales du solveur par effet de bord.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Étudie la quantité nécessaire aux cartouches poreuses du panneau RER B avec les mêmes bandes et sources entre candidats comparables. La réduction de matière doit résulter des calculs. Les divisions par deux ou trois et la fraction de 40 % citées comme perspectives dans SOTA.md ne sont pas des résultats imposés. Compare les performances et la quantité à épaisseur et profondeur annoncées.

Affiche les bandes et régimes RER B dans les axes ou légendes, distingue conception et validation, et indique si les poids viennent d’une quadrature de test ou d’un spectre documenté.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Ajoute une courbe du critère moyen pondéré et du maximum échantillonné en fonction de material_length_m. Les valeurs proviennent des optimisations à différents budgets réellement réalisées par Yann et Antoine. Pour un volume, utilise épaisseur et profondeur documentées par Mathis. Vérifie que source, loi, géométrie et bande sont comparables. Si les épaisseurs varient, identifie les comparaisons à même volume. Ne remplace jamais une longueur par une fraction de nœuds. Ne crée aucun chiffre manquant pour compléter une courbe.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les quantités et leurs unités sont explicites et les courbes proviennent de budgets effectivement évalués.

**Passage de main.** Discuter les compromis avec Mathis et Antoine, puis remettre la figure au groupe pour le choix de produit.
