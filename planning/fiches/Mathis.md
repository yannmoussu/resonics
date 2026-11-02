# Mathis — Matériaux poreux, unités et bandes de fréquences

Les repères **M1 à M5** du Gantt correspondent aux cinq journées, du lundi au vendredi.

## Livrable

Tu produis un seul fichier, `materiaux.py`. Il contient toutes les fonctions de ce lot, les paramètres des modèles réellement documentés, les fonctions de vérification et un petit exemple autonome sous `if __name__ == "__main__":`. Les bibliothèques autorisées sont NumPy, SciPy, Matplotlib et la bibliothèque standard. Ton fichier ne doit importer aucun des autres fichiers du groupe pour exécuter son exemple ou ses vérifications.

Le but est de fournir à Yann une loi complexe de matériau cohérente avec le solveur, ainsi que les informations nécessaires pour choisir les bandes route et rail. Le matériau et ses paramètres restent à identifier lundi. La constante complexe du programme de démonstration n'est pas un matériau identifié. Si le modèle ou des données manquent, tu le signales dans les résultats au lieu de leur attribuer une valeur supposée.

Le fichier doit permettre de générer une table CSV, un fichier JSON de provenance et des courbes. Il doit aussi pouvoir être utilisé comme module sans lancer automatiquement les calculs, ouvrir des fenêtres ou écrire des fichiers. Les commentaires et les docstrings sont des phrases françaises sans équations ni symboles mathématiques. Les formules peuvent figurer dans les explications ci-dessous et dans les calculs Python.

## Signatures et contrat des données

La signature publique commune à conserver est :

```python
def compute_material_response(frequencies_hz, material_parameters, air_parameters):
    ...
```

- `frequencies_hz` est un tableau réel à une dimension contenant des fréquences strictement positives et finies, en hertz. La fonction conserve leur ordre dans tous ses résultats. Un scalaire doit être converti explicitement en tableau à une entrée par l'appelant ou par une règle documentée de ta fonction.
- `air_parameters` contient la célérité en mètres par seconde et la masse volumique de l'air en kilogrammes par mètre cube. Ces valeurs sont arrêtées au cadrage commun, avec leur provenance. Elles doivent être réelles, strictement positives et finies.
- Les clés des paramètres d'air sont `c_m_s` et `rho_air_kg_m3`.
- Les clés du matériau sont `name`, `thickness_m`, `model`, `parameters`, `valid_frequency_hz` et `provenance`. Le modèle ou les tables complexes sont décrits dans `parameters`.
- `material_parameters` contient le nom du matériau ou du cas de vérification, l'épaisseur de couche en mètres, le type de modèle, tous ses paramètres avec leurs unités, sa plage de validité et sa provenance. La provenance doit préciser une référence consultable, la page ou la section utile et le montage décrit, notamment la présence éventuelle d'un fond rigide.
- Le modèle fourni dans ce même fichier doit permettre de calculer l'impédance de surface complexe aux fréquences demandées. Une fonction passée dans le dictionnaire de paramètres peut servir de callback pour une identification encore en cours ; les données et les équations réellement retenues doivent être présentes dans le fichier final.

Le dictionnaire retourné contient au minimum, sous des noms explicites et documentés :

```python
{
    "frequency_hz": ...,                    # tableau réel
    "angular_frequency_rad_s": ...,         # tableau réel
    "k_per_m": ...,                         # tableau réel
    "wavelength_m": ...,                    # tableau réel
    "surface_impedance_pa_s_per_m": ...,     # tableau complexe
    "alpha_phys_per_m": ...,                # tableau complexe
    "alpha_code_per_m": ...,                # tableau complexe
    "valid_mask": ...,                      # tableau booléen
    "valid_frequency_hz": ...,              # domaine de validité
    "material_name": ...,
    "thickness_m": ...,
    "provenance": ...,
}
```

Les noms de colonnes ci-dessus sont retenus pour la première intégration et rendent les unités visibles. La signature et les grandeurs du contrat commun restent inchangées. Les tableaux ont la même longueur que l'entrée. L'impédance est définie comme la pression divisée par la vitesse normale sortant du domaine fluide, donc entrant dans le matériau. Les coefficients de Robin sont en inverse de mètres lorsque le coefficient de la dérivée normale vaut un.

Tu peux ajouter les fonctions pures suivantes dans ce même fichier :

```python
def convert_frequencies(frequencies_hz, air_parameters):
    ...

def impedance_to_robin(frequencies_hz, impedance, air_parameters):
    ...

def plane_reflection(impedance, air_parameters):
    ...

def validate_material_response(response, tolerance=1e-10):
    ...

def export_material_response(response, output_prefix):
    ...
```

Le choix de ces auxiliaires ne change pas l'interface commune. Leurs vérifications se trouvent dans le même fichier et ne demandent ni solveur de Helmholtz ni autre module du projet.

## Étapes numérotées de réalisation

### 1. Séparer les trois grandeurs fréquentielles

Pour chaque fréquence publique en hertz, calcule la pulsation, le nombre d'onde dans l'air et la longueur d'onde :

\[
\omega=2\pi f,\qquad k=\omega/c,\qquad \lambda=c/f
\]

Le paramètre historique `omega` de `processing.solve_helmholtz` reçoit **le nombre d'onde**. Yann fait cette adaptation dans son fichier. Ton module retourne les quatre grandeurs afin qu'aucun appel ne remplace accidentellement le nombre d'onde par les hertz ou la pulsation. Ne donne jamais le même nom à une fréquence en hertz et à un nombre d'onde.

### 2. Choisir et documenter les bandes route et rail

Consulte les documents fournis pour présenter les mécanismes et les exemples, puis complète par une source d'émission adaptée à chaque application si nécessaire. La table du support Filoche donne des valeurs de matériaux à certaines fréquences ; elle ne prescrit pas la bande du projet pour les voitures ou les trains. Le graphe de trafic du même document ne donne pas à lui seul un spectre ferroviaire exploitable.

Pour chaque application, fournis une petite fiche de données : borne basse, borne haute, source documentaire, type de bruit ou conditions d'émission visées, dimensions du modèle, plage de validité du matériau et éventuelle pondération spectrale. Précise si les niveaux sont linéaires ou déjà pondérés en fréquence. Une pondération uniforme peut servir de premier protocole, mais elle doit être annoncée comme telle.

La bande finalement retenue doit rester dans le domaine de validité du matériau et être calculable avec le maillage prévu. Si une bande complète est trop coûteuse, propose un sous-domaine de démonstration clairement nommé, puis garde la bande initiale comme objectif de validation. Ne présente pas ce sous-domaine comme tout le bruit routier ou ferroviaire.

Le choix des irrégularités se confronte à la règle orale d'une dimension de l'ordre de la demi-longueur d'onde. L'énoncé impose en plus au moins dix points par longueur d'onde. Retourne à Olympia et Yann les longueurs d'onde extrêmes et les tailles de détail à examiner, sans imposer un niveau fractal avant d'avoir vérifié sa résolution.

### 3. Lever l'absence de modèle de matériau lundi

Le code fourni ne contient pas `compute_alpha`. Avant de nommer un matériau réel dans une courbe, obtiens soit un modèle de propagation dans le poreux et tous ses paramètres, soit une impédance de surface complexe documentée pour l'épaisseur et le montage considérés. Une fiche ne donnant que des coefficients d'absorption réels ne suffit pas.

En effet, dans une référence plane, le coefficient d'absorption renseigne sur le module du coefficient de réflexion, mais il ne donne pas sa phase. Plusieurs impédances complexes peuvent donc conduire au même coefficient d'absorption. Ne déduis pas arbitrairement une phase pour remplir la partie imaginaire.

Dans `materiaux.py`, sépare explicitement les données physiques documentées des cas synthétiques de vérification. Si seuls ces derniers sont disponibles lundi matin, le développement du module peut avancer, mais les courbes doivent porter cette qualification et ne doivent pas être utilisées pour annoncer un produit ou une performance acoustique.

Si tu disposes d'une table d'impédances complexes, trie les fréquences de la table et vérifie leur unicité. Interpole séparément les parties réelle et imaginaire à l'intérieur de sa plage de validité. Ne fais pas d'extrapolation silencieuse. Une table trop peu résolue près d'une variation rapide demande davantage de données. Si tu utilises plutôt un modèle analytique, écris ses équations et son domaine de validité dans la note remise au groupe, puis place son implémentation et tous ses paramètres dans ce seul fichier.

### 4. Fixer les signes avant de calculer le coefficient de Robin

Le contrat commun utilise une dépendance temporelle négative, une normale sortante et la condition physique :

\[
\partial_n u+a_{\mathrm{phys}}u=0
\]

Le support fourni représente, après élimination du bord, la condition avec le signe opposé devant le coefficient enregistré dans son tableau :

\[
\partial_n u-a_{\mathrm{code}}u=0,\qquad
a_{\mathrm{code}}=-a_{\mathrm{phys}}
\]

Avec l'impédance de surface définie dans le contrat commun, applique :

\[
a_{\mathrm{code}}=\frac{i\omega\rho_{\mathrm{air}}}{Z_s},\qquad
a_{\mathrm{phys}}=-\frac{i\omega\rho_{\mathrm{air}}}{Z_s}
\]

Le cas de Sommerfeld correspond ainsi au coefficient de code imaginaire positif égal au nombre d'onde multiplié par l'unité imaginaire. La page 6 du support Filoche emploie une autre convention temporelle dans son écriture : la formule doit être convertie, jamais recopiée sans ce contrôle.

Ne multiplie pas à nouveau ce coefficient par l'épaisseur si celle-ci a déjà servi à calculer l'impédance de la couche. La densité de conception est ensuite multipliée au coefficient de code par Yann ; ton module calcule le coefficient du matériau présent, sans optimiser cette densité.

### 5. Vérifier une référence plane et la passivité

Dans une référence à incidence normale, calcule :

\[
Z_0=\rho_{\mathrm{air}}c,\qquad
R=\frac{Z_s-Z_0}{Z_s+Z_0},\qquad
A_{\mathrm{abs}}=1-|R|^2
\]

Cette vérification est indépendante de la géométrie fractale et n'est pas le résultat d'une simulation de mur. Pour une impédance passive, sa partie réelle doit être positive ou nulle et l'absorption plane doit rester entre zéro et un, à la précision numérique près. Avec la convention retenue, la partie imaginaire du coefficient de code est également positive ou nulle pour une fréquence positive et une surface passive.

Vérifie que le cas d'impédance égale à celle de l'air donne une réflexion nulle et le coefficient de Sommerfeld attendu. Vérifie que l'impédance très grande tend vers une paroi réfléchissante et un coefficient de Robin nul. Une impédance nulle ou un dénominateur presque nul réclame un traitement explicite ; ne laisse pas des valeurs non finies se propager vers le solveur.

Ne ramène pas automatiquement à zéro une absorption négative pour masquer un défaut de signe ou de données. Enregistre le diagnostic et refuse une utilisation physique de paramètres non passifs tant que leur convention n'a pas été corrigée.

### 6. Préparer l'interface avec les campagnes

Ton résultat doit couvrir chaque fréquence demandée par Olympia, y compris les fréquences ajoutées pour vérifier les pics. Retourne les unités et la provenance avec les valeurs numériques. Si certaines fréquences sortent du modèle, renvoie un diagnostic explicite et bloque leur usage comme résultat physique.

Les campagnes utilisent le même modèle de matériau et la même épaisseur pour comparer deux géométries. Une comparaison de plusieurs matériaux doit les nommer séparément et indiquer les propriétés qui changent. Si le temps ou les données ne permettent qu'un matériau correctement identifié, privilégie cette étude complète plutôt qu'une liste de matériaux non caractérisés.

### 7. Exporter des résultats lisibles et traçables

Le CSV contient une ligne par fréquence et au moins les colonnes suivantes : nom du matériau, fréquence en hertz, pulsation, nombre d'onde, longueur d'onde, épaisseur, parties réelle et imaginaire de l'impédance, parties réelle et imaginaire de chacun des deux coefficients de Robin, coefficient d'absorption plan et indicateur de validité.

Le JSON contient les paramètres de l'air, le modèle, ses paramètres avec unités, la provenance, le domaine de validité, la convention temporelle, la définition de la normale et les résultats des contrôles. Les nombres complexes sont enregistrés par deux champs réels, jamais comme chaînes impossibles à relire de façon fiable.

Les figures utiles sont : impédance complexe en fonction de la fréquence, coefficient de Robin de code en fonction de la fréquence et absorption de la référence plane. Les deux parties d'un coefficient complexe doivent être identifiées. Les titres et légendes précisent l'épaisseur et le modèle. Une courbe d'absorption ne doit pas porter le même nom de grandeur que le coefficient complexe de Robin.

## Tests et critères d'acceptation

1. Une fréquence doublée double la pulsation et le nombre d'onde, et divise la longueur d'onde par deux lorsque la célérité est fixée.
2. Les fréquences nulles, négatives, non finies et les paramètres d'air invalides sont refusés avec un message explicite.
3. Les sorties gardent la forme et l'ordre des fréquences d'entrée. Un petit essai utilise des fréquences dans un ordre différent pour vérifier ce point.
4. Les coefficients physique et de code sont exactement opposés à la précision numérique près.
5. L'impédance adaptée, test synthétique, donne les limites de réflexion et de Robin attendues. Une très grande impédance retrouve approximativement la limite réfléchissante.
6. Les critères de passivité sont contrôlés à toutes les fréquences. Une impédance artificiellement active doit être détectée et non corrigée silencieusement.
7. Un appel hors du domaine d'une table ou d'un modèle signale le défaut ; aucune extrapolation physique n'est produite sans décision documentée.
8. Le CSV et le JSON peuvent être relus et restituent les mêmes valeurs. Les paramètres numériques possèdent leurs unités et une provenance ou portent explicitement le statut de données de vérification.

L'exemple autonome emploie une impédance synthétique choisie pour vérifier une identité connue, sans nom de matériau réel ni annonce de gain. Il affiche seulement le statut des contrôles et peut générer un petit graphe marqué comme vérification.

## Jalons de la semaine

- **Lundi matin :** arrêter les conventions avec Joachim et Yann ; rechercher le modèle de matériau absent et ses paramètres ; proposer les bandes route et rail avec leurs justifications. Avant le point quotidien, fournir l'interface exécutée sur une référence synthétique et une liste précise des données encore manquantes.
- **Lundi, point entre 14 h 30 et 17 h :** faire valider le matériau, l'épaisseur, les bandes et la signification du coefficient complexe. Présenter ce qui est déjà physique et ce qui est encore un contrôle de programme.
- **Mardi :** livrer les courbes de matériau et les contrôles de passivité ; vérifier les coefficients sur toutes les fréquences de la première campagne ; aider à interpréter les écarts entre mur plan et profils irréguliers.
- **Mercredi :** couvrir les fréquences supplémentaires de l'étude multifréquence et des pics ; comparer un autre matériau seulement si ses données sont suffisamment documentées ; participer au contrôle des quantités physiques et des unités.
- **Jeudi :** valider les paramètres du produit retenu et relire toutes les affirmations sur le matériau et l'absorption. Séparer résultats calculés, hypothèses de modèle et données expérimentales externes.
- **Vendredi matin :** geler les tables et les courbes, vérifier leurs unités et préparer ta partie de l'oral. Valider ton travail lors de la répétition de l'équipe.

## Intervention de quatre minutes à l'oral

Tu présentes le besoin physique et les bandes visées, puis tu expliques comment le matériau est transformé en une condition de Robin complexe. Tu montres une courbe de coefficient et le contrôle plan qui vérifie le signe et la passivité. Tu termines par le choix de matériau et d'épaisseur retenu, en citant ses données et ses limites. Les paramètres d'impédance ne doivent pas être présentés comme une optimisation si tu les as seulement identifiés dans une source.

## Limites à annoncer

Une impédance de surface dépend du matériau, de l'épaisseur et du montage. Un modèle local à incidence normale peut devenir une approximation lorsque le champ est très oblique ou varie fortement à petite échelle. Une absorption de référence plane ne constitue pas la performance du profil complet. Une baisse du critère de pression dans le domaine ne fournit pas à elle seule une certification de mur antibruit ou l'indice d'un essai en chambre réverbérante.

Les performances de l'ancien produit illustré dans le cours ne sont pas celles de ResoniCS. Tant que le modèle complexe manque, les calculs avec le coefficient de démonstration restent des vérifications numériques.

## Sources à lire et à citer

- `Sujet-EI-EXT-2026.md` : objectifs route/rail, quantité fixée de matériau, détermination du coefficient complexe, référence de mur entièrement absorbant et règle de discrétisation.
- M. Filoche, `Mur-antibruit-Filoche.pdf`, page 6 : modèle d'impédance effective et importance de la convention temporelle ; pages 17–24 : paroi rigide, pertes et localisation ; page 56 : coefficients d'absorption réels ; pages 57–70 : matériau et exemples de murs, protocole expérimental et spectre de trafic.
- La fiche du modèle poreux ou les données d'impédance complexes effectivement retenues : référence à obtenir et à consigner lundi avec toutes les unités et conditions de mesure. Ne pas remplacer cette source par une table d'absorption réelle seule.
- Contrat commun : distinction entre coefficient physique et coefficient transmis au support. Yann et Joachim valident la correspondance avec le code distribué.
