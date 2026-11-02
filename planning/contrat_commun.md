# Contrat commun ResoniCS

Cinq fichiers à produire, un seul fichier à écrire par personne : Yann `resonics.py`, Mathis `materiaux.py`, Olympia `campagnes.py`, Joachim `objectif.py`, Antoine `optimisation.py`. Chaque fichier possède un petit exemple autonome sous `if __name__ == "__main__":`. Les essais de fonctions emploient de petits exemples explicitement synthétiques ; ils ne sont jamais publiés comme performances acoustiques. NumPy, SciPy, Matplotlib et bibliothèque standard uniquement. Commentaires en phrases françaises sans équations ni symboles mathématiques. Les équations restent dans les explications et les calculs Python. Les signatures ci-dessous sont des contrats proposés, pas des fonctions déjà présentes dans le support.

Le support distribué reste conservé. Yann écrit l'adaptation et les appels, sans demander aux autres d'éditer les modules fournis. Les noms pédagogiques `your_compute_objective_function` et `your_optimization_procedure` sont conservés. Si l'appel long du programme distribué est gardé, son adaptation aux nouveaux arguments est faite dans `resonics.py`, hors des blocs signalés comme imposés.

## Unités et signes

La fréquence publique `frequency_hz` est en hertz. On définit la pulsation `angular_frequency_rad_s = 2*pi*frequency_hz`, puis `k_per_m = angular_frequency_rad_s / c_m_s` et la longueur d'onde `wavelength_m = c_m_s / frequency_hz`. Le paramètre historique `omega` de `processing.solve_helmholtz` reçoit en réalité **le nombre d'onde**, jamais directement les hertz ou la pulsation.

Convention temporelle : exp(-i*omega*t). Avec normale sortante, la Robin physique s'écrit `partial_n u + a_phys*u = 0`. Le support élimine la valeur de bord par `u_B = u_I/(1-h*a_code)` lorsque les coefficients imposés valent un et le second membre Robin est nul. Il représente donc `partial_n u - a_code*u = 0`. On utilise `a_code = -a_phys`. Pour une impédance de surface documentée `Z_s = pression/vitesse_normale_sortante`, `a_code = i*omega*rho_air/Z_s`. Sommerfeld correspond à `a_code = i*k`. Une vérification sur onde plane et un contrôle de passivité précèdent toute conclusion physique. La constante `10-10j` du démo n'identifie aucun matériau réel.

## Conception et quantité

La densité `chi` est un vecteur réel de taille B, borné entre zéro et un, associé uniquement aux nœuds Robin du mur qui touchent au moins une face intérieure. Les Robin d'ouverture sont exclues de la conception. La géométrie reste fixée pendant une optimisation ; on compare les niveaux géométriques dans des optimisations séparées.

Pour chaque nœud de conception, `design_weights` vaut le pas multiplié par le nombre de faces adjacentes au fluide, avec les mêmes faces que l'assemblage. Ce sont des longueurs discrètes en mètres, à confronter à la longueur du profil lors du raffinement. On impose `dot(design_weights, chi) = material_length_m`, budget absolu commun entre formes. Avec épaisseur et profondeur constantes, le volume poreux est proportionnel à cette longueur. La fraction nodale `V_obj` du démo ne remplace pas ce budget. Le cas entièrement recouvert est une référence qui utilise généralement plus de matériau, pas une borne assurée du coût.

## Assemblage pour Joachim

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

## Appel d'optimisation pour Antoine

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

## Matériaux et campagnes

Mathis fournit `compute_material_response(frequencies_hz, material_parameters, air_parameters) -> dict` avec impédance complexe, coefficients Robin physique et code, domaine de validité, unités et provenance. Les courbes de coefficients d'absorption réels ne suffisent pas à identifier la phase d'une impédance complexe. Le modèle doit être documenté ou fourni par les enseignants ; l'absence de ce modèle est un point à lever lundi, pas une donnée à inventer.

Olympia reçoit les fonctions de construction, d'évaluation et d'optimisation comme arguments, donc son fichier n'importe pas les fichiers en cours de rédaction. Un cas transmis par Yann contient identifiant, métadonnées de géométrie/source, `design_weights`, budget, densité initiale. `evaluate_case(case, chi, frequency_hz)` retourne énergie, champ complexe intérieur, coordonnées et masques, résidu, traces Robin par face et puissance dissipée si le coefficient physique est validé. `optimize_case(case, frequencies_hz, frequency_weights, chi0)` retourne le dictionnaire d'Antoine.

Les bandes route et rail, dimensions, lois de matériau et budget sont des choix à documenter au premier jalon. À défaut d'une pondération spectrale documentée, une pondération uniforme est annoncée comme telle. La règle d'au moins dix points par longueur d'onde vient du sujet ; l'échelle d'irrégularité proche de la demi-longueur d'onde est une règle de conception donnée oralement, à tester. Aucune performance de produit n'est déjà acquise.

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

Les paramètres d'air sont nommés `c_m_s` et `rho_air_kg_m3`. Le dictionnaire de matériau utilise `name`, `thickness_m`, `model`, `parameters`, `valid_frequency_hz` et `provenance`. Le modèle ou les tables complexes sont décrits dans `parameters`. La première intégration retient les clés de sortie indiquées dans la fiche de Mathis.
