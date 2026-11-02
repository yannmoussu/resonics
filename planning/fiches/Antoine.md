# Antoine — projection et optimisation sous quantité fixée

Les repères **A1 à A5** du Gantt correspondent aux cinq journées, du lundi au vendredi.

## Mission et livrable

Tu prends en charge la conservation de la quantité de matériau et la méthode de descente utilisée pour répartir celui-ci sur un mur. Tu écris **un seul fichier Python, `optimisation.py`**. Ce fichier reçoit une fonction d'évaluation en argument ; il n'importe donc ni le fichier de Yann ni celui de Joachim et ne modifie aucun module fourni.

Les seuls imports autorisés sont NumPy, SciPy, Matplotlib et la bibliothèque standard. NumPy suffit pour le cœur de ton lot. Le fichier comporte ses propres tests, sur de petits coûts synthétiques, dans un bloc `if __name__ == "__main__":`. Les commentaires et docstrings sont des phrases françaises, sans expressions mathématiques ni équations. Les formules de cette fiche servent à écrire les calculs Python.

### Livraisons de la semaine

- **Lundi 2 novembre** : projection pondérée validée, interface du callback et descente vérifiée sur un coût quadratique synthétique.
- **Mardi 3 novembre** : première descente monofréquence avec le coût et le gradient acoustiques validés par Joachim ; courbe du coût, carte de densité et budget contrôlé.
- **Mercredi 4 novembre** : utilisation du même optimiseur avec un callback multifréquence, puis comparaison de plusieurs budgets et de plusieurs initialisations.
- **Jeudi 5 novembre** : répétitions de validation, raisons d'arrêt explicites, comparaison des candidats et réception des calculs au maillage plus fin.
- **Vendredi 6 novembre** : fichiers et résultats figés, répétition puis intervention d'environ quatre minutes dans la soutenance de vingt minutes, suivie de dix minutes de questions.

La présentation quotidienne des progrès se déroule dans le créneau **14 h 30–17 h**. Tu présentes la faisabilité des densités, la décroissance obtenue et le motif d'arrêt des essais.

## 1. Problème que ton fichier résout

La géométrie est fixée pendant une optimisation. Le vecteur `chi`, réel et de taille `B`, décrit uniquement les nœuds de conception du mur, compris entre zéro et un. Les frontières ouvertes sont exclues de la conception. La même densité doit servir à toutes les fréquences d'un calcul multifréquence.

Chaque entrée de `design_weights` est une longueur discrète strictement positive. Elle vaut le pas de grille multiplié par le nombre de faces intérieures adjacentes au nœud de conception. On conserve une quantité absolue de matériau, exprimée par la longueur

$$
\sum_{\ell=1}^{B} w_\ell\chi_\ell=L_{\mathrm{mat}}
$$

À épaisseur et profondeur fixées, le volume poreux est proportionnel à cette longueur. Une fraction constante de nœuds recouverts ne conserve pas nécessairement la même quantité entre des formes dont les longueurs diffèrent.

Ton problème est

$$
\min_{\chi\in\mathcal C}F(\chi),
\qquad
\mathcal C=\left\{\chi\in[0,1]^B:\sum_\ell w_\ell\chi_\ell=L_{\mathrm{mat}}\right\}
$$

Le gradient fourni est **réel et euclidien** : son produit scalaire avec une direction donne la dérivée directionnelle. Tu utilises ce gradient avec la projection euclidienne décrite ci-dessous.

Le coût peut être l'intégrale de pression au carré pour une fréquence ou une somme de tels critères pour une bande. Il ne s'agit pas directement d'une puissance dissipée. Ton fichier minimise le coût transmis ; les unités, signes acoustiques et coefficients des matériaux sont traités par les fonctions d'évaluation.

## 2. Contrats publics et callback

Tu écris exactement ces deux fonctions :

```python
def project_density(z, design_weights, material_length_m,
                    tol=1e-10, max_iter=100):
    ...


def your_optimization_procedure(chi0, evaluate, design_weights, material_length_m,
                                step0=1.0, max_iter=100,
                                feasibility_tol=1e-10, gradient_tol=1e-6,
                                armijo=1e-4, reduction=0.5, increase=1.1,
                                min_step=1e-12, max_backtracks=40):
    ...
```

Le nom pédagogique `your_optimization_procedure` est conservé. Yann écrira l'adaptateur de l'ancienne signature longue du démo dans son propre fichier. Ton fichier n'a besoin que du callback suivant :

```python
result = evaluate(chi, with_gradient=True)
```

Il renvoie au moins :

```python
{
    "value": valeur_reelle,
    "gradient": vecteur_reel_de_taille_B_ou_None
}
```

- Avec `with_gradient=True`, le coût et le gradient euclidien sont calculés à la densité reçue.
- Avec `with_gradient=False`, le coût est calculé et le gradient peut valoir `None`. Cet appel sert aux essais de pas et évite les résolutions adjointes inutiles.
- Le callback ne modifie pas `chi`. Le coût, les fréquences, leurs poids et leurs éventuelles références sont fixés pendant toute une optimisation.
- Une erreur de taille ou une valeur de gradient non finie est une erreur de contrat. Elle doit être signalée avec son contexte.

L'évaluation acoustique est basée sur un système complexe, mais ses sorties de coût et de gradient sont réelles. Joachim résout un système adjoint à transposée conjuguée et accumule toutes les faces du mur. Ton fichier peut être développé et vérifié avec des callbacks quadratiques avant que ce calcul acoustique soit disponible.

## 3. Projection sur les densités admissibles

### 3.1 Définition

Pour un vecteur d'essai réel `z`, la projection euclidienne résout

$$
\min_{\chi\in\mathcal C}\frac12\sum_\ell(\chi_\ell-z_\ell)^2
$$

En introduisant un multiplicateur scalaire, les composantes s'écrivent

$$
\chi_\ell(\lambda)=\min\left(1,\max\left(0,z_\ell-\lambda w_\ell\right)\right)
$$

Le multiplicateur est choisi pour respecter

$$
V(\lambda)=\sum_\ell w_\ell\chi_\ell(\lambda)=L_{\mathrm{mat}}
$$

Cette fonction est continue et décroissante, ce qui permet une dichotomie. Les poids peuvent être différents. La translation de chaque composante dépend donc de son poids. Cette projection est cohérente avec le gradient euclidien transmis par le callback.

### 3.2 Vérifications d'entrée

- `z` et `design_weights` sont des vecteurs unidimensionnels réels, finis, de même taille non nulle.
- Tous les poids sont strictement positifs : les nœuds sans face active ont été exclus avant l'appel.
- Le budget est un réel fini compris entre zéro et la somme des poids.
- La tolérance est strictement positive et le nombre maximum d'itérations est un entier positif.
- Les tableaux d'entrée ne sont pas modifiés.

### 3.3 Algorithme de dichotomie

1. Si le budget est nul, renvoyer un vecteur nul. S'il est égal à la somme des poids, renvoyer un vecteur de uns.
2. Construire l'encadrement

$$
\lambda_{\min}=\min_\ell\frac{z_\ell-1}{w_\ell},
\qquad
\lambda_{\max}=\max_\ell\frac{z_\ell}{w_\ell}
$$

À la première borne, la projection est entièrement à un ; à la seconde, elle est entièrement à zéro.

3. Prendre le milieu, tronquer les composantes entre zéro et un, puis calculer le budget pondéré.
4. Si le budget calculé est trop grand, augmenter le multiplicateur en remplaçant la borne inférieure par le milieu. S'il est trop petit, remplacer la borne supérieure par le milieu.
5. Arrêter dès que l'erreur absolue de budget est inférieure ou égale à `tol`, exprimée en mètres.
6. Si la limite d'itérations est atteinte, vérifier le meilleur résultat calculé. Signaler un échec si la tolérance reste non satisfaite. Une valeur de budget approchée ne doit pas être présentée comme exactement conservée.

Les composantes appartiennent toujours aux bornes après troncature. Il faut néanmoins contrôler l'erreur de budget après la dernière opération.

### 3.4 Tests de réception

Les tests restent dans le même fichier :

- une densité déjà admissible est inchangée à la tolérance près ;
- projeter deux fois donne le même résultat ;
- les budgets nul et maximal donnent respectivement zéro et un ;
- des poids non uniformes respectent le budget ;
- un vecteur d'essai contenant des valeurs hors des bornes est ramené dans l'ensemble admissible ;
- des entrées invalides donnent une erreur descriptive ;
- les entrées ne sont pas modifiées.

Pour un contrôle indépendant simple, prendre deux poids égaux à un, un budget égal à un et le vecteur d'essai dont les composantes valent huit dixièmes et six dixièmes. La projection attendue vaut six dixièmes et quatre dixièmes.

## 4. Descente projetée avec recherche de pas

### 4.1 Initialisation

Copier `chi0`, vérifier ses dimensions et sa finitude, puis la projeter avec les poids et le budget reçus. Cette projection initiale assure une comparaison correcte même lorsqu'une distribution de départ avait été créée par comptage de nœuds.

Évaluer le coût et le gradient à cette densité projetée. Enregistrer une première ligne d'historique correspondant à cette évaluation réelle. Initialiser le nombre d'itérations acceptées à zéro.

Vérifier les paramètres : pas initial et pas minimum strictement positifs ; nombre d'itérations et de retours arrière positifs ; facteur de réduction strictement entre zéro et un ; facteur d'augmentation au moins un ; coefficient d'Armijo strictement entre zéro et un ; tolérances strictement positives.

### 4.2 Mesure de stationnarité

Un gradient ordinaire non nul peut être normal à la contrainte de budget et correspondre à une solution contrainte. Utiliser donc le gradient projeté. Une convention simple et reproductible est

$$
r_{\mathrm{proj}}(\chi)
=\left\|\chi-P_{\mathcal C}(\chi-\nabla F(\chi))\right\|_\infty
$$

Le pas de référence de cette mesure vaut un. Cette convention doit rester la même d'une itération à l'autre et apparaître dans les résultats. Le seuil par défaut est `gradient_tol`. Il s'agit d'une mesure de stationnarité du problème discrétisé, sensible à l'échelle du coût ; les références de normalisation éventuelles doivent donc être fixées avant le calcul.

Si ce résidu est sous le seuil et que le budget respecte `feasibility_tol`, on peut arrêter avec le motif `projected_gradient` et `converged=True`. Une faible variation de coût constitue un diagnostic supplémentaire, pas à elle seule un certificat de stationnarité.

### 4.3 Essai de pas

Pour une densité courante, son gradient et un pas strictement positif, former

$$
\chi_{\mathrm{essai}}=P_{\mathcal C}(\chi-s\nabla F(\chi)),
\qquad d=\chi_{\mathrm{essai}}-\chi
$$

Appeler `evaluate(chi_trial, with_gradient=False)` et accepter lorsque la condition suivante est vérifiée :

$$
F(\chi_{\mathrm{essai}})
\leq F(\chi)+\texttt{armijo}\;\nabla F(\chi)\cdot d
$$

Le déplacement `d` contient déjà l'effet du pas. Le terme de droite ne doit donc pas être multiplié une seconde fois par ce pas.

Pour une projection euclidienne exacte et une densité courante admissible,

$$
\nabla F(\chi)\cdot d\leq-\frac{\|d\|_2^2}{s}
$$

Le membre de droite de la condition d'acceptation demande donc une baisse réelle, sauf lorsque le déplacement est nul à la précision numérique.

Si l'essai est refusé, multiplier le pas par `reduction`, reprojeter et recalculer le coût. La densité courante reste celle du dernier essai accepté. Limiter cette boucle avec `max_backtracks` et `min_step`.

Un coût d'essai non fini peut être classé comme essai refusé. Une erreur de dimensions ou une incohérence du callback doit être signalée. Si le code choisit de rejeter une défaillance de résolution numérique, cette défaillance est identifiée précisément et enregistrée, afin de ne pas masquer une erreur de programmation.

### 4.4 Après acceptation

1. Remplacer la densité courante par l'essai accepté.
2. Évaluer coût et gradient à cette nouvelle densité. Le coût doit être cohérent avec celui utilisé pour accepter l'essai ; cette vérification détecte un callback dont les paramètres changeraient pendant la recherche de pas.
3. Incrémenter le nombre d'itérations acceptées.
4. Enregistrer les mesures réelles dans l'historique.
5. Préparer le pas suivant en multipliant le pas accepté par `increase`.
6. Recalculer le résidu projeté et vérifier le motif d'arrêt.

Le propriétaire du callback peut réutiliser des factorisations ou la dernière évaluation pour gagner du temps. Ton algorithme respecte le contrat public et reste correct même sans ce cache.

### 4.5 Raisons d'arrêt distinctes

Prévoir au moins :

| Motif | Interprétation |
|---|---|
| `projected_gradient` | Seuil de stationnarité atteint avec budget respecté |
| `max_iter` | Nombre maximal d'itérations acceptées atteint |
| `min_step` | Pas devenu inférieur au minimum avant une nouvelle acceptation |
| `max_backtracks` | Limite d'essais atteinte sans acceptation |
| `numerical_stagnation` | Déplacement devenu indiscernable numériquement alors que la stationnarité annoncée n'est pas atteinte |

Seul le premier motif permet de renseigner `converged=True` dans cette convention. Les autres motifs renvoient le dernier candidat admissible réellement évalué, avec son coût et son gradient cohérents.

## 5. Historique et dictionnaire final

L'historique contient la ligne initiale puis une ligne par itération acceptée. Il peut être une liste de dictionnaires comportant :

- `iteration` : numéro, à partir de zéro ;
- `value` : coût réellement évalué ;
- `step` : pas accepté, nul par convention pour la ligne initiale ;
- `projected_gradient_norm` : résidu défini ci-dessus ;
- `budget_error` : erreur absolue de quantité ;
- `backtracks` : nombre de réductions du pas pour cette acceptation.

Les essais rejetés peuvent être comptés séparément. L'historique n'est pas complété par des zéros pour atteindre une longueur prédéfinie, car ces zéros créeraient une fausse courbe de convergence.

Le dictionnaire final propose les clés suivantes :

```python
{
    "chi": densite_finale,
    "value": cout_final,
    "gradient": gradient_final,
    "history": historique_reel,
    "budget_error": erreur_absolue_de_budget,
    "projected_gradient_norm": residu_projete_final,
    "stop_reason": motif_arret,
    "converged": convergence_locale,
    "n_iterations": nombre_iterations_acceptees,
    "n_evaluations": nombre_appels_callback
}
```

Les clés supplémentaires éventuelles ne remplacent pas celles-ci. La densité, le coût et le gradient se rapportent au même point final. L'appelant pourra obtenir le champ acoustique en réévaluant cette densité avec ses propres fonctions.

## 6. Tests autonomes de l'optimiseur

### 6.1 Quadratique à solution contrainte connue

Employer deux variables, des poids de conception égaux à un et deux, et un budget égal à un mètre et un dixième. Le coût synthétique est

$$
F(\chi)=\frac12\left[2(\chi_1-0,1)^2+4(\chi_2-0,2)^2\right]
$$

et son gradient est

$$
\nabla F(\chi)=\left(2(\chi_1-0,1),4(\chi_2-0,2)\right)
$$

La solution contrainte est

$$
\chi^*=(0,3;0,4),\qquad F(\chi^*)=0,12
$$

Son gradient ordinaire n'est pas nul ; il est proportionnel aux poids de budget. C'est un exemple utile pour vérifier le choix d'un critère de gradient **projeté**.

Partir par exemple d'une densité de neuf dixièmes puis un dixième, qui respecte déjà le budget. Vérifier que le coût diminue, que la quantité reste fixée, que la densité finale se rapproche du résultat connu et que le dernier coût correspond à une réévaluation indépendante.

### 6.2 Retour arrière

Reprendre le même problème avec un pas initial volontairement grand. Vérifier qu'au moins un essai est rejeté, que le pas est réduit et qu'aucun essai refusé ne remplace la densité courante. Vérifier l'inégalité d'Armijo pour chaque transition enregistrée.

### 6.3 Arrêts et erreurs

Ajouter :

- budget nul et budget maximal : l'ensemble admissible ne contient qu'une densité ; le résidu projeté est nul ;
- coût constant avec gradient nul : une seule ligne d'historique, pas une suite fictive de baisses ;
- limite d'itérations très faible : motif `max_iter` si le seuil n'est pas atteint ;
- callback renvoyant un gradient de mauvaise taille : erreur explicite ;
- callback renvoyant un coût d'essai non fini : essai refusé ou arrêt numérique clairement identifié ;
- vérification que la densité initiale et les poids fournis n'ont pas été modifiés.

Tous les résultats de cette section sont des **contrôles d'algorithme**, sans signification de performance pour un mur acoustique.

## 7. Plusieurs fréquences et plusieurs initialisations

### Multifréquence

Aucune modification du cœur de l'optimiseur n'est nécessaire. Yann ferme la bande dans un callback, qui renvoie la somme pondérée des coûts et la somme des gradients avec les mêmes poids. Les fréquences, poids et références restent fixés pendant la descente. Le vecteur de conception reste unique.

Tu peux réceptionner ce comportement avec un callback synthétique additionnant deux quadratiques à poids fixés. Le coût final doit correspondre à la somme annoncée et respecter le même budget. Les courbes acoustiques finales sont ensuite évaluées sur une grille fréquentielle plus dense par Olympia et Yann.

### Multidémarrages

Ajouter, dans le même fichier, un helper facultatif qui appelle plusieurs fois `your_optimization_procedure`. Il peut recevoir directement une liste de densités initiales. Chaque densité est projetée avec les mêmes poids et le même budget. Une première campagne raisonnable comprend la distribution de référence, une distribution uniforme admissible et une ou plusieurs distributions pseudo-aléatoires à graines fixées.

Comparer les coûts finaux réellement obtenus, conserver les raisons d'arrêt et les compteurs de coût. Le candidat retenu est le meilleur candidat admissible calculé. Les statistiques distinguent un arrêt de stationnarité d'une interruption au nombre maximal d'itérations. Plusieurs initialisations améliorent la recherche empirique ; elles ne prouvent pas un optimum global.

Avant les premières optimisations acoustiques, Joachim et Yann vérifient le gradient sur un petit cas du support. Un contrôle à seize colonnes, trente-deux lignes et frontière de niveau un a déjà montré une décroissance quadratique de l'erreur des différences centrées, jusqu'à quelques milliardièmes. Il confirme notamment qu'un nœud Robin peut contribuer par deux faces intérieures. Cette réception concerne la dérivée de l'algorithme ; elle ne fournit aucune mesure de performance du produit.

## 8. Références et articulation avec les autres lots

- **G. Allaire, `GAllaire-OptimParam.pdf`**, section 5.3.2 : pages PDF 18–20, pages imprimées 94–96. Le document présente le gradient projeté, la projection par troncature et décalage, la recherche du multiplicateur par dichotomie et une adaptation du pas. La projection pondérée de cette fiche est sa formulation euclidienne pour les longueurs discrètes effectivement employées.
- **Même document**, pages PDF 25–29, pages imprimées 101–105 : intérêt de l'état adjoint pour calculer le gradient avec un nombre de résolutions indépendant du nombre de variables. Joachim fournit cette partie.
- **`Dirichlet_Nonhomogene.pdf`**, pages 1 et 2 : traitement du Dirichlet non homogène et emploi du champ total dans le gradient. Cette vérification relève de Joachim et Yann ; ton callback reçoit le gradient déjà cohérent.
- **`Sujet-EI-EXT-2026.md`** : matériau en quantité fixée, optimisation monofréquence puis multifréquence, comparaison des quantités et préparation de la soutenance collective.

Le modèle acoustique n'est généralement pas un problème convexe en la densité. La méthode et le seuil d'arrêt fournissent une réception locale et reproductible du candidat. Les résultats doivent donc être nommés selon ce qui a été réellement calculé, sans certificat global non démontré.

### Liste de réception

- [ ] Un seul fichier `optimisation.py`, dont les tests fonctionnent sans les fichiers des autres membres.
- [ ] Projection correcte pour des poids différents et budget en longueur absolue.
- [ ] Deux signatures publiques respectées, avec un callback transmis en argument.
- [ ] Recherche de pas effectuée sur le coût recalculé après projection.
- [ ] Critère d'Armijo avec le déplacement projeté et comptage des essais.
- [ ] Arrêt fondé sur la stationnarité projetée et raisons d'arrêt explicites.
- [ ] Densité, coût et gradient finaux cohérents ; historique sans données fictives.
- [ ] Test quadratique à solution connue, retour arrière et multidémarrages réceptionnés.
- [ ] Résultats d'algorithme distingués des performances physiques.
