# Antoine — Lundi 2 novembre 2026

**Objectif du jour 1.** Obtenir un premier calcul compréhensible avec le code fourni : un cas RER B, ses paramètres, une figure du champ initial et son énergie. Le groupe présente aussi les choix physiques et les formules demandées. La descente et l’adjoint seront programmés mardi. Aucune nouvelle organisation générale du code n’est à construire lundi.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

**Résultat attendu avant le point quotidien.** Une liste de paramètres, une figure initiale, une valeur d’énergie et les explications de chaque membre. Le coefficient d’exemple du code reste identifié comme tel tant que le matériau n’est pas validé.

## formulate optimization problem ;

**Repère :** J1.5. **Rôle :** responsable.

**Ce qui est fait.** Formuler le problème à quantité de matériau fixée.

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
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Écris ce que l’on minimise, la variable chi et ses contraintes. Pour le premier profil fixe, définis la quantité nodale utilisée par le support : V_obj est la moyenne de chi sur les points Robin. Distingue cette fraction de points d’une longueur physique ou d’un volume. Explique le problème continu du cours et le lien avec le calcul fourni. La comparaison de plusieurs géométries demandera ensuite une mesure physique commune.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Le critère, les bornes de chi et la quantité imposée sont écrits et compris par le groupe.

## to choose porous material(s) and its quantity ;

**Repère :** J1.7. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier que la quantité annoncée correspond au premier cas.

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
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Lis la construction de chi et de V_obj dans le support. Avec Mathis, annonce la fraction de points recouverts pour le profil initial. Si une épaisseur et une profondeur sont choisies, précise comment une longueur absorbante permettra de calculer un volume. Ne présente pas V_obj comme une quantité physique identique entre des profils différents. Cette contribution reste une explication, sans nouveau calcul de poids de bord lundi.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** La quantité utilisée dans le premier essai est correctement nommée.

## formulate/consider the numerical gradient descent method.

**Repère :** J1.10. **Rôle :** responsable.

**Ce qui est fait.** Présenter la descente projetée sans la programmer dès lundi.

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
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Décris les étapes du §7.6 : calculer l’état et le gradient, faire un essai de descente, ramener chi entre zéro et un en conservant la quantité, puis recalculer l’énergie et réduire le pas si nécessaire. Pour une forme fixe et la quantité nodale du support, explique une projection par décalage et dichotomie. Donne un petit exemple chiffré. Garde your_optimization_procedure commentée dans le lancement tant que le gradient n’est pas vérifié. L’implémentation de la descente est prévue mardi.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Un algorithme écrit et un exemple de projection, sans bibliothèque d’optimisation à construire lundi.

**Ordre des modifications du fichier commun.** Joachim complète le coût, puis Yann ajoute les paramètres et l’affichage du premier résultat. Antoine prépare la méthode dans le texte.
