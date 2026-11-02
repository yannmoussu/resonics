# Mathis — Lundi 2 novembre — Choix des données et coefficient du matériau

**Organisation.** On travaille à partir des versions à jour. On ne modifie que le fichier cible et on conserve les fonctions déjà écrites par les autres. Les fonctions nouvelles sont ajoutées dans ce fichier et les fonctions des jours précédents sont conservées. Aucune de ces fiches ne demande de créer un nouveau module Python.

## Tâche — Choix des données et coefficient du matériau

**Fichier à compléter :** `support/preprocessing.py`.

On choisit une loi de matériau utilisable dans les bandes routière et ferroviaire proposées par le groupe. On enregistre ses paramètres, ses unités et sa provenance, puis on calcule le coefficient complexe utilisé par le solveur. La constante de démonstration `10-10j` ne permet pas d'identifier un matériau réel. Les coefficients d'absorption réels du document Filoche ne donnent pas, à eux seuls, une impédance complexe.

On propose au groupe les bandes, la célérité, la masse volumique et l'épaisseur, avec leur justification. Ces valeurs restent des choix à valider avant les calculs physiques.

### Fichiers à joindre

- `support/preprocessing.py`
- `support/processing.py`
- `support/demo_control_polycopie2024.py`
- `support/_env.py`
- `context/Sujet-EI-EXT-2026.md`
- `context/Mur-antibruit-Filoche.pdf`

On joint les fichiers complets et à jour. Seul le fichier cible est modifiable ; les autres servent à comprendre les appels et les conventions.

### Prompt à copier

```text
Complète uniquement support/preprocessing.py. Après les ajouts de géométrie de Yann, ajoute compute_material_response(frequencies_hz, material, air), sans modifier ces ajouts.

frequencies_hz est un tableau de fréquences strictement positives en hertz. air contient c_m_s et rho_air_kg_m3. material contient name, thickness_m, valid_frequency_hz, provenance et les données nécessaires à une loi ou table d'impédance complexe documentée. Si ces données manquent, explique précisément lesquelles sont nécessaires et refuse le calcul physique au lieu d'inventer des valeurs. Une table d'absorption réelle n'est pas une table d'impédance.

Utilise la convention temporelle exp(-i*omega_phys*t), la normale sortant du fluide et l'impédance Z_s=pression/vitesse_normale_sortante. Calcule omega_phys=2*pi*f, k=omega_phys/c et lambda=c/f. La Robin physique est partial_n u + alpha_phys*u=0, avec alpha_phys=-i*omega_phys*rho_air/Z_s. Le solveur fourni représente partial_n u-alpha_code*u=0, donc alpha_code=-alpha_phys=+i*omega_phys*rho_air/Z_s. Son argument historique omega reçoit k, pas la fréquence en hertz.

Retourne un dictionnaire contenant frequency_hz, angular_frequency_rad_s, k_per_m, wavelength_m, surface_impedance_pa_s_per_m, alpha_phys_per_m, alpha_code_per_m, valid_mask et provenance. Tous les tableaux ont la même forme que frequencies_hz. Vérifie les unités et signale les fréquences hors de validité, sans extrapolation silencieuse. Ne change pas les coefficients unitaires imposés de _set_coefficients_of_pde.

Si les pièces jointes ne contiennent pas de modèle complexe complet, commence par proposer une loi publiée ou une table d’impédances librement accessible avec sa source primaire, ses paramètres nécessaires et sa bande de validité. Soumets ce choix au groupe avant les campagnes. Une valeur non disponible reste une donnée à obtenir. À partir des pièces jointes, sépare les informations effectivement disponibles de celles qui restent à obtenir. Donne aussi un bref état de l’art à partir du document Filoche et une courte proposition motivée de bandes, de source et de dimensions, sans les imposer arbitrairement dans le programme. Prévois un contrôle purement synthétique de conversion d'une impédance complexe en coefficient, clairement présenté comme un contrôle de code et non comme un matériau réel.

Rends uniquement la version complète du fichier cible et une courte explication des modifications et des contrôles. Ne crée aucun autre fichier Python. Conserve toutes les fonctions sans rapport avec cette tâche et les modifications déjà faites par les autres. Les commentaires sont de courtes phrases françaises expliquant les étapes, sans formules mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import.
```

### Résultat attendu et contrôles

- Une table ou une loi complexe a une provenance et un domaine de validité, ou les données manquantes sont listées explicitement.
- Les conversions hertz, pulsation et nombre d'onde sont cohérentes.
- Le coefficient physique et le coefficient du support ont des signes opposés.
- Les valeurs proposées et leur provenance sont prêtes pour le point de groupe avant 14h30.

### Passage de main

Yann publie d'abord ses ajouts dans `preprocessing.py`, puis Mathis travaille sur cette version et lui transmet le fichier complet. Yann intégrera les appels dans le programme principal à partir de mardi.
