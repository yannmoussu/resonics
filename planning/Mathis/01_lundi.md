# Mathis — Lundi 2 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

## the state of the art ;

**Repère :** J1.1. **Rôle :** contributeur.

**Contribution de Mathis.** On aid’Olympia à distinguer les résultats connus sur les formes de mur, les propriétés du matériau et les données effectivement disponibles pour le modèle.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Prompt à copier

```text
À partir de ces documents, prépare une courte contribution à l’état de l’art sur les matériaux poreux et les conditions de leur efficacité. Sépare les exemples expérimentaux du document et les performances qui restent à calculer pour ResoniCS. Indique les pages utiles et les données de matériau qui manquent, notamment une loi ou table d’impédance complexe. Ne crée aucun fichier et ne transforme pas un coefficient d’absorption réel en impédance sans information de phase.

```

**Contrôle attendu.** Les conclusions sont rattachées aux documents et aucun chiffre de performance extérieure au projet n’est présenté comme un résultat de ResoniCS.

**Passage de main.** Transmettre cette contribution à Olympia, responsable de la synthèse de l’état de l’art.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** responsable.

**Contribution de Mathis.** On propose les bandes routière et ferroviaire, les dimensions physiques et la source commune. On vérifie leur compatibilité avec le coût des différences finies.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.
- `support/preprocessing.py` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.

### Prompt à copier

```text
Propose au groupe des bandes de fréquences, des dimensions de domaine et une source de bruit à partir des documents joints et des données réellement disponibles. Justifie chaque valeur ou identifie les données à obtenir. Conserve la source imposée par Dirichlet en haut du domaine pour la première campagne. Distingue la fréquence en hertz, la pulsation physique et le nombre d’onde : omega_phys=2*pi*f, k=omega_phys/c et lambda=c/f. L’argument omega du solveur fourni reçoit k. Vérifie la règle de dix points par longueur d’onde au plus haut de la bande, et la résolution des reliefs dont l’ordre de grandeur à explorer est lambda/2. Prépare une liste courte de paramètres avec unités, provenance et statut de validation. Ne modifie aucun programme pour cette proposition.

```

**Contrôle attendu.** Les bandes et dimensions ont une justification, les valeurs de célérité et de masse volumique sont annoncées, et la plus petite longueur d’onde est calculée.

**Passage de main.** Faire valider les choix au point collectif, puis les communiquer à Yann et Olympia avant les campagnes physiques.

## to choose porous material(s) and its quantity ;

**Repère :** J1.7. **Rôle :** responsable.

**Contribution de Mathis.** On choisit un ou plusieurs matériaux avec des données complexes utilisables, puis on annonce la quantité disponible sous une forme physique comparable entre les murs.

**Fichier à compléter :** aucun pour cette contribution d’analyse ou de restitution.

### Fichiers à joindre

- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Prompt à copier

```text
Présente un choix de matériau poreux, avec son épaisseur, sa provenance, sa bande de validité et les paramètres nécessaires à son modèle d’impédance complexe. Si les documents ne suffisent pas, propose une source primaire librement accessible et liste précisément les données à obtenir avant de lancer la campagne. Ne remplace pas ces données par une valeur inventée. Propose un budget absolu de longueur absorbante en mètres. À épaisseur et profondeur uniformes, le volume vaut longueur_absorbante*epaisseur*profondeur. Les poids de longueur du maillage viennent de Yann et la contrainte sera dot(design_weights,chi)=material_length_m. Vérifie avec Antoine que le budget est réalisable sur toutes les formes. La contrainte d’aire de l’ancien devoir ne s’applique pas ici. Donne le choix et les questions restantes directement dans ta réponse, sans créer de fichier.

```

**Contrôle attendu.** Le matériau et sa quantité sont identifiables avec des unités et une provenance. La même quantité physique est utilisée dans les comparaisons à budget égal.

**Passage de main.** Transmettre le choix au groupe, puis utiliser les données validées pour le calcul du coefficient de la tâche suivante.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** responsable.

**Contribution de Mathis.** On ajoute le calcul du coefficient complexe du matériau au module de préparation existant, après les ajouts de géométrie de Yann.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers à joindre

- `support/preprocessing.py` — cible à modifier.
- `support/processing.py` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Prompt à copier

```text
Modifie uniquement support/preprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Après les ajouts de géométrie de Yann, ajoute compute_material_response(frequencies_hz, material, air) dans preprocessing.py, sans modifier ces ajouts. frequencies_hz est un tableau de fréquences positives en hertz. air contient c_m_s et rho_air_kg_m3. material contient name, thickness_m, valid_frequency_hz, provenance et les paramètres d’une loi ou table d’impédance complexe documentée. Si ces données manquent, indique lesquelles et refuse le calcul physique.

Utilise la convention exp(-i*omega_phys*t), la normale sortant du fluide et Z_s=pression/vitesse_normale_sortante. Calcule omega_phys=2*pi*f, k=omega_phys/c et lambda=c/f. La condition physique est partial_n u+alpha_phys*u=0 avec alpha_phys=-i*omega_phys*rho_air/Z_s. Le support utilise partial_n u-alpha_code*u=0, donc alpha_code=-alpha_phys. Son argument omega reçoit k. Une table d’absorption réelle seule ne détermine pas Z_s et la constante 10-10j du démo n’identifie pas un matériau réel.

Retourne frequency_hz, angular_frequency_rad_s, k_per_m, wavelength_m, surface_impedance_pa_s_per_m, alpha_phys_per_m, alpha_code_per_m, valid_mask et provenance dans un dictionnaire. Les tableaux suivent la forme de frequencies_hz. Contrôle unités, finitude et domaine de validité, sans extrapolation silencieuse. Conserve les coefficients unitaires imposés de _set_coefficients_of_pde. Donne un petit contrôle synthétique de conversion dans le même fichier, sans effet à l’import. Si plusieurs matériaux documentés sont disponibles, prépare leur évaluation avec cette même fonction sans inventer un second matériau.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les conversions sont cohérentes et les coefficients physique et assemblé ont des signes opposés. Les paramètres manquants sont signalés avant toute annonce de performance.

**Passage de main.** Renvoyer le fichier complet à Yann, qui l’appellera depuis la démonstration. Chaque matériau comparé doit être validé dans sa bande.
