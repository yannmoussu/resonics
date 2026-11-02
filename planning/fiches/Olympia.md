# Olympia — Campagnes numériques, comparaisons et choix du produit

Les repères **O1 à O5** du Gantt correspondent aux cinq journées, du lundi au vendredi.

## Livrable

Tu produis un seul fichier, `campagnes.py`. Il contient le protocole des études, les traitements de données, les graphiques, les exports et un petit exemple autonome sous `if __name__ == "__main__":`. Les bibliothèques autorisées sont NumPy, SciPy, Matplotlib et la bibliothèque standard. Ton exemple et tes vérifications ne doivent importer aucun autre fichier du groupe.

Yann te transmet les fonctions de construction, d'évaluation et d'optimisation comme arguments. Ton rôle est d'organiser leurs appels, de garantir des comparaisons cohérentes et de transformer les calculs en résultats interprétables. Les fonctions de support restent conservées et tu n'as pas à redessiner une fractale ni à modifier leur solveur. Les premiers essais utilisent les niveaux déjà fournis.

Les résultats finaux permettent de comparer un mur plan, des profils irréguliers de niveaux un et deux, une couverture complète du mur et plusieurs répartitions à quantité de matériau fixée. Tu sélectionnes les fréquences problématiques, puis tu vérifies les distributions optimisées sur toute la bande et sur des fréquences non employées dans leur optimisation. Les commentaires et les docstrings de ton fichier sont des phrases françaises sans équations ni symboles mathématiques.

## Signatures et contrat des données

Les callbacks communs à utiliser sans modifier leur sens sont :

```python
case = build_case(specification)

result = evaluate_case(case, chi, frequency_hz)

optimization_result = optimize_case(
    case, frequencies_hz, frequency_weights, chi0
)
```

La première signature est une manière pratique de recevoir le constructeur passé par Yann. `specification` décrit le cas voulu ; `case` reste l'objet commun qu'il renvoie. Les deux callbacks d'évaluation et d'optimisation sont ceux du contrat commun. Tu ne fais pas d'import croisé pour les appeler.

Un cas contient son identifiant, les métadonnées de géométrie et de source, les poids de conception, le budget absolu et une densité initiale. Pour coder les contrôles, convenez avec Yann de noms explicites, par exemple :

```python
{
    "case_id": ...,
    "design_weights": ...,
    "material_length_m": ...,
    "chi0": ...,
    "metadata": {
        "level": ...,
        "spacestep_m": ...,
        "c_m_s": ...,
        "geometry": ...,
        "source": ...,
        "material": ...,
    },
}
```

Cette convention de rangement est retenue pour la première intégration et conserve les grandeurs du contrat. Le vecteur `chi` possède une entrée réelle par nœud Robin de conception et reste entre zéro et un. Les ouvertures traitées par Robin sont exclues de cette conception. `design_weights` contient des longueurs positives, obtenues en multipliant le pas par le nombre de faces adjacentes au fluide utilisé dans l'assemblage. La contrainte est un budget **absolu de longueur de matériau**, conservé entre les formes. Avec épaisseur et profondeur fixées, il correspond à un volume de poreux proportionnel.

`evaluate_case` retourne l'énergie, le champ complexe intérieur, les coordonnées, les masques, le résidu et les traces Robin par face. La puissance dissipée n'est disponible comme grandeur physique que si le coefficient de matériau a été validé. Conservez des clés lisibles, par exemple `energy`, `u`, `coordinates`, `masks`, `relative_residual`, `robin_traces` et `dissipated_power`. Ton module doit signaler une grandeur manquante au lieu de l'inventer.

`optimize_case` retourne le dictionnaire du lot d'Antoine : densité finale, coût, gradient final, historique réel des itérations, erreur de budget, résidu projeté et raison de l'arrêt. La densité optimisée est commune à toutes les fréquences de son appel.

Les auxiliaires suivants sont proposés dans ton unique fichier :

```python
def validate_case(case, frequencies_hz, min_points_per_wavelength=10):
    ...

def make_frequency_weights(frequencies_hz, spectral_density=None):
    ...

def detect_local_maxima(frequencies_hz, energies, prominence=None):
    ...

def refine_frequency_grid(frequencies_hz, peak_indices, subdivisions=5):
    ...

def run_frequency_scan(case, chi, frequencies_hz, evaluate_case):
    ...

def run_campaign(case_specifications, frequencies_hz, frequency_weights,
                 budgets_m, build_case, evaluate_case, optimize_case,
                 output_dir):
    ...
```

Chaque fonction doit être testable avec de petits callbacks synthétiques écrits dans ce même fichier. Les noms d'auxiliaires peuvent être adaptés, mais l'entrée des callbacks communs et les unités ne doivent pas être changées.

## Étapes numérotées de réalisation

### 1. Créer un manifeste d'expériences avant de lancer les calculs

Une ligne du manifeste identifie la géométrie, son niveau, ses dimensions physiques, son pas, la source, le matériau, son épaisseur, la bande fréquentielle, le budget, la densité initiale et les réglages d'optimisation. Ne te limite pas au nom d'une figure pour identifier un résultat.

L'énoncé demande un domaine testé dans des conditions réfléchissantes défavorables, une source sur le bord supérieur et un mur de Robin en bas. La comparaison ouverte/réfléchissante est préparée avec Joachim et Yann. Les changements de conditions aux limites doivent donner des cas distincts dans les données. La source de la partie précédente, située dans une cavité et normalisée par la matrice de masse, ne doit pas être réintroduite automatiquement ici.

Commence par trois niveaux de forme, zéro, un et deux, construits avec le générateur fourni. Le nom `create_motif_koch` du support désigne un motif orthogonal à huit segments de quart ; les documents doivent décrire le contour réellement obtenu, sans le confondre avec le Koch triangulaire du projet précédent.

### 2. Contrôler le maillage et la dimension des détails

La fréquence publique est en hertz. Le calcul des longueurs d'onde utilise la célérité arrêtée avec Mathis. Vérifie pour la plus haute fréquence de chaque campagne :

\[
\lambda_{\min}=c/f_{\max},\qquad \lambda_{\min}/h\geq10
\]

Cette règle vient de l'énoncé et constitue un minimum, pas une preuve suffisante de convergence. Vérifie aussi le nombre de cellules représentant le plus petit détail géométrique. Les subdivisions du motif doivent être représentables sur la grille ; Yann contrôle notamment la compatibilité entre la résolution et les quarts successifs du profil. Ne conserve pas un niveau qui a été déformé ou supprimé par les arrondis.

L'échelle d'irrégularité de l'ordre de la demi-longueur d'onde est une règle de conception donnée oralement. Pour chaque fréquence cible, enregistre le rapport entre la taille caractéristique du détail et la demi-longueur d'onde. Un profil à plusieurs niveaux peut proposer plusieurs tailles ; cela ne garantit pas leur efficacité avant le calcul.

Le cadre informatique comporte des points complémentaires sous le mur. Ne les compte ni dans l'aire fluide ni dans le critère de pression. La fonction d'évaluation doit te fournir le masque intérieur exact.

### 3. Construire les références entièrement recouvertes

Pour chaque forme, prends une densité égale à un sur tous les nœuds de conception du mur, puis calcule la réponse sur la même bande. C'est le mur entièrement recouvert par le matériau choisi, et non une surface assurée sans réflexion à toute incidence.

Enregistre la longueur totale ainsi consommée : elle varie lorsque le périmètre change. Ces références répondent à la demande de l'énoncé et servent à analyser l'effet de la forme. Elles ne sont pas des comparaisons à quantité égale ni des bornes mathématiques assurant une énergie toujours plus faible.

Le mur plan entièrement recouvert doit être calculé en premier. Les niveaux un et deux entièrement recouverts suivent avec les mêmes unités, la même excitation et le même matériau. Trace les trois énergies absolues sur les mêmes axes avant de choisir un produit ou une fréquence d'optimisation.

### 4. Calculer les références initiales à budget fixé

Choisis avec le groupe un budget de longueur réalisable pour toutes les formes comparées. Il doit rester entre zéro et la plus petite longueur totale disponible sur ces formes. Pour chaque cas, contrôle :

\[
0\leq\chi_l\leq1,\qquad \sum_l w_l\chi_l=Q
\]

Les poids de conception proviennent des mêmes faces que le solveur. La fraction de nœuds du programme de démonstration ne remplace pas cette quantité physique. Le budget ne doit pas être appliqué à des nœuds de l'ouverture ou à des points du complément.

Une référence initiale simple et exactement faisable consiste à prendre une densité uniforme égale au budget divisé par la longueur totale de conception. Elle représente une variable de conception relaxée ; ne la décris pas comme des blocs binaires déjà fabriqués. Si l'on préfère une répartition par portions de contour, son budget doit aussi être vérifié et corrigé exactement avant l'évaluation.

Pour chaque géométrie, compare cette référence partielle à sa référence entièrement recouverte en affichant les deux quantités de matériau. Entre géométries, compare également les distributions partielles de même budget absolu.

### 5. Balayer la fréquence et repérer les maxima problématiques

Effectue un premier balayage croissant et commun aux cas comparés. La grille fréquentielle de départ et son étendue viennent du cadrage avec Mathis. Conserve toutes les valeurs brutes, le résidu et le statut de validité du matériau.

Repère les maxima locaux à l'aide de comparaisons entre voisins ou de `scipy.signal.find_peaks`. Une prominence peut éviter de retenir une simple oscillation de petite amplitude, mais son choix doit être enregistré. Traite séparément les extrémités de bande : une courbe encore croissante au dernier point peut demander une extension ou une vérification de bord, même si ce point n'est pas un maximum local intérieur.

Ajoute des points dans les intervalles voisins des principaux maxima, puis recalcule le champ à ces nouvelles fréquences. Ne remplace pas une résolution par une interpolation de courbe. Répète si nécessaire jusqu'à ce que le déplacement du maximum et sa hauteur soient suffisamment stables pour sélectionner les fréquences d'optimisation. Les seuils de stabilité sont choisis puis conservés dans les données.

Un point non fini ou un résidu refusé ne devient pas une grande énergie ordinaire. Garde un statut d'échec, vérifie la proximité d'une résonance et ne raccorde pas artificiellement les deux côtés d'une singularité. Le cas sans matériau peut demander une attention particulière dans le tunnel réfléchissant.

### 6. Fixer la signification des poids après raffinement fréquentiel

Des poids égaux à chaque point ne représentent plus une moyenne uniforme sur la bande lorsque tu ajoutes beaucoup de points autour d'un pic. Sinon, le simple raffinement donnerait davantage de poids à ce pic et changerait l'objectif sans décision scientifique.

Si l'on veut approcher une moyenne uniforme en fréquence sur une grille irrégulière, utilise les poids de la règle du trapèze puis normalise leur somme : demi-intervalle au premier et au dernier point, et demi-distance entre les deux voisins pour un point intérieur. Si une densité spectrale documentée est disponible, multiplie les poids de quadrature par cette densité avant de les normaliser.

Si l'on optimise seulement une liste de fréquences problématiques, des poids égaux peuvent être un choix valable. Il faut alors parler d'une somme sur ces fréquences sélectionnées, et non d'une intégrale uniforme sur toute la bande.

Dans tous les cas, fige la grille et les poids avant chaque optimisation. La validation peut employer une autre grille, avec ses propres poids de quadrature explicitement calculés. Ne change pas les poids à chaque itération d'optimisation. Vérifie qu'ils sont réels, positifs ou nuls et que leur somme vaut un.

### 7. Lancer les optimisations mono puis multifréquences

Pour une fréquence problématique, appelle `optimize_case` avec une seule fréquence et un poids unitaire. Vérifie le budget de la densité retournée, puis réévalue cette densité sur toute la bande. Un résultat très bon au seul point d'optimisation peut dégrader des fréquences voisines.

Passe ensuite au même problème avec plusieurs fréquences sélectionnées et des poids fixés. Une seule densité est optimisée pour l'ensemble de ces fréquences. Il serait incorrect d'optimiser une densité différente à chaque fréquence puis de présenter cette collection comme un seul mur fabriqué.

Le coût multifréquence peut être normalisé par des énergies de référence strictement positives. Elles sont alors calculées avant l'optimisation, gelées et communes aux produits comparés. Par exemple, une référence plane commune permet une comparaison de coûts normalisés entre formes. Ne normalise pas chaque produit par sa propre performance si l'objectif est de les classer directement. Dans les figures, conserve toujours aussi les énergies absolues.

Tu ne réécris pas le gradient ou la projection d'Antoine. Tu contrôles les données transmises, la cohérence de l'historique et l'énergie obtenue par réévaluation indépendante du résultat final. Un arrêt au nombre maximal d'itérations ou une convergence locale ne doit pas être présenté comme une garantie d'optimalité globale.

### 8. Vérifier sur des fréquences non utilisées et sur un maillage plus fin

Prépare une grille de validation commune avant de lire les résultats optimisés : elle contient notamment des fréquences intermédiaires absentes de l'entraînement et des points supplémentaires près des pics. Réévalue les mêmes densités, sans les réoptimiser sur cette grille.

Compare les moyennes de bande, les énergies maximales observées et leurs fréquences, les écarts par rapport à la référence initiale et la quantité de matériau. La grille d'optimisation et la grille de validation sont enregistrées séparément. Si la grille de validation sert ensuite à modifier la conception, elle devient une partie du nouveau protocole d'optimisation ; une autre validation doit alors être annoncée.

Refais les configurations importantes sur une grille spatiale plus fine. La densité de conception doit être transférée le long du même profil et son budget doit être conservé ; Yann fournit cette adaptation géométrique. Vérifie les conclusions et les pics, pas seulement le résidu d'un système linéaire. Une petite erreur de résolution ne prouve pas que les pics sont bien discrétisés.

### 9. Étudier la quantité de matériau

Compare plusieurs budgets absolus réalisables pour toutes les formes. Les valeurs sont décidées à partir des dimensions et du périmètre disponibles ; elles ne sont pas remplacées par une fraction nodale identique d'une forme à l'autre. Chaque optimisation commence avec une densité faisable et emploie les mêmes règles d'arrêt et de validation.

Trace la performance validée en fonction de la quantité de matériau et garde la référence entièrement recouverte. Ce graphe permet de distinguer le gain d'un meilleur placement du gain obtenu simplement en utilisant davantage de matériau. Les épaisseurs et la profondeur restent fixées pendant cette étude ; si elles changent, il faut convertir les quantités en volume et créer une comparaison distincte.

Si l'optimisation est répétée avec plusieurs répartitions initiales, conserve toutes les valeurs finales et indique la règle de sélection. Ne présente pas un seul minimum local obtenu comme le meilleur possible sur toutes les densités et toutes les formes.

### 10. Produire les figures, les tables et la recommandation

Les courbes indispensables sont : énergie du mur plan entièrement recouvert, comparaison des formes entièrement recouvertes, comparaison initial/optimisé à budget fixé, performances mono et multifréquences sur la grille de validation, puis performance en fonction de la quantité de matériau.

Les cartes de densité et de champ doivent utiliser les mêmes coordonnées et les mêmes échelles dans une comparaison. Pour l'amplitude, calcule un maximum commun aux cartes comparées et affiche la même barre de couleurs. Si tu montres aussi des champs renormalisés individuellement pour étudier leur forme, sépare cette figure et écris qu'elle compare des formes, pas des amplitudes absolues. Les points complémentaires doivent être masqués.

L'énergie est le critère de pression du sujet. Elle n'est pas directement la puissance absorbée. Une puissance dissipée au mur ne peut être affichée que si les traces de bord et le coefficient physique ont été validés. Ne transforme pas une baisse d'énergie simulée en indice réglementaire de mur ou en performance d'un produit commercial.

Jeudi, propose une configuration retenue sur la base des résultats de validation : forme, niveau, dimensions, matériau, épaisseur, quantité, bande visée et compromis observés. Les données doivent aussi montrer une configuration moins performante ou une limite utile, pour expliquer le choix. Le résultat est le meilleur parmi les configurations effectivement testées, avec la précision et les contraintes annoncées.

## Données CSV et JSON à fournir

Un CSV de balayage comporte au moins : identifiant du cas, géométrie, niveau, pas en mètres, fréquence en hertz, nombre d'onde, matériau, épaisseur, type de répartition, budget absolu, quantité réellement obtenue, énergie, résidu, statut du calcul et éventuelle puissance dissipée validée. Les champs volumineux ne doivent pas être copiés dans chaque cellule du CSV ; ils peuvent être sauvegardés séparément avec un chemin enregistré dans le JSON.

Un CSV de synthèse comporte, pour chaque produit et chaque budget : moyenne validée de bande, maximum échantillonné, fréquence du maximum, coût final de l'optimiseur, erreur de budget, résidu projeté, nombre d'itérations et raison de l'arrêt. Les maxima sont nommés comme maxima échantillonnés tant que leur convergence fréquentielle n'a pas été établie.

Le JSON rassemble le manifeste, les paramètres des callbacks, les versions des bibliothèques, les grilles fréquentielles et spatiales, les poids, les références gelées, la provenance du matériau, les statuts d'échec et l'historique de chaque optimisation. Les noms de fichiers doivent être déterministes et ne doivent pas faire écraser deux cas différents. Une graine est enregistrée si un tirage intervient.

## Tests et critères d'acceptation

1. **Exemple autonome :** crée dans le même fichier de petits callbacks synthétiques qui renvoient des énergies et des densités connues. Les fichiers de vérification sont clairement distincts des résultats acoustiques et ne portent aucun nom de produit réel.
2. **Maillage :** un cas ne respectant pas dix points par longueur d'onde est refusé avant son balayage. Les niveaux non représentables sur la grille sont signalés.
3. **Budget :** vérifie les densités, la taille des poids et la quantité réellement obtenue. Un budget négatif ou supérieur à la longueur disponible est refusé. Les cas zéro et couverture complète sont traités explicitement.
4. **Fréquences :** refuse les fréquences non finies, nulles ou négatives. Trie et déduplique les points ajoutés avant leur évaluation en gardant une correspondance fiable avec leurs résultats.
5. **Pondération :** la somme des poids vaut un. Sur une fonction constante, le coût est inchangé quand le maillage fréquentiel est raffiné localement. Sur une fonction affine, la règle du trapèze retrouve la moyenne analytique de l'intervalle. Ce contrôle doit échouer si l'on remplace les poids par des poids égaux sur une grille fortement irrégulière.
6. **Pics :** une petite courbe synthétique à deux maxima permet de vérifier le repérage et les intervalles raffinés. Les extrémités sont examinées séparément.
7. **Multifréquence :** vérifie que le callback reçoit la même densité pour chaque fréquence et que le budget reste le même après optimisation.
8. **Validation :** les fréquences de contrôle non utilisées dans l'optimisation sont identifiées dans les données. Une réévaluation finale retrouve le coût annoncé lorsque l'on reprend exactement les mêmes fréquences, poids et références.
9. **Traçabilité :** deux exécutions d'un même petit cas produisent les mêmes valeurs et les mêmes identifiants. Tous les échecs restent enregistrés.
10. **Figures :** les cartes comparées possèdent la même échelle et le complément du domaine reste masqué. Une grandeur physique non disponible est marquée comme non calculée, et non remplacée par zéro.

## Jalons de la semaine

- **Lundi matin :** convenir des métadonnées avec Yann et des unités avec Mathis ; écrire les contrôles et les callbacks synthétiques ; préparer le manifeste des références plan/niveaux un et deux.
- **Lundi, point entre 14 h 30 et 17 h :** présenter le protocole et les dépendances encore manquantes. Faire valider les bandes, les dimensions, les comparaisons de quantité et les premiers critères de qualité du calcul.
- **Mardi :** produire les balayages des formes entièrement recouvertes, puis ceux des répartitions initiales à budget fixé ; repérer et raffiner les pics ; fournir les fréquences problématiques à Joachim et Antoine. Intégrer une première optimisation monofréquence dès que leurs callbacks sont validés.
- **Mercredi :** comparer mono et multifréquences sur une grille de validation commune ; lancer la variation du budget ; commencer le raffinement spatial des cas utiles. Les critères et les poids restent enregistrés et fixés pour chaque optimisation.
- **Jeudi :** terminer les contrôles essentiels, établir le tableau de compromis et proposer le produit. Préparer les figures finales et les interprétations associées au rapport et à la présentation.
- **Vendredi matin :** geler les résultats et leurs fichiers de provenance ; vérifier que toutes les figures des documents proviennent de cette version ; préparer l'oral et valider les conclusions avec toute l'équipe.

## Intervention de quatre minutes à l'oral

Tu présentes les références et les règles de comparaison, puis une courbe montrant les fréquences problématiques. Tu expliques l'effet de l'optimisation multifréquence sur une grille de validation et l'influence de la quantité de matériau. Tu termines par le compromis qui motive le produit retenu. Tu précises les unités, le sens de l'énergie et les limites observées, sans annoncer une certification ou une optimalité globale.

## Limites à annoncer

Le meilleur profil est sélectionné dans une famille finie et à une précision de calcul donnée. Le critère de pression dépend de la source et des conditions aux limites. La même quantité de matériau n'impose ni la même fraction du périmètre ni une couverture complète identique entre formes. Une densité intermédiaire est une variable relaxée tant qu'une répartition fabricable n'a pas été construite et réévaluée. Les comparaisons expérimentales de l'ancien mur du cours servent d'état de l'art, pas de validation expérimentale du produit simulé.

## Sources à lire et à citer

- `Sujet-EI-EXT-2026.md` : ordre des études demandé du mardi au jeudi, références entièrement recouvertes, optimisation à plusieurs fréquences, quantité de matériau et défense de vingt minutes à cinq.
- `preprocessing.py` : générateur fourni et définition des régions ; l'adaptation est fournie par Yann et ne doit pas être recodée dans ce lot.
- `processing.py` : sens des tableaux retournés et traitement des bords, à vérifier avec Yann avant d'exploiter les traces de Robin.
- `postprocessing.py` : fonctions de dessin initiales ; les campagnes doivent ajouter les unités, le masquage et les échelles communes nécessaires à la comparaison.
- M. Filoche, `Mur-antibruit-Filoche.pdf`, pages 21–29 et 35–55 : différence entre localisation, pertes et forme des champs ; pages 57–70 : exemple de mur et distinction entre simulations et mesure globale d'absorption.
- Fiche de Mathis et provenance du matériau retenu : validité fréquentielle et unités des coefficients. Contrat commun pour le budget physique, les callbacks et la distinction entre énergie et puissance dissipée.

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
