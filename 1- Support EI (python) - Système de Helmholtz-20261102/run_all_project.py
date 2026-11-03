# -*- coding: utf-8 -*-
"""
Script principal : run_all_project.py
Exécute l'intégralité de la chaîne numérique du projet EI ST5 (Jours 1 à 4)
et génère l'ensemble des graphiques et données dans :
  - resultats_jour1/
  - resultats_jour2/
  - resultats_jour3/
  - resultats_jour4/
"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if "MPLCONFIGDIR" not in os.environ:
    os.environ["MPLCONFIGDIR"] = "/tmp/mplconfig"
    os.makedirs("/tmp/mplconfig", exist_ok=True)

import jour1_etude_theorique_et_materiaux as j1
import jour2_spectre_et_optimisation_mono as j2
import jour3_multifrequence_et_volume as j3
import jour4_analyse_performances_et_produit as j4


def main():
    t_start = time.time()
    print("======================================================================")
    print("   PROJET EI ST5 - CONTRÔLE DE LA POLLUTION ACOUSTIQUE (RESONICS)     ")
    print("======================================================================\n")

    print(">>> EXÉCUTION DU JOUR 1 (Matériaux JCA, Sommerfeld vs Réfléchissant, Validation Adjoint)...")
    j1.study_porous_materials()
    j1.study_sommerfeld_open_air_vs_reflexive()
    j1.validate_adjoint_gradient()

    print("\n>>> EXÉCUTION DU JOUR 2 (Spectres fréquentiels, Formes fractales, Optimisation Mono-Fréquence)...")
    j2.run_day2_studies()

    print("\n>>> EXÉCUTION DU JOUR 3 (Analyse large bande, Optimisation Multi-Fréquentielle, Volume optimal)...")
    j3.run_day3_studies()

    print("\n>>> EXÉCUTION DU JOUR 4 (Binarisation industrielle, Robustesse aux ondes, Choix du produit)...")
    j4.run_day4_studies()

    elapsed = time.time() - t_start
    print("\n======================================================================")
    print(f"   EXÉCUTION TERMINÉE AVEC SUCCÈS EN {elapsed:.1f} SECONDES.")
    print("======================================================================")


if __name__ == "__main__":
    main()
