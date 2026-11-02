# Joachim — objectif, état adjoint et gradient

Les repères **J1 à J5** du Gantt correspondent aux cinq journées, du lundi au vendredi.

## Mission et livrable

Tu prends en charge le calcul du critère acoustique, sa dérivée par rapport à la répartition du matériau et l'étude théorique comparant une paroi réfléchissante à une ouverture. Tu écris **un seul fichier Python, `objectif.py`**, qui ne modifie aucun fichier du support. Les imports autorisés sont NumPy, SciPy, Matplotlib et la bibliothèque standard. Le fichier doit pouvoir être lancé seul pour exécuter des vérifications synthétiques.

Ton fichier reçoit la fonction d'assemblage comme argument. Il n'importe donc ni le fichier de Yann ni le fichier d'Antoine. Les conventions, signatures, algorithmes et vérifications nécessaires sont décrits ci-dessous. Les commentaires et docstrings du code sont des phrases françaises ; les expressions mathématiques restent dans les calculs Python et dans les explications du présent document.

### Livraisons de la semaine

- **Lundi 2 novembre** : objectif sur grille, contrats de retour, dérivation de l'adjoint discret et premiers tests sur une petite matrice. Tu fixes aussi le scénario ouvert/réfléchissant avec Yann.
- **Mardi 3 novembre** : gradient vérifié par différences centrées, puis réception de la première descente monofréquence réalisée par Antoine. Tu vérifies le sens de la variation du coût et les conventions du modèle.
- **Mercredi 4 novembre** : somme multifréquence et test de son gradient ; interprétation des résultats sur la bande de fréquences et sur plusieurs quantités de matériau.
- **Jeudi 5 novembre** : vérifications sur maillage plus fin, analyse de la comparaison ouverte/réfléchissante et rédaction des équations et limites effectivement validées.
- **Vendredi 6 novembre** : validation finale et préparation d'une intervention d'environ quatre minutes pour la soutenance collective de vingt minutes, suivie de dix minutes de questions.

La séance quotidienne de suivi se situe dans le créneau **14 h 30–17 h**. Tu y présentes une équation justifiée, un test reproductible et l'état des difficultés de ton lot.

## 1. Modèle, unités et inconnues

On travaille en différences finies sur une grille régulière de pas `spacestep`, exprimé en mètres. La fréquence publique `frequency_hz` est en hertz. La pulsation et le nombre d'onde sont

$$
\omega=2\pi f,\qquad k=\frac{\omega}{c},\qquad \lambda=\frac{c}{f}
$$

La variable historique `omega` du solveur distribué est utilisée au carré dans sa matrice. Avec les coefficients fournis, elle reçoit **le nombre d'onde**, et non les hertz ou la pulsation physique. Yann effectue cette conversion avant l'assemblage.

La convention temporelle commune est une dépendance en exponentielle complexe de signe négatif. Avec une normale sortante, la condition physique sur le mur s'écrit

$$
\partial_n u+a_{\mathrm{phys}}\chi u=0
$$

La condition effectivement assemblée par le support correspond à

$$
\partial_n u-a_{\mathrm{code}}\chi u=0,
\qquad a_{\mathrm{code}}=-a_{\mathrm{phys}}
$$

Pour une impédance de surface documentée, définie comme la pression divisée par la vitesse normale sortante,

$$
a_{\mathrm{code}}=\frac{\mathrm{i}\omega\rho_{\mathrm{air}}}{Z_s}
$$

Le coefficient complexe constant du démo sert à vérifier un calcul ; il ne suffit pas à identifier un matériau réel. La validation physique de ce coefficient est du ressort de Mathis et Yann. Les formules de ton fichier utilisent les coefficients et dérivées effectivement transmis par la fonction d'assemblage.

La densité `chi` est un vecteur **réel** de longueur `B`, compris entre zéro et un. Chaque composante correspond à un nœud Robin de conception du mur qui touche au moins une face intérieure. Les frontières Robin employées pour une ouverture ne font pas partie de ce vecteur. La géométrie ne change pas pendant une optimisation ; chaque forme fait l'objet d'un calcul distinct.

Les `design_weights` sont des longueurs discrètes : pour chaque variable de conception, on multiplie le pas par le nombre de faces adjacentes au fluide. Le budget physique est fixé par

$$
\sum_{\ell=1}^{B}w_\ell\chi_\ell=L_{\mathrm{mat}}
$$

Ces poids servent à la projection écrite par Antoine. Le gradient que tu renvoies est **euclidien**, c'est-à-dire qu'une variation réelle vérifie

$$
\mathrm{d}J[\delta\chi]=\sum_{\ell=1}^{B}g_\ell\,\delta\chi_\ell
$$

Tu ne divises donc pas ce gradient par les longueurs de conception.

### Propriétés du problème à formuler lundi

Écris la formulation faible avec les parties Dirichlet, Neumann et Robin clairement séparées, puis indique les hypothèses de régularité du domaine, des données et du coefficient complexe employées. Pour le problème homogène, utilise la partie imaginaire de l'identité énergétique pour expliquer le rôle de la dissipation ou de la frontière ouverte dans l'unicité. Précise les hypothèses supplémentaires du résultat invoqué et sa référence. Le cas entièrement réfléchissant peut présenter des fréquences propres singulières ; la méthode coercive du problème de Poisson ne se transpose pas automatiquement à Helmholtz.

Distingue le résultat continu de la condition d'inversibilité de la matrice effectivement résolue. Un petit résidu contrôle la résolution d'un système, tandis que le raffinement et les cas de référence contrôlent la représentation du problème. Présente ces propriétés au premier point et fais valider l'interprétation de la demande d'étude de l'énergie en fonction de la forme. Si une dérivée géométrique de forme est attendue, sépare cette tâche de la dérivée de densité calculée ci-dessous.

## 2. Fonctions publiques à écrire

```python
def your_compute_objective_function(domain_omega, u, spacestep):
    ...


def evaluate_frequency(chi, frequency_hz, assemble, with_gradient=True):
    ...


def evaluate_band(chi, frequencies_hz, frequency_weights, assemble,
                  reference_energies=None, with_gradient=True):
    ...
```

Les trois fonctions ainsi que leurs éventuels helpers et tests restent dans `objectif.py`. L'adaptation à l'ancienne signature longue du démo sera faite dans le fichier de Yann.

### Contrat de `assemble`

Tu appelles la fonction reçue en argument de la manière suivante :

```python
payload = assemble(chi, frequency_hz)
```

Elle renvoie un dictionnaire contenant :

| Clé | Type et taille | Sens |
|---|---|---|
| `A` | Matrice creuse complexe, taille `(n, n)` | Système après élimination des valeurs aux bords, restreint aux nœuds intérieurs |
| `b` | Vecteur complexe, taille `(n,)` | Second membre, incluant le Dirichlet non homogène |
| `cell_weights` | Vecteur réel strictement positif, taille `(n,)` | Poids de l'intégrale intérieure ; avec le support, chaque poids vaut le carré du pas |
| `face_rows` | Vecteur d'entiers, taille `(n_faces,)` | Ligne intérieure à laquelle contribue une face de conception |
| `face_design` | Vecteur d'entiers, taille `(n_faces,)` | Indice de la variable de conception contrôlant cette face |
| `dA_diag` | Vecteur complexe, taille `(n_faces,)` | Dérivée de la contribution diagonale de la face par rapport à cette variable |

Les indices des lignes vont de zéro à `n-1` et ceux des variables de zéro à `B-1`. Les répétitions sont normales : un nœud de conception peut toucher plusieurs faces intérieures, et une ligne intérieure peut recevoir plusieurs contributions de bord. Toutes ces contributions doivent être additionnées.

Le contrat suppose que `b` est indépendant de `chi`. C'est le cas des données imposées avec second membre Robin nul. Une modification de cette hypothèse demanderait une dérivée du second membre, qui n'est pas fournie par cette interface.

## 3. Objectif sur la grille fournie

`your_compute_objective_function(domain_omega, u, spacestep)` prend deux tableaux de même forme. Le domaine contient les labels suivants :

| Label | Signification |
|---|---|
| `-1` | Intérieur du fluide |
| `-2` | Complémentaire du domaine |
| `1` | Dirichlet |
| `2` | Neumann |
| `3` | Robin |

La fonction calcule

$$
J_h=h^2\sum_{(i,j)\,\text{intérieur}}|u_{i,j}|^2
$$

Méthode :

1. Vérifier que le pas est un réel fini strictement positif et que les deux tableaux ont la même forme bidimensionnelle.
2. Former le masque des nœuds dont le label vaut moins un.
3. Vérifier que les valeurs du champ sur ce masque sont finies.
4. Calculer le module des valeurs complexes, l'élever au carré, additionner et multiplier par le carré du pas.
5. Renvoyer un `float` réel positif ou nul.

Le support renvoie des zéros aux nœuds de bord même quand la pression physique n'y est pas nulle. L'intégration porte ici sur les seuls nœuds intérieurs. Le carré complexe de la pression ne représente pas le module au carré.

Le critère du sujet mesure l'intégrale de pression au carré. Il n'est pas directement une puissance dissipée. Les cartes et les bilans physiques doivent être interprétés séparément.

### Tests autonomes de cette fonction

Dans un petit tableau de labels construit directement dans ton fichier, placer quatre nœuds intérieurs et un champ constant égal à un nombre complexe dont la partie réelle vaut trois et la partie imaginaire quatre. Avec un pas de deux dixièmes, le résultat attendu est quatre. Tester également :

- champ nul : résultat nul ;
- valeurs différentes hors de l'intérieur : résultat inchangé ;
- multiplication de tout le champ par une phase complexe de module un : résultat inchangé ;
- tailles incompatibles, pas nul ou négatif et valeur intérieure non finie : erreur descriptive.

Ces valeurs servent uniquement à réceptionner la fonction d'intégration.

## 4. Évaluation à une fréquence

### 4.1 État direct et objectif

Avec la densité et la fréquence reçues, appeler `assemble`, vérifier les dimensions et résoudre

$$
A(\chi,f)U=b(f)
$$

Le vecteur `U` est le champ **total** aux nœuds intérieurs. Poser

$$
W=\operatorname{diag}(\texttt{cell\_weights}),\qquad J=U^*WU
$$

Le symbole étoile désigne ici la transposée conjuguée. Il suffit de multiplier les poids composante par composante ; aucune matrice diagonale dense n'est nécessaire.

Le second membre inclut déjà l'effet de la pression imposée au bord source. Le document sur Dirichlet non homogène montre que la formule du gradient doit utiliser le champ total. Remplacer ce champ par sa seule partie de trace homogène ferait perdre une contribution.

Calculer et enregistrer le résidu relatif

$$
r_u=\frac{\|AU-b\|_2}{\max(\|b\|_2,10^{-30})}
$$

La petite valeur au dénominateur évite une division par zéro lorsque le second membre est nul. Pour les petits tests proposés, un résidu inférieur à un cent-millionième constitue un seuil de réception raisonnable. Un petit résidu vérifie la résolution du système ; il ne vérifie pas à lui seul la discrétisation physique.

### 4.2 État adjoint discret

Lorsque `with_gradient` est vrai, résoudre

$$
A^*P=2WU
$$

La conjugaison est nécessaire parce que les coefficients sont complexes. Le facteur deux vient de la dérivée réelle du module au carré. On peut factoriser la matrice creuse une seule fois avec SciPy, puis résoudre le système direct et son transposé conjugué avec cette factorisation. Une seconde résolution avec la matrice transposée conjuguée est également correcte pour une première version. Aucune inverse explicite n'est calculée.

Calculer le résidu de l'adjoint avec la même définition que pour l'état, en remplaçant le second membre par son expression ci-dessus.

### 4.3 Gradient réel euclidien

Pour une variation de densité réelle et un second membre indépendant de la densité,

$$
A\,\delta U=-\delta A\,U
$$

et le choix de l'adjoint donne

$$
\mathrm{d}J[\delta\chi]=-\operatorname{Re}(P^*\delta A\,U)
$$

Pour chaque variable,

$$
g_\ell=-\operatorname{Re}\left(P^*\frac{\partial A}{\partial\chi_\ell}U\right)
$$

Le tableau de faces transmis par `assemble` rend ce calcul explicite. Initialiser un vecteur réel nul de taille `B`, puis pour chaque face ajouter

$$
-\operatorname{Re}\left(
\overline{P_{\texttt{face\_rows}}}
\;\texttt{dA\_diag}\;
U_{\texttt{face\_rows}}
\right)
$$

à la composante désignée par `face_design`. Pour une version vectorisée, `numpy.add.at` permet une accumulation correcte lorsque les indices de conception se répètent.

Dans le cas fourni avec coefficients unitaires et second membre Robin nul, la correction issue de l'élimination d'un voisin de bord est

$$
c(a)=1+\frac{ha}{1-ha}=\frac{1}{1-ha},\qquad a=\mathrm{Alpha}_{\mathrm{code}}\chi_\ell
$$

Sa dérivée est donc

$$
\frac{\partial c}{\partial\chi_\ell}
=\frac{h\,\mathrm{Alpha}_{\mathrm{code}}}
{(1-h\,\mathrm{Alpha}_{\mathrm{code}}\chi_\ell)^2}
$$

C'est la valeur de `dA_diag` de chaque face concernée. Le dénominateur est un **carré complexe**, pas un module au carré. La partie réelle est prise à la fin du produit avec le champ et l'adjoint.

### 4.4 Valeurs renvoyées

`evaluate_frequency` renvoie au moins :

```python
{
    "value": valeur_reelle,
    "gradient": gradient_reel_ou_None,
    "state": champ_interieur_complexe,
    "state_residual": residu_reel,
    "adjoint_residual": residu_reel_ou_None,
    "frequency_hz": frequence_reelle
}
```

Lorsque `with_gradient=False`, le coût et l'état sont calculés, mais aucune résolution adjointe n'est effectuée. Les deux champs liés à l'adjoint valent `None`. Les entrées sont préservées.

## 5. Somme sur plusieurs fréquences

`evaluate_band` reçoit des vecteurs de fréquences et de poids de même longueur non nulle. Les fréquences sont finies et strictement positives ; les poids sont finis, positifs ou nuls et de somme un. Les poids sont fixés pendant l'optimisation.

Sans normalisation, prendre une énergie de référence unitaire à chaque fréquence. Si `reference_energies` est fourni, vérifier qu'il a la bonne taille et contient uniquement des réels finis strictement positifs. Les références sont gelées avant l'optimisation et communes aux produits comparés. On calcule

$$
F(\chi)=\sum_{m=1}^{Q}q_m\frac{J_m(\chi)}{J_m^{\mathrm{ref}}},
\qquad
\nabla F(\chi)=\sum_{m=1}^{Q}\frac{q_m}{J_m^{\mathrm{ref}}}\nabla J_m(\chi)
$$

La même densité est transmise à toutes les fréquences. Conserver les énergies brutes pour les graphiques, même si le coût d'optimisation est normalisé.

Le dictionnaire contient au minimum :

```python
{
    "value": cout_total_reel,
    "gradient": gradient_total_reel_ou_None,
    "energies": energies_brutes_par_frequence,
    "state_residuals": residus_par_frequence
}
```

Une fréquence de poids nul peut être évaluée pour conserver sa mesure, sans calculer un adjoint inutile. La somme des gradients doit utiliser exactement les coefficients employés dans la somme des coûts.

## 6. Réception du gradient dans le même fichier

Écrire un petit assembleur **synthétique** dans le bloc de tests. Il construit une matrice creuse de taille trois, un second membre complexe fixé et deux variables de conception. Un exemple utile emploie les tableaux de faces suivants :

```python
face_rows = numpy.array([0, 1, 1])
face_design = numpy.array([0, 0, 1])
```

La première variable agit donc sur deux lignes intérieures et la deuxième partage une ligne avec elle. Choisir une matrice de base clairement inversible, par exemple une matrice tridiagonale symétrique réelle à diagonale dominante, puis ajouter à chaque ligne de face la correction Robin ci-dessus. Utiliser le même calcul analytique pour construire `dA_diag`.

Pour chaque composante, puis pour une direction réelle non nulle, comparer le gradient à

$$
\frac{F(\chi+td)-F(\chi-td)}{2t}
\quad\text{et}\quad g\cdot d
$$

Partir d'une densité strictement intérieure aux bornes, afin que les perturbations restent admissibles. Utiliser plusieurs pas entre un centième et un millionième. Les erreurs doivent d'abord décroître approximativement comme le carré du pas, puis être limitées par l'arrondi. Si l'on teste une direction tangentielle au budget, vérifier également que son produit scalaire avec les longueurs de conception est nul.

Ajouter les vérifications suivantes :

- les appels sans gradient et avec gradient donnent le même coût ;
- le gradient est réel, fini et de taille `B` ;
- les contributions répétées des faces sont bien additionnées ;
- le gradient de bande coïncide avec la somme pondérée des gradients individuels ;
- le test centré reste correct avec des références fréquentielles non unitaires ;
- multiplier le second membre par une phase complexe commune conserve le coût et le gradient ;
- une taille incohérente, un poids cellulaire non positif ou une référence nulle déclenche une erreur claire.

Un contrôle local a déjà confirmé la formule sur le support intact. Ses paramètres sont une grille de **16 colonnes et 32 lignes**, une frontière de niveau **1**, un nombre d'onde **3,1**, un coefficient code de partie réelle **2** et de partie imaginaire **3**, puis une densité uniforme **0,4**. Le test comporte **32 nœuds Robin**, avec jusqu'à **deux voisins intérieurs** par nœud. Il porte sur la dérivée de l'objectif avant projection.

| Pas de différence centrée | Erreur relative de dérivée directionnelle |
|---|---|
| `1e-2` | `1.8128e-5` |
| `1e-3` | `1.8129e-7` |
| `1e-4` | `1.8335e-9` |

Ces valeurs sont des **contrôles du gradient**, pas des performances d'un matériau ou d'un produit.

## 7. Étude théorique : ouverture et réflexion

Cette étude compare des problèmes définis de façon cohérente. Le scénario de départ garde une pression imposée non nulle sur le bord supérieur, un mur poreux sur sa frontière de conception et des côtés réfléchissants. Pour le scénario ouvert, Yann remplace explicitement **une paroi latérale** par la condition de Sommerfeld, en conservant le bord source. Cela évite de supprimer simultanément la source et la réflexion. Le choix précis de la paroi est enregistré dans les paramètres.

Avec notre convention temporelle, la condition ouverte est

$$
\partial_nu-\mathrm{i}ku=0
$$

Cette condition locale constitue l'approximation ouverte proposée dans le sujet. Pour le problème physique

$$
\Delta u+k^2u=f\quad\text{dans }\Omega,
\qquad u=g\quad\text{sur }\Gamma_D
$$

avec une Robin physique sur le mur et une ouverture sur une autre partie du bord, une identité de Green donne

$$
\int_\Omega|\nabla u|^2-k^2\int_\Omega|u|^2
+\int_{\Gamma}\!a_{\mathrm{phys}}\chi|u|^2
-\mathrm{i}k\int_{\Gamma_O}|u|^2
=
\int_{\Gamma_D}\partial_nu\,\overline g
-\int_\Omega f\overline u
$$

Tu dois en présenter les termes réels et imaginaires, définir les intégrales et préciser les hypothèses nécessaires. L'ouverture ajoute un terme de fuite ; le mur poreux absorbe selon la partie imaginaire de son coefficient dans la convention choisie. Une paroi réfléchissante a une dérivée normale nulle et ne fournit pas ce terme de fuite.

Pour une pression acoustique et une masse volumique fixées, les puissances sortantes sur le mur et sur l'ouverture sont associées à

$$
P_{\mathrm{abs}}=
\frac{1}{2\rho_{\mathrm{air}}\omega}
\int_\Gamma -\operatorname{Im}(a_{\mathrm{phys}})\chi|u|^2,
\qquad
P_{\mathrm{ouvert}}=
\frac{k}{2\rho_{\mathrm{air}}\omega}\int_{\Gamma_O}|u|^2
$$

La reconstruction des traces et les contrôles de signe sont réalisés avec Yann avant d'utiliser ces expressions sur le schéma distribué. À pression source imposée, le flux injecté peut dépendre de la configuration. Un coût plus faible doit donc être discuté avec les cartes et, lorsque le bilan est validé, avec les puissances correspondantes.

La comparaison comprend une figure du coût en fonction de la fréquence pour les deux cas, à géométrie, matériau et source annoncés. Le changement de condition peut déplacer les résonances ; un classement uniforme entre les deux courbes ne doit pas être supposé. Les affirmations de monotonie nécessitent des hypothèses et une justification spécifiques.

## 8. Références et portée des résultats

- **G. Allaire, `GAllaire-OptimParam.pdf`**, section sur le gradient : pages PDF 13–20, pages imprimées 89–96. On y trouve l'état adjoint, la démarche de Lagrangien et la méthode de gradient projeté.
- **Même document**, approche discrète : pages PDF 25–29, pages imprimées 101–105. La formule du gradient discret ne nécessite que l'état et l'adjoint. La coïncidence entre gradient continu discrétisé et gradient discret y est démontrée sous des hypothèses précises de discrétisation et d'intégration.
- **`Dirichlet_Nonhomogene.pdf`**, pages 1 et 2. Le relèvement traite la trace non nulle et la formule de dérivée conserve le champ total.
- **`Sujet-EI-EXT-2026.md`** : comparaison ouverte/réfléchissante, optimisation sur plusieurs fréquences et au moins dix points par longueur d'onde.

Le signe de l'adjoint dépend de la convention du Lagrangien et de l'opérateur. Ton implémentation se réfère à la définition matricielle explicite de cette fiche, puis vérifie sa dérivée par le calcul. Le résultat numérique de descente est un candidat local, réceptionné selon un critère annoncé. Il ne certifie pas que toutes les distributions possibles ont été comparées.

### Liste de réception

- [ ] Un seul fichier `objectif.py`, exécutable sans les fichiers des autres membres grâce aux tests synthétiques.
- [ ] Trois signatures publiques respectées et entrées non modifiées.
- [ ] Module au carré, pondération d'intégrale et facteur deux corrects.
- [ ] Transposée conjuguée et accumulation de toutes les faces.
- [ ] Gradient centré validé, puis gradient de bande validé.
- [ ] Champ total conservé malgré le Dirichlet non homogène.
- [ ] Convention ouverte/réfléchissante et distinction entre critère et puissance expliquées.
- [ ] Résultats de validation distingués des résultats physiques.
