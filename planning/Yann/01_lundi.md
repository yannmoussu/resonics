# Yann — Lundi 2 novembre 2026

**Objectif du jour.** On obtient un premier champ et son énergie avec le code fourni. Chacun apporte une explication ou un petit calcul nécessaire au résultat du groupe.

**Cas de départ.** Le choix `SOURCE` du programme principal est commun au champ initial, à la descente et à la courbe de fréquences. On utilise par défaut `source_rer_b(y, omega)` et la laine de roche `MATERIAUX["LAINE_ROCHE"]`, avec `ALPHA0=[50, -50]`. Le coefficient suit la convention `d_n u + alpha(omega)*chi*u=0` et est calculé à chaque pulsation. Le cas initial utilise `OMEGA=3430 rad/s`, puis la bande va de 50 à 3 500 Hz, avec N=128, M=256 et c=343 m/s.

**À montrer lundi.** Les paramètres, un champ initial, sa valeur d’énergie et les explications du groupe. Les formules demandées sont étudiées lundi, puis utilisées quand la descente est programmée mardi.

## the model to consider,

**Repère :** J1.2. **Rôle :** responsable.

**Ce qui est fait.** Obtenir une première carte de pression avec le programme fourni.

**Fichier à modifier :** `support/demo_control_polycopie2024.py`, pour les seuls changements nécessaires.

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
Modifie seulement demo_control_polycopie2024.py. Conserve intégralement les deux blocs « Do not modify this cell, these are the values that you will be assessed against. », avec leurs lignes, commentaires et indentation. Garde l’appel de solve_helmholtz et les copies chi0 et u0. Complète les fonctions étudiantes et les blocs « Fell free to modify the function call in this cell. ». Les essais supplémentaires utilisent leurs propres tableaux après les blocs protégés. Conserve les signatures et les retours du support.

1. Garde la géométrie actuelle level=1. Repère le bord supérieur excité, les côtés réfléchissants et le mur inférieur Robin.
2. Reprends OMEGA=3430 rad/s et C=343 m/s pour le cas initial, puis calcule wavenumber=OMEGA/C. Garde une source choisie, avec la même phase, sur le bord supérieur Dirichlet.
3. Lance solve_helmholtz par le programme existant. Affiche le module abs(u0) avec myimshow déjà fournie dans postprocessing.py, puis l’énergie donnée par la fonction complétée par Joachim. Présente cette carte comme le champ initial. Note les paramètres à côté de la figure.

Réutilise les calculs présents. Ajoute seulement le calcul nécessaire à ces étapes. Les commentaires restent des phrases françaises. Aucun nouveau fichier Python.
```

**Interprétation physique.** Les zones où le module de la pression est élevé indiquent où les oscillations sont les plus fortes. Un premier champ suffit pour comprendre le modèle avant de chercher à améliorer le mur.

**Résultat à transmettre.** Une figure du champ initial, une valeur d’énergie et la liste des paramètres utilisés.

## the plage of frequencies of the interest, dimensions, noise sources ;

**Repère :** J1.3. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier que la grille représente correctement la fréquence choisie.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Calcule lambda=c/f pour f=OMEGA/(2*pi) et c=343 m/s. Compare cette longueur au pas h du support.
2. Vérifie lambda/h>=10, comme demandé dans l’énoncé. Avec N=128 et h=0,0078125 m, la règle est respectée jusqu’à 3 500 Hz.
3. Relève N, M, h, level et les dimensions effectivement obtenues dans les coordonnées. Transmets ce petit tableau à Mathis et Olympia.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Une onde doit être décrite par plusieurs points de grille pour que sa propagation soit correctement approchée. Les dimensions sont celles du domaine calculé.

**Résultat à transmettre.** Un petit tableau avec les unités et le nombre de points par longueur d’onde.

## Theoretical study : considering that one boundary is open-air (the wave go through without coming back) derive the energy over the form and compare the result with the analogous result with a reflexive boundary[^1].

**Repère :** J1.6. **Rôle :** contributeur.

**Ce qui est fait.** Donner à Joachim les conditions aux limites utilisées dans le programme.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Repère les côtés Neumann, le bord Dirichlet et le mur Robin dans le domaine fourni.
2. Lis compute_robin_condition et relève son signe. Aide Joachim à traduire la condition ouverte de l’énoncé avec cette convention.
3. Explique sur un schéma quelle paroi latérale serait ouverte dans son étude. La source supérieure reste la même.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Une paroi rigide réfléchit l’onde. Une condition ouverte représente au contraire un départ d’onde hors du domaine et introduit un flux sortant.

**Résultat à transmettre.** Le schéma des frontières et les conventions nécessaires à l’étude théorique.

## find numerically the corresponding complex coefficient(s) $\alpha(\omega)$ for the porous matherial(s) ; to compare the performances if several ;

**Repère :** J1.8. **Rôle :** contributeur.

**Ce qui est fait.** Vérifier que le coefficient de compute_alpha est utilisé avec le signe du support.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Lis compute_alpha.py et repère le matériau, les unités, la pulsation et le couple de départ choisis au début du programme principal.
2. Utilise partout la condition du polycopié d_n u+alpha*chi*u=0. compute_alpha fournit directement ce coefficient complexe, donc alpha_rob=Alpha*chi est construit avec la valeur renvoyée.
3. Vérifie la réussite du calcul et la construction de alpha_rob dans le bloc autorisé. Pour la courbe fréquentielle, le coefficient est recalculé à chaque pulsation avec la même source choisie.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Le signe et la partie complexe du coefficient décrivent l’échange avec le mur. Une erreur de convention peut transformer un effet absorbant attendu en un résultat non physique.

**Résultat à transmettre.** Une valeur de coefficient avec sa fréquence, son origine et la convention du code.

## find energy derivative over the distribution of the porous inclusions ;

**Repère :** J1.9. **Rôle :** contributeur.

**Ce qui est fait.** Comprendre où la répartition de matériau intervient dans le système.

**Fichier à modifier :** aucun pour cette contribution.

### Fichiers concernés

- `SOTA.md` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `support/processing.py` — lecture seule.
- `support/preprocessing.py` — lecture seule.

### Contexte

```text
Lis les fichiers concernés pour expliquer cette tâche et donne le résultat dans la réponse. Les programmes restent inchangés pour cette contribution.

1. Repère la ligne alpha_rob=Alpha*chi et son utilisation dans compute_robin_condition.
2. Avec Joachim, compare verbalement chi=0 et chi=1 sur un point du mur. Note quelle entrée du système dépend de cette valeur.
3. Donne-lui cette information pour sa dérivée. Le calcul du gradient sera ajouté seulement au moment de la descente.

Explique les grandeurs utilisées et appuie la conclusion sur les documents ou les résultats fournis.
```

**Interprétation physique.** Faire varier chi modifie le comportement local du mur et, par propagation, le champ de pression dans tout le domaine.

**Résultat à transmettre.** L’endroit du code concerné et une explication du rôle de chi.

[^1]: To model the open-air type of boundaries, it is convient to consider the Sommerfeld radiation condition of the form $\frac{\partial v}{\partial n} - ik\operatorname{Tr}v = 0$ with the notation $u(x,t) = e^{-ikt}v(x)$ for the propagative wave.

**Fichier commun.** Joachim complète le coût, puis Yann ajoute les paramètres et l’affichage du premier résultat. Antoine prépare la méthode dans le texte.
