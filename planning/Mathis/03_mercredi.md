# Mathis — Mercredi 4 novembre — Comparaison des matériaux et des quantités

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Comparaison des matériaux et des quantités

**Fichier à compléter :** `support/preprocessing.py`.

On prépare les propriétés des matériaux pour les calculs multibandes et pour la comparaison de plusieurs budgets. À épaisseur et profondeur fixées, le volume de poreux est proportionnel à la longueur absorbante pondérée. Si plusieurs matériaux documentés sont disponibles, on prépare leur comparaison avec les mêmes conventions.

### Fichiers à joindre

- `support/preprocessing.py`
- `support/demo_control_polycopie2024.py`
- `context/Sujet-EI-EXT-2026.md`

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/preprocessing.py. Étends proprement les contrôles de compute_material_response pour traiter successivement les matériaux documentés déjà choisis, sans changer sa signature ni inventer un deuxième matériau si aucune donnée ne le permet.

Pour chaque matériau, conserve name, thickness_m, valid_frequency_hz et provenance, ainsi que les paramètres réels de la loi. Vérifie que toute la grille de fréquences utilisée par le groupe reste dans le domaine de validité. Une variation de fréquence ne doit pas réutiliser par erreur un coefficient constant calculé pour une autre fréquence. Les coefficients d'ouverture de Sommerfeld appartiennent à un autre bord et ne sont pas des données de matériau.

Ajoute, si nécessaire, une petite fonction de conversion du budget de longueur en volume à épaisseur et profondeur uniformes : volume = longueur_absorbante*epaisseur*profondeur. Vérifie que les longueurs sont en mètres et distingue le budget absolu des fractions de nœuds. Les poids de longueur viennent des faces du maillage ; on ne remplace pas le budget par le nombre de nœuds Robin.

Explique quelles comparaisons conservent le même volume. Si les épaisseurs diffèrent, indique la longueur compatible avec le même volume et les restrictions de faisabilité. Transmets des paramètres utilisables par le pilote, sans lancer de résolution ni changer demo_control_polycopie2024.py. Les contrôles restent dans ce seul fichier.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Chaque matériau comparé possède des données complexes et des paramètres identifiables.
- La validité fréquentielle est contrôlée sur toute la bande.
- Les volumes annoncés ont des unités et se calculent à partir du budget de longueur réellement utilisé.
- Les comparaisons à même volume sont identifiées sans supposer qu'une fraction nodale fixe suffit.

### Passage de main

Mathis fournit les paramètres à Yann et les unités à Olympia. Yann lance les calculs à budget fixé, Antoine optimise et Olympia prépare les comparaisons.
