Etat de l’art : RER B 

**1\. Contexte et typologie des sources de bruit sur le RER B:**  Le RER B concentre les scénarios acoustiques les plus sévères du transport ferroviaire périurbain (opéré par la RATP et la SNCF), avec un passage de rames (MI 79 / MI 84 et le futur matériel MI 20\) toutes les 3 à 5 minutes en heure de pointe :

* **Bruit de roulement ($250Hz\ à\ 2000Hz$) :** Source prépondérante dès que la vitesse dépasse $50km/h$. Il est généré par les rugosités combinées du rail et de la roue qui excitent mécaniquement la traverse, le ballast et le voile de la roue.  
* **Bruit de traction et d'équipements auxiliaires ($100Hz\ à\ 500Hz$) :** Bruit des moteurs électriques, hacheurs de courant, compresseurs et systèmes de ventilation/climatisation en toiture ou sous caisse, dominant lors des phases d'accélération et de freinage en gare.  
* **Bruit de crissement en courbe ($1500Hz\ à\ 4000Hz$) :** Typique des courbes serrées de la vallée de Chevreuse ou des entrées de tunnels parisiens (glissement transversal *stick-slip* roue/rail).  
* **Le cas critique des tranchées couvertes et tunnels (*Reflex Tunnels*) :** Dans les gares souterraines, tranchées semi-couvertes ou couloirs bétonnés (ex. : traversée de Massy, Antony, Bourg-la-Reine ou Gentilly), les parois en béton brut agissent comme des conditions de Neumann parfaites. L'onde acoustique subit de multiples réflexions sans dissipation, augmentant le niveau sonore de **\+6 à \+10 dB(A)** par réverbération en champ confiné.

**2\. Solutions actuelles déployées sur le réseau (SNCF Réseau / RATP) et leurs limites** Face aux normes européennes et au Plan de Prévention du Bruit dans l'Environnement (PPBE), les gestionnaires d'infrastructure utilisent trois grandes familles de solutions, qui présentent chacune des verrous technologiques majeurs :

* **Écrans acoustiques plans traditionnels (Béton lisse ou bois) :**  
  * *Principe :* Créer une zone d'ombre acoustique par diffraction au sommet du mur.  
  * *Limites :* Ces murs sont **non-absorbants** (réfléchissants). Lorsqu'ils sont placés de part et d'autre des voies du RER B ou dans un tunnel, ils créent un phénomène d'ondes stationnaires (effet de canyon) entre la caisse métallique du train et le mur, annulant jusqu'à $5dB(A)$ de leur efficacité théorique.  
* **Panneaux entièrement absorbants (Cassettes métalliques perforées \+ laine minérale ou béton de bois) :**  
  * *Principe :* Recouvrir 100 % de la paroi d'un matériau poreux (laine de roche haute densité, béton d'argile expansée).  
  * *Limites :* Coût matière et d'installation très élevé, empreinte carbone lourde, et dégradation rapide des performances en milieu ferroviaire (colmatage des pores par les poussières métalliques de freinage du RER B, humidité, gel, et fragilité face à l'effet de souffle aérodynamique des trains).  
* **Résonateurs de Helmholtz et métamatériaux acoustiques (Quart d'onde) :**  
  * *Principe :* Cavités accordées pour piéger l'énergie par interférence destructive.  
  * *Limites :* Efficacité limitée à une **bande de fréquences très étroite** (souvent centrée sur un seul pic tonal), alors que le spectre du RER B est large bande.

**3\. L'état de l'art scientifique : Géométries fractales et Optimisation Topologique** Pour dépasser le compromis « coût / durabilité / absorption large bande », la recherche académique récente (notamment les travaux issus du laboratoire PMMH / École Polytechnique / CentraleSupélec de **B. Sapoval, M. Filoche et S. Félix**) a introduit deux ruptures majeures sur lesquelles repose votre projet :

* **Le piégeage géométrique par frontières pré-fractales (courbe de Koch) :**  
  * Contrairement à un mur plan où l'onde incidente repart immédiatement après une seule interaction, une géométrie fractale (de niveau \$1, 2\\dots\$) augmente le périmètre développé dans un encombrement fixe et brise la réflexion spéculaire.  
  * Elle induit des **réflexions multiples dans les sous-cavités** et une **localisation spatiale des modes acoustiques** (*localized eigenmodes*) : l'énergie acoustique se concentre fortement dans certaines zones géométriques précises de la frontière pour une large gamme de fréquences.  
* **L'optimisation de la distribution d'inclusions poreuses ($\chi (x)$) :**  
  * Au lieu d'utiliser un mur 100 % absorbant, coûteux et fragile, l'optimisation mathématique (via l'équation de Helmholtz, l'état adjoint $p$ et la descente de gradient projetée) permet de placer une **quantité réduite et fixée de matériau poreux** (ex. : \$40\\text{ \\%}\$ de la surface) exactement là où la pression acoustique \$\\vert{}u\\vert{}^2\$ et le couplage avec l'état adjoint $Re(\alpha up)$ sont maximaux.

**4\. Positionnement de votre Startup pour le cas d'usage RER B** En conclusion de cet état de l'art pour vos slides du Jour 1 :

* **Le besoin client (RATP / Île-de-France Mobilités) :** Réduire drastiquement la réverbération dans les tranchées couvertes, tunnels et zones pavillonnaires proches du RER B sans reconstruire les ouvrages d'art et en minimisant la quantité de matériau poreux exposé aux poussières de freinage.  
* **Votre proposition de valeur :** Un panneau préfabriqué en béton bas-carbone (rigide, robuste, non-absorbant) moulé selon un profil fractal ou optimisé, dans lequel on insère uniquement aux endroits stratégiques (déterminés par votre algorithme de gradient) des cartouches amovibles de matériau poreux (laine de roche ou fibre de chanvre). On obtient ainsi des performances proches d'un mur 100 % absorbant avec une fraction de matériau divisée par deux ou trois

On trouve des écrans absorbants réels sur tout type de ligne, mais aucun n’optimise la position du matériau poreux.

**En Île-de-France**

* **Villeneuve-le-Roi (94), ligne Massy–Valenton (SNCF).** 185 m d’écrans antibruit conçus en 2012, avec un béton acoustique issu de pneus recyclés. [atelierbourlois](https://www.atelierbourlois.com/projet/ecrans-antibruit-sncf/)  
* **Gentilly, Arcueil, Cachan (94), RER B.** Pas de mur : la Région finance des études acoustiques et l’isolation des façades. [iledefrance](https://www.iledefrance.fr/tous-les-services/ma-region-pres-de-chez-moi/100991-rer-b-travaux-disolation-acoustique-gentilly-arcueil-et-cachan)  
* **Paris 14e, RER B.** C’est un problème, pas une solution : le conseil d’arrondissement demandait en 2019 des murs antibruit vitrés entre la sortie de Denfert-Rochereau et le jardin Montsouris. [paris](https://www.api-site.paris.fr/mairies/public/assets/2019%2F5%2FV14%202019%2025.pdf)

**Ailleurs en France**

* **Ligne fret Gisors–Serqueux (27, 76).** 13 écrans acoustiques pour un linéaire total de 7 686 m. [agilis](https://agilis.net/nos-realisations/ecrans-acoustiques-de-la-ligne-sncf-gisors-serqueux/)  
* **Calais (62).** Des écrans le long de la voie mère, réalisés pour SNCF Réseau en site ferroviaire exploité. [nge](https://www.nge.fr/nos-realisations/ecrans-acoustiques-ferroviaires-voie-mere-sncf-reseau/)  
* **Talence (33).** Un mur de 135 m sur 2,75 m de haut, premier écran bas carbone choisi par SNCF Réseau. Côté voie, les panneaux sont en béton de bois rainuré. [constructionbtpconstructionbtp](https://www.constructionbtp.com/batiment/article/2021/09/02/135914/talence-sncf-choisit-des-ecrans-acoustiques-bas-carbone)

**À l’étranger**

* **Ladenburg (Allemagne).** Un mur antibruit végétalisé d’environ 600 m de long et jusqu’à 6 m de haut le long d’une voie ferrée. [rau](https://rau.de/fr/references/ladenburg-insonorisation-durable-dune-zone-residentielle-et-commerciale)  
* **Réseau Deutsche Bahn.** Le MetaWindow de Phononic Vibes, premier panneau transparent et très absorbant du secteur ferroviaire, certifié avec DB. [phononic-vibes](https://phononic-vibes.com/metawindow-for-railway/)  
* **Allemagne, écran bas.** Le Quie@Rail, posé à 2,10 m de l’axe du rail et à 50 cm au-dessus du plan de roulement, en béton de granulats légers à structure ouverte. [deltabloc](https://deltabloc.com/fr/produits/phonobloc/serie-special-rail)  
* **Gospić (Croatie).** Des barrières RUCONBAR très absorbantes, mesurées in situ près de la gare. [grad](https://cetra.grad.hr/ocs/index.php/cetra7/cetra2022/paper/download/1476/1056)  
* **Suisse, à la source.** La Suisse a financé l’équipement de tout son parc de wagons de fret en semelles de frein composites. [admin](https://www.bav.admin.ch/dam/bav/fr/dokumente/richtlinien/eisenbahn/ch-tsi-noi-nntr-ed.pdf.download.pdf/CH-TSI-NOI%20NNTR%20Ed.%202024-f.pdf)

**À étudier en priorité**

1. **Villeneuve-le-Roi** : visitable depuis Paris, matériau recyclé, ligne mixte TGV et RER C.  
2. **Quie@Rail** : l’écran bas est le format le plus proche de notre domaine de calcul.  
3. **MetaWindow** : la preuve qu’une startup peut faire certifier un écran innovant par un grand réseau ferré.

**Étude de marché**

Le marché des solutions acoustiques ferroviaires est en pleine mutation, avec l'émergence de startups qui délaissent les murs 100 % absorbants au profit de métamatériaux et d'optimisations géométriques pour réduire le bruit. Des entreprises comme **Metacoustic** (issue du Mans) et **Metabsorber** (issue de l'Institut FEMTO-ST à Besançon) développent de nouveaux matériaux architecturés et des métamatériaux capables de piéger les ondes sonores de manière ciblée, se rapprochant des principes de cavités résonantes et d'optimisation topologique. Par ailleurs, des consortiums industriels tels que **Tecnalia** et **Becsa** ont récemment lancé une startup dédiée spécifiquement à l'atténuation des impacts acoustiques des infrastructures ferroviaires, tandis que des acteurs comme **STRAILwave** ou **PHONOBLOC** proposent des blocs préfabriqués (en béton ou matériaux composites) pour un déploiement rapide le long des voies.