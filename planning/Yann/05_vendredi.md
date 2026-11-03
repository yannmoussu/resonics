# Yann — Vendredi 6 novembre 2026

**Objectif du jour.** On termine le rapport et on prépare ensemble la soutenance à partir des résultats obtenus.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[-50, 50]`. Le coefficient suit la convention `d_n u - alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

## To finalize everything

**Repère :** J5.1. **Rôle :** responsable.

**Ce qui est fait.** Terminer les corrections nécessaires sur sa contribution.

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

1. Relis le fichier principal et les résultats utilisés dans le document final.
2. Refais un calcul déjà réalisé et vérifie les paramètres, les unités et les noms de figures.
3. Corrige seulement les erreurs trouvées dans le fichier attribué. Signale les corrections nécessaires ailleurs à la personne concernée.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Le résultat présenté doit correspondre aux paramètres et aux hypothèses réellement utilisés.

**Résultat à transmettre.** Une contribution relue et un exemple qui s’exécute.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** responsable.

**Ce qui est fait.** Préparer son explication pour la soutenance.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Prépare une explication orale sur le modèle, les dimensions et les calculs, en t’appuyant sur une figure retenue.
2. Explique ce qui a été calculé, ce que l’on observe et ce que l’on en conclut. Ajoute un exemple simple pour une notion difficile.
3. Répète avec le groupe pour tenir vingt minutes à cinq, puis prépare les dix minutes de questions.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** La figure doit permettre de relier le calcul numérique au comportement acoustique que l’on cherche à améliorer.

**Résultat à transmettre.** Un texte oral court fourni dans la réponse pour les documents communs.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** responsable.

**Ce qui est fait.** Fournir le texte final de sa contribution.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

Utiliser aussi les paramètres et résultats déjà obtenus pour cette tâche.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Rédige le passage sur le modèle, les dimensions et les calculs avec les figures, les paramètres et les références utilisés.
2. Écris une courte interprétation au-dessous de chaque résultat et annonce clairement les hypothèses.
3. Transmets le texte à Yann pour le document commun au format LaTeX, puis relis son intégration.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le rapport explique les résultats calculés et le raisonnement qui conduit au choix du panneau.

**Résultat à transmettre.** Le texte et les légendes prêts à intégrer dans le modèle LaTeX précédent.
