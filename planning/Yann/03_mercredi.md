# Yann — Mercredi 4 novembre 2026

Les titres ci-dessous reprennent exactement les tâches de l’énoncé. Les développements techniques sont les étapes de ma contribution, dans les fichiers partagés. Chaque étape de code modifie uniquement son fichier cible.

## Analyze the obtained results to compare to the efficient performances on the fixed range of frequencies ; to compare to a fully absorbing wall ;

**Repère :** J3.1. **Rôle :** contributeur.

**Contribution de Yann.** On recalcule les réponses des distributions obtenues sur toute la bande, y compris entre les fréquences de conception.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Pour chaque densité initiale ou optimisée de mardi, calcule une bande de validation commune avec des points intermédiaires et des voisinages de pics. Conserve les références entièrement recouvertes et leurs quantités. Transmets les records à Olympia pour le critère moyen pondéré et le maximum échantillonné.
Sépare les fréquences ayant servi à optimiser de celles ajoutées pour valider. Donne les paramètres, le budget, les résidus et les motifs d'arrêt. Si le classement dépend d'un pic mal résolu, raffine les calculs correspondants.
En complément de l'étude théorique J1.6, fournis à Joachim une comparaison numérique ouverte/réfléchissante avec source supérieure inchangée. L'ouverture concerne un côté latéral, son alpha_code=+1j*k, son masque est exclu de la conception et du budget. La règle des coins source est annoncée. Le tunnel réfléchissant reste le scénario de comparaison des produits ; ne déduis pas une inégalité universelle entre les coûts.
```

**Contrôle et transmission.** Olympia et Joachim reçoivent les réponses réellement calculées, avec les différences entre conception et validation.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Contribution de Yann.** On optimise une distribution unique de matériau commune à plusieurs fréquences.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Branche evaluate_band de Joachim avec un callback assemble_frequency(chi,frequency_hz). Celui-ci renvoie le même dictionnaire que l'assembleur monofréquence. Les fréquences, les poids de somme un et les références optionnelles strictement positives sont fixés avant la descente et communs aux candidats comparés.
Appelle l'optimiseur existant avec une fermeture evaluate(chi,with_gradient=True) qui utilise ce coût de bande. La même densité sert à toutes les fréquences et on ne moyenne pas des densités optimisées séparément. evaluate_band renvoie u=None ; pour une carte, réévalue la densité finale à une fréquence annoncée avec evaluate_density.
Recalcule ensuite la bande de validation indépendante et publie les records state='multi'. Si des points ont été ajoutés près d'un pic, recalcule les poids d'intégration, afin que leur simple accumulation ne modifie pas arbitrairement l'importance de ce voisinage. Vérifie les résidus, la faisabilité et le coût final.
```

**Contrôle et transmission.** Antoine valide les appels de descente et Olympia reçoit les courbes sur la bande, avec les fréquences de conception identifiées.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Contribution de Yann.** On lance les mêmes expériences pour plusieurs quantités physiques de poreux et on transmet les résultats au groupe.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`.

### Fichiers à joindre

- `support/demo_control_polycopie2024.py`, version actuelle.
- `support/preprocessing.py`, version actuelle.
- `support/processing.py`, version actuelle.
- `support/postprocessing.py`, version actuelle.
- `support/_env.py`, version actuelle.
- `context/Sujet-EI-EXT-2026.md`, version actuelle.

### Prompt à copier

```text
Modifie uniquement demo_control_polycopie2024.py joint et renvoie le fichier complet, sans créer de module. Les autres fichiers sont en lecture seule. Conserve les cellules imposées et toutes les fonctions validées des autres membres. Les commentaires sont des phrases françaises expliquant les étapes, sans notation mathématique. Ne lance aucune campagne à l'import et ne présente aucun résultat synthétique comme une performance physique.
Prends les budgets absolus validés avec Mathis et Antoine. Vérifie leur faisabilité pour toutes les formes. Avec une épaisseur et une profondeur constantes, le volume vaut longueur absorbante multipliée par épaisseur et profondeur. Si ces dimensions changent entre matériaux, adapte la longueur pour annoncer réellement un volume identique.
Pour chaque budget, projette l'initialisation avec la fonction existante, puis lance les optimisations et la validation de bande sans changer la source ni la loi de matériau. Conserve les références entièrement recouvertes avec leurs quantités propres.
Transmets à Olympia coûts de bande, maxima échantillonnés, densités finales et arrêts, ainsi que les longueurs et volumes. Les budgets sont des quantités physiques et non des pourcentages de nœuds.
```

**Contrôle et transmission.** Mathis valide les unités et les volumes, Antoine les contraintes et Olympia illustre les résultats réellement calculés.

**Passage de main du programme principal :** Joachim → Antoine → Yann. Les résultats sont ensuite transmis à Olympia et aux autres responsables pour validation.
