# ResoniCS — Synthèse des décisions de modélisation de la source sonore du RER B

> **Document de transmission à un agent IA**  
> **Objet :** expliquer les choix physiques, mathématiques, numériques et logiciels discutés pour représenter le bruit du RER B dans le projet de contrôle acoustique par différences finies.  
> **Statut :** synthèse des échanges et de l'implémentation actuelle ; les valeurs non mesurées sont explicitement identifiées comme hypothèses.  
> **Dernière mise à jour :** 2 novembre 2026.

## 1. Objectif et périmètre

ResoniCS est un projet étudiant d'optimisation d'un **panneau acoustique** face au bruit du RER B, dans le **tunnel réfléchissant idéalisé** demandé dans le sujet. Le modèle est bidimensionnel et travaille sur un domaine d'air délimité par une frontière supérieure excitatrice, deux côtés réfléchissants et une paroi inférieure (plane ou préfractale) partiellement garnie de poreux.

Le but principal **n'est pas** de simuler exhaustivement la cinématique et le rayonnement de chaque élément d'une rame. Il est de **comparer dans des conditions reproductibles** différentes géométries de paroi et répartitions d'une quantité donnée de matériau poreux, puis de minimiser une mesure d'énergie acoustique sur une plage de fréquences représentative.

La source sera donc, pour le **MVP**, une **source de Dirichlet équivalente spatialement uniforme, mais spectralement non uniforme**, appliquée sur le bord supérieur du domaine. Le code devra conserver la possibilité d'affiner ce modèle ultérieurement.

## 2. Sources documentaires et degré de confiance

### Document d'orientation `SOTA.md` fourni par l'équipe

Le document distingue trois catégories de bruit :

| Catégorie | Bande indicative | Origine physique |
|---|---:|---|
| Traction et équipements auxiliaires | 100–500 Hz | Moteurs, électronique de traction, compresseurs, ventilation |
| Roulement | 250–2 000 Hz | Interactions roue–rail et excitation mécanique |
| Crissement en courbe | 1 500–4 000 Hz | Phénomènes de frottement et vibrations en courbe |

Ces plages proviennent du **document d'orientation du projet**. Elles **ne constituent pas un spectre de pression acoustique du RER B mesuré et validé** ; les amplitudes et centres spectraux exacts devront être confirmés par des mesures ou des références appropriées. Ne pas attribuer aux gaussiennes numériques des valeurs « mesurées ».

### Références pédagogiques jointes

- `Sujet-EI-EXT-2026(3).md` : tunnel réfléchissant, Dirichlet en haut, Neumann homogène à gauche et à droite, Robin sur la paroi étudiée ; au moins dix points de grille par longueur d'onde.
- `Poly-ST5-57-2026.pdf` : équations de Helmholtz et de Robin, source acoustique projetée sur la frontière Dirichlet, optimisation d'énergie sur une bande de fréquences (section 7.7.2, intégration par quadrature).
- `Dirichlet_Nonhomogene(1).pdf` : traitement d'une source de Dirichlet non homogène dans les formulations d'état/adjoint.
- `Mur-antibruit-Filoche.pdf` : effet de l'irrégularité des frontières sur la localisation et la dissipation acoustique.

## 3. Modèle mathématique de propagation

À **chaque fréquence** physique \(f\) en hertz, résoudre le problème stationnaire de Helmholtz pour la pression complexe \(u_f\) :

\[
\begin{cases}
\Delta u_f+k_f^2u_f=0 & \text{dans }\Omega,\\
u_f=g(x,f) & \text{sur }\Gamma_D\quad\text{(bord supérieur)},\\
\partial_nu_f=0 & \text{sur }\Gamma_N\quad\text{(côtés rigides)},\\
\partial_nu_f+\alpha(f)\chi\,u_f=0 & \text{sur }\Gamma_R\quad\text{(paroi étudiée)}.
\end{cases}
\qquad k_f=\frac{2\pi f}{c}.
\]

- \(c\) est la célérité du son dans l'air ; **343 m/s** est une hypothèse de travail à préciser selon les conditions ambiantes.
- \(\chi\in[0,1]\) décrit localement le matériau poreux sur la frontière Robin.
- \(\alpha(f)\) est le coefficient complexe du poreux : **sa loi en fréquence doit être identifiée ou validée** ; le code de démonstration emploie actuellement une valeur simplifiée constante.
- Dans `processing.solve_helmholtz`, l'argument nommé `omega` est utilisé comme **nombre d'onde** \(k\) dans la matrice, **pas directement comme fréquence en Hz**. Il faut passer `2*pi*f/c` et non `f` ni `2*pi*f`.

**Important :** Helmholtz résout **une fréquence à la fois**. Une source large bande signifie **plusieurs résolutions**, pas une somme de fréquences injectée dans un unique système matriciel.

## 4. Répartition spatiale retenue pour le MVP

### Décision

\[
\boxed{g(x,f)=G(f)\quad\text{pour tout point }x\text{ du bord Dirichlet supérieur}.}
\]

La source est donc **constante dans l'espace** pour chaque fréquence, mais son amplitude dépend de la fréquence.

### Justification et limite physique

La rame est une source **mobile et étendue**. À l'échelle d'un panneau et en considérant son exposition sur l'ensemble d'un passage, une excitation équivalente homogène est une **simplification raisonnable pour comparer les géométries**. Elle évite d'ajouter immédiatement une position du train, une vitesse, des phases individuelles et une évolution temporelle.

**Ne pas affirmer** que le mouvement du train rend rigoureusement le champ de pression uniforme. Le modèle \(g(x,f)=G(f)\) impose non seulement la même **amplitude**, mais aussi la même **phase** sur tout le bord : il correspond à une excitation cohérente, de type onde plane à incidence normale. Un vrai train possède plusieurs sources dont les phases, directivités et positions diffèrent.

La frontière **supérieure** porte la source équivalente ; la paroi **inférieure** est la paroi à optimiser. Ne pas présenter la condition Dirichlet comme une source directement posée sur les cellules Robin du mur.

### Validation future, optionnelle, sans complexifier le MVP

Étudier la sensibilité de la solution optimale à une source oblique :

\[
g_\theta(x,f)=G(f)\,e^{i k_f x\sin\theta}.
\]

Cette variante garde une amplitude uniforme et change seulement la phase ; \(\theta=0\) retrouve la source du MVP. Une source localisée ou mobile, ou un ensemble de sources incohérentes, constitue un prolongement possible, **pas une exigence actuelle**.

## 5. Spectre fréquentiel retenu : somme de gaussiennes

### Principe

On représente les contributions de traction, roulement et crissement par :

\[
\boxed{G(f)=\sum_{m=1}^{3}A_m\exp\!\left[-\frac{(f-f_m)^2}{2\sigma_m^2}\right].}
\]

- \(f_m\) : fréquence centrale d'une composante, en Hz ;
- \(\sigma_m\) : largeur caractéristique de la gaussienne, en Hz ;
- \(A_m\) : amplitude relative de pression pour l'exemple actuel.

### Paramètres **illustratifs** actuellement codés

| Mécanisme | Centre \(f_m\) | Largeur \(\sigma_m\) | Amplitude relative \(A_m\) |
|---|---:|---:|---:|
| Traction / moteurs | 200 Hz | 80 Hz | 1,0 |
| Roulement | 650 Hz | 250 Hz | 0,8 |
| Crissement | 2 500 Hz | 450 Hz | 0,5 |

**Ces neuf nombres sont des hypothèses de démonstration, et non des mesures du RER B.** Une somme de gaussiennes à valeurs positives constitue un modèle d'enveloppe spectrale pratique, pas une description exhaustive de tonalités ou de leur phase réelle. Les composantes se recouvrent et les amplitudes s'additionnent dans cette approximation cohérente.

**Attention aux grandeurs spectrales :** si les données d'entrée futures décrivent une **densité spectrale de puissance** ou un niveau en dB plutôt qu'une **amplitude de pression**, il ne faut pas les utiliser telles quelles comme valeur complexe de Dirichlet. Convertir les unités et, pour une densité de puissance, utiliser une amplitude de pression proportionnelle à la racine carrée de la puissance selon la normalisation choisie. Une loi en dB exige également une conversion préalable.

Il manque une calibration physique en pascals, les phases spectrales, les conditions de mesure et éventuellement un choix de pondération perceptive (dB(A)). Tant qu'elles manquent, annoncer des **énergies relatives** et non des niveaux absolus certifiés.

## 6. Application dans le code et convention de Dirichlet

La structure historique est :

```python
f_dir[:, :] = 0.0
f_dir[0, 0:N] = 1.0
```

Avec les coefficients fournis `alpha_dir = 1`, ceci correspond à une valeur de pression complexe unitaire sur les cellules du **bord supérieur étiquetées Dirichlet**. Le bord supérieur comprend des coins étiquetés Neumann dans la géométrie d'origine ; leur valeur écrite dans `f_dir` n'est pas effectivement exploitée par la condition de Dirichlet du solveur.

Pour un balayage en fréquence, conserver la convention du support **sans modifier les fonctions initialement fournies** :

```python
f_dir_freq = numpy.zeros_like(f_dir)
f_dir_freq[0, :] = source_rer_b(frequency_hz)
k = 2.0 * numpy.pi * frequency_hz / sound_speed_m_s
u_freq = processing.solve_helmholtz(
    domain_omega, spacestep, k,
    f, f_dir_freq, f_neu, f_rob,
    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob
)
```

Les tableaux `f_dir_freq` sont **indépendants** du cas initial. Les appels existants à `_set_coefficients_of_pde`, `_set_rhs_of_pde` et `_set_geometry_of_domain` ne doivent pas être redéfinis ou modifiés pour ajouter la source RER B.

## 7. Calculs fréquentiels et fonction objectif

Pour chaque fréquence \(f_i\) :

1. Calculer l'amplitude \(G(f_i)\).
2. Construire un second membre Dirichlet indépendant, uniforme spatialement.
3. Calculer le nombre d'onde \(k_i=2\pi f_i/c\).
4. Résoudre Helmholtz pour obtenir \(u_{f_i}\) sur **une géométrie et une répartition poreuse fixées** pendant tout le balayage.
5. Calculer l'énergie numérique sur les **seuls nœuds intérieurs** :

\[
J(f_i,\chi)\approx h^2\sum_{(r,s)\in\Omega_h}|u_{f_i}(r,s;\chi)|^2.
\]

On peut ensuite calculer une mesure intégrée sur la bande étudiée :

\[
J_{\mathrm{bande}}(\chi)\approx \sum_i
\frac{f_{i+1}-f_i}{2}\,[J(f_i,\chi)+J(f_{i+1},\chi)].
\]

C'est une **intégrale fréquentielle d'une norme quadratique du champ**, pas automatiquement une énergie acoustique absolue en joules (la normalisation physique n'est pas établie ici).

### Éviter la double pondération

Deux formulations **équivalentes pour un profil spatial de source fixé et une réponse linéaire** sont possibles :

- **Méthode actuellement implémentée :** imposer directement \(G(f_i)\) dans `f_dir_freq`, résoudre Helmholtz et intégrer les \(J(f_i)\) obtenus. Le poids spectral est **déjà incorporé** dans le champ, donc dans son module au carré. **Ne pas multiplier une seconde fois par \(|G(f_i)|^2\)**.
- **Autre méthode :** résoudre avec une source complexe unitaire à chaque fréquence, puis multiplier l'énergie unitaire par \(|G(f_i)|^2\) une seule fois avant l'intégration.

Lors de l'optimisation multifréquence, l'objectif est de trouver **une seule répartition de poreux \(\chi\)** qui minimise la quantité agrégée sur le spectre, et non une répartition différente pour chaque fréquence (sauf étude comparative explicite).

## 8. Bornes en fréquence et résolution du maillage

L'énoncé demande **au moins dix points par longueur d'onde**, donc :

\[
\frac{\lambda_{\min}}{h}=\frac{c}{f_{\max}h}\ge10,
\qquad \lambda_{\min}=\frac{c}{f_{\max}}.
\]

À \(c=343\,\mathrm{m/s}\) :

| Fréquence maximale | Pas spatial maximal compatible avec 10 points/longueur d'onde |
|---|---:|
| 1 000 Hz | 34,3 mm |
| 2 000 Hz | 17,15 mm |
| 4 000 Hz | 8,575 mm |

La **campagne existante** parcourt seulement **100 à 1 000 Hz, par pas de 25 Hz** : elle explore principalement la traction et une partie du roulement ; **le pic de crissement à 2 500 Hz est présent dans la définition du spectre mais n'est pas réellement simulé par cette campagne**.

Si l'on choisit, à titre illustratif et sous réserve de validation, un panneau de largeur physique \(L=4\,\mathrm{m}\), les campagnes devront utiliser :

\[
h=L/(N-1),\qquad N-1\text{ multiple de }4^{\mathrm{level}}.
\]

Exemple : niveau 2, \(N=129\), \(h=0{,}03125\,\mathrm{m}\) : compatible avec 1 000 Hz mais **pas** avec 4 000 Hz. Pour atteindre 4 000 Hz à niveau 2 sur 4 m, \(N=481\) fournit un pas de \(8{,}33\,\mathrm{mm}\), sous réserve de prévoir également une hauteur et un coût calcul adaptés. Le maillage doit aussi **représenter les plus petits reliefs** des profils comparés.

**Attention :** le cas pédagogique initial `N=50`, `spacestep=1/N` n'est **pas**, par lui-même, la validation d'une largeur réelle de 4 m. Ne pas confondre coordonnées discrètes historiques et géométrie physique des campagnes.

## 9. Architecture logicielle retenue

La séparation des responsabilités discutée et **visible dans les fichiers présents** est la suivante :

| Fichier | Rôle pour la source RER B | Fonction actuelle |
|---|---|---|
| `preprocessing.py` | **Définir/préparer la donnée d'entrée spectrale** | `source_rer_b(frequency_hz)` |
| `processing.py` | **Réaliser le balayage et les résolutions de Helmholtz** | `run_rer_b_frequency_sweep(...)` |
| `postprocessing.py` | **Tracer les résultats et enregistrer les figures** | `plot_rer_b_frequency_sweep(results)` |
| `demo_control_polycopie2024.py` | **Orchestrer la campagne** et fixer ses paramètres | Appels aux trois fonctions |

L'architecture évite de placer les tracés dans le programme principal ou les routines de résolution dans le prétraitement. Ne pas modifier les fonctions historiques protégées ; ajouter ou corriger les fonctions de projet à côté. La logique existante des cellules évaluées du programme principal doit rester inchangée.

### Contrat actuel de la fonction de balayage

`processing.run_rer_b_frequency_sweep(...)` prend le domaine, le pas, le vecteur de fréquences en Hz, les seconds membres et coefficients de Helmholtz, ainsi que `sound_speed_m_s`. Elle renvoie un dictionnaire :

- `frequencies_hz` : fréquences effectivement explorées ;
- `amplitudes` : \(G(f_i)\) ;
- `energies` : valeurs de \(J(f_i,\chi)\) ;
- `solutions` : dictionnaire `frequence -> champ complexe` ;
- `band_energy` : intégrale numérique de la courbe d'énergie sur la bande.

`postprocessing.plot_rer_b_frequency_sweep(results)` enregistre les courbes du spectre et de l'énergie. Le programme principal ne doit que configurer puis appeler ces fonctions.

## 10. Tests et garde-fous attendus de l'agent

1. Vérifier que l'amplitude \(G(f)\) est finie et non négative sur la bande considérée et qu'aucune fréquence fournie n'est invalide.
2. Vérifier la présence d'une frontière supérieure Dirichlet et le respect de sa convention `f_dir/alpha_dir`, sans modifier les fonctions fournies.
3. Vérifier qu'une campagne n'altère pas les tableaux du cas initial par effet de bord, notamment `f_dir`, `domain_omega` et `chi`.
4. Vérifier le nombre minimal de points par longueur d'onde à la fréquence maximale et la représentation effective des plus petits reliefs.
5. Garder **exactement la même source, les mêmes fréquences et la même quantité absolue de matériau poreux** pour comparer différents profils ; fixer également la zone d'observation de l'énergie lorsque c'est nécessaire pour une comparaison physique juste.
6. Ne jamais multiplier deux fois par l'enveloppe spectrale lorsque cette enveloppe a déjà été appliquée à Dirichlet.
7. Distinguer explicitement **source hypothétique**, **spectre mesuré éventuel**, **hypothèses géométriques** et **paramètres physiques à valider**.
8. Ne pas présenter l'étude comme une simulation temporelle de rame mobile ; la validation de robustesse à une incidence oblique pourra être ajoutée après le MVP.
9. Mettre à jour \(\alpha(f)\) si et seulement si une loi de matériau fiable a été définie, au lieu de la supposer connue.

## 11. Décisions finales / éléments ouverts

| Sujet | Position retenue |
|---|---|
| Type de problème | Helmholtz harmonique, une fréquence par résolution |
| Lieu de la source | Bord **supérieur** Dirichlet |
| Répartition spatiale | **Uniforme** pour le MVP ; même amplitude **et phase** sur le bord |
| Répartition fréquentielle | Somme de trois gaussiennes : traction, roulement, crissement |
| Calibration du spectre | **Non effectuée** ; coefficients illustratifs à valider |
| Mouvement de la rame | Non simulé ; excitation équivalente stationnaire |
| Côtés | Neumann homogène, tunnel idéalement réfléchissant |
| Paroi étudiée | Robin complexe et répartition de poreux \(\chi\) |
| Quantité de poreux | Longueur physique absorbante fixée et commune entre profils |
| Objectif | Réduction de l'énergie numérique intégrée sur la bande |
| Bande actuellement simulée | 100–1 000 Hz ; **pas** la totalité des 100–4 000 Hz du document d'orientation |
| Validation avec Mathis | Dimensions, plages étudiées, données spectrales, loi de matériau, quantité de poreux |
| Étape ultérieure possible | Incidence oblique, source non uniforme, données mesurées, source mobile |

**Consigne générale pour l'agent :** implémenter le modèle simple et reproductible validé pour le MVP, en respectant les interfaces existantes et en ne transformant pas les hypothèses de démonstration en affirmations de fidélité expérimentale au RER B.
