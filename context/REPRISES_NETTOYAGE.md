# Nettoyage et vérifications terminés

- Les quatre fichiers du support utilisent les systèmes complets fournis. La classe de résolution supplémentaire et les études redondantes ont été retirées.
- Les quatre modes sont disponibles : mono, trois_pics, pics_resonance et bande. Le mode complet rassemble les comparaisons et les contrôles.
- Les anciennes données sont dans support/archives_numeriques. Les 39 figures des études retirées ont été supprimées.
- Les nouveaux calculs N128 et dix itérations par procédure sont dans support/resultats_antoine. Le bilan numérique et les paramètres y indiquent exactement les calculs effectués.
- Les gradients pondérés concordent avec les différences finies. Les étapes acceptées décroissent, les volumes continus sont conservés et les murs binaires comportent 204 points garnis sur 512.
- La validation commune porte sur 7145 fréquences. Le contrôle final d'intégrale vaut environ 0,38 %. L'écart entre les moyennes binaires de bande sur les grilles d'optimisation et de validation vaut environ 0,83 %.
- Dans cet essai, le mode aux pics repérés est meilleur après binarisation que le mode de bande. Un pic de ce dernier reste vers 452 Hz. Le bilan le précise sans généraliser cette observation.
- La présentation canonique comporte 34 diapositives dans presentation/presentation.tex et presentation/presentation.pdf. Une copie est conservée dans context/Slides_EI, avec les chemins adaptés.
- Le PDF a été compilé sans débordement ni référence indéfinie et inspecté visuellement.
- Les modifications locales du rapport et les autres documents du groupe ont été conservés. Le rapport reste à reprendre séparément, conformément à la priorité donnée aux calculs.
- La règle des dix points par longueur d'onde est satisfaite à N128. La convergence spatiale et la résolution des plus petites portions de revêtement restent distinctes de ce contrôle.
