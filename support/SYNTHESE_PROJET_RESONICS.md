# Code utilisé et rapport de la soutenance

Les six fichiers Python de ce dossier reprennent la version actuellement présente dans
context/EI_Antoine/. Les algorithmes sont conservés. Seuls les chemins de sortie et
l'indication du dossier source ont été adaptés à l'installation dans support/.

Python 3, NumPy, SciPy et Matplotlib sont nécessaires. Depuis la racine :

~~~sh
python support/demo_control_polycopie2024.py
~~~

Ce lancement peut être long. Il utilise les paramètres présents en tête du programme :
quatre matériaux, niveaux zéro à trois pour les références, descente au niveau trois,
bande 50–2 000 Hz au pas de 5 Hz et au plus cent itérations.
Les nouveaux calculs vont dans support/resultats_antoine/.
Les données conservées dans support/resultats/ proviennent de l'ancienne version.

Le rapport et les figures de la soutenance sont dans report/ et context/SlidesVF/.
L'exécution actuelle ne reproduit pas automatiquement toutes les figures historiques :
elle ne lance notamment pas l'étude de quantité optimisée au niveau deux avec 20 % de
matériau, ni la sélection des cinq plus grands maxima. Le rapport reprend les résultats
présentés et ne prétend pas les avoir recalculés.

L'ancien rapport, les anciens programmes et leurs données sont conservés localement dans
context/archives/avant_rapport_SlidesVF_2026-11-15/, dossier ignoré par Git.

Pour compiler le rapport :

~~~sh
latexmk -cd -pdf -outdir=build report/report.tex
~~~
