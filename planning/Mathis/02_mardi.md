# Mathis — Mardi 3 novembre 2026

**Objectif du jour.** On compare les premières courbes puis on essaie la descente prévue par le sujet à une fréquence problématique.

**Cas de départ.** Bruit de roulement du RER B. Premier essai proposé à 500 Hz avec c=343 m/s. Les comparaisons utilisent une pression imposée unitaire avec la même phase sur le bord supérieur. La plage 250–2 000 Hz de SOTA.md reste indicative. Avec la grille actuelle, on commence sur 250–1 500 Hz avant d’élargir si nécessaire.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** contributeur.

**Ce qui est fait.** Fournir le coefficient du même matériau pour les fréquences étudiées.

**Fichier à modifier :** `support/preprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/preprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement preprocessing.py pour le calcul demandé. Garde inchangées les fonctions initialement fournies, notamment _set_coefficients_of_pde, _set_rhs_of_pde et _set_geometry_of_domain. Les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Reprends le calcul de la veille pour les fréquences choisies avec Yann.
2. Trace ou liste brièvement les parties réelle et imaginaire pour repérer une variation anormale. Vérifie les unités et la convention de signe déjà discutée.
3. Transmets les valeurs à Yann avec les hypothèses du matériau.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Le matériau peut réagir différemment suivant la fréquence. Cette variation doit être prise en compte pour interpréter les pics du domaine.

**Résultat à transmettre.** Les coefficients aux fréquences effectivement calculées.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** contributeur.

**Ce qui est fait.** Garder le même matériau lorsque la forme du mur change.

**Fichier à modifier :** `support/preprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/preprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement preprocessing.py pour le calcul demandé. Garde inchangées les fonctions initialement fournies, notamment _set_coefficients_of_pde, _set_rhs_of_pde et _set_geometry_of_domain. Les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Compare les paramètres des essais plan et irrégulier transmis par Yann.
2. Vérifie qu’une même fréquence utilise les mêmes paramètres de matériau et le même coefficient.
3. Note la quantité totale lorsque chaque mur est entièrement recouvert. Corrige seulement une erreur identifiée dans ta fonction de coefficient.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Cette étape permet de distinguer ce qui vient du relief et ce qui vient d’une quantité de matériau plus importante.

**Résultat à transmettre.** Une comparaison où le matériau est identique et les quantités sont connues.
