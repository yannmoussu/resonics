# Mathis — Jeudi 5 novembre — Choix physique du matériau

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Choix physique du matériau

**Fichier à compléter :** `support/preprocessing.py`.

On relit les hypothèses du matériau au regard des résultats calculés et des dimensions retenues. On précise les données fiables, les contraintes d'épaisseur et les éventuelles limites de validité, puis on valide les paramètres du produit choisi en groupe.

### Fichiers à joindre

- `support/preprocessing.py`
- `support/demo_control_polycopie2024.py`
- `context/Sujet-EI-EXT-2026.md`

- Les paramètres validés et les résultats de comparaison transmis par Yann et Olympia.

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Relis et, si nécessaire, corrige uniquement support/preprocessing.py. Conserve les fonctions et interfaces déjà intégrées. Contrôle la cohérence des paramètres du matériau finalement retenu : unités de l'impédance, coefficient Robin en inverse de mètres, épaisseur, célérité, masse volumique, bande de validité et provenance.

Vérifie qu'un changement de matériau ou d'épaisseur ne laisse pas dans le dictionnaire une ancienne valeur de coefficient. Les hypothèses propres à la loi utilisée doivent être lisibles et contrôlées lorsque les données permettent de le faire. N'annonce aucune sensibilité chiffrée sans calcul ni plage de paramètres sourcée.

Prépare dans ta réponse une courte fiche de choix : matériau retenu, données d'entrée, quantité physique, motifs tirés des calculs du groupe et limites factuelles de la loi. Si les résultats de comparaison ne sont pas joints, donne la trame sans inventer le classement. Cette fiche sera intégrée ensuite au rapport et à l'oral par Yann ; ne crée aucun document supplémentaire dans le programme.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Les mêmes paramètres sont utilisés par tous les calculs retenus.
- Les résultats hors de la bande de validité sont écartés ou identifiés.
- Le groupe peut expliquer le matériau choisi et sa quantité avec des données vérifiables.

### Passage de main

Mathis valide sa partie avant le point de groupe et donne à Yann le texte court et les valeurs définitives. Les figures de comparaison restent produites par Olympia.
