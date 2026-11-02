# Olympia — Jeudi 5 novembre — Robustesse et choix du produit

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Robustesse et choix du produit

**Fichier à compléter :** `support/postprocessing.py`.

On vérifie que le choix reste cohérent lorsque le maillage est raffiné et que l'initialisation de l'optimisation varie. On produit quelques figures décisives et une synthèse chiffrée permettant au groupe de retenir un produit dans la famille réellement testée.

### Fichiers à joindre

- `support/postprocessing.py`
- `support/demo_control_polycopie2024.py`
- `context/Sujet-EI-EXT-2026.md`

- Les données de calcul transmises par Yann pour la journée, avec les paramètres et les tableaux `records`. Pour les cartes ou historiques, joindre également les champs et les itérations réellement enregistrés. Si ces données ne sont pas encore disponibles, les demander avant toute conclusion physique.

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/postprocessing.py, à partir des résultats calculés et transmis par Yann. records conserve le format des jours précédents et metadata précise notamment l'initialisation, le matériau, la source et les fréquences de conception. Ne crée aucune donnée de performance artificielle.

Ajoute un comparatif des courbes sur deux pas de maillage, pour une même géométrie physique, une même source et un même budget. Sépare les niveaux de géométrie des niveaux de raffinement du maillage. Vérifie que chaque groupe contient des cas comparables avant de calculer un écart relatif de critère. Pour les champs, une grille plus fine doit être comparée avec une interpolation explicitée, ou être montrée séparément sans soustraction directe incompatible.

Montre la dispersion des critères finaux obtenus pour plusieurs initialisations. Si les données ne contiennent qu'une initialisation, signale ce manque et demande un calcul à Yann plutôt que d'inventer une dispersion. Si un champ de densité a été seuillé en zones binaires, distingue le résultat relaxé du résultat seuillé, et exige le budget et la réponse recalculés après seuillage.

Prépare une synthèse compacte des candidats : géométrie, matériau, budget, critère moyen pondéré, maximum échantillonné, stabilité au raffinement et état de convergence. Donne une recommandation fondée sur les résultats disponibles, qui ne prétend pas être un optimum global de toutes les formes. Les panneaux et les légendes doivent rester lisibles dans la présentation.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Le raffinement conserve les dimensions et le budget physiques.
- Les différents départs sont identifiables et les conclusions restent proportionnées aux données.
- Le choix du produit s'appuie sur une courbe de bande et quelques chiffres vérifiables.
- Les figures utiles et leurs légendes sont prêtes avant le point de validation.

### Passage de main

Olympia présente la synthèse au groupe, puis transmet à Yann les figures finales et les résultats qui les justifient. Chaque responsable valide l'interprétation de son lot.
