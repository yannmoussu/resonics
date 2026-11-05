# Bilan numérique de l’optimisation sur la bande

Les quatre configurations sont évaluées sur la même grille, avec la même source, le même matériau et le même domaine.

| Configuration | Intégrale de l’Énergie J | Réduction relative | Maximum de l’Énergie J | Fréquence du maximum (Hz) |
| --- | ---: | ---: | ---: | ---: |
| Mur initial | 14482.976 | 0.000 % | 7493.1038 | 403.613 |
| Optimisation aux trois pics, binaire | 1922.2432 | 86.728 % | 16.280882 | 165.625 |
| Optimisation sur la bande, continue | 1067.0783 | 92.632 % | 8.8112009 | 178.516 |
| Optimisation sur la bande, binaire | 1319.6086 | 90.889 % | 7.6194 | 180.352 |

La descente sur la bande a accepté 20 étapes. L’intégrale sur sa grille passe de 1660.6592 à 1067.9052 pour la densité continue.
Après le tri binaire, l’intégrale recalculée sur cette même grille vaut 1320.0189. Ce résultat est conservé séparément de l’historique continu.

Le maximum du placement binaire optimisé sur la bande a diminué par rapport au mur initial sur la grille d’évaluation.

La réduction de l’intégrale par rapport au placement binaire à trois pics vaut 31.351 %.

La descente sur la bande part de la densité continue obtenue aux trois pics. Les deux procédures sont donc successives. Le gain observé compare cette succession à la référence aux trois pics, et ne mesure pas le seul effet du critère à budget d’itérations identique.

Les trois pics ont demandé 20 étapes acceptées, puis la bande 20 étapes, soit 40 étapes au total.

La grille d’optimisation contient 387 fréquences, avec des intervalles de 3.125 à 25 Hz. La grille d’évaluation contient 3791 fréquences, avec des intervalles de 0.0195312 à 5 Hz.

Le maillage spatial utilise N = 128 et représente 12.544 points par longueur d’onde à la fréquence maximale.

Pour « densité continue », l’écart relatif entre l’intégrale estimée pendant la descente et celle de la grille d’évaluation vaut 0.0775 %.

Pour « placement binaire », l’écart relatif entre l’intégrale estimée pendant la descente et celle de la grille d’évaluation vaut 0.03109 %.

Les fichiers sampling_history et validation_history décrivent les essais de raffinement fréquentiel. Les maxima cités sont ceux de la grille effectivement évaluée. La minimisation de l’intégrale ne garantit pas la disparition de tous les pics.
