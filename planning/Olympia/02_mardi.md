# Olympia — Mardi 3 novembre — Courbes de référence et pics d’énergie

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Courbes de référence et pics d’énergie

**Fichier à compléter :** `support/postprocessing.py`.

On trace d'abord les courbes des murs entièrement recouverts, puis celles des distributions initiales à budget limité. On repère les fréquences des maxima locaux et on demande à Yann de recalculer plus finement autour des pics, puis on illustre la première optimisation avec des échelles de couleur communes.

### Fichiers à joindre

- `support/postprocessing.py`
- `support/demo_control_polycopie2024.py`
- `support/_env.py`
- `context/Sujet-EI-EXT-2026.md`

- Les données de calcul transmises par Yann pour la journée, avec les paramètres et les tableaux `records`. Pour les cartes ou historiques, joindre également les champs et les itérations réellement enregistrés. Si ces données ne sont pas encore disponibles, les demander avant toute conclusion physique.

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/postprocessing.py. Utilise records, liste de dictionnaires contenant case_id, frequency_hz, energy, level, state, material_length_m, spacestep_m, relative_residual et metadata. Les calculs réels viendront de Yann ; si les données manquent, vérifie les tracés avec un petit jeu synthétique identifié comme tel.

Ajoute plot_frequency_response(records, filename=None) et find_energy_peaks(frequencies_hz, energies). Trie les fréquences et refuse les valeurs invalides. Détecte les maxima intérieurs, traite les plateaux explicitement et signale les extrémités élevées sans les présenter comme des maxima intérieurs démontrés. Retourne les fréquences et les énergies candidates ainsi que les intervalles voisins à raffiner. Le tracé ne réalise aucun nouveau calcul acoustique.

Trace successivement le mur plan entièrement recouvert, les autres profils entièrement recouverts puis les distributions initiales de ces profils. Ajoute l'état mono s'il a effectivement été calculé. Distingue les budgets absolus et ne présente pas le mur entièrement recouvert comme une borne minimale assurée. Le critère vaut h**2*sum(abs(u)**2) aux nœuds intérieurs et représente un critère de pression, pas directement une puissance dissipée.

Ajoute plot_field_comparison(u_before, u_after, domain_omega, spacestep, filename=None). Représente abs(u) avec la même échelle de couleur pour les deux champs et masque l'extérieur ainsi que les valeurs de bord non reconstruites. Le solveur laisse les valeurs de bord à zéro ; ce ne sont pas des traces physiques. N'affiche pas une normalisation séparée qui ferait perdre la comparaison des amplitudes. Les légendes et les titres restent courts.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Les références demandées au deuxième jour sont lisibles et identifiables.
- Les pics sont candidats à confirmer par des calculs plus fins, avec leurs intervalles.
- Les distributions initiale et optimisée sont comparées au même budget lorsque cette comparaison est annoncée.
- Une même couleur entre deux cartes signifie une même amplitude.

### Passage de main

Yann transmet les premières courbes après intégration. Olympia lui renvoie les intervalles des pics pour raffinement, puis actualise les figures avant la validation du jour.
