# -*- coding: utf-8 -*-
"""On compare les placements sur le spectre et différentes quantités de matériau."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import _env
import preprocessing
from demo_control_polycopie2024 import SOURCE, CAR_MAT, C
from fast_helmholtz import (FastHelmholtzSolver, project_chi, binarize_chi,
                            optimize_single_frequency, optimize_multi_frequency)
from jour2_spectre_et_optimisation_mono import (compute_material_coefficients,
                                               evaluate_spectrum, select_peak_indices)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour3")


def run_day3_studies(N=128, frequencies=None, iterations=80, V_obj=0.30, quantities=None):
    """On réalise les trois études du troisième jour avec les paramètres communs."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    freqs = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    volumes = np.asarray([.10, .30, .50, .70, 1.0] if quantities is None else quantities, dtype=float)
    if len(freqs) == 0 or len(volumes) == 0 or N < 16 or N % 16 != 0:
        print("Il faut au moins une fréquence, une quantité et une largeur multiple de seize.")
        return None
    if np.any(volumes <= 0) or np.any(volumes > 1):
        print("Les fractions de mur garni doivent être strictement positives et au plus égales à un.")
        return None
    M, spacestep = 2 * N, 1.0 / N
    k_vals = 2.0 * np.pi * freqs / C
    Alphas = compute_material_coefficients(freqs)
    if Alphas is None:
        return None
    if C / (np.max(freqs) * spacestep) < 10:
        print("Attention, le maillage comporte moins de dix points par longueur d'onde au maximum de fréquence.")

    # Jour 3, première tâche. On observe chaque placement sur toute la bande.
    print("Jour 3 : spectres des placements à une fréquence.")
    studies = {}
    for level in (0, 1, 2):
        domain, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
        solver = FastHelmholtzSolver(domain, spacestep)
        raw = preprocessing._set_chi(M, N, x, y)
        chi0 = project_chi(raw, domain, V_obj)
        full_wall = (domain == _env.NODE_ROBIN).astype(float)
        full = evaluate_spectrum(solver, domain, full_wall, k_vals, Alphas)
        initial = evaluate_spectrum(solver, domain, chi0, k_vals, Alphas)
        targets = select_peak_indices(freqs, k_vals, initial, count=2)
        mono_spectra, mono_placements, mono_histories = [], [], []
        for index in targets:
            continuous, history, _, _ = optimize_single_frequency(
                solver, k_vals[index], Alphas[index], chi0, V_obj=V_obj,
                numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
            )
            binary = binarize_chi(continuous, domain, V_obj)
            mono_spectra.append(evaluate_spectrum(solver, domain, binary, k_vals, Alphas))
            mono_placements.append(binary)
            mono_histories.append(history)
        studies[level] = {
            "domain": domain, "solver": solver, "raw": raw, "chi0": chi0,
            "full": full, "initial": initial, "mono_targets": targets,
            "mono_spectra": mono_spectra, "mono_placements": mono_placements,
            "mono_histories": mono_histories,
        }

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, level in zip(axes, (0, 1, 2)):
        study = studies[level]
        ax.semilogy(freqs, study["initial"], "--", label=f"Densité initiale, {V_obj:.0%}")
        ax.semilogy(freqs, study["full"], color="black", label="Mur entièrement garni")
        for index, spectrum in zip(study["mono_targets"], study["mono_spectra"]):
            line, = ax.semilogy(freqs, spectrum, label=f"Placement à {freqs[index]:.0f} Hz")
            ax.plot(freqs[index], spectrum[index], "o", color=line.get_color())
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
    fig.suptitle("Spectres des placements binaires optimisés à une seule fréquence")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_1_analyse_resultats_jour2_spectre.jpg"), dpi=160)
    plt.close(fig)

    # Jour 3, deuxième tâche. On minimise la moyenne sur plusieurs fréquences.
    print("Jour 3 : placements pour plusieurs fréquences.")
    for level in (0, 1, 2):
        study = studies[level]
        targets = select_peak_indices(freqs, k_vals, study["initial"], count=3)
        # Le champ contient déjà l'amplitude de la source à chaque fréquence.
        # On donne donc le même poids aux coûts des fréquences retenues.
        continuous, history, per_frequency = optimize_multi_frequency(
            study["solver"], k_vals[targets], Alphas[targets], study["chi0"],
            V_obj=V_obj, numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
        )
        binary = binarize_chi(continuous, study["domain"], V_obj)
        spectrum = evaluate_spectrum(study["solver"], study["domain"], binary, k_vals, Alphas)
        study.update({"multi_targets": targets, "chi_multi_cont": continuous,
                      "chi_multi": binary, "multi_history": history,
                      "multi_history_frequencies": per_frequency, "multi_spectrum": spectrum})
        print("Niveau", level, ": fréquences cibles en Hz =", freqs[targets],
              "; coût moyen continu =", history[-1],
              "; coût moyen binaire =", np.mean(spectrum[targets]))

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for level in (0, 1, 2):
        study = studies[level]
        ax = axes[0, level]
        for column, index in enumerate(study["multi_targets"]):
            ax.plot(study["multi_history_frequencies"][:, column], alpha=.65,
                    label=f"{freqs[index]:.0f} Hz")
        ax.plot(study["multi_history"], "k--", label="Moyenne continue")
        ax.plot(len(study["multi_history"]) - 1,
                np.mean(study["multi_spectrum"][study["multi_targets"]]), "kx", label="Placement binaire")
        ax.set(title=f"Niveau {level}", xlabel="Itération acceptée", ylabel="Coût acoustique")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
        ax = axes[1, level]
        ax.semilogy(freqs, study["initial"], "--", label="Densité initiale")
        for index, spectrum in zip(study["mono_targets"], study["mono_spectra"]):
            ax.semilogy(freqs, spectrum, alpha=.65, label=f"Une fréquence, {freqs[index]:.0f} Hz")
        ax.semilogy(freqs, study["multi_spectrum"], lw=2, label="Plusieurs fréquences")
        ax.semilogy(freqs, study["full"], color="black", label="Mur entièrement garni")
        ax.set(xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
    fig.suptitle("Optimisation commune à plusieurs fréquences et spectres des placements binaires")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_2_optimisation_multifrequence.jpg"), dpi=160)
    plt.close(fig)

    # Jour 3, troisième tâche. On répète le calcul pour les quantités indiquées.
    print("Jour 3 : étude de la quantité de matériau.")
    for level in (0, 1, 2):
        study = studies[level]
        solver, domain = study["solver"], study["domain"]
        # Les fréquences restent identiques pour toutes les quantités d'un mur.
        mono_index = select_peak_indices(freqs, k_vals, study["initial"], count=1)[0]
        multi_indices = study["multi_targets"]
        mono_costs, multi_costs, actual_volumes = [], [], []
        for volume in volumes:
            if volume == 1.0:
                # Le mur entièrement garni fournit directement cette extrémité.
                mono_costs.append(study["full"][mono_index])
                multi_costs.append(np.mean(study["full"][multi_indices]))
                actual_volumes.append(1.0)
                continue
            chi0 = project_chi(study["raw"], domain, volume)
            chi_mono_cont, _, _, _ = optimize_single_frequency(
                solver, k_vals[mono_index], Alphas[mono_index], chi0,
                V_obj=volume, numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
            )
            chi_mono = binarize_chi(chi_mono_cont, domain, volume)
            mono_cost = evaluate_spectrum(solver, domain, chi_mono,
                                           k_vals[[mono_index]], Alphas[[mono_index]])[0]
            chi_multi_cont, _, _ = optimize_multi_frequency(
                solver, k_vals[multi_indices], Alphas[multi_indices], chi0,
                V_obj=volume, numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
            )
            chi_multi = binarize_chi(chi_multi_cont, domain, volume)
            multi_cost = np.mean(evaluate_spectrum(solver, domain, chi_multi,
                                                    k_vals[multi_indices], Alphas[multi_indices]))
            mono_costs.append(mono_cost)
            multi_costs.append(multi_cost)
            actual_volumes.append(np.mean(chi_multi[domain == _env.NODE_ROBIN]))
        study.update({"volume_mono_index": mono_index, "volume_mono_costs": np.asarray(mono_costs),
                      "volume_multi_costs": np.asarray(multi_costs), "actual_volumes": np.asarray(actual_volumes)})
        best_mono, best_multi = np.argmin(mono_costs), np.argmin(multi_costs)
        print("Niveau", level, ": parmi les quantités testées, minimum à une fréquence =",
              volumes[best_mono], "; minimum à plusieurs fréquences =", volumes[best_multi])

    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for level in (0, 1, 2):
        study = studies[level]
        percentages = 100 * study["actual_volumes"]
        for ax, costs, full_cost, title in (
            (axes[0, level], study["volume_mono_costs"], study["full"][study["volume_mono_index"]],
             f'Une fréquence, {freqs[study["volume_mono_index"]]:.0f} Hz'),
            (axes[1, level], study["volume_multi_costs"], np.mean(study["full"][study["multi_targets"]]),
             "Plusieurs fréquences"),
        ):
            ax.plot(percentages, costs, "o-", label="Placements binaires")
            ax.axhline(full_cost, color="black", ls="--", label="Mur entièrement garni")
            best = np.argmin(costs)
            ax.plot(percentages[best], costs[best], "r*", ms=10, label="Minimum testé")
            ax.set(xlabel="Part du mur garnie (%)", ylabel="Coût acoustique")
            ax.set_title(f"Niveau {level} — {title}", fontsize=10)
            ax.grid(alpha=.3)
            ax.legend(fontsize=7)
    fig.suptitle("Coûts des placements binaires en fonction de la quantité de matériau")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_3_etude_quantite_optimale_poreux.jpg"), dpi=160)
    plt.close(fig)

    # On sauvegarde les résultats de chaque mur pour conserver la trace des comparaisons.
    data = {"freqs": freqs, "k_vals": k_vals, "Alphas": Alphas, "N": N,
            "iterations_requested": iterations,
            "sound_speed_m_s": C, "volume_fraction": V_obj, "V_list": volumes,
            "source_name": SOURCE.__name__, "material_parameters": np.asarray(CAR_MAT)}
    for level in (0, 1, 2):
        study = studies[level]
        data[f"E_init_spec_l{level}"] = study["initial"]
        data[f"E_full_spec_l{level}"] = study["full"]
        data[f"E_multi_spec_l{level}"] = study["multi_spectrum"]
        data[f"chi_multi_l{level}"] = study["chi_multi"]
        data[f"chi_multi_cont_l{level}"] = study["chi_multi_cont"]
        data[f"multi_frequencies_l{level}"] = freqs[study["multi_targets"]]
        data[f"multi_history_l{level}"] = study["multi_history"]
        data[f"multi_history_frequencies_l{level}"] = study["multi_history_frequencies"]
        data[f"J_vol_l{level}"] = study["volume_mono_costs"]
        data[f"J_multi_vol_l{level}"] = study["volume_multi_costs"]
        data[f"actual_volumes_l{level}"] = study["actual_volumes"]
        data[f"volume_mono_frequency_l{level}"] = freqs[study["volume_mono_index"]]
        for number, (target, spectrum, placement) in enumerate(zip(study["mono_targets"], study["mono_spectra"], study["mono_placements"]), start=1):
            data[f"mono_frequency_l{level}_peak{number}"] = freqs[target]
            data[f"E_mono_spec_l{level}_peak{number}"] = spectrum
            data[f"chi_mono_l{level}_peak{number}"] = placement
    np.savez(os.path.join(OUTPUT_DIR, "data_jour3.npz"), **data)
    return {"frequencies": freqs, "volumes": volumes, "studies": studies}


if __name__ == "__main__":
    run_day3_studies()
