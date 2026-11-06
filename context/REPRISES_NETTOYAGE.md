# Comparaison des quatre matériaux terminée

Les quatre descentes ont terminé leurs 100 itérations au niveau 3, avec le maillage de 128 points en largeur et la bande de 50 à 3 500 Hz au pas de 5 Hz. Il ne faut pas relancer 64 optimisations. Les matériaux sont MELAMINE, LAINE_ROCHE, LAINE_VERRE et OUATE_POLYESTER.

Les références et les études de quantité couvrent les niveaux 0, 1, 2 et 3. La quantité est étudiée en allongeant une portion centrale garnie, à position fixée. Les quatre murs binaires de niveau 3 conservent exactement 410 points garnis sur les 1 024 du contour.

## Résultats et contrôles

Les données, les CSV, les paramètres et les 50 PNG sont dans support/resultats. Les mêmes PNG sont copiés à plat dans presentation. Le bilan chiffré est dans support/resultats/README.md. Les historiques acceptés sont strictement décroissants et les contraintes de volume sont respectées.

La grille de contrôle au pas de 2,5 Hz révèle un pic initial à 397,5 Hz, mal mesuré au pas de 5 Hz. Pour la mélamine, elle révèle aussi un maximum final à 732,5 Hz supérieur à celui mesuré au pas de 5 Hz. Les réductions de l'énergie intégrée calculées sur la grille de contrôle vont d'environ 81 à 88 pour cent. Aucun matériau n'est choisi définitivement.

Le gradient a été contrôlé par différences finies sur petit maillage et au niveau 3 avec 128 points. Les matrices complètes ont été comparées à la version précédente du solveur. Les écarts de matrice sont nuls. Aucune classe de solveur n'a été ajoutée. Les méthodes utilisent la convention positive du polycopié.

## Présentation

La présentation de travail est presentation/presentation.tex, compilée dans presentation/presentation.pdf. La base fournie dans context/Slides_EI est préservée. Les trente-deux blocs de frames hors des cinq blocs remplacés sont conservés, à l'exception du retrait global des sous-titres demandé. Aucun schéma TikZ n'est ajouté. Les comparaisons d'optimisation occupent deux slides.

Le programme installé a été exécuté depuis le vrai dossier du projet avec les données enregistrées. Il a régénéré les figures sans recalculer les descentes. La présentation a été compilée depuis ce même dossier. Les nouvelles slides ont été vérifiées visuellement et n'ajoutent pas de débordement.

## Nettoyage et éléments préservés

Les anciennes sorties de support/resultats_antoine et les figures obsolètes du support ont été retirées. Les archives déjà supprimées par l'utilisateur n'ont pas été restaurées. Les images encore appelées par le rapport sont conservées. Le rapport, les fichiers de contexte fournis et les modifications personnelles restent inchangés.

La présentation d'origine conserve une référence eole sans entrée bibliographique, plusieurs débordements, une affirmation de régularité H2 sur le domaine irrégulier et des dimensions d'annexe différentes de la grille utilisée. Ces blocs restent à relire avec l'équipe. Ils sont hors du périmètre des modifications autorisées pour cette étape.

## Exécution

Depuis la racine : python support/demo_control_polycopie2024.py. Le guide est support/SYNTHESE_PROJET_RESONICS.md. Les paramètres sont au début du programme. Les résultats enregistrés sont réutilisés lorsque les paramètres sont identiques.

L'optimisation reste au pas de 5 Hz. Le contrôle plus fin compare deux grilles et ne garantit pas l'absence de toute résonance plus étroite. Aucune étude de convergence spatiale n'a été réalisée pour cette comparaison.
