# Joachim — Mercredi 4 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution de Joachim. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Contribution de Joachim.** On ajoute un critère commun à plusieurs fréquences et la somme de leurs gradients, pour une distribution unique de matériau.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- Les fréquences, poids et références validés par le groupe, copiés dans le message
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Protection du support : recopie à l’identique les deux cellules portant « Do not modify this cell, these are the values that you will be assessed against. », de leur en-tête jusqu’à la cellule suivante. La première initialise les coefficients, les seconds membres et la géométrie ; la seconde appelle processing.solve_helmholtz puis copie chi0 et u0. Garde toutes leurs lignes, commentaires, indentation, ordre, noms et arguments. Aucun ajout à l’intérieur, déplacement, suppression, changement d’appel ni nouvelle condition qui empêche leur exécution. Les fonctions étudiantes et les cellules « Fell free to modify the function call in this cell. » accueillent les compléments. Les campagnes sont appelées dans la dernière cellule autorisée, après le second bloc protégé, avec des tableaux indépendants des valeurs initiales. Compare les deux blocs à la version jointe avant de rendre le fichier et confirme leur identité.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Optimise une distribution commune sur plusieurs fréquences de la bande RER B choisie. Sans spectre mesuré, utilise une quadrature fréquentielle normalisée explicitement annoncée. Avec un spectre de source disponible, documente les poids physiques et évite de pondérer à nouveau une amplitude déjà incluse dans la source. Les plages exploratoires se recouvrent ; leurs recouvrements ne doivent pas compter deux fois dans un coût de bande unique. Une conception couvrant plusieurs régimes est annoncée comme telle et conserve le même panneau et la même densité.

Prépare des poids normalisés de quadrature lorsque le spectre du RER B n’est pas mesuré. Une pondération par un spectre disponible a une provenance et une normalisation explicites, fixes pendant la descente.

Complète uniquement demo_control_polycopie2024.py en ajoutant evaluate_band(chi, frequencies_hz, frequency_weights, assemble_frequency, reference_energies=None, with_gradient=True) et un contrôle local non appelé automatiquement. Préserve evaluate_density, les fonctions d'Antoine et les cellules imposées. Ne crée pas de fichier.

assemble_frequency(chi, frequency_hz) est le callback de Yann. Il renvoie le dictionnaire déjà attendu par evaluate_density : A,b,cell_weights,face_rows,face_design,dA_diag. Pour chaque fréquence, passe à evaluate_density une fermeture assemble(chi) qui fige cette fréquence. La même densité chi est utilisée à chaque fréquence.

Les fréquences sont positives et finies. Les poids fréquentiels sont finis, positifs ou nuls, de somme un. Les références optionnelles sont strictement positives et fixées avant la descente ; à défaut, prends un vecteur de uns. Calcule F=sum(q_m*J_m/Jref_m) et son gradient avec exactement les mêmes facteurs. Garde les J_m bruts dans energies.

Renvoie value,gradient,energies,state_residuals,adjoint_residuals et u=None, car un coût de bande n'a pas un unique champ associé. Avec with_gradient=False, aucune résolution adjointe n'est faite. Toutes les données de fréquence et de normalisation restent constantes pendant une optimisation.

Construis un petit test synthétique à deux fréquences avec les assembleurs locaux déjà disponibles. Compare la somme des gradients à une différence centrée du coût total. Vérifie aussi qu'une seule fréquence de poids un redonne evaluate_density et que deux jeux de références non unitaires emploient les bons facteurs.

Explique dans la réponse que les fréquences supplémentaires ajoutées près d'un pic demandent de recalculer les poids d'intégration si l'on veut approximer une intégrale sur la bande. Une optimisation sur une liste de fréquences n'exclut pas une dégradation entre ces points, qui sera contrôlée séparément.

Renvoie le fichier complet et les résultats réellement exécutés, avec commentaires en phrases françaises sans notation mathématique.
```

**Contrôle et passage de main.** On transmet evaluate_band vérifiée à Antoine puis à Yann. Une carte de champ sera obtenue par réévaluation à une fréquence annoncée, car le coût de bande renvoie u=None.
