# Étude de l’échantillonnage fréquentiel

Ces calculs utilisent N=128, le niveau géométrique deux, la source RER B et l’ouate polyester. Le mur initial contient 204 points garnis sur 512 points de Robin, avec la même quantité pour les comparaisons.

La référence à trois pics de cette étude exploratoire a effectué 30 itérations. Elle est distincte de l’exécution principale `OUATE_POLYESTER_N128_20iterations`, qui utilise 20 itérations aux trois pics puis 20 sur la bande.

Les données comprennent les évaluations sur des grilles régulières de 50, 25, 12,5 et 6,25 Hz, puis des raffinements locaux autour des pics observés. Chaque point du NPZ correspond à un calcul. Les doublons à moins de dix nanohertz ont été regroupés en conservant une valeur calculée.

Le pic initial dominant observé est situé vers 403,6101 Hz et sa largeur à mi-hauteur est d’environ 0,271 Hz. La comparaison de grilles montre pourquoi un pas universel de 10 ou 20 Hz ne suffit pas dans ce cas. Les derniers raffinements stabilisent les pics dominants observés, sans certifier la détection de toute autre résonance.

La figure illustre uniquement des échantillons réellement présents dans le NPZ. Elle se régénère avec `postprocessing.plot_frequency_sampling_analysis`, à partir du dictionnaire des tableaux et du résumé JSON placé dans sa clé `summary`.

La résolution spatiale représente environ 12,54 pas par longueur d’onde à 3 500 Hz. Les résultats restent ceux de ce maillage.
