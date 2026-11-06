# Calculs en cours avec la version d’Antoine

Le seul répertoire de travail actif est context/EI_Antoine. Les anciens calculs de support ne sont pas utilisés comme données d’entrée.

Bande retenue après la dernière consigne : 50 à 2 000 Hz. Maillage de 128 points en largeur pour la fractale de niveau trois. Quatre matériaux et quatre méthodes de descente au niveau trois, au plus cent étapes acceptées. Les références et quantités couvrent les quatre niveaux. La comparaison principale est la bande au pas de cinq hertz. Les autres méthodes sont une fréquence, les pics détectés et la bande au pas de cinquante hertz. Un contrôle au pas de deux virgule cinq hertz complète les spectres binaires.

Les six fichiers originaux ont été conservés dans le commit 52f670b avant correction. Les changements sont expliqués dans README.md. Les contrôles du solveur, du gradient, de la descente, du volume et de la reprise passent. Les rapports sont dans resultats/verification.

Le programme parallèle est /tmp/run_antoine_studies.py, le journal est /tmp/antoine_studies.log. Il appelle le vrai programme de ce dossier avec quatre processus indépendants. Il écrit ANTOINE_STUDIES_DONE à la fin. Ne pas lancer une deuxième copie des calculs. Les fichiers reprise par matériau permettent de continuer une descente interrompue. Les paramètres et empreintes des programmes sont enregistrés avant chaque étude.

Après les calculs : vérifier les NPZ, volumes, historiques, binarisation et contrôles fréquentiels ; relire toutes les nouvelles figures ; actualiser dans la présentation les paramètres passés à deux mille hertz ; compiler ; conserver les autres blocs et le rapport ; commits et push des deux branches. Les figures sont dans resultats et copiées à plat dans presentation par le programme de tracé.
