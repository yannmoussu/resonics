# Olympia — Lundi 2 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

## the state of the art ;

**Repère :** J1.1. **Rôle :** responsable.

**Contribution d’Olympia.** On rassemble les idées de l’état de l’art sur les murs antibruit et les formes irrégulières, puis on les distingue des résultats à calculer pendant la semaine.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Prompt à copier

```text
Prépare une courte synthèse de l’état de l’art avec les pièces jointes. Explique le rôle des formes de paroi et des matériaux poreux, les applications routière et ferroviaire, puis le problème étudié par ResoniCS. Cite les pages ou figures utilisées. Utilise la contribution de Mathis sur les matériaux. Ne présente pas les performances expérimentales du document comme les performances de notre produit et ne crée aucun fichier.

```

**Contrôle attendu.** Chaque affirmation de contexte peut être retrouvée dans les documents. Les résultats propres au projet restent à calculer.

**Passage de main.** Faire valider la synthèse par le groupe et transmettre à Yann le texte court pour le cadrage du premier jour.

## the model to consider,

**Repère :** J1.2. **Rôle :** contributeur.

**Contribution d’Olympia.** On représente le domaine de calcul, ses conditions aux limites et le matériau pour que le modèle choisi soit visible.

**Fichier à compléter :** `support/postprocessing.py`.

### Fichiers à joindre

- `support/postprocessing.py` — cible à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.

### Prompt à copier

```text
Modifie uniquement support/postprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Conserve les fonctions de tracé existantes et leurs appels. Corrige myimshow pour que vmin=0 et vmax=0 soient pris en compte lorsqu’ils sont fournis et pour que les limites ne dépendent pas de la présence d’une autre option.

Ajoute plot_domain(domain_omega,chi,spacestep,filename=None) afin de distinguer intérieur, extérieur, Dirichlet, Neumann et Robin avec les constantes de _env.py. chi est nul hors du mur de conception et compris entre zéro et un dessus. Affiche des coordonnées physiques, des unités et un rapport d’axes égal. La boîte de stockage ne représente pas entièrement le fluide.

Les profils fournis utilisent un motif orthogonal à huit segments de quart malgré le nom create_motif_koch. Présente leur forme effective. Donne un petit exemple synthétique pour contrôler la légende et les dimensions, sans simulation acoustique ni effet à l’import.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Le dessin identifie le domaine et les conditions aux limites, puis les limites de couleur égales à zéro sont respectées.

**Passage de main.** Transmettre la signature à Yann afin qu’il appelle le tracé depuis la démonstration.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Contribution d’Olympia.** On prépare les comparaisons sur les bandes et les dimensions proposées par Mathis, en fixant les informations à recevoir après chaque calcul.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.

### Prompt à copier

```text
Propose un protocole de comparaison à partir des bandes, dimensions et sources discutées par le groupe. Décris les références entièrement recouvertes, l’état initial à budget limité, puis les états optimisés. records est une liste de dictionnaires avec case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state vaut full, initial, mono ou multi. Les paramètres de source, de matériau, les fréquences de conception et les conditions de calcul sont décrits dans metadata. Précise les données nécessaires aux cartes et aux historiques, et les paramètres à garder communs. Les données synthétiques serviront seulement à vérifier les tracés. Donne ce protocole dans ta réponse sans modifier de fichier ni inventer de bande numérique.

```

**Contrôle attendu.** Les configurations sont identifiables et les unités, la source et les quantités seront disponibles pour comparer les courbes.

**Passage de main.** Transmettre le format à Yann avant ses premières campagnes et faire valider le protocole avec Mathis.
