# Olympia — Jeudi 5 novembre 2026

**Objectif du jour 4.** Vérifier les meilleurs résultats et choisir un produit. On limite les nouveaux essais à ceux qui peuvent changer la conclusion.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** responsable.

**Ce qui est fait.** Vérifier que les conclusions résistent aux derniers calculs.

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

Compare les courbes au pas initial et au pas plus fin, puis les quelques départs testés. Utilise les mêmes références et quantités. Sélectionne les figures qui changent ou confirment le choix du produit. Un tableau court et une courbe sont suffisants.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une comparaison claire des vérifications utiles au choix final.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** responsable.

**Ce qui est fait.** Contribuer au choix du panneau avec les courbes comparatives et le compromis performance/matériau.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.

Joindre aussi les paramètres et les résultats de la veille utilisés dans cette tâche.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

À partir des résultats fournis, propose une conclusion courte sur les courbes comparatives et le compromis performance/matériau. Le choix concerne un panneau pour le scénario RER B et la bande réellement calculés. Cite les valeurs décisives, les quantités et les formes comparées. Distingue les résultats obtenus des perspectives de SOTA.md. Fais valider la conclusion par le groupe sans inventer de performance manquante.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une décision appuyée sur une figure et quelques valeurs vérifiables.
