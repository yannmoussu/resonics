# Yann — Mercredi 4 novembre 2026

**Objectif du jour.** On regarde toute la bande et on teste quelques fréquences et quantités ensemble avec les calculs déjà construits.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## Analyze the obtained results to compare to the efficient performances on the fixed range of frequencies ; to compare to a fully absorbing wall ;

**Repère :** J3.1. **Rôle :** contributeur.

**Ce qui est fait.** Regarder l’effet de la première optimisation sur toute la bande.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », avec leurs lignes, commentaires et indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les essais supplémentaires utilisent leurs propres tableaux après les blocs protégés. Conserve les signatures et les retours du support.

1. Reprends les répartitions initiale, optimisée à une fréquence et entièrement recouverte.
2. Recalcule leur énergie sur les mêmes fréquences avec la source choisie dans le programme principal. Ajoute quelques points entre les fréquences calculées si un pic semble mal décrit.
3. Transmets les courbes à Olympia en indiquant la fréquence d’optimisation et la quantité de chaque cas.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Réduire un pic peut laisser d’autres résonances importantes. La courbe complète montre si l’amélioration est étendue ou limitée à une fréquence.

**Résultat à transmettre.** Les trois courbes sur la même bande et les pics restant élevés.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Ce qui est fait.** Lancer la même recherche avec quelques fréquences à la fois.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

La note sur la source décrit le spectre hypothétique existant. Il reste facultatif pour les comparaisons.

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », avec leurs lignes, commentaires et indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les essais supplémentaires utilisent leurs propres tableaux après les blocs protégés. Conserve les signatures et les retours du support.

1. Reprends le coût préparé par Joachim et la descente d’Antoine. Choisis avec Olympia quelques fréquences problématiques dans les courbes obtenues.
2. Optimise une seule répartition chi commune à ces fréquences, avec des poids fixés pour tout le calcul.
3. Refais la courbe d’énergie sur la bande pour cette répartition. En complément, avec les autres forçages nuls, multiplie une seule fois les énergies unitaires par G(f)**2 pour illustrer l’effet des gaussiennes. La courbe de run_rer_b_frequency_sweep est déjà pondérée et se lit directement.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Une répartition commune doit trouver un compromis entre plusieurs résonances. Un spectre hypothétique favorise certaines fréquences et sert ici seulement à examiner l’effet de cette hypothèse.

**Résultat à transmettre.** Une répartition commune et sa courbe comparée au résultat monofréquence.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Ce qui est fait.** Tester quelques quantités de matériau avec les calculs déjà disponibles.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », avec leurs lignes, commentaires et indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les essais supplémentaires utilisent leurs propres tableaux après les blocs protégés. Conserve les signatures et les retours du support.

1. Choisis avec Mathis et Antoine deux ou trois quantités réalisables. Ils donnent la correspondance entre chi et la longueur absorbante, ou le volume si l’épaisseur et la profondeur sont fixées.
2. Pour chaque quantité, reprends la même recherche et la même bande avec la source choisie dans le programme principal.
3. Pour comparer des formes différentes, utilise une même quantité physique et note celle réellement obtenue sur chaque grille. Transmets les résultats à Olympia.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Cette étude sert à savoir si ajouter du matériau apporte encore une amélioration notable. La quantité totale permet de comparer le coût matériel et la réduction des oscillations.

**Résultat à transmettre.** Quelques couples quantité/résultat obtenus avec les mêmes hypothèses.

**Fichier commun.** Joachim ajoute le calcul de dérivée, Antoine complète la descente, puis Yann lance les essais en repartant de la dernière version.
