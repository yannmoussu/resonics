# Joachim — Mardi 3 novembre 2026

**Objectif du jour 2.** Lire les premières courbes, puis obtenir une première baisse d’énergie en déplaçant le matériau.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## Optimize numerically for one or several of the most problematic frequencies (at which there is a maximum of the energy) ;

**Repère :** J2.4. **Rôle :** contributeur.

**Ce qui est fait.** Calculer le gradient nécessaire à la première descente.

**Fichier à modifier :** `support/processing.py`, seulement pour les fonctions de calcul ajoutées.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.
- `support/processing.py` — fichier à modifier.
- `support/postprocessing.py` — lecture seule.
- `support/_env.py` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.
- `context/Dirichlet_Nonhomogene.pdf` — lecture seule.

### Contexte

```text
Modifie seulement les fonctions de calcul ajoutées dans processing.py, en particulier compute_state, compute_adjoint, compute_gradient et validate_adjoint_gradient. Conserve les fonctions initiales du support et la convention du polycopié. Le programme principal importe ces calculs et conserve ses deux blocs protégés.

1. Vérifie dans compute_state et compute_adjoint le calcul de l’adjoint décrit lundi. Reprends les appels d’assemblage de processing.py pour obtenir exactement le système A U=b du solveur fourni, sans modifier ses fonctions. U est le champ rangé dans un vecteur. Pour le critère J=U.conj().T W U, W vaut h² aux points intérieurs et zéro ailleurs.
2. Résous A.conj().T P=2*W*U : P est l’adjoint discret et conj().T désigne la transposée conjuguée. Avec la source fixée et f_rob nul, une variation de chi modifie A et la dérivée vaut -Re(P.conj().T A_prime U). Déduis A_prime de la formule Robin réellement assemblée. Pour les coefficients unitaires du support, le terme diagonal -h*Alpha*chi/(1+h*Alpha*chi) a pour dérivée -h*Alpha/(1+h*Alpha*chi)**2. Additionne les contributions des voisins intérieurs de chaque point Robin.
3. Utilise validate_adjoint_gradient et vérifie une seule direction de variation d sur une petite grille : compare la somme grad*d à (J(chi+t*d)-J(chi-t*d))/(2*t), pour deux petites valeurs de t. Utilise une chi permettant les perturbations. Explique les valeurs obtenues, puis transmets le calcul de coût, champ et gradient à Antoine.

Utilise la version reçue du fichier commun et les résultats réellement calculés. Explique chaque grandeur et chaque étape. Les commentaires du code sont des phrases françaises sans équations.
```

**Interprétation physique.** Le gradient relie une modification locale du matériau à la variation de l’énergie totale. Le petit essai confirme le sens de variation avant de lancer une descente.

**Vérification et résultat à transmettre.** Un gradient compris et vérifié sur un exemple, prêt pour la descente du même jour.

**Fichier commun.** Joachim transmet son calcul à Antoine, qui complète la descente, puis Yann lance les essais. Chacun utilise la dernière version reçue.
