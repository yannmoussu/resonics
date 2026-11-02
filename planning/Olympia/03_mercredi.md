# Olympia — Mercredi 4 novembre 2026

**Objectif du jour.** On regarde toute la bande et on teste quelques fréquences et quantités ensemble avec les calculs déjà construits.

**Cas de départ.** Bruit de roulement du RER B. Premier essai proposé à 500 Hz avec c=343 m/s. Les comparaisons utilisent une pression imposée unitaire avec la même phase sur le bord supérieur. La plage 250–2 000 Hz de SOTA.md reste indicative. Avec la grille actuelle, on commence sur 250–1 500 Hz avant d’élargir si nécessaire.

## Analyze the obtained results to compare to the efficient performances on the fixed range of frequencies ; to compare to a fully absorbing wall ;

**Repère :** J3.1. **Rôle :** responsable.

**Ce qui est fait.** Vérifier si la baisse d’énergie s’étend à la bande.

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

1. Superpose les courbes initiale, optimisée à une fréquence et entièrement recouverte.
2. Compare le plus grand pic calculé et une moyenne sur la bande avec la méthode des trapèzes, qui tient compte des écarts entre fréquences.
3. Repère les fréquences où l’amélioration est faible ou où l’énergie augmente.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Une amélioration à un pic ne garantit pas une amélioration partout. Cette figure explique pourquoi une recherche sur plusieurs fréquences peut être utile.

**Résultat à transmettre.** Une courbe de comparaison et une conclusion sur l’étendue de l’amélioration.

## to optimize the energy at once at several different frequencies ;

**Repère :** J3.2. **Rôle :** contributeur.

**Ce qui est fait.** Comparer la recherche à une fréquence et le compromis multifréquence.

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

1. Ajoute la courbe obtenue avec une seule répartition optimisée pour plusieurs fréquences.
2. Indique les fréquences utilisées pour la recherche et garde les mêmes source et quantité dans la comparaison.
3. Compare les plus grands pics et la même moyenne de bande. Si le groupe teste les gaussiennes, présente séparément cette pondération hypothétique.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Une répartition commune peut réduire plusieurs résonances au prix d’un gain moindre sur un seul pic. Les poids du spectre influencent ce compromis.

**Résultat à transmettre.** Une figure montrant le compromis obtenu avec les fréquences réellement utilisées.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** contributeur.

**Ce qui est fait.** Montrer le lien entre quantité de matériau et résultat.

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

1. Reprends les deux ou trois quantités calculées par Yann et Mathis sur une même forme.
2. Trace la moyenne d’énergie de bande en fonction de la longueur ou du volume de matériau, avec les unités.
3. Garde le recouvrement complet comme référence avec sa propre quantité. Décris si le gain change beaucoup entre deux quantités voisines.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** La courbe aide à choisir une quantité raisonnable lorsque l’ajout de matériau n’apporte plus qu’une faible amélioration dans les essais effectués.

**Résultat à transmettre.** Une petite courbe quantité/performance et son interprétation.
