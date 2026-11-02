# Olympia — Mardi 3 novembre 2026

**Objectif du jour 2.** Calculer les références demandées, repérer quelques pics et faire une première descente après vérification du gradient. On complète les fonctions prévues dans le support, avec des tableaux simples de fréquences et d’énergies.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** responsable.

**Ce qui est fait.** Tracer énergie et fréquences pour le mur plan.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

À partir des deux tableaux transmis par Yann, trace l’énergie en fonction de la fréquence. Repère les maxima locaux par comparaison avec les valeurs voisines. Renvoie à Yann les intervalles à calculer plus précisément. Une fonction de tracé courte dans postprocessing.py suffit ; indique les unités et les paramètres du cas.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une courbe lisible et quelques pics à confirmer.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** responsable.

**Ce qui est fait.** Comparer les références entièrement recouvertes.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

Ajoute les courbes des profils calculés au même graphique que le plan, avec une légende claire. Vérifie les mêmes bande, source et matériau. Affiche la quantité de chaque mur entièrement recouvert. Reprends la même recherche de pics, sans créer un format général de résultats.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une comparaison directe du plan et des profils disponibles.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** responsable.

**Ce qui est fait.** Comparer répartition initiale et recouvrement complet.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

Trace les deux courbes d’une même forme avec les données de Yann. Indique la quantité dans chaque cas et conserve les valeurs d’énergie calculées. Si un rapport en décibels est présenté, utilise 10*log10(E_reference/E_cas) avec des énergies positives et une référence clairement nommée. Il s’agit du critère du modèle, pas d’une mesure du bruit du RER B en situation réelle.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une comparaison dont les différences de quantité sont visibles.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Ce qui est fait.** Montrer le résultat de la première descente.

**Fichier à modifier :** `support/postprocessing.py`, seulement pour les changements nécessaires.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/postprocessing.py` — fichier à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/_env.py` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Modifie seulement postprocessing.py pour les figures nécessaires. Les autres fichiers restent inchangés, notamment les deux blocs « Do not modify this cell » du programme principal. Conserve les noms et arguments déjà utilisés par les appels de tracé.

Utilise les tracés du support pour afficher chi et le champ avant et après la descente. Les deux champs doivent partager la même échelle de couleur. Trace seulement les valeurs d’énergie effectivement calculées aux itérations acceptées, sans ajouter les zéros inutilisés d’un tableau créé à l’avance. Indique la fréquence et la quantité.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une comparaison avant/après qui correspond à un calcul réellement effectué.
