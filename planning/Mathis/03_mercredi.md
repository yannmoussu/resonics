# Mathis — Mercredi 4 novembre 2026

**Objectif du jour.** On regarde toute la bande et on teste quelques fréquences et quantités ensemble avec les calculs déjà construits.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[-50, 50]`. Le coefficient suit la convention `d_n u - alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** responsable.

**Ce qui est fait.** Donner un sens physique à la quantité de matériau.

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
Réutilise compute_alpha dans compute_alpha.py avec les paramètres du programme principal. Explique le coefficient obtenu et ses unités. Les fonctions de maillage et les blocs protégés du programme principal restent inchangés.

1. Avec Yann et Antoine, additionne les longueurs des segments absorbants représentés sur le mur. Pour une densité intermédiaire, utilise la contribution correspondante de chi.
2. Si une épaisseur et une profondeur sont fixées, calcule volume=longueur_absorbante*epaisseur*profondeur. Donne les unités et les hypothèses.
3. Choisis deux ou trois quantités réalisables. Ajoute un calcul court dans preprocessing.py seulement s’il manque au moment de cette étude.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Une même fraction des points peut représenter davantage de matériau sur une paroi plus longue. La longueur ou le volume permet une comparaison à ressource égale.

**Résultat à transmettre.** Les quantités physiques qui serviront aux quelques essais du groupe.
