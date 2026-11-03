# Yann — Mardi 3 novembre 2026

**Objectif du jour.** On compare les premières courbes puis on essaie la descente prévue par le sujet à une fréquence problématique.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** contributeur.

**Ce qui est fait.** Calculer la courbe de référence du mur plan entièrement recouvert.

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

1. Prépare un essai level=0 dans un bloc autorisé, puis mets chi à un sur le mur Robin. Conserve les tableaux du cas initial.
2. Utilise une boucle simple sur 50 à 3 500 Hz, par exemple par pas de 50 Hz, avec c=343 m/s. Pour chaque fréquence, impose la même source Dirichlet choisie, calcule k et le coefficient du matériau, puis appelle solve_helmholtz et your_compute_objective_function.
3. Transmets les fréquences et les énergies à Olympia. La fonction run_rer_b_frequency_sweep existante utilise déjà les gaussiennes et reste un essai séparé, facultatif.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** La courbe montre la réponse à la source choisie. Les pics dépendent du domaine, du matériau et de l’amplitude imposée à chaque fréquence.

**Résultat à transmettre.** Deux tableaux et une première courbe d’énergie sur la bande.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** contributeur.

**Ce qui est fait.** Reprendre le même calcul avec un mur irrégulier fourni.

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

1. Reprends les paramètres de J2.1 et change seulement level pour le profil irrégulier fourni. Utilise le même solveur et le même matériau.
2. Calcule les énergies aux mêmes fréquences avec la même source choisie. Garde le recouvrement complet pour cette comparaison.
3. Note les dimensions et la quantité de matériau de chaque mur, puis envoie les tableaux à Olympia. Un profil irrégulier suffit pour le premier résultat.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Le relief peut déplacer les résonances et modifier les zones de forte pression. Un mur entièrement recouvert plus long contient aussi davantage de matériau, ce qui doit être indiqué.

**Résultat à transmettre.** Les courbes du plan et du premier relief, avec leurs quantités.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** contributeur.

**Ce qui est fait.** Comparer le recouvrement complet et la répartition initiale du matériau.

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

1. Reprends une des formes calculées et la répartition chi créée par le support.
2. Refais la même boucle de fréquences avec la source choisie dans le programme principal et le même matériau. Garde séparés les résultats du recouvrement complet et de cette répartition.
3. Transmets les deux courbes et les quantités correspondantes à Olympia.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Cette comparaison montre l’effet du retrait d’une partie du matériau. Elle fournit le point de départ de la recherche d’une meilleure répartition à quantité fixée.

**Résultat à transmettre.** Deux courbes comparables sur une même forme, avec la quantité dans chaque cas.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Ce qui est fait.** Exécuter une première descente sur un pic identifié.

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

1. Prends le fichier commun après les contributions de Joachim et d’Antoine. Conserve les arguments et le retour chi,energy,u,grad de your_optimization_procedure.
2. Choisis une fréquence où la courbe présente un pic confirmé. Lance la descente après leur vérification simple de la dérivée.
3. Recalcule le champ final et l’énergie, puis vérifie avec Antoine que la quantité de matériau est conservée. Donne les figures et l’historique calculé à Olympia.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** On cherche à placer la même quantité de matériau aux endroits où elle réduit le mieux les oscillations à cette fréquence. Le résultat concerne d’abord ce seul pic.

**Résultat à transmettre.** Une carte avant/après, une baisse d’énergie calculée et une quantité conservée.

**Fichier commun.** Joachim ajoute le calcul de dérivée, Antoine complète la descente, puis Yann lance les essais en repartant de la dernière version.
