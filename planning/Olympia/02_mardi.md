# Olympia — Mardi 3 novembre 2026

**Objectif du jour.** On compare les premières courbes puis on essaie la descente prévue par le sujet à une fréquence problématique.

**Cas de départ.** Bruit de roulement du RER B. Premier essai proposé à 500 Hz avec c=343 m/s. Les comparaisons utilisent une pression imposée unitaire avec la même phase sur le bord supérieur. La plage 250–2 000 Hz de SOTA.md reste indicative. Avec la grille actuelle, on commence sur 250–1 500 Hz avant d’élargir si nécessaire.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** responsable.

**Ce qui est fait.** Tracer la première courbe et repérer ses pics.

**Fichier à modifier :** `support/postprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures demandées. Conserve les noms et arguments utilisés par les appels existants. Les fonctions fournies, les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Utilise les fréquences et les énergies du mur plan fournies par Yann. Trace une courbe avec les unités et le nom du cas.
2. Repère les points dont l’énergie est plus grande que celle des deux voisins. Propose à Yann quelques fréquences supplémentaires autour des pics les plus élevés.
3. Décris les deux ou trois pics les plus visibles. Réutilise les fonctions de tracé existantes avant d’en ajouter une courte si nécessaire.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Un pic indique une forte réponse du domaine à une source unitaire à cette fréquence. Il donne une fréquence intéressante pour la première optimisation.

**Résultat à transmettre.** Une courbe lisible et une liste courte de pics à confirmer.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** responsable.

**Ce qui est fait.** Comparer les courbes du mur plan et du relief.

**Fichier à modifier :** `support/postprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures demandées. Conserve les noms et arguments utilisés par les appels existants. Les fonctions fournies, les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Ajoute au même graphique les données du mur irrégulier calculées par Yann.
2. Utilise une légende indiquant les formes et les quantités. Vérifie les mêmes fréquences, source et matériau.
3. Compare la hauteur et la position des principaux pics.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Une variation des pics montre que la forme change les résonances et la réponse du domaine. La quantité de matériau doit être indiquée pour interpréter la différence.

**Résultat à transmettre.** Une figure commune et une observation sur les principaux changements.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** responsable.

**Ce qui est fait.** Montrer l’effet d’un recouvrement partiel.

**Fichier à modifier :** `support/postprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures demandées. Conserve les noms et arguments utilisés par les appels existants. Les fonctions fournies, les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Trace pour une même forme les courbes de la répartition initiale et du recouvrement complet.
2. Indique la quantité de matériau dans chaque cas et conserve la même échelle d’énergie.
3. Relève une ou deux fréquences où la différence est importante.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Cette comparaison mesure le changement de réponse lorsque seule une partie du mur porte du matériau. Elle prépare l’étude du meilleur emplacement de cette quantité.

**Résultat à transmettre.** Deux courbes comparées et leurs quantités, avec une courte lecture physique.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Ce qui est fait.** Illustrer ce que la première descente a changé.

**Fichier à modifier :** `support/postprocessing.py`, pour les seuls changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures demandées. Conserve les noms et arguments utilisés par les appels existants. Les fonctions fournies, les autres fichiers et les blocs protégés du programme principal restent inchangés.

1. Affiche la répartition chi avant et après le calcul d’Antoine et de Yann.
2. Compare les champs à la même fréquence avec une même échelle de couleur.
3. Trace les valeurs d’énergie réellement calculées pendant la descente. Note la quantité conservée et le motif d’arrêt transmis par Antoine.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** La descente déplace le matériau pour diminuer l’énergie à la fréquence choisie. Les cartes montrent où le matériau a été placé et comment le champ a réagi.

**Résultat à transmettre.** Une figure avant/après et une courbe de l’énergie pendant la descente.
