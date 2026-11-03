"""On exécute les études successives et on enregistre leurs figures et leurs données."""

from time import perf_counter

import jour1_etude_theorique_et_materiaux as j1
import jour2_spectre_et_optimisation_mono as j2
import jour3_multifrequence_et_volume as j3
import jour4_analyse_performances_et_produit as j4


def main():
    """On lance les quatre journées avec les paramètres de chaque étude."""
    start = perf_counter()
    print("ResoniCS — études numériques pour le bruit du RER B")
    print("Jour 1 : matériaux, conditions de bord et vérification du gradient")
    if j1.study_porous_materials() is None:
        return
    if j1.study_sommerfeld_open_air_vs_reflexive() is None:
        return
    if j1.validate_adjoint_gradient() is None:
        return
    print("Jour 2 : spectres, géométries et optimisation à une fréquence")
    if j2.run_day2_studies() is None:
        return
    print("Jour 3 : optimisation à plusieurs fréquences et quantité de matériau")
    if j3.run_day3_studies() is None:
        return
    print("Jour 4 : répartition binaire, profils incidents et matériaux candidats")
    if j4.run_day4_studies() is None:
        return
    print("Calculs terminés en", round(perf_counter() - start, 1), "secondes")


if __name__ == "__main__":
    main()
