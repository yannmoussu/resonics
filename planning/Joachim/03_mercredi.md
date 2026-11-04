# Joachim — Mercredi 4 novembre 2026

**Objectif du jour 3.** Réutiliser la descente pour plusieurs fréquences et quelques quantités de matériau.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[-50, 50]`. Le coefficient suit la convention `d_n u - alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Ce qui est fait.** Additionner les calculs déjà faits pour plusieurs fréquences.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — fichier à modifier.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », leurs commentaires et leur indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les fonctions fournies restent inchangées et les ajouts restent dans ce seul fichier.

1. Choisis avec le groupe une petite liste de fréquences, par exemple quelques pics observés mardi. Utilise une même chi et la source choisie, uniforme sur le bord supérieur à chaque fréquence.
2. Pour chaque fréquence, reprends le coût et le gradient de mardi. Forme une somme pondérée des coûts et la somme des gradients avec exactement les mêmes poids. Pour une moyenne sur des fréquences régulièrement espacées, annonce des poids égaux. Pour approximer l’intégrale d’une bande, emploie les poids des trapèzes du §7.7.2. Fixe ces choix avant la descente.
3. Ajoute seulement cette boucle au calcul existant et vérifie une petite perturbation comme mardi. Donne à Antoine le coût total et son gradient. Pour essayer ensuite le spectre hypothétique, multiplie les énergies unitaires déjà calculées par |G(f)|². Les énergies issues du calcul actuel run_rer_b_frequency_sweep contiennent déjà cette pondération, car G(f) est imposé à la source.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** On recherche un compromis : une même répartition de matériau doit agir sur plusieurs fréquences. Améliorer un pic peut en dégrader un autre.

**Vérification et résultat à transmettre.** Une somme de coûts et de gradients vérifiée, avec les fréquences et les poids annoncés.

**Fichier commun.** Joachim transmet son calcul à Antoine, qui complète la descente, puis Yann lance les essais. Chacun utilise la dernière version reçue.
