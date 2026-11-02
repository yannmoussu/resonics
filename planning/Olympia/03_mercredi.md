# Olympia — Mercredi 4 novembre — Comparaisons multibandes et quantités de matériau

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Comparaisons multibandes et quantités de matériau

**Fichier à compléter :** `support/postprocessing.py`.

On compare la distribution initiale, l'optimisation sur un pic et l'optimisation sur plusieurs fréquences sur toute la bande. On montre aussi l'effet du budget de matériau et les éventuelles dégradations entre les fréquences utilisées pour l'optimisation.

### Fichiers à joindre

- `support/postprocessing.py`
- `support/demo_control_polycopie2024.py`
- `context/Sujet-EI-EXT-2026.md`

- Les données de calcul transmises par Yann pour la journée, avec les paramètres et les tableaux `records`. Pour les cartes ou historiques, joindre également les champs et les itérations réellement enregistrés. Si ces données ne sont pas encore disponibles, les demander avant toute conclusion physique.

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/postprocessing.py en conservant les fonctions déjà intégrées. records contient case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. state distingue full, initial, mono et multi. Les fréquences d'optimisation sont indiquées dans metadata ; la grille de validation doit aussi contenir d'autres fréquences calculées par Yann.

Ajoute summarize_band(records, frequency_weights=None). Pour chaque configuration comparable, retourne le maximum échantillonné, sa fréquence et un critère moyen pondéré. Si aucun poids n'est fourni, utilise une quadrature trapézoïdale normalisée sur les fréquences triées. Les poids doivent être cohérents avec l'espacement : une zone où les pics ont été raffinés ne doit pas compter davantage uniquement parce qu'elle comporte plus de points. Ne prétends pas mesurer le maximum continu entre les fréquences calculées.

Ajoute un tracé comparant initial, mono, multi et full sur la même bande, puis un tracé du critère en fonction de material_length_m. Annote les fréquences d'optimisation et distingue-les des fréquences de validation. Compare à même source et à même loi de matériau. Les volumes sont obtenus avec l'épaisseur et la profondeur documentées ; un pourcentage de nœuds ne remplace pas une quantité physique.

Si une réduction est exprimée en décibels à partir des énergies, utilise 10*log10(E_reference/E_configuration), précise la référence et ne calcule ce rapport que pour des énergies strictement positives. Il s'agit d'un indicateur relatif du critère de pression de la simulation. Signale les données manquantes et les groupes incompatibles au lieu de les mélanger.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Les comparaisons portent sur toute la bande, y compris hors des fréquences de conception.
- Les mêmes poids et références sont utilisés entre les produits comparés.
- Les courbes montrent l'effet de plusieurs quantités effectivement calculées.
- Les cas donnant un critère de pression plus faible à une seule fréquence ne sont pas déclarés meilleurs sur toute la bande.

### Passage de main

Antoine fournit les distributions optimisées à Yann, qui calcule la validation fréquentielle. Olympia produit alors les comparaisons et indique les fréquences où un calcul complémentaire est utile.
