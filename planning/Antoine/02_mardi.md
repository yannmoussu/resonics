# Antoine — Mardi 3 novembre 2026

**Objectif du jour 2.** Lire les premières courbes, puis obtenir une première baisse d’énergie en déplaçant le matériau.

**Cas de départ.** RER B, source uniforme unitaire en haut et c=343 m/s. Le premier essai est proposé à 500 Hz. La bande 250–2 000 Hz vient de SOTA.md. Avec le maillage actuel, on commence au plus à 1 500 Hz et on vérifie les dix points par longueur d’onde. Les trois gaussiennes restent un essai de sensibilité facultatif.

## Compare the energy of the initial distribution of the porous material (this time the wall has not only absorbing parts but also reflective ones) with the energy for the fully absorbing wall.

**Repère :** J2.3. **Rôle :** contributeur.

**Ce qui est fait.** Comparer la quantité initiale à celle du mur entièrement couvert.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Les fichiers concernés sont en lecture seule. Fournis une explication pour le travail commun.

1. Relève chi et V_obj pour la forme étudiée. Vérifie que les valeurs Robin sont entre zéro et un.
2. Donne à Yann la quantité utilisée pour la future descente. Note aussi celle du cas chi=1 sur tout le mur.
3. Explique à Olympia la différence entre les deux comparaisons : même matériau avec quantité différente pour initial/plein, puis même quantité pour initial/optimisé.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le mur entièrement couvert donne une référence utile. La comparaison initial/optimisé montre l’effet du placement pour une quantité fixée.

**Vérification et résultat à transmettre.** Les deux quantités et la règle à conserver pendant la première descente.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** responsable.

**Ce qui est fait.** Compléter la descente prévue par le support.

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

### Contexte

```text
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », leurs commentaires et leur indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0 dans le second bloc. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les fonctions fournies restent inchangées et les ajouts restent dans ce seul fichier.

1. Reprends le fichier contenant le calcul de Joachim. Complète your_optimization_procedure en gardant sa liste d’arguments et son retour chi,energy,u,grad. Pars d’une seule répartition initiale et d’une seule fréquence choisie parmi les pics.
2. Dans une boucle simple, calcule le coût et le gradient, essaie chi-mu*grad puis applique la projection expliquée lundi aux seuls points Robin. Pour cette forme fixe, la somme à conserver vaut V_obj*S, où S est le nombre de points Robin. Si le coût augmente, divise mu par deux et refais l’essai à partir de la dernière répartition acceptée.
3. Trace les énergies initiale et acceptées, vérifie la somme de chi et ses bornes, puis transmets le fichier à Yann. Prévois un nombre maximal d’itérations et un arrêt si le pas devient trop petit. Annonce la raison de l’arrêt et recalcule le coût final.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** La courbe montre si déplacer le matériau permet de réduire le champ avec la même quantité. Un arrêt du calcul ne garantit pas à lui seul le meilleur placement possible.

**Vérification et résultat à transmettre.** Une première descente qui baisse l’énergie, une répartition finale et sa quantité vérifiée.

**Fichier commun.** Joachim transmet son calcul à Antoine, qui complète la descente, puis Yann lance les essais. Chacun utilise la dernière version reçue.
