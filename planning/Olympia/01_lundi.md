# Olympia — Lundi 2 novembre 2026

**Objectif du jour 1.** Obtenir un premier calcul compréhensible avec le code fourni : un cas RER B, ses paramètres, une figure du champ initial et son énergie. Le groupe présente aussi les choix physiques et les formules demandées. La descente et l’adjoint seront programmés mardi. Aucune nouvelle organisation générale du code n’est à construire lundi.

**Cas retenu.** Bruit de roulement du RER B. La plage 250–2 000 Hz vient de SOTA.md et reste à documenter. Pour le premier calcul, 500 Hz et c=340 m/s sont proposés ; ils sont à confirmer par le groupe. La source est imposée en haut. Les titres des tâches restent ceux de l’énoncé.

**Résultat attendu avant le point quotidien.** Une liste de paramètres, une figure initiale, une valeur d’énergie et les explications de chaque membre. Le coefficient d’exemple du code reste identifié comme tel tant que le matériau n’est pas validé.

## the state of the art ;

**Repère :** J1.1. **Rôle :** responsable.

**Ce qui est fait.** Présenter en quelques points l’état de l’art déjà disponible.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Mur-antibruit-Filoche.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Réutilise SOTA.md réalisé avec Mathis. Prépare une synthèse courte sur le besoin RER B, les solutions existantes et la piste d’un mur irrégulier avec une quantité fixée de poreux. Sépare les performances de la littérature des résultats que le groupe doit encore calculer. Cite les documents utiles. L’objectif est de pouvoir présenter ce choix au premier point avec les enseignants.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une synthèse courte et sourcée, sans refaire un dossier complet.

## the model to consider,

**Repère :** J1.2. **Rôle :** contributeur.

**Ce qui est fait.** Rendre le modèle visible à partir des figures existantes.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `context/Poly-ST5-57-2026.pdf` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

Utilise les figures initiales déjà produites par le code de Yann. Indique où se trouvent la source, l’air, les parois réfléchissantes et le mur comportant du matériau. Un schéma simple ou une légende suffit pour le premier jour. Décris ce que représente la couleur et la fréquence du calcul. Aucune nouvelle fonction de tracé n’est nécessaire si les figures fournies sont lisibles.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une figure initiale compréhensible avec ses conditions aux limites.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Ce qui est fait.** Préparer une comparaison simple pour le lendemain.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.

### Contexte

```text
Cette contribution est une analyse ou une explication. Les fichiers de code joints restent en lecture seule. Donne la réponse dans le message, sans modifier de fichier.

À partir du scénario et des paramètres de Mathis, prépare la liste des calculs de mardi : mur plan entièrement recouvert, profil fourni entièrement recouvert, puis répartition initiale. Note les paramètres à garder identiques. Pour recevoir les résultats, deux tableaux, fréquences et énergies, ainsi que le nom du cas suffisent. Aucun format général de stockage de résultats n’est demandé.

Relis la version reçue et réutilise les calculs déjà présents. Utilise des phrases simples. Conserve les notations du cours, explique les notions nécessaires et distingue les choix du groupe des données fournies. Ne crée aucun nouveau fichier Python. Annonce seulement les calculs réellement exécutés.
```

**Vérification et résultat à transmettre.** Une liste claire de comparaisons et des axes à utiliser pour les courbes.
