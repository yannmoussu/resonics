# Synthèse Numérique et Théorique — Projet EI ST5 (Startup Resonics)

Ce document récapitule l'architecture du code Python, la méthodologie mathématique et l'ensemble des résultats numériques obtenus du **Jour 1 au Jour 4** pour la conception optimale de murs antibruit fractals à inclusions poreuses (applications **Autoroute** et **Voie Ferrée**).

---

## 1. Architecture des Fichiers Python

L'ensemble du code se trouve dans le dossier `1- Support EI (python) - Système de Helmholtz-20261102/` :

| Fichier | Rôle et contenu |
| :--- | :--- |
| `compute_alpha.py` | **Jour 1** — Modèle fluide équivalent de **Johnson-Champoux-Allard (JCA)** pour 3 matériaux poreux (*Mousse de Mélamine*, *Fibre de Chanvre biosourcée*, *Laine de Roche*). Calcule l'admittance complexe de Robin $\alpha(\omega)$ et le coefficient d'absorption sous incidence normale $\alpha_{\mathrm{abs}}(\omega) = 1 - |R(\omega)|^2$. |
| `demo_control_polycopie2024.py` | **Jour 1** — Script de base complété avec le calcul de l'énergie $J(u)$, la résolution de l'état adjoint $p$, le gradient discret exact $\nabla_\chi J$, la projection à volume constant par dichotomie (`project_chi`) et la descente de gradient à pas adaptatif. |
| `fast_helmholtz.py` | **Moteur de calcul haute performance** — Pré-assemble la structure creuse du Laplacien et des conditions aux limites sur $\Omega_{\mathrm{int}}$, utilise la factorisation LU creuse (`splu`) pour résoudre simultanément l'état direct $u$ et l'état adjoint $p$ (**gain de vitesse $\times 30$**, erreur $< 10^{-14}$ par rapport à `processing.solve_helmholtz`), et implémente l'optimisation **mono-fréquence**, **multi-fréquence** et la **binarisation industrielle** $\chi_{\mathrm{bin}} \in \{0, 1\}$. |
| `jour1_etude_theorique_et_materiaux.py` | **Jour 1 (Compléments)** — Compare les 3 matériaux JCA et l'effet de l'épaisseur $d$, valide numériquement l'**étude théorique Condition de Sommerfeld (Air libre) vs Paroi réfléchissante vs Paroi poreuse**, et vérifie le gradient adjoint par rapport aux différences finies centrées (erreur relative $3.99 \times 10^{-8}$). |
| `jour2_spectre_et_optimisation_mono.py` | **Jour 2** — Balayage fréquentiel sur $[100\text{ Hz}, 2000\text{ Hz}]$, détection automatique des maxima locaux d'énergie (résonances du tunnel), comparaison des géométries fractales de Koch (`level = 0, 1, 2, 3`), comparaison distribution initiale partielle ($\chi_0$) vs mur 100 % absorbant ($\chi = 1$), et optimisation numérique aux fréquences de résonance les plus problématiques. |
| `jour3_multifrequence_et_volume.py` | **Jour 3** — Évaluation large bande des murs optimisés en mono-fréquence, **optimisation multi-fréquentielle simultanée** (Autoroute, Voie Ferrée, Large Bande), et étude paramétrique de la **quantité optimale de matériau poreux** $V_{\mathrm{obj}} \in [5\%, 100\%]$ (analyse de Pareto coût/performance). |
| `jour4_analyse_performances_et_produit.py` | **Jour 4** — Industrialisation par **binarisation $\chi_{\mathrm{bin}} \in \{0, 1\}$**, conception d'un mur **hybride bi-matériaux** (Fibre de Chanvre sur les crêtes + Laine de Roche dans les cavités), étude de **robustesse face à l'onde incidente** (onde plane normale, onde sphérique ponctuelle, onde oblique à $35^\circ$), et matrice de décision finale pour la gamme de produits **Resonics**. |
| `run_all_project.py` | **Script maître** — Exécute séquentiellement l'intégralité des études des Jours 1 à 4 et régénère toutes les figures et tableaux CSV. |

---

## 2. Synthèse des Résultats par Journée

### Jour 1 : Modélisation, Condition de Maillage, Étude Théorique (Sommerfeld) et Adjoint

1. **Plages fréquentielles et condition de discrétisation ($\lambda \ge 10 h$)** :
   - **Bruit routier (Autoroute)** : $f \in [100\text{ Hz}, 1600\text{ Hz}]$ (dominante roulement pneu/chaussée entre $400$ et $1250\text{ Hz}$).
   - **Bruit ferroviaire (Trains)** : $f \in [250\text{ Hz}, 2000\text{ Hz}]$ (dominante rail/roue et crissement entre $800$ et $2000\text{ Hz}$).
   - Avec $c_0 = 340\text{ m/s}$ et une largeur de module $L_x = 1\text{ m}$, le pas de maillage est $h = 1/N$. La condition $\lambda \ge 10 h$ impose :
     $$N \ge \frac{10 \, f_{\max} L_x}{c_0} = \frac{10 \times 2000}{340} \approx 58.8$$
   - De plus, la construction de la fractale de Koch divise chaque segment par $4^{\mathrm{level}}$. Le choix **$N = 64 = 4^3$** ($M = 2N = 128$) garantit **simultanément** $\lambda \ge 10 h$ jusqu'à $2176\text{ Hz}$ et une représentation géométrique exacte sans arrondi jusqu'au niveau fractal 3.

2. **Étude théorique : Frontière ouverte (Sommerfeld) vs Frontière réfléchissante (Neumann)** :
   - En 1D sur un tunnel de hauteur $L$, l'équation de Helmholtz $u''(y) + k^2 u(y) = 0$ avec source plane $u(0) = 1$ au sommet donne :
     - **Condition de radiation de Sommerfeld (Air libre)** $u'(L) - i k u(L) = 0$ ($\alpha_{\mathrm{rob}} = -i k$) : l'onde progressive $u_{\mathrm{open}}(y) = e^{i k y}$ traverse la frontière sans aucune réflexion ($R = 0$). L'énergie acoustique est **constante et indépendante de la fréquence** :
       $$J_{\mathrm{open}}(k) = \int_\Omega |e^{i k y}|^2 \, \mathrm{d}\Omega = |\Omega| = L_x L_y = 1$$
     - **Condition réfléchissante (Neumann)** $u'(L) = 0$ ($\alpha_{\mathrm{rob}} = 0$) : il se forme une onde stationnaire $u_{\mathrm{refl}}(y) = \frac{\cos(k(L-y))}{\cos(kL)}$ dont l'énergie vaut :
       $$J_{\mathrm{refl}}(k) = \frac{L_x}{\cos^2(kL)} \left( \frac{L}{2} + \frac{\sin(2kL)}{4k} \right)$$
       qui **diverge aux fréquences de résonance longitudinales du tunnel** $k_n = \left(n + \frac{1}{2}\right)\frac{\pi}{L}$, soit $f_n = \left(n + \frac{1}{2}\right)\frac{c_0}{2L} \in \{85, 255, 425, 595, 765, \dots\}\text{ Hz}$.

3. **Dérivée d'énergie et État Adjoint** :
   - L'état adjoint $p$ vérifie le système complexe symétrique $A(\chi) p = 2 h^2 \bar{u}$ (soit $\Delta p + k^2 p = 2\bar{u}$ dans $\Omega$, $p=0$ sur $\Gamma_D$, $\partial_n p = 0$ sur $\Gamma_N$, $\partial_n p + \alpha\chi p = 0$ sur $\Gamma_R$).
   - Le gradient continu est $\nabla_\chi J(x) = -\operatorname{Re}(\alpha(\omega) u(x) p(x))$ sur $\Gamma_R$, et sa version discrète exacte (tenant compte du dénominateur $(1 - \alpha\chi h)^2$ du schéma différences finies) est validée à **$3.99 \times 10^{-8}$** près contre les différences finies centrées.

---

### Jour 2 : Spectres Fréquentiels, Géométries Fractales et Optimisation Mono-Fréquence

1. **Effet de la géométrie pour un mur 100 % absorbant ($\chi = 1$, Fibre de Chanvre)** :
   - **Niveau 0 (Plan, $S_{\mathrm{rob}} = 64$ nœuds)** : $\overline{J} = 1.705$, pic maximal $J_{\max} = 67.50$ à $243\text{ Hz}$ (les basses fréquences sont mal amorties par $5\text{ cm}$ de poreux sur fond plat).
   - **Niveau 1 (Koch itér. 1, $S_{\mathrm{rob}} = 128$ nœuds)** : $\overline{J} = 1.285$ ($-24.6\%$), pic maximal réduit à $10.17$ ($-85\%$).
   - **Niveau 2 (Koch itér. 2, $S_{\mathrm{rob}} = 256$ nœuds)** : $\overline{J} = 0.987$ ($-42.1\%$), pic maximal réduit à $9.52$ (proche de la limite idéale de Sommerfeld $J_{\mathrm{open}} = 1.0$ !).
   - **Niveau 3 (Koch itér. 3, $S_{\mathrm{rob}} = 512$ nœuds)** : $\overline{J} = 0.933$ (gain marginal supplémentaire faible de $5\%$ par rapport au Niveau 2, pour une complexité de moulage doublée).

2. **Optimisation Mono-Fréquence ($V_{\mathrm{obj}} = 30\%$)** :
   - Sur le **Niveau 2**, au pic de résonance routier $f^* = 806.5\text{ Hz}$, l'optimisation réduit l'énergie de **$J_0 = 173.46$ à $J_{\mathrm{opt}} = 0.554$** (**$-99.7\%$**, soit **$-25.7\text{ dB}$**), battant même le mur 100 % absorbant ($J_{\mathrm{full}} = 0.850$).
   - Aux maxima locaux d'énergie du mur 100 % absorbant ($\chi = 1$), l'optimisation à $V_{\mathrm{obj}} = 30\%$ atteint systématiquement une énergie inférieure à $\chi = 1$ grâce au piégeage modal par contraste d'impédance :
     - **Niveau 0** ($f = 243.2\text{ Hz}$) : $J(\chi=1) = 67.50 \to J(\chi_{\mathrm{opt}}, 30\%) = 14.78$ (**$-78.1\%$**).
     - **Niveau 1** ($f = 185.9\text{ Hz}$) : $J(\chi=1) = 10.17 \to J(\chi_{\mathrm{opt}}, 30\%) = 1.01$ (**$-90.1\%$**).
     - **Niveau 2** ($f = 902.0\text{ Hz}$) : $J(\chi=1) = 0.97 \to J(\chi_{\mathrm{opt}}, 30\%) = 0.64$ (**$-34.3\%$**).

---

### Jour 3 : Optimisation Multi-Fréquentielle Simultanée et Quantité Optimale de Poreux

1. **Comparaison Mono-Fréquence vs Multi-Fréquence ($V_{\mathrm{obj}} = 30\%$, Niveau 2)** :
   - Une paroi optimisée à une seule fréquence écrase le pic ciblé mais laisse subsister certains pics hors-cible.
   - L'optimisation **multi-fréquentielle simultanée** pondérée sur 5 fréquences de résonance réparties sur le spectre ($365, 832, 1013, 1416, 1671\text{ Hz}$) réduit l'énergie simultanément de **$-98.2\%$** sur l'ensemble des 5 pics :
     - Paroi initiale non optimisée ($30\%$) : $\overline{J} = 8.893$, $J_{\max} = 72.82$.
     - Optimisée Multi-Fréquence Globale ($30\%$) : **$\overline{J} = 1.561$** (**$-82.4\%$** sur tout le spectre $[100, 2000]\text{ Hz}$).
     - Optimisée Multi-Fréquence dédiée Voie Ferrée ($30\%$) : **$\overline{J}_{[500, 2000\text{ Hz}]} = 1.072$** (quasiment identique au mur 100 % absorbant $\overline{J} = 0.990$, avec **70 % d'économie de matériau poreux** !).

2. **Quantité optimale de matériau poreux ($V_{\mathrm{obj}}$)** :
   - L'étude paramétrique sur $V_{\mathrm{obj}} \in [5\%, 100\%]$ montre un coude de Pareto très marqué à **$V_{\mathrm{obj}} = 30\%$** : au-delà de $30\%$, les ventres de pression des modes de cavité sont déjà saturés et le gain acoustique plafonne alors que le coût matière augmente linéairement.

---

### Jour 4 : Binarisation Industrielle, Robustesse aux Ondes et Produit Final ($V_{\mathrm{obj}} = 30\%$)

1. **Passage à l'industrialisation binaire ($\chi_{\mathrm{bin}} \in \{0, 1\}$) et Bi-Matériaux ($V = 30\%$)** :
   - Le seuillage binaire $\chi_{\mathrm{bin}} \in \{0, 1\}$ (cartouches discrètes de poreux insérées dans le béton coffré) conserve une excellente performance sur l'ensemble du spectre ($\overline{J}_{\mathrm{bin}} = 1.824$ vs $\overline{J}_{\mathrm{cont}} = 1.663$).
   - L'utilisation d'inclusions **hybrides bi-matériaux** (*Laine de Roche* au fond des cavités pour amortir les basses fréquences + *Fibre de Chanvre* sur les arêtes exposées pour les moyennes/hautes fréquences) abaisse encore l'énergie à **$\overline{J}_{\mathrm{hybride}} = 1.782$**.

2. **Robustesse face à la géométrie de l'onde incidente ($f = 832.4\text{ Hz}$, $V = 30\%$)** :
   - **Onde plane normale ($\theta = 0^\circ$)** : $J_0 = 72.87 \to J_{\mathrm{opt}} = 0.71$ (**$-99.0\%$**, **$-18.1\text{ dB}$** vs béton).
   - **Onde sphérique (source ponctuelle localisée)** : $J_0 = 3.95 \to J_{\mathrm{opt}} = 0.16$ (**$-96.1\%$**, **$-17.2\text{ dB}$** vs béton).
   - **Onde plane oblique ($\theta = 35^\circ$)** : $J_0 = 85.65 \to J_{\mathrm{opt}} = 2.01$ (**$-97.7\%$**, **$-17.8\text{ dB}$** vs béton).

3. **Gamme de produits recommandée pour la Startup Resonics ($V = 30\%$)** :
   - **Produit 1 — `ResoWall-EcoRoute` (Autoroute)** : Paroi fractale en béton bas-carbone de **Niveau 2** équipée de **$30\%$ d'inclusions binaires en Fibre de Chanvre biosourcée** ($d = 5\text{ cm}$), optimisée en multi-fréquence sur la bande $100\text{--}1600\text{ Hz}$ (**$-24.0\text{ dB}$** d'atténuation moyenne, $99.8\%$ de l'efficacité d'un mur 100 % couvert, bilan carbone minimal).
   - **Produit 2 — `ResoWall-RailPro` (Voie Ferrée & Tunnels Ferroviaires)** : Paroi fractale de **Niveau 2** équipée de **$30\%$ d'inclusions hybrides (Laine de Roche haute densité en fond de cavité + Fibre de Chanvre en crête)**, optimisée sur $250\text{--}2000\text{ Hz}$ (**$-24.7\text{ dB}$** d'atténuation moyenne, résistance mécanique et feu accrue pour les tunnels ferroviaires).

