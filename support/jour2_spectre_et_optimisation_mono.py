# -*- coding: utf-8 -*-
"""On étudie le spectre, la forme du mur et les placements à une fréquence."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import _env
import preprocessing
from compute_alpha import compute_alpha
from demo_control_polycopie2024 import SOURCE, CAR_MAT, ALPHA0, C
from fast_helmholtz import (FastHelmholtzSolver, project_chi, binarize_chi,
                            optimize_single_frequency)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour2")


def find_local_maxima(freqs, k_vals, energies, min_prominence_ratio=0.01):
    """On renvoie les pics dont la hauteur dépasse le seuil relatif indiqué."""
    freqs, k_vals, energies = map(np.asarray, (freqs, k_vals, energies))
    indices = []
    energy_range = np.max(energies) - np.min(energies)
    for i in range(1, len(energies) - 1):
        if energies[i] > energies[i - 1] and energies[i] >= energies[i + 1]:
            left = np.min(energies[max(0, i - 6):i + 1])
            right = np.min(energies[i:min(len(energies), i + 7)])
            prominence = energies[i] - max(left, right)
            if prominence >= min_prominence_ratio * energy_range:
                indices.append(i)
    indices = np.asarray(indices, dtype=int)
    return indices, freqs[indices], k_vals[indices], energies[indices]


def compute_material_coefficients(frequencies, car_mat=CAR_MAT):
    """On calcule le coefficient complexe du matériau à chaque fréquence."""
    alphas = []
    for frequency in frequencies:
        # On transmet la pulsation temporelle à la fonction de Joachim.
        pair, success, message = compute_alpha(2.0 * np.pi * frequency,
                                               SOURCE, car_mat, ALPHA0)
        alpha = complex(pair[0], pair[1])
        if not success or not np.isfinite(alpha) or alpha.real <= 0 or alpha.imag >= 0:
            print("Coefficient non validé à", frequency, "Hz pour", car_mat, ":", message)
            return None
        # On conserve directement le signe de la condition de Robin du polycopié.
        alphas.append(alpha)
    return np.asarray(alphas, dtype=np.complex128)


def evaluate_spectrum(solver, domain, chi, k_vals, Alphas):
    """On calcule les coûts avec la source choisie à chaque fréquence."""
    energies = []
    chi_wall = np.where(domain == _env.NODE_ROBIN, chi, 0.0)
    for wavenumber, alpha in zip(k_vals, Alphas):
        solver.set_source(SOURCE, wavenumber * C)
        u = solver.solve(wavenumber, alpha * chi_wall)
        energies.append(solver.compute_energy(u))
    return np.asarray(energies)


def select_peak_indices(freqs, k_vals, energies, count=2):
    """On retient les pics les plus élevés puis les maxima échantillonnés au besoin."""
    energies = np.asarray(energies)
    peaks = find_local_maxima(freqs, k_vals, energies)[0]
    ranked_peaks = peaks[np.argsort(energies[peaks])[::-1]]
    indices = list(ranked_peaks[:count])
    # Une grille de fréquences courte peut ne contenir aucun maximum intérieur.
    for candidate in np.argsort(energies)[::-1]:
        if len(indices) >= min(count, len(energies)):
            break
        if candidate not in indices:
            indices.append(int(candidate))
    return np.asarray(sorted(indices, key=lambda i: freqs[i]), dtype=int)


def run_day2_studies(N=128, frequencies=None, iterations=80, V_obj=0.30):
    """On réalise les quatre études du deuxième jour avec les paramètres communs."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    freqs = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    if len(freqs) == 0 or N < 16 or N % 16 != 0:
        print("Il faut au moins une fréquence et une largeur multiple de seize pour les deux premiers niveaux.")
        return None
    M, spacestep = 2 * N, 1.0 / N
    k_vals = 2.0 * np.pi * freqs / C
    Alphas = compute_material_coefficients(freqs)
    if Alphas is None:
        return None
    if C / (np.max(freqs) * spacestep) < 10:
        print("Attention, le maillage comporte moins de dix points par longueur d'onde au maximum de fréquence.")

    # Jour 2, première et deuxième tâches. On compare les murs entièrement garnis.
    print("Jour 2 : spectres des murs entièrement garnis.")
    levels = [0, 1, 2, 3] if N % 64 == 0 else [0, 1, 2]
    if 3 not in levels:
        print("Le niveau trois est écarté de ce calcul réduit car son motif demande une largeur multiple de soixante-quatre.")
    domains, solvers, coordinates, full, maxima = {}, {}, {}, {}, {}
    for level in levels:
        domain, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
        solver = FastHelmholtzSolver(domain, spacestep)
        domains[level], solvers[level], coordinates[level] = domain, solver, (x, y)
        full[level] = evaluate_spectrum(solver, domain, (domain == _env.NODE_ROBIN).astype(float), k_vals, Alphas)
        maxima[level] = find_local_maxima(freqs, k_vals, full[level])
        print("Niveau", level, ": coût moyen =", np.mean(full[level]), "; pics en Hz =", maxima[level][1])

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(freqs, full[0], label="Mur plan entièrement garni")
    ax.plot(maxima[0][1], maxima[0][3], "ro", label="Maxima locaux échantillonnés")
    ax.set(xlabel="Fréquence (Hz)", ylabel="Coût acoustique", title="Spectre du mur plan")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_1_mur_plan_absorbant_maxima.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for level in levels:
        axes[0].plot(freqs, full[level], label=f"Niveau {level}")
        axes[1].semilogy(freqs, full[level], label=f"Niveau {level}")
        for ax in axes:
            ax.plot(maxima[level][1], maxima[level][3], ".")
    for ax in axes:
        ax.set(xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend()
    axes[0].set_title("Échelle linéaire")
    axes[1].set_title("Échelle logarithmique")
    fig.suptitle("Spectres des différentes formes de murs entièrement garnis")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_2_comparaison_formes_fractales.jpg"), dpi=160)
    plt.close(fig)

    # Jour 2, troisième tâche. On fixe la quantité de matériau pour chaque mur.
    print("Jour 2 : répartition initiale et mur entièrement garni.")
    initial, chi_initial = {}, {}
    for level in (0, 1, 2):
        x, y = coordinates[level]
        raw = preprocessing._set_chi(M, N, x, y)
        chi_initial[level] = project_chi(raw, domains[level], V_obj)
        initial[level] = evaluate_spectrum(solvers[level], domains[level], chi_initial[level], k_vals, Alphas)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, level in zip(axes, (0, 1, 2)):
        ax.semilogy(freqs, initial[level], "--", label=f"Densité initiale, {V_obj:.0%}")
        ax.semilogy(freqs, full[level], label="Mur entièrement garni")
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_3_initial_partiel_vs_total.jpg"), dpi=160)
    plt.close(fig)

    # Jour 2, quatrième tâche. On optimise séparément deux fréquences critiques.
    print("Jour 2 : placements à une fréquence.")
    results = {}
    for level in (0, 1, 2):
        results[level] = []
        solver, domain = solvers[level], domains[level]
        indices = select_peak_indices(freqs, k_vals, initial[level], count=2)
        for index in indices:
            solver.set_source(SOURCE, 2.0 * np.pi * freqs[index])
            u0 = solver.solve(k_vals[index], Alphas[index] * chi_initial[level])
            continuous, history, _, _ = optimize_single_frequency(
                solver, k_vals[index], Alphas[index], chi_initial[level],
                V_obj=V_obj, numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
            )
            # On mesure aussi le placement constitué uniquement de points garnis ou nus.
            binary = binarize_chi(continuous, domain, V_obj)
            u_binary = solver.solve(k_vals[index], Alphas[index] * binary)
            cost_binary = solver.compute_energy(u_binary)
            results[level].append({
                "f_target": freqs[index], "k_target": k_vals[index], "idx_peak": index,
                "J0_proj": solver.compute_energy(u0), "J_relaxed": history[-1],
                "J_opt": cost_binary, "J_full": full[level][index],
                "chi0": chi_initial[level], "chi_cont": continuous, "chi_opt": binary,
                "u0": u0, "u_opt": u_binary, "ene_hist": history,
            })
            print("Niveau", level, "à", freqs[index], "Hz : initial =", initial[level][index],
                  "; continu =", history[-1], "; binaire =", cost_binary, "; entièrement garni =", full[level][index])

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for level in (0, 1, 2):
        ax = axes[0, level]
        for result in results[level]:
            line, = ax.plot(result["ene_hist"], label=f'{result["f_target"]:.0f} Hz, continu')
            ax.plot(len(result["ene_hist"]) - 1, result["J_opt"], "x", color=line.get_color(),
                    label=f'{result["f_target"]:.0f} Hz, binaire')
        ax.set(title=f"Niveau {level}", xlabel="Itération acceptée", ylabel="Coût acoustique")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    # On compare les deux champs avec la même échelle de couleurs.
    result, domain = results[2][0], domains[2]
    extent = [-spacestep / 2, (N - .5) * spacestep, (M - .5) * spacestep, -spacestep / 2]
    vmax = max(np.max(np.abs(result["u0"])), np.max(np.abs(result["u_opt"])))
    ymax = (np.max(np.where(domain == _env.NODE_ROBIN)[0]) + 2) * spacestep
    for ax, field, title in zip(axes[1, :2], (result["u0"], result["u_opt"]), ("Champ initial", "Champ après placement binaire")):
        image = ax.imshow(np.ma.masked_where(domain != _env.NODE_INTERIOR, np.abs(field)),
                          extent=extent, origin="upper", vmin=0, vmax=vmax, cmap="magma")
        ax.set(title=title, xlabel="Position horizontale (m)", ylabel="Distance à la source (m)", ylim=(ymax, 0))
        fig.colorbar(image, ax=ax, label="Module du champ")
    rows, cols = np.where(domain == _env.NODE_ROBIN)
    scatter = axes[1, 2].scatter(cols * spacestep, rows * spacestep,
                                 c=result["chi_opt"][rows, cols], cmap="viridis", vmin=0, vmax=1, s=12)
    axes[1, 2].set(title=f'Placement, niveau 2, {result["f_target"]:.0f} Hz',
                   xlabel="Position horizontale (m)", ylabel="Distance à la source (m)")
    axes[1, 2].invert_yaxis()
    axes[1, 2].set_aspect("equal")
    fig.colorbar(scatter, ax=axes[1, 2], label="Point garni ou nu")
    fig.suptitle("Optimisations à une fréquence et coût après passage au placement binaire")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_4_optimisation_mono_frequence.jpg"), dpi=160)
    plt.close(fig)

    # On enregistre les valeurs réellement calculées et les paramètres associés.
    data = {"freqs": freqs, "k_vals": k_vals, "Alphas": Alphas, "N": N,
            "iterations_requested": iterations,
            "sound_speed_m_s": C, "volume_fraction": V_obj,
            "source_name": SOURCE.__name__, "material_parameters": np.asarray(CAR_MAT)}
    for level in levels:
        data[f"energies_full_l{level}"] = full[level]
    for level in (0, 1, 2):
        data[f"energies_initial_l{level}"] = initial[level]
        data[f"chi0_l{level}"] = chi_initial[level]
        for number, result in enumerate(results[level], start=1):
            data[f"chi_opt_l{level}_peak{number}"] = result["chi_opt"]
            data[f"chi_cont_l{level}_peak{number}"] = result["chi_cont"]
            data[f"f_target_l{level}_peak{number}"] = result["f_target"]
            data[f"history_l{level}_peak{number}"] = result["ene_hist"]
            data[f"cost_binary_l{level}_peak{number}"] = result["J_opt"]
    np.savez(os.path.join(OUTPUT_DIR, "data_jour2.npz"), **data)
    return {"frequencies": freqs, "full": full, "initial": initial, "optimizations": results}


if __name__ == "__main__":
    run_day2_studies()
