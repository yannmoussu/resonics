# Yann — Voie numérique, solveur et intégration de ResoniCS

Les repères **Y1 à Y5** du Gantt correspondent aux cinq journées, du lundi au vendredi.

## Livrable unique et responsabilité

**Un seul fichier Python à produire : `resonics.py`.** Il constitue le point d'entrée du projet, adapte le support distribué et relie les quatre contributions `materiaux.py`, `objectif.py`, `optimisation.py` et `campagnes.py`. Les programmes du dossier de support sont conservés pour permettre les comparaisons. Les corrections ou adaptations nécessaires sont écrites dans `resonics.py`, sans demander aux autres membres de modifier les fichiers fournis.

Le fichier doit pouvoir exécuter ses petits contrôles avec le support seul, même lorsque les autres contributions ne sont pas encore disponibles. On effectue donc les imports des contributions au moment des commandes qui en ont besoin. Les exemples de contrôle sont explicitement synthétiques et restent distincts des données des applications route et rail.

Yann coordonne également la cohérence des unités, des paramètres et des résultats exportés, puis la compilation du rapport et de la présentation. Les membres valident eux-mêmes les éléments qu'ils présentent. Les résultats antérieurs de maillage et de FEM servent de méthode de travail et de vérification, et ne sont pas repris comme performances du produit ResoniCS.


## Contrat commun intégral à respecter

Cinq fichiers à produire, un seul fichier à écrire par personne : Yann `resonics.py`, Mathis `materiaux.py`, Olympia `campagnes.py`, Joachim `objectif.py`, Antoine `optimisation.py`. Chaque fichier possède un petit exemple autonome sous `if __name__ == "__main__":`. Les essais de fonctions emploient de petits exemples explicitement synthétiques ; ils ne sont jamais publiés comme performances acoustiques. NumPy, SciPy, Matplotlib et bibliothèque standard uniquement. Commentaires en phrases françaises sans équations ni symboles mathématiques. Les équations restent dans les explications et les calculs Python. Les signatures ci-dessous sont des contrats proposés, pas des fonctions déjà présentes dans le support.

Le support distribué reste conservé. Yann écrit l'adaptation et les appels, sans demander aux autres d'éditer les modules fournis. Les noms pédagogiques `your_compute_objective_function` et `your_optimization_procedure` sont conservés. Si l'appel long du programme distribué est gardé, son adaptation aux nouveaux arguments est faite dans `resonics.py`, hors des blocs signalés comme imposés.

### Unités et signes

La fréquence publique `frequency_hz` est en hertz. On définit la pulsation `angular_frequency_rad_s = 2*pi*frequency_hz`, puis `k_per_m = angular_frequency_rad_s / c_m_s` et la longueur d'onde `wavelength_m = c_m_s / frequency_hz`. Le paramètre historique `omega` de `processing.solve_helmholtz` reçoit en réalité **le nombre d'onde**, jamais directement les hertz ou la pulsation.

Convention temporelle : exp(-i*omega*t). Avec normale sortante, la Robin physique s'écrit `partial_n u + a_phys*u = 0`. Le support élimine la valeur de bord par `u_B = u_I/(1-h*a_code)` lorsque les coefficients imposés valent un et le second membre Robin est nul. Il représente donc `partial_n u - a_code*u = 0`. On utilise `a_code = -a_phys`. Pour une impédance de surface documentée `Z_s = pression/vitesse_normale_sortante`, `a_code = i*omega*rho_air/Z_s`. Sommerfeld correspond à `a_code = i*k`. Une vérification sur onde plane et un contrôle de passivité précèdent toute conclusion physique. La constante `10-10j` du démo n'identifie aucun matériau réel.

### Conception et quantité

La densité `chi` est un vecteur réel de taille B, borné entre zéro et un, associé uniquement aux nœuds Robin du mur qui touchent au moins une face intérieure. Les Robin d'ouverture sont exclues de la conception. La géométrie reste fixée pendant une optimisation ; on compare les niveaux géométriques dans des optimisations séparées.

Pour chaque nœud de conception, `design_weights` vaut le pas multiplié par le nombre de faces adjacentes au fluide, avec les mêmes faces que l'assemblage. Ce sont des longueurs discrètes en mètres, à confronter à la longueur du profil lors du raffinement. On impose `dot(design_weights, chi) = material_length_m`, budget absolu commun entre formes. Avec épaisseur et profondeur constantes, le volume poreux est proportionnel à cette longueur. La fraction nodale `V_obj` du démo ne remplace pas ce budget. Le cas entièrement recouvert est une référence qui utilise généralement plus de matériau, pas une borne assurée du coût.

### Assemblage pour Joachim

Yann fournit une fonction passée en argument :

```python
assemble(chi, frequency_hz) -> {
    "A": matrice creuse complexe de taille (n, n),
    "b": vecteur complexe de taille (n,),
    "cell_weights": vecteur réel positif de taille (n,),
    "face_rows": indices entiers de taille (n_faces,),
    "face_design": indices de conception de taille (n_faces,),
    "dA_diag": valeurs complexes de taille (n_faces,)
}
```

`A` et `b` sont restreints aux nœuds intérieurs après élimination des bords avec le support. `cell_weights` vaut le carré du pas. Chaque entrée de face apporte une dérivée diagonale de `A` à la ligne `face_rows`, relativement à la variable `chi[face_design]`. Les répétitions sont conservées si un nœud Robin touche plusieurs intérieurs. Dans le cas imposé de coefficients unitaires et de second membre Robin nul, la valeur de face est `h*Alpha_code/(1-h*Alpha_code*chi_l)**2`. `b` ne dépend pas de la densité. Tout changement de cette dernière hypothèse demande de compléter la dérivée du second membre.

Joachim fournit :

```python
your_compute_objective_function(domain_omega, u, spacestep) -> float
evaluate_frequency(chi, frequency_hz, assemble, with_gradient=True) -> dict
evaluate_band(chi, frequencies_hz, frequency_weights, assemble,
              reference_energies=None, with_gradient=True) -> dict
```

L'objectif sur grille vaut le carré du pas multiplié par la somme des modules au carré **aux nœuds intérieurs**, dont le code fourni vaut moins un. Pour une fréquence : résoudre `A*U=b`, puis `A.conj().T*P=2*cell_weights*U`. Le gradient réel euclidien s'obtient en ajoutant pour chaque face `-real(conj(P[row])*dA_diag*U[row])` à la variable indiquée. La dépendance par Dirichlet non homogène est déjà dans le champ total et dans le second membre. On ne remplace pas le champ total par un champ homogénéisé dans le gradient.

`evaluate_band` retourne au minimum `{"value": float, "gradient": vecteur réel de taille B ou None, "energies": vecteur par fréquence, "state_residuals": vecteur}`. Les poids fréquentiels sont fixés, positifs ou nuls, et de somme un. Des énergies de référence strictement positives peuvent normaliser chaque fréquence, à condition d'être gelées avant optimisation et communes aux produits comparés. L'énergie définie ici est le critère de pression du sujet, pas directement une puissance dissipée.

### Appel d'optimisation pour Antoine

Yann ferme les paramètres de bande dans un callback :

```python
evaluate(chi, with_gradient=True) -> {
    "value": float,
    "gradient": vecteur réel de taille B ou None
}
```

Antoine fournit :

```python
project_density(z, design_weights, material_length_m,
                tol=1e-10, max_iter=100) -> chi
your_optimization_procedure(chi0, evaluate, design_weights, material_length_m,
                            step0=1.0, max_iter=100,
                            feasibility_tol=1e-10, gradient_tol=1e-6,
                            armijo=1e-4, reduction=0.5, increase=1.1,
                            min_step=1e-12, max_backtracks=40) -> dict
```

Avec le gradient euclidien, la projection utilise `clip(z-lambda*design_weights, 0, 1)` ; le décalage scalaire est trouvé par dichotomie pour respecter le budget pondéré. La descente utilise un retour arrière et le coût réellement recalculé après projection. La même densité sert à toutes les fréquences. Le retour contient densité finale, coût final, gradient final, historique sans lignes fictives, erreur de budget, résidu projeté et raison de l'arrêt. Une convergence locale ou une limite d'itérations n'est pas un certificat d'optimalité globale.

### Matériaux et campagnes

Mathis fournit `compute_material_response(frequencies_hz, material_parameters, air_parameters) -> dict` avec impédance complexe, coefficients Robin physique et code, domaine de validité, unités et provenance. Les courbes de coefficients d'absorption réels ne suffisent pas à identifier la phase d'une impédance complexe. Le modèle doit être documenté ou fourni par les enseignants ; l'absence de ce modèle est un point à lever lundi, pas une donnée à inventer.

Olympia reçoit les fonctions de construction, d'évaluation et d'optimisation comme arguments, donc son fichier n'importe pas les fichiers en cours de rédaction. Un cas transmis par Yann contient identifiant, métadonnées de géométrie/source, `design_weights`, budget, densité initiale. `evaluate_case(case, chi, frequency_hz)` retourne énergie, champ complexe intérieur, coordonnées et masques, résidu, traces Robin par face et puissance dissipée si le coefficient physique est validé. `optimize_case(case, frequencies_hz, frequency_weights, chi0)` retourne le dictionnaire d'Antoine.

Les bandes route et rail, dimensions, lois de matériau et budget sont des choix à documenter au premier jalon. À défaut d'une pondération spectrale documentée, une pondération uniforme est annoncée comme telle. La règle d'au moins dix points par longueur d'onde vient du sujet ; l'échelle d'irrégularité proche de la demi-longueur d'onde est une règle de conception donnée oralement, à tester. Aucune performance de produit n'est déjà acquise.

## Signatures fournies et organisation du fichier

Le contrat ci-dessus est complet. Les fonctions `assemble`, `evaluate_case`, `optimize_case` et le callback `evaluate` sont fournis aux autres contributions par le coordinateur. Les signatures des fonctions rédigées par Mathis, Joachim et Antoine sont reprises sans renommer leurs paramètres. Les fonctions d'Olympia reçoivent les callbacks, ce qui leur permet de fonctionner sans importer les contributions encore en rédaction.

L'architecture interne de `resonics.py` peut suivre cet ordre : imports standard et scientifiques, paramètres et étiquettes, chargement du support, construction d'un cas, numérotation des inconnues et des faces, assemblage réduit, reconstruction du champ et des traces, contrôles, raccordement aux contributions, exports, puis interface en ligne de commande. Les noms des aides internes sont libres ; leurs sorties doivent aboutir exactement aux contrats communs.

**Entrées physiques à fixer explicitement au premier jalon :** vitesse du son en mètres par seconde, masse volumique de l'air, dimensions en mètres, source imposée et son unité, liste de fréquences en hertz, modèle matériau avec sa provenance et ses hypothèses, niveau géométrique, pas en mètres et quantité absolue de matériau. Une valeur présente dans le démonstrateur ne constitue pas à elle seule une donnée matériau ou une donnée de bruit routier ou ferroviaire.

**Métadonnées à conserver pour chaque cas :** identifiant stable, scénario, dimensions, pas, niveau, nombre de nœuds intérieurs, nombre de variables de conception, liste des faces de conception, poids de conception, longueur du profil, longueur discrète des faces et budget. Les métadonnées décrivent aussi la position des bords et la convention d'orientation des coordonnées.

## Étapes de réalisation

### 1. Établir la référence du support avant toute adaptation

1. Lire le démonstrateur et les fonctions appelées dans `preprocessing.py`, `processing.py`, `postprocessing.py` et `_env.py`. Conserver les fichiers distribués et noter leurs empreintes pour savoir quelle version sert de référence.
2. Identifier les blocs signalés comme imposés dans le démonstrateur et conserver leur contenu. L'adaptation et les appels sont placés dans `resonics.py`, hors de ces blocs.
3. Relever les étiquettes : intérieur moins un, extérieur complémentaire moins deux, Dirichlet un, Neumann deux et Robin trois. Les masques sont toujours construits à partir de ces étiquettes, jamais à partir d'un test approximatif sur la couleur d'un graphique.
4. Vérifier la convention de numérotation complète du support : la case de ligne et colonne de grille est aplatie avec la largeur du tableau, et non sa hauteur. Conserver une correspondance dans les deux sens entre cet indice complet et l'indice intérieur réduit.
5. Exécuter un petit cas plan sans optimisation. Noter les paramètres effectivement employés et les grandeurs renvoyées. Le support n'affiche et ne renvoie le champ que sur les nœuds intérieurs ; ses zéros de bord ne sont donc pas des traces de pression calculées.
6. Relever les éléments à compléter dans le démonstrateur : objectif initial nul, boucle pédagogique contenant des variables non définies si elle est activée, appel d'objectif dont le nom diffère du nom pédagogique, et invocation de l'optimisation commentée. Les fonctions de Joachim et Antoine seront raccordées par le coordinateur. Ne pas présenter ces points comme déjà corrigés.
7. Vérifier les fonctions auxiliaires avant de les appeler. Certaines fonctions de traitement de bord ou de coloriage non employées par le chemin principal font référence à des noms non définis dans `_env.py` ou dans leur module. On peut conserver ces fonctions inutilisées sans prétendre les avoir validées.

### 2. Construire et contrôler les géométries et leurs unités

8. Appeler le générateur fourni en conservant sa définition du motif et en faisant d'abord varier le niveau. Le nom `create_motif_koch` désigne ici un motif de huit segments au quart et des rotations à angle droit. Il faut montrer et décrire ce motif réel, plutôt que reprendre le Koch triangulaire à quatre segments au tiers du précédent projet.
9. Définir des coordonnées physiques à partir des indices et du pas. Préciser si l'ordonnée augmente vers le bas de la grille ou vers le haut du dessin. Les normales sortantes sont déterminées à partir du fluide et du bord considéré, indépendamment du sens d'affichage.
10. Vérifier que les nœuds intérieurs ne touchent jamais le bord extérieur du tableau. Les stencils accèdent aux quatre voisins ; une case intérieure sur ce bord pourrait utiliser un indice négatif ou sortir du tableau. Vérifier aussi la connexion de la région fluide, l'absence d'ouvertures involontaires et l'appartenance de chaque bord à une catégorie explicite.
11. Examiner la partition obtenue à chaque niveau. Les branches de la routine de partitionnement utilisent des indices de ligne et de colonne différents ; un domaine rectangulaire ne permet pas d'intervertir leurs bornes. Un nouveau test doit porter sur les dimensions réellement choisies. On signale un cas invalide au lieu de le corriger silencieusement.
12. Au niveau géométrique fixé, construire au moins deux résolutions qui représentent les mêmes sommets et les mêmes dimensions physiques. Les pas successifs subdivisent les segments existants. Le contrôle porte sur les coordonnées et le profil, pas seulement sur le numéro du niveau.
13. Vérifier la règle du sujet à la fréquence maximale. Avec `wavelength_min_m = c_m_s / max(frequencies_hz)`, on impose au moins dix points par longueur d'onde, donc un pas au plus égal au dixième de cette longueur. Le nombre de points, le nombre d'intervalles et la longueur physique ne sont pas interchangeables ; les bornes réelles du tableau doivent être calculées.
14. Vérifier séparément la représentation des plus petits motifs. Le générateur emploie des subdivisions puis des conversions en entiers ; un segment plus court que la maille peut disparaître. Choisir des dimensions et subdivisions compatibles, vérifier que les sommets existent après discrétisation et refuser les niveaux non résolus. Au besoin, fixer plusieurs mailles par plus petit segment et tester une résolution supérieure.
15. Comparer la taille physique des irrégularités à la demi-longueur d'onde dans la bande visée. Cette règle donnée oralement est une piste de conception à tester. Elle ne remplace pas le critère de résolution de la longueur d'onde ni le contrôle des motifs les plus fins.

### 3. Construire les variables de conception et compter les faces

16. Séparer le mur à optimiser des éventuelles frontières ouvertes. Ces deux ensembles peuvent porter une étiquette Robin, mais seuls les nœuds du mur appartiennent à la conception. Une frontière ouverte conserve son coefficient et ne reçoit aucune part du budget de matériau.
17. Parcourir les quatre voisins de chaque nœud intérieur. Pour chaque voisin appartenant au mur Robin, enregistrer une face avec l'indice intérieur réduit, l'indice du nœud de bord, la direction et l'indice de la variable de conception correspondante. L'ordre de ce relevé est déterministe.
18. Conserver une seule variable de densité par nœud de conception, mais une entrée par face. Un nœud Robin peut toucher plusieurs nœuds intérieurs et doit alors apparaître plusieurs fois dans la liste des faces. Ne pas supprimer ces répétitions par une opération sur les indices de conception.
19. Définir les poids de conception en additionnant le pas sur les faces associées à chaque variable. La somme des poids est la longueur de contact discrète entre le mur et le fluide. La comparer à la longueur du profil fourni et suivre leur évolution pendant le raffinement, notamment aux coins.
20. Vérifier le budget absolu et sa faisabilité. La quantité de matériau demandée doit être comprise entre zéro et la somme des poids. Le cas « mur entièrement absorbant » correspond à la densité unitaire et peut employer davantage de matériau que les produits optimisés. Il sert de référence distincte et n'est pas une borne garantie de l'objectif.
21. Construire une densité initiale faisable ou la projeter avec la fonction d'Antoine dès qu'elle est disponible. Pour comparer les formes, garder le même budget physique et le même scénario source, plutôt qu'une même moyenne des valeurs nodales.

### 4. Assembler le problème réduit, avec les mêmes coefficients que le support

22. Préparer les coefficients et seconds membres avec les routines distribuées. Le contrat commun de cette semaine porte sur les coefficients imposés unitaires et sur un second membre Robin nul. Vérifier ces hypothèses dans l'adaptation et refuser une généralisation silencieuse à des coefficients variables.
23. Construire les matrices complètes du support avec `compute_stiffness_matrix` et `compute_mass_matrix`, puis appliquer les conditions Dirichlet, Neumann et Robin dans le même ordre que `solve_helmholtz`. Le coefficient de masse est multiplié par le carré du nombre d'onde, puisque la variable historique `omega` de cette fonction contient ce nombre d'onde.
24. Employer le champ total avec la donnée Dirichlet non homogène. Les contributions de cette donnée sont reportées dans le second membre. Ne pas annuler l'excitation lorsqu'on prépare l'adjoint et ne pas substituer au champ total une inconnue de relèvement homogène dans le contrat de Joachim.
25. Après traitement des bords, extraire les lignes et colonnes intérieures ainsi que le second membre intérieur. Convertir la matrice au format creux adapté à la factorisation et ramener le second membre à un vecteur unidimensionnel. La matrice complète contient des équations d'identité aux autres nœuds ; celles-ci ne doivent pas devenir des variables d'optimisation.
26. Fournir `cell_weights` constant, égal au carré du pas sur les inconnues intérieures. Ce choix correspond au critère discret commun et doit être le même dans l'objectif et dans l'adjoint.
27. Pour chaque face du mur, poser le coefficient local comme le coefficient matériau de code multiplié par sa densité. Avec les hypothèses du contrat, l'élimination fournit une contribution diagonale correspondant à la trace divisée par le terme de Robin. Construire la dérivée de cette même contribution, sans reprendre une formule continue qui ne différencierait pas exactement le code.
28. La dérivée diagonale retournée par face est exactement :

   ```python
   dA_diag = h * Alpha_code / (1.0 - h * Alpha_code * chi[face_design])**2
   ```

   `face_rows` et `face_design` ont la même longueur que ce tableau. Les faces d'une ouverture fixe ne figurent pas dans ces trois tableaux de dérivées. Les répétitions sont conservées et seront additionnées par Joachim.
29. Vérifier que le second membre reste indépendant de la densité dans le cas retenu. Si un second membre Robin non nul ou une autre paramétrisation est ensuite introduit, il faut modifier et valider le contrat de dérivation avant de poursuivre les optimisations.
30. Contrôler tous les dénominateurs de Robin avant la résolution. Signaler un dénominateur trop petit, une matrice singulière, des valeurs non finies ou un résidu excessif, avec l'identifiant du cas et la fréquence. Ne pas enregistrer une énergie nulle comme remplacement d'une résolution échouée.

### 5. Vérifier le signe physique de Robin et les frontières ouvertes

31. Établir explicitement le lien entre la Robin physique et son écriture dans le support. Pour une face dont le second membre est nul et les coefficients unitaires, la trace éliminée satisfait :

   ```python
   u_boundary_face = u_interior[face_row] / (1.0 - h * a_code_face)
   ```

   La différence entre la trace de bord et la valeur intérieure, divisée par le pas, représente la dérivée vers la normale sortante. Elle vaut ici le coefficient de code multiplié par la trace. Le signe est donc celui indiqué dans le contrat commun.
32. La fonction de Mathis reçoit des fréquences en hertz et renvoie une réponse matériau documentée. Yann convertit les unités à une seule interface, vérifie le coefficient physique et le coefficient de code, puis injecte uniquement le coefficient de code dans les routines du support. La constante complexe du démonstrateur reste un paramètre de contrôle, pas une identité de matériau.
33. Préparer le cas réfléchissant avec un coefficient Robin de code nul sur le mur, ce qui doit retrouver le comportement Neumann homogène. À la limite d'une densité nulle, les deux implémentations doivent donner les mêmes champs intérieurs.
34. Préparer un cas d'ouverture locale avec le coefficient de code égal au nombre d'onde multiplié par l'unité imaginaire. Il s'agit de l'approximation de Sommerfeld du premier ordre, à contrôler sur une onde sortante normale. Une ouverture fixe est exclue du budget et du gradient.
35. Pour comparer une frontière réfléchissante et une frontière ouverte, conserver la source, sa normalisation et les autres paramètres. Si l'ouverture remplace la frontière qui portait la source Dirichlet, imposer une condition incidente non homogène cohérente. Remplacer simplement cette source par une Sommerfeld homogène supprimerait l'excitation. La frontière modifiée et le choix de source doivent être approuvés au premier jalon avec la partie théorique.
36. Contrôler l'absorption et la réflexion sur un problème plan avant les géométries irrégulières. Avec une source unitaire en haut, un axe vertical orienté du haut vers le bas et un bas ouvert, la référence continue à incidence normale est une exponentielle qui se propage vers le bas. Pour le bas réfléchissant, une combinaison de cosinus satisfait la dérivée normale nulle, en évitant ses fréquences singulières. Le support est une approximation discrète de ces références ; l'écart doit diminuer avec le pas.
37. Ne pas transférer directement le calcul spectral réel du précédent projet au nouvel opérateur complexe. Une factorisation directe creuse constitue la référence pour les réponses d'état et d'adjoint. Le choix d'un autre solveur doit conserver les résidus et les mêmes équations.

Pour rendre le contrôle plan directement programmable, on prend un rectangle de hauteur physique `H`, une profondeur `y` croissante du haut vers le bas, une pression unitaire en haut et Neumann sur les côtés. À nombre d'onde non nul, avec un coefficient de code constant `a_code` en bas, la référence est :

```python
u_reference = (
    numpy.cos(k * (H - y))
    - (a_code / k) * numpy.sin(k * (H - y))
) / (
    numpy.cos(k * H)
    - (a_code / k) * numpy.sin(k * H)
)
```

La hauteur `H` est celle du mur plan effectivement représenté, pas la hauteur du tableau contenant aussi le complément extérieur. Avec `a_code=0`, cette expression donne la solution réfléchissante ; avec `a_code=1j*k`, elle donne l'onde sortante `numpy.exp(1j*k*y)`. Le test choisit des paramètres dont le dénominateur est éloigné de zéro, compare le champ aux nœuds intérieurs et vérifie la baisse de l'erreur au raffinement. Ces expressions sont des solutions analytiques de contrôle de l'équation plane et de ses conditions au bord, sans représenter des résultats des scénarios route et rail.

### 6. Reconstruire le champ et les traces sans perdre les faces

38. Replacer les valeurs intérieures calculées dans une grille complexe destinée à l'affichage. Marquer séparément le fluide, les frontières et le complément extérieur. Les données de Dirichlet peuvent être réinsérées avec leur vraie valeur imposée ; les zéros initialisés par le support sur les autres cases ne sont pas interprétés comme une pression physique nulle.
39. Reconstruire une trace Robin **par face** avec la relation précédente. Conserver la correspondance face, nœud intérieur, nœud de bord et variable de densité. Si plusieurs faces partagent un nœud de bord, leurs traces éliminées peuvent différer dans ce schéma ; on conserve ces valeurs pour les intégrales et pour les vérifications.
40. Pour une image de la densité ou de la trace, une agrégation nodale peut être définie et annoncée comme affichage. Elle ne remplace ni le relevé de faces de l'assemblage, ni les poids du budget, ni le calcul de la dissipation.
41. Lorsque l'impédance et la convention physique ont été validées, calculer éventuellement la puissance dissipée par somme sur ces mêmes faces. Pour une impédance pression sur vitesse normale, la puissance moyenne par unité de profondeur est la moitié du module carré de la trace, multipliée par la partie réelle de l'admittance et par la longueur de face. La densité multiplie ici l'admittance de référence. Contrôler le signe de cette quantité avec la loi effectivement retenue.
42. Retourner l'énergie de pression comme objectif et la puissance dissipée comme mesure distincte. Une baisse de l'objectif et une hausse de la dissipation peuvent être confrontées, mais on ne les assimile pas et on ne présente pas un rapport de normes comme une puissance en watts.

### 7. Intégrer les quatre contributions avec les callbacks communs

43. Charger `materiaux.py` pour obtenir la loi complexe aux fréquences demandées et ses métadonnées. Vérifier la longueur des tableaux, la correspondance entre fréquences et valeurs, les unités, les coefficients finis et la plage de validité. Arrêter une campagne qui sortirait du modèle validé, ou la séparer explicitement comme exploration.
44. Fournir à `objectif.py` un assembleur fermé sur la géométrie, les conditions fixes, la source et la loi matériau. Cet assembleur reçoit uniquement la densité et la fréquence publique. Il retourne exactement les sept champs du contrat. Une même géométrie peut réutiliser ses indices et ses listes de faces ; ses coefficients changent avec la densité et la fréquence.
45. Après validation du gradient avec Joachim, fermer les paramètres de bande dans le callback destiné à Antoine :

   ```python
   def evaluate(chi, with_gradient=True):
       return evaluate_band(
           chi,
           frequencies_hz,
           frequency_weights,
           assemble,
           reference_energies=reference_energies,
           with_gradient=with_gradient,
       )
   ```

   Le dictionnaire retourné contient au moins le coût scalaire et le gradient réel ou `None`. La même densité est employée pour toute la bande. Les poids et éventuelles énergies de référence sont fixés avant optimisation.
46. Appeler `your_optimization_procedure` avec la densité initiale, ce callback, les poids physiques et le budget absolu. Transmettre les paramètres d'arrêt de façon explicite. Conserver la raison de l'arrêt et l'historique réel, y compris lorsqu'une optimisation atteint sa limite d'itérations.
47. Fournir à `campagnes.py` les fonctions `evaluate_case` et `optimize_case`. La première renvoie pour un cas, une densité et une fréquence l'énergie, le champ intérieur, les coordonnées et masques, le résidu, les traces par face et la dissipation si elle a été validée. La seconde ferme le cas et la bande puis renvoie le dictionnaire de l'optimiseur.
48. Garder les évaluations de campagne sans effet de bord sur les cas. Une densité testée ne modifie pas la densité initiale enregistrée. Des tableaux transmis au support peuvent être copiés lorsque ses routines les modifient en place.
49. Prévoir des messages d'erreur nommant le module ou la fonction manquante. Les commandes d'état seul et les contrôles du support doivent fonctionner sans `optimisation.py` ni `campagnes.py`. Une fonction encore absente ne sera jamais remplacée par une sortie qui simulerait une convergence.

### 8. Préparer une interface d'exécution et des exports reproductibles

50. Donner un point d'entrée `main()` sous `if __name__ == "__main__":`. L'interface peut distinguer les modes contrôle, référence, optimisation, campagnes et export. L'usage doit être affiché avec l'aide en ligne de commande. Les noms exacts d'options sont une organisation interne du coordinateur, pas un changement des contrats communs.
51. Calculer les chemins à partir du fichier `resonics.py` pour permettre un lancement depuis un autre dossier. Identifier explicitement le dossier de support avant de charger ses modules, car leurs imports internes emploient des noms simples. Éviter d'exécuter automatiquement le démonstrateur lors d'un import.
52. Enregistrer les paramètres physiques et numériques, versions des bibliothèques, fréquences, lois et provenance matériau, quantités, densités, coûts, résidus, contrôles de gradient, historiques et raisons d'arrêt. Les données complexes sont stockées avec des parties réelle et imaginaire identifiables ; le JSON ne doit contenir ni valeur non finie ni conversion cachée en partie réelle seule.
53. Employer des identifiants stables pour les cas et nommer les résultats à partir de leur scénario, géométrie, budget et protocole. Conserver la précision calculée dans les données ; l'arrondi intervient seulement dans les tableaux et les figures.
54. Exporter des fichiers CSV pour les courbes et des fichiers JSON pour les paramètres et contrôles. Produire les tableaux et constantes LaTeX à partir de ces mêmes résultats, afin d'éviter une valeur recopiée différemment dans le rapport et les diapositives.
55. Prévoir le recalcul propre dans un dossier de sortie séparé, sans anciens résultats. Comparer les scalaires à la référence enregistrée en excluant seulement les mesures de durée ou les métadonnées qui changent par définition. Le test est à réaliser jeudi avant de figer les figures.

### 9. Coordonner les documents et la soutenance

56. Reprendre pour le rapport le template récent : article onze points sur A4, marges de deux virgule deux centimètres, français, Latin Modern, outils mathématiques usuels, tableaux `booktabs`, figures explicites et liens cliquables. Conserver une protection raisonnable des titres, la table des matières avec sous-sections et une pagination compacte. Les figures sont citées dans leur analyse, avec des légendes nominales courtes.
57. Reprendre pour les diapositives Beamer douze points, format seize neuvièmes, thème `CambridgeUS`, légendes de figures numérotées et même réglage d'espacements que le projet précédent. Placer le plan après le titre et un rappel avant les nouvelles grandes parties. Le rappel conserve les autres parties visibles et estompées avec `currentsection`, `sectionstyle=show/shaded` et `subsectionstyle=show/shaded`.
58. Les imports de nombres et les images pointent vers les sorties du nouveau projet. Aucun ancien nombre d'onde, ancien rapport d'amélioration ou ancien pourcentage de localisation n'est conservé par défaut. Un schéma explicatif est distingué d'un champ réellement calculé.
59. Demander à chaque membre de relire les équations, le sens physique, les paramètres et les résultats de sa partie. Vérifier entre textes, figures et code la même définition de la source, du budget, du coût, des gains et de la convention de signes.
60. Préparer une soutenance de vingt minutes suivie de dix minutes de questions, avec les cinq membres. Une première répartition de quatre minutes par personne peut servir de base et être ajustée après répétition. Les explications longues restent dans les notes de préparation, tandis que les diapositives montrent surtout les courbes, les cartes, les équations introduites et les conclusions effectivement établies.

Réglages de présentation à conserver dans les sources LaTeX coordonnées par Yann :

```tex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{lmodern,amsmath,amssymb,amsfonts}
\usepackage{graphicx,booktabs,array}
\usepackage[margin=2.2cm]{geometry}
\usepackage{float,needspace,microtype}
\usepackage[section]{placeins}
\usepackage[colorlinks=true,linkcolor=blue!45!black,
  urlcolor=blue!45!black,citecolor=blue!45!black]{hyperref}
\usepackage[figure]{hypcap}
\usepackage{xcolor,xurl}
\setlength{\emergencystretch}{3em}
\setlength{\parskip}{4pt}
\setlength{\intextsep}{9pt plus 2pt minus 2pt}
\setlength{\abovecaptionskip}{5pt}
\setlength{\belowcaptionskip}{0pt}
\AddToHook{cmd/section/before}{\Needspace{10\baselineskip}}
\AddToHook{cmd/subsection/before}{\Needspace{8\baselineskip}}
\setcounter{tocdepth}{2}
\clubpenalty=10000
\widowpenalty=10000
\newcommand{\dd}{\,\mathrm{d}}
\newcommand{\norm}[1]{\left\lVert#1\right\rVert}
\newcommand{\code}[1]{{\small\nolinkurl{#1}}}
```

```tex
\documentclass[12pt,aspectratio=169,t]{beamer}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{lmodern,amsmath,amssymb,booktabs,graphicx,tikz,xurl}
\usetikzlibrary{arrows.meta,positioning,calc}
\usetheme{CambridgeUS}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{itemize items}[circle]
\setbeamertemplate{caption}[numbered]
\setbeamerfont{caption}{size=\scriptsize}
\setbeamerfont{caption name}{size=\scriptsize}
\setlength{\abovecaptionskip}{4pt}
\setlength{\belowcaptionskip}{3pt}
\setlength{\jot}{3pt}
\begin{document}
\begin{frame}{Présentation du projet}
\titlepage
\end{frame}
\begin{frame}{Plan}
\tableofcontents
\end{frame}
\section{Titre de la partie}
\begin{frame}{Rappel du plan}
\tableofcontents[currentsection,sectionstyle=show/shaded,
  subsectionstyle=show/shaded]
\end{frame}
\end{document}
```

Le titre, les cinq auteurs, l'institut et les chemins des figures sont renseignés pour ResoniCS. On reprend également les espacements communs du modèle antérieur, soit cinq points autour des équations et quatre points entre les éléments d'une liste. Le deuxième bloc illustre la structure et doit être complété par les parties et diapositives réellement retenues. Les données du rapport sont importées seulement après calcul et validation.

## Tests à inclure dans le même fichier

Les critères chiffrés d'acceptation ci-dessous sont des réglages de vérification à choisir et à enregistrer, pas des constantes imposées par le cours. On utilise d'abord de petites tailles pour localiser les erreurs avant de lancer les campagnes.

1. **Étiquettes et indices.** Vérifier les masques, la numérotation aller-retour et l'absence d'intérieur sur le bord du tableau. Un tableau rectangulaire permet de détecter les confusions entre hauteur et largeur.
2. **Réduction du support.** À coefficients unitaires, comparer le champ du système réduit avec la restriction intérieure de `processing.solve_helmholtz` sur plusieurs petites géométries. Comparer aussi les matrices et seconds membres construits avant leur restriction lorsque c'est possible.
3. **Donnée Dirichlet non homogène.** Utiliser une source imposée non nulle et vérifier que sa contribution reste dans le second membre réduit. Le champ ne doit pas devenir nul lors du branchement de l'adjoint.
4. **Mur nul et Neumann.** Comparer un mur étiqueté Robin dont le coefficient est nul à un mur réfléchissant traité par la routine Neumann, hors des fréquences singulières.
5. **Signe et onde plane.** Sur le cas plan ouvert, vérifier la direction de propagation, le signe du coefficient et la diminution de l'erreur au raffinement. Un test qui ne regarde que le résidu ne suffit pas à valider le sens physique de propagation.
6. **Trace par face.** Substituer chaque trace reconstruite dans la relation de Robin éliminée et mesurer son défaut. Inclure un nœud de bord adjacent à plusieurs intérieurs pour vérifier que ses différentes faces sont conservées.
7. **Dérivée de matrice.** Pour une densité strictement comprise dans les bornes et une direction réelle, comparer la différence centrée de la matrice appliquée à un vecteur complexe avec l'action des contributions diagonales de faces. Cette vérification porte sur le même ordre de faces et les mêmes répétitions que le gradient.
8. **Indépendance du second membre.** Vérifier numériquement l'absence de variation du second membre quand seule la densité change dans le cas contractuel.
9. **Gradient d'objectif.** Avec Joachim, comparer le produit du gradient avec une direction réelle à une différence centrée du coût recalculé. Explorer plusieurs amplitudes de perturbation ; l'accord doit s'améliorer avant la domination des arrondis. Utiliser une direction compatible avec le budget pour un contrôle supplémentaire, mais tester aussi le gradient euclidien avant projection.
10. **Budget par faces.** Vérifier la somme des poids, une densité nulle, une densité unitaire et une densité faisable non uniforme. Comparer le budget absolu entre formes et entre résolutions au lieu de comparer seulement des pourcentages nodaux.
11. **Une fréquence et une bande.** Une bande réduite à une seule fréquence de poids un doit retrouver l'évaluation de cette fréquence, coût et gradient compris. Modifier la liste de fréquences sans changer les densités ni les conventions.
12. **Descente intégrée.** Après chaque pas accepté par Antoine, recalculer le coût, le budget et les bornes. Vérifier que l'historique n'est pas rempli avec des zéros correspondant à des itérations jamais effectuées.
13. **Raffinement physique.** Garder les dimensions, le niveau, les sources et la loi matériau. Comparer au minimum les courbes d'énergie, les fréquences des pics et les conclusions de classement entre les deux pas, en raffinant autour des pics déplacés.
14. **Dissipation.** Lorsque la loi est validée, vérifier la non-négativité de la puissance absorbée selon la convention retenue. Les traces nulles doivent donner une contribution nulle. Ne pas accepter un changement de signe en prenant arbitrairement une valeur absolue.
15. **Exécution propre et documents.** Lancer le programme depuis un autre répertoire, avec un dossier de sortie vide. Vérifier que les données nécessaires sont régénérées, puis compiler le rapport et la présentation sans figure manquante, référence non définie ou débordement de marge.

## Jalons quotidiens et dépendances

| Jour | Travail de Yann | Élément à remettre avant le point quotidien |
|---|---|---|
| Lundi 2 novembre | Audit du support conservé, conventions physiques et unités, cas plans, géométries valides, comptage des faces, assembleur réduit et contrats stabilisés avec les quatre autres membres. | Paramètres et décisions documentés, comparaison réduit/support, premiers tests de signe et d'ouverture ; questions matériau et source encore ouvertes explicitement listées. |
| Mardi 3 novembre | Intégration de l'objectif de Joachim et de la projection/descente d'Antoine, validation du gradient, raccordement des références d'Olympia. | Gradient contrôlé par perturbation, objectif et résidu contrôlés, budgets faisables, baselines entièrement recouvertes et à quantité limitée comparables. |
| Mercredi 4 novembre | Intégration de la bande multi-fréquence, variation des budgets et des formes, raffinements à dimensions fixes. | Même densité sur la bande, mêmes budgets absolus entre formes, premières comparaisons de robustesse et de résolution, limites encore non levées identifiées. |
| Jeudi 5 novembre | Gel des paramètres et données retenus, recalcul propre, contrôle des exports, raccordement des figures et tableaux aux documents. | Résultats reproduits, fichiers de données et paramètres archivés, rapport et présentation compilés ; toute affirmation de performance renvoie à un calcul identifiable. |
| Vendredi 6 novembre | Vérification finale, archive de livraison, répétition et coordination des prises de parole. | Archive exécutable avec sources/PDF et dépendances nécessaires, documents lisibles, vingt minutes de présentation réparties entre les cinq membres, préparation aux dix minutes de questions. |

La plage de validation collective annoncée est de quatorze heures trente à dix-sept heures. Chaque livrable quotidien doit être prêt avant cette plage et chaque membre doit pouvoir en expliquer et en valider sa portion. Elle n'est pas comptée comme une plage pleine de développement individuel ; le créneau exact de la soutenance du vendredi reste celui communiqué par l'enseignement.

## Limites et décisions à faire valider

- Le contrat d'assemblage et de dérivation suppose les coefficients unitaires imposés et un second membre Robin nul. Toute extension doit redéfinir les dérivées correspondantes avant optimisation.
- Une identification matériau absente des documents ne sera pas remplacée par la constante complexe du démonstrateur. La loi, les paramètres et leur provenance sont une décision du premier jour avec Mathis et la partie théorique.
- Le coût est l'intégrale discrète du module carré de la pression sur les inconnues intérieures. Il n'est pas une puissance dissipée ni un niveau sonore en décibels sans définition supplémentaire.
- La quantité de matériau est celle du modèle de bord. Son lien avec un volume ou une masse de produit suppose une épaisseur, une profondeur et éventuellement une masse volumique documentées.
- Le schéma de trace et la longueur de bord sont discrets. Une égalité de budget discrète n'annule pas le besoin d'étudier leur convergence géométrique.
- Les optimisations portent sur une densité pour une géométrie fixée. La comparaison des niveaux géométriques se fait à l'extérieur de la boucle d'optimisation ; on ne change pas le domaine au cours d'une descente sans nouvelle dérivation.
- Une limite d'itérations, un petit gradient projeté ou la meilleure solution parmi plusieurs départs ne constitue pas une preuve d'optimalité globale. Le bilan distingue le résultat obtenu, les cas testés et la tolérance du protocole.
- Les contrôles proposés dans cette fiche restent à réaliser. Aucun défaut du support n'est déclaré corrigé et aucune performance acoustique n'est annoncée à ce stade.

## Sources à relire pour les choix concernés

- **Énoncé EI, `Sujet-EI-EXT-2026.md`** : objectifs route et rail, tunnel réfléchissant, quantité poreuse fixée, étapes des cinq jours, dix points par longueur d'onde, validation quotidienne et format de soutenance.
- **Support distribué** : `_env.py` pour les étiquettes ; `preprocessing.py` pour coefficients, sources, motifs et partition ; `processing.py` pour les stencils, l'élimination des conditions au bord et les traces à vérifier ; `postprocessing.py` pour les tracés ; `demo_control_polycopie2024.py` pour le scénario et les blocs pédagogiques.
- **Cours de modélisation** : diapositives dix-huit et dix-neuf pour la convention temporelle et les conversions ; trente-trois à quarante-deux pour les conditions au bord ; cinquante-neuf à soixante-six pour l'identification d'un coefficient Robin et les exemples de matériaux ; soixante-quatorze et soixante-quinze pour le lien avec l'amortissement d'une onde plane. La formule de chaque modèle matériau doit être disponible et vérifiée, car les termes d'erreur de la méthode d'identification ne sont pas intégralement donnés dans ce support.
- **Document sur Dirichlet non homogène** : choix de l'inconnue, de l'espace des perturbations et traitement du champ total, à relier aux équations établies par Joachim.
- **G. Allaire, optimisation paramétrique** : différentiation de l'état, adjoint, contraintes et descente, à relier au gradient discret effectivement validé.
- **Rapport et présentation antérieurs** : démarche de contrôle numérique et templates. Leur modèle sans absorption et leurs données numériques ne sont pas une référence de performance pour l'EI.

## Clés de retour retenues pour la première intégration

Le dictionnaire de `your_optimization_procedure` emploie les mêmes clés dans les cinq lots :

```python
{
    "chi": densite_finale,
    "value": cout_final,
    "gradient": gradient_final,
    "history": historique,
    "budget_error": erreur_absolue_de_budget,
    "projected_gradient_norm": residu_projete,
    "stop_reason": motif_arret,
    "converged": convergence_annoncee,
    "n_iterations": iterations_acceptees,
    "n_evaluations": appels_evaluation,
}
```

`history` est une liste de dictionnaires avec `iteration`, `value`, `step`, `projected_gradient_norm`, `budget_error` et `backtracks`. La ligne initiale a le numéro zéro et un pas nul. Les clés supplémentaires sont autorisées, mais ces noms restent communs.

## Clés des callbacks de campagne

Les clés suivantes sont retenues pour la première intégration. Un cas construit par `build_case(specification)` contient `case_id`, `design_weights`, `material_length_m`, `chi0` et `metadata`. Les métadonnées contiennent au minimum `level`, `spacestep_m`, `c_m_s`, `geometry`, `source` et `material`.

`evaluate_case(case, chi, frequency_hz)` renvoie `energy`, `u`, `coordinates`, `masks`, `relative_residual`, `robin_traces` et `dissipated_power`. Le champ `u` est un tableau complexe de la même forme que la grille. `coordinates` contient `x`, les abscisses des colonnes, et `y`, les ordonnées des lignes. `masks` contient `interior`, `design` et `open`, tableaux booléens de la forme de la grille. `robin_traces` conserve une valeur par face du mur et `dissipated_power` vaut `None` tant qu'un bilan physique n'est pas disponible. L'énergie est calculée avec le seul masque intérieur. Les poids et l'ordre des faces sont fournis par le constructeur.

Le callback d'optimisation retourne les clés communes de l'optimiseur, sans les renommer.
