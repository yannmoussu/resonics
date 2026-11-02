# Mathis — Mardi 3 novembre — Vérification de la loi complexe et de la passivité

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Vérification de la loi complexe et de la passivité

**Fichier à compléter :** `support/preprocessing.py`.

On contrôle que le matériau choisi absorbe de l'énergie avec la convention du solveur. On vérifie la conversion de l'impédance en coefficient sur une onde plane, puis on fournit à Yann les coefficients des fréquences de la campagne. Un résidu faible de résolution ne suffit pas à valider le sens physique de l'absorption.

### Fichiers à joindre

- `support/preprocessing.py`
- `support/processing.py`
- `support/demo_control_polycopie2024.py`
- `context/Sujet-EI-EXT-2026.md`

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/preprocessing.py, en conservant compute_material_response et les ajouts de géométrie. Les données complexes sourcées et les paramètres validés par le groupe sont ceux présents dans le fichier actuel ; s'ils n'y sont pas, indique qu'il faut les fournir.

Ajoute un contrôle de conversion et de passivité à incidence normale. Pour la convention exp(-i*omega_phys*t), Z_s est l'impédance de surface définie avec la vitesse normale sortante, Z0=rho_air*c, R=(Z_s-Z0)/(Z_s+Z0) et l'absorption de référence vaut 1-abs(R)**2. Pour une surface passive, Re(Z_s)>=0 et l'absorption plane doit être comprise entre zéro et un aux erreurs d'arrondi près. Ce résultat est un contrôle sur onde plane, pas une mesure de la performance du tunnel.

Vérifie les cas synthétiques Z_s=Z0, Z_s grand devant Z0 et une impédance purement réactive non singulière. Ne présente pas ces cas comme des matériaux disponibles. Signale les divisions presque nulles, les données non finies et les paramètres invalides. N'utilise pas 10-10j pour annoncer une performance physique.

Vérifie alpha_code=+i*omega_phys*rho_air/Z_s et alpha_phys=-alpha_code. Retourne si utile des diagnostics par fréquence dans le dictionnaire existant, en conservant toutes ses clés. Prépare la plage validée de fréquences pour Yann. Ne lance aucune campagne Helmholtz dans preprocessing.py.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- L'adaptation d'impédance donne une réflexion nulle dans le cas plan synthétique correspondant.
- Une impédance purement réactive donne une absorption plane nulle aux arrondis près.
- Le matériau réel est utilisé uniquement dans sa bande de validité.
- Yann peut comparer le signe physique avec son contrôle du solveur plan.

### Passage de main

Mathis transmet à Yann les paramètres validés et les diagnostics, sans modifier le pilote partagé. Yann relance la campagne, puis Olympia trace les résultats.
