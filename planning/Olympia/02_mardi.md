# Olympia — Mardi 3 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** responsable.

**Contribution d’Olympia.** On trace la réponse du mur plan entièrement recouvert et on repère les fréquences candidates à des maxima locaux.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : la cible est uniquement postprocessing.py. Les autres modules sont en lecture seule et les deux cellules « Do not modify this cell » du programme principal restent inchangées. Les corrections concernent les tracés et leurs fonctions ; elles ne modifient pas les appels protégés ni les données initiales du solveur par effet de bord.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Calcule d’abord la référence du mur plan entièrement recouvert sur la plage de roulement proposée de 250 à 2 000 Hz après validation de ses paramètres. Les pics recherchés sont les pics de réponse du modèle ; ils ne constituent pas un spectre mesuré du RER B. Les cas complémentaires de traction ou de crissement sont identifiés séparément et utilisent leurs propres bandes validées.

Regroupe les records par noise_regime, frequency_band_hz et source_model dans metadata, en plus de la forme et du budget. Les configurations de régimes différents sont montrées séparément et ne sont pas mélangées dans un même rapport de gains.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Ajoute plot_frequency_response(records,filename=None) et find_energy_peaks(frequencies_hz,energies). Commence par les données du mur plan entièrement recouvert. Trie les fréquences et refuse les données invalides. Détecte les maxima intérieurs, traite les plateaux explicitement et signale les extrémités élevées sans les annoncer comme des maxima intérieurs démontrés. Retourne les fréquences et énergies candidates ainsi que les intervalles voisins à raffiner. Le module de tracé ne recalcule pas de solution acoustique. Le critère intérieur vaut h**2*sum(abs(u)**2), ce qui n’est pas directement une puissance dissipée. Si les données réelles manquent, utilise un petit jeu synthétique identifié pour vérifier les figures et demande les vrais résultats avant de conclure.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** La courbe plane et les intervalles de pics sont lisibles, puis Yann confirme les pics par des calculs plus fins.

**Passage de main.** Retourner les intervalles à Yann, puis actualiser la courbe lorsque les fréquences supplémentaires ont été calculées.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** responsable.

**Contribution d’Olympia.** On applique la même analyse aux autres formes entièrement recouvertes avec les mêmes paramètres physiques.

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

Compare au plan les profils fournis entièrement recouverts pour le même régime de bruit RER B, avec mêmes source, bande et dimensions de référence annoncées. Chaque profil reste fixe pendant le parcours de sa bande. Affiche les longueurs et quantités de matériau de chaque mur.

Regroupe les records par noise_regime, frequency_band_hz et source_model dans metadata, en plus de la forme et du budget. Les configurations de régimes différents sont montrées séparément et ne sont pas mélangées dans un même rapport de gains.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Réutilise plot_frequency_response et find_energy_peaks pour comparer les niveaux zéro, un et deux entièrement recouverts. Ajoute seulement les adaptations de regroupement ou de légende nécessaires dans postprocessing.py. Garde source, matériau et bande identiques. Affiche la quantité absorbante de chaque référence, car les longueurs de paroi peuvent différer. Les profils sont comparés selon leur forme réelle et non selon une courbe triangulaire supposée. Fournis les intervalles de pics à préciser et ne présente pas le recouvrement complet comme une borne minimale assurée du critère.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les courbes sont identifiées par forme et quantité. La méthode de repérage des pics est identique à celle du mur plan.

**Passage de main.** Communiquer à Yann les intervalles à raffiner et au groupe les différences de réponse observées entre formes.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** responsable.

**Contribution d’Olympia.** On confronte les courbes de la distribution initiale à budget limité avec celles des murs entièrement recouverts.

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

Pour le même scénario RER B, compare les états initial et entièrement recouvert en indiquant leurs quantités physiques, leur bande et leur source. Le calcul doit montrer les écarts réels et ne doit pas imposer le gain ou la division de matière annoncés comme perspective dans SOTA.md.

Regroupe les records par noise_regime, frequency_band_hz et source_model dans metadata, en plus de la forme et du budget. Les configurations de régimes différents sont montrées séparément et ne sont pas mélangées dans un même rapport de gains.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Complète les regroupements et tracés existants pour comparer les états initial et full d’une même géométrie. Contrôle la compatibilité de la source, de la loi de matériau, du pas et de la bande avant de calculer un rapport. Fais apparaître les quantités absolues et conserve les énergies brutes. Le recouvrement complet peut utiliser plus de matériau que l’état initial. Ne mélange pas des candidats incompatibles. Si une réduction est exprimée en décibels à partir des énergies, emploie 10*log10(E_reference/E_configuration) pour des valeurs strictement positives et indique la référence.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** La référence, la forme et le budget de chaque courbe sont explicites, puis le rapport éventuel utilise des énergies positives compatibles.

**Passage de main.** Transmettre les courbes comparables au groupe pour sélectionner les fréquences problématiques à optimiser.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Contribution d’Olympia.** On illustre la première optimisation conduite par Antoine et calculée par Yann avec les répartitions, les champs et l’historique.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/postprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : la cible est uniquement postprocessing.py. Les autres modules sont en lecture seule et les deux cellules « Do not modify this cell » du programme principal restent inchangées. Les corrections concernent les tracés et leurs fonctions ; elles ne modifient pas les appels protégés ni les données initiales du solveur par effet de bord.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Choisis les fréquences problématiques parmi les pics confirmés de la réponse du panneau sur la bande RER B retenue, d’abord le roulement. Identifie le régime de bruit et la fréquence de chaque descente. Recalcule ensuite la réponse sur la bande pour vérifier qu’une baisse à ce pic ne dégrade pas excessivement les autres fréquences.

Regroupe les records par noise_regime, frequency_band_hz et source_model dans metadata, en plus de la forme et du budget. Les configurations de régimes différents sont montrées séparément et ne sont pas mélangées dans un même rapport de gains.

Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

À partir des champs, densités et historiques réels transmis par Yann, ajoute plot_field_comparison(u_before,u_after,domain_omega,spacestep,filename=None). Représente abs(u) avec une même échelle pour les deux champs. Masque le complémentaire et les valeurs de bord non reconstruites, car les zéros retournés au bord par le solveur ne sont pas des traces physiques.

Compare les densités et les champs avant/après à fréquence annoncée et budget identique. Trace l’état initial puis seulement les itérations acceptées de l’optimiseur. Une queue de zéros préallouée doit être exclue. Les données absentes ne deviennent pas des performances nulles. Les titres restent courts et descriptifs. Ne recode pas la descente ni le solveur dans postprocessing.py.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Une même couleur représente une même amplitude. Le budget et la baisse du critère correspondent aux valeurs réellement calculées.

**Passage de main.** Faire valider l’interprétation par Antoine et Yann avant de présenter les premières figures d’optimisation.
