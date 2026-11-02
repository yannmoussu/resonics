# Olympia — Lundi 2 novembre — Figures de géométrie et préparation des comparaisons

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Figures de géométrie et préparation des comparaisons

**Fichier à compléter :** `support/postprocessing.py`.

On prépare les représentations du domaine, des conditions aux limites et de la répartition du matériau. On fixe aussi le format des résultats à transmettre par Yann afin que les figures puissent être construites sans réécrire le solveur. Les données synthétiques servent uniquement à vérifier les tracés.

### Fichiers à joindre

- `support/postprocessing.py`
- `support/preprocessing.py`
- `support/_env.py`
- `support/demo_control_polycopie2024.py`
- `context/Sujet-EI-EXT-2026.md`

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/postprocessing.py. Préserve les fonctions de tracé existantes et leurs appels. Corrige myimshow pour que vmin=0 et vmax=0 soient pris en compte quand ils sont fournis, et pour que les limites ne dépendent pas de la présence d'une autre option.

Ajoute plot_domain(domain_omega, chi, spacestep, filename=None) afin de distinguer intérieur, extérieur, Dirichlet, Neumann et Robin à partir des constantes de _env.py. chi est nul hors du mur de conception et compris entre zéro et un dessus. Affiche les coordonnées physiques et les unités, avec un rapport d'axes égal. Le domaine utile n'est pas toute la boîte de stockage.

Prépare le format des courbes ultérieures : records est une liste de dictionnaires contenant case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state prend les valeurs full, initial, mono ou multi. Yann fournira ces données après ses calculs. Les champs et l'historique sont optionnels et seront transmis séparément si nécessaire. Ne lance pas de simulation dans le module de tracé.

Les profils fournis de niveaux zéro, un et deux doivent être présentés selon leur forme effective : le motif de create_motif_koch comporte huit segments orthogonaux de quart, donc ne le dessine pas comme la courbe triangulaire classique. Donne un petit exemple synthétique clairement identifié pour contrôler la légende et les dimensions de plot_domain. Ne crée pas de nouveau module Python.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Le dessin identifie les conditions aux limites et le matériau.
- La limite de couleur égale à zéro est respectée.
- Le format de `records` est annoncé à Yann pour les campagnes de mardi.
- Le module s'importe sans lancer de figures ou de calculs.

### Passage de main

Olympia prépare les tracés en parallèle des autres membres, car elle est seule à modifier `postprocessing.py`. Elle transmet les signatures à Yann, qui les appellera depuis le pilote.
