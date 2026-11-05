# État du nettoyage et des calculs

- Branche de travail refactor, commits 5e11734 et c12fe35. Ils ont été poussés sur origin/refactor. Main attend la validation finale.
- Les quatre fichiers du support utilisent les systèmes complets fournis. La classe et les études redondantes ont été retirées. Les tests numériques conservés dans support/verification_numerique passent.
- Les 39 anciennes figures concernées ont été supprimées. Leurs données brutes sont conservées dans support/archives_numeriques.
- Le rapport et les modifications locales des documents sont préservés.

## Calcul en cours

- Programme : /tmp/run_clean_production.py, PID 54777, session exec 27119, journal /tmp/clean_production.log.
- N128, ouate polyester, niveau 2, dix itérations par descente. Les quatre descentes sont terminées. La descente de bande a utilisé 813 fréquences. Le critère continu passe de 0,4478801 à 0,3275859, puis le critère binaire vaut 0,4478668 sur cette grille.
- Résultats intermédiaires : /tmp/resonics_antoine_clean/support/resultats_antoine.
- Les études des trois matériaux et cinq quantités sont terminées. Le gradient à N128 concorde avec les différences finies à environ 5,7e-7 près en erreur relative.
- /tmp/run_parallel_validation.py a suspendu le calcul séquentiel et répartit la même validation commune entre quatre processus. PID 55439, session 97426, journal /tmp/parallel_validation.log. Les quatre processus de validation sont actifs. En cas d'échec, il reprend automatiquement le programme initial. Ne pas lancer un troisième calcul identique.

## À terminer

1. Attendre PARALLEL_VALIDATION_DONE, vérifier convergence et indicateurs réels.
2. Exécuter /tmp/finalize_clean_results.py pour réunir résultats principaux et auxiliaires et régénérer les figures.
3. Installer les deux dernières mises à jour de demo et postprocessing depuis /tmp/resonics_antoine_clean/support. Elles ajoutent les dernières présentations de figures et isolent les sorties futures par étude.
4. Copier les résultats réels, écrire leur bilan, puis compiler et inspecter la présentation de /tmp/resonics_antoine_clean/presentation/presentation.tex. Le début a déjà été compilé sans débordement avec des figures réelles. Ne pas utiliser de figures de remplacement.
5. Installer la présentation canonique dans presentation et en conserver une copie dans context/Slides_EI en adaptant les chemins relatifs. Préserver les fichiers d'entrée des autres membres.
6. Commits finaux, fetch et intégration sans écrasement sur main. Le worktree main propre est /private/tmp/resonics_main.
