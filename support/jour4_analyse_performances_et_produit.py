"""On évalue la répartition binaire, les profils incidents et les matériaux candidats."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import _env
import compute_alpha
import fast_helmholtz
import preprocessing
from demo_control_polycopie2024 import SOURCE, CAR_MAT, C
from jour2_spectre_et_optimisation_mono import (
    compute_material_coefficients,
    evaluate_spectrum,
    select_peak_indices,
)


OUTPUT_DIR = Path(__file__).resolve().parent / "resultats_jour4"


def mean_cost(frequencies, costs):
    """On calcule le coût moyen sur la bande de fréquences considérée."""
    if len(frequencies) == 1:
        return float(costs[0])
    return float(np.trapezoid(costs, frequencies) / (frequencies[-1] - frequencies[0]))


def run_day4_studies(N=128, frequencies=None, iterations=75):
    """On compare plusieurs répartitions puis on évalue les candidats pour le RER B."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    frequencies = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    wavenumbers = 2.0 * np.pi * frequencies / C
    M = 2 * N
    h = 1.0 / N
    V_obj = 0.30
    alphas = compute_material_coefficients(frequencies, CAR_MAT)
    if alphas is None:
        return None

    # On garde le même matériau et la même excitation que dans le programme principal.
    domain, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=2)
    solver = fast_helmholtz.FastHelmholtzSolver(domain, h)
    robin = domain == _env.NODE_ROBIN
    initial = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), domain)
    initial = fast_helmholtz.project_chi(initial, domain, V_obj)
    initial_costs = evaluate_spectrum(solver, domain, initial, wavenumbers, alphas)
    targets = select_peak_indices(frequencies, wavenumbers, initial_costs, count=3)
    target_k = wavenumbers[targets]

    # On choisit les fréquences cibles dans le spectre qui vient d'être calculé.
    continuous, history, _ = fast_helmholtz.optimize_multi_frequency(
        solver, target_k, alphas[targets], initial, V_obj=V_obj,
        numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
    )
    binary = fast_helmholtz.binarize_chi(continuous, domain, V_obj)
    full = np.zeros(domain.shape)
    full[robin] = 1.0
    continuous_costs = evaluate_spectrum(solver, domain, continuous, wavenumbers, alphas)
    binary_costs = evaluate_spectrum(solver, domain, binary, wavenumbers, alphas)
    full_costs = evaluate_spectrum(solver, domain, full, wavenumbers, alphas)

    # On teste un second matériau dans la partie basse de la paroi déjà sélectionnée.
    alternative = "MELAMINE" if not np.allclose(CAR_MAT, compute_alpha.MATERIAUX["MELAMINE"]) else "LAINE_VERRE"
    other_alphas = compute_material_coefficients(frequencies, compute_alpha.MATERIAUX[alternative])
    if other_alphas is None:
        return None
    rows, cols = np.where(robin)
    deep = rows >= N
    mixed_costs = np.zeros(len(frequencies))
    for i, wavenumber in enumerate(wavenumbers):
        boundary = alphas[i] * binary.astype(complex)
        boundary[rows[deep], cols[deep]] = other_alphas[i] * binary[rows[deep], cols[deep]]
        solver.set_source(SOURCE, wavenumber * C)
        mixed_costs[i] = solver.compute_energy(solver.solve(wavenumber, boundary))

    # On recalcule les coûts après la binarisation et après le changement de matériau.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7))
    for costs, label in (
        (initial_costs, "Répartition initiale"),
        (continuous_costs, "Répartition continue optimisée"),
        (binary_costs, "Répartition binaire"),
        (mixed_costs, "Répartition binaire mixte testée"),
        (full_costs, "Paroi entièrement garnie"),
    ):
        axes[0].semilogy(frequencies, costs, label=label)
    axes[0].set(xlabel="Fréquence (Hz)", ylabel="Coût du champ", title="Coûts des répartitions de matériau")
    axes[0].grid(alpha=0.3)
    axes[0].legend(fontsize=7)
    selected = binary[robin] > 0.5
    axes[1].scatter(cols[~selected] * h, rows[~selected] * h, c="gray", marker="s", s=9, label="Paroi non garnie")
    axes[1].scatter(cols[selected & ~deep] * h, rows[selected & ~deep] * h, c="tab:blue", s=11, label="Matériau sélectionné")
    axes[1].scatter(cols[selected & deep] * h, rows[selected & deep] * h, c="tab:orange", s=11, label=alternative.replace("_", " ").title())
    axes[1].set(xlabel="Position horizontale (m)", ylabel="Profondeur (m)", title="Répartition mixte testée")
    axes[1].invert_yaxis()
    axes[1].set_aspect("equal")
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig_j4_1_industrialisation_binaire_et_hybride.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(OUTPUT_DIR / "comparaison_repartitions.csv", np.column_stack((frequencies, initial_costs, continuous_costs, binary_costs, mixed_costs, full_costs)), delimiter=",", header="frequency_hz,J_initial,J_continuous,J_binary,J_mixed,J_full", comments="")

    # On garde la même paroi pour examiner trois profils d'excitation sur le bord supérieur.
    test_index = targets[np.argmax(initial_costs[targets])]
    test_k = wavenumbers[test_index]
    omega = test_k * C
    amplitude = SOURCE(0.0, omega)
    dirichlet = domain == _env.NODE_DIRICHLET
    uniform = np.ones(N, dtype=complex)
    localized = np.zeros(N, dtype=complex)
    localized[N // 2] = 1.0
    oblique = np.exp(1j * test_k * np.arange(N) * h * np.sin(np.deg2rad(35.0)))
    profiles = (("Profil uniforme", uniform), ("Excitation localisée", localized), ("Profil de phase oblique", oblique))
    f, _, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    fig, axes = plt.subplots(2, 3, figsize=(11, 7.5))
    source_costs = []
    for col, (name, profile) in enumerate(profiles):
        # On impose la même somme des amplitudes au carré sur le bord pour comparer les profils.
        load = np.zeros(domain.shape, dtype=complex)
        load[0, :] = profile
        norm = np.sqrt(np.mean(np.abs(load[dirichlet]) ** 2))
        load *= amplitude / norm
        solver.update_rhs(f, load, f_neu, f_rob)
        first = solver.solve(test_k, alphas[test_index] * initial)
        second = solver.solve(test_k, alphas[test_index] * binary)
        first_cost = solver.compute_energy(first)
        second_cost = solver.compute_energy(second)
        source_costs.append((name, first_cost, second_cost))
        # On utilise la même échelle de couleurs pour les deux cartes d'un profil donné.
        exterior = domain == _env.NODE_COMPLEMENTARY
        first_map = np.where(exterior, np.nan, np.abs(first))
        second_map = np.where(exterior, np.nan, np.abs(second))
        maximum = max(np.nanmax(first_map), np.nanmax(second_map), 1e-14)
        for row, (values, cost, title) in enumerate(((first_map, first_cost, "Initiale"), (second_map, second_cost, "Binaire"))):
            image = axes[row, col].imshow(values, vmin=0.0, vmax=maximum, cmap="magma", extent=(0, N * h, M * h, 0))
            axes[row, col].set(title=f"{name}\n{title}, coût = {cost:.4g}", xlabel="Position horizontale (m)")
            axes[row, col].set_ylim(1.4, 0.0)
            fig.colorbar(image, ax=axes[row, col], fraction=0.046)
        print(name, ": coût initial =", first_cost, ", coût binaire =", second_cost)
    axes[0, 0].set_ylabel("Profondeur (m)")
    axes[1, 0].set_ylabel("Profondeur (m)")
    fig.suptitle(f"Réponses à différents profils incidents à {frequencies[test_index]:g} Hz")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig_j4_2_robustesse_sources_ondes.jpg", dpi=160)
    plt.close(fig)
    with (OUTPUT_DIR / "robustesse_sources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("profile", "J_initial", "J_binary"))
        writer.writerows(source_costs)

    # On compare les niveaux et les matériaux du dictionnaire avec la fraction de couverture annoncée.
    material_names = ("LAINE_ROCHE", "MELAMINE", "LAINE_VERRE")
    material_alphas = {name: compute_material_coefficients(frequencies, compute_alpha.MATERIAUX[name]) for name in material_names}
    if any(values is None for values in material_alphas.values()):
        return None
    candidates = []
    for level in (0, 1, 2):
        candidate_domain, cx, cy, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
        candidate_solver = fast_helmholtz.FastHelmholtzSolver(candidate_domain, h)
        candidate_initial = preprocessing.set2zero(preprocessing._set_chi(M, N, cx, cy), candidate_domain)
        candidate_robin = candidate_domain == _env.NODE_ROBIN
        candidate_full = np.zeros(candidate_domain.shape)
        candidate_full[candidate_robin] = 1.0
        for name in material_names:
            candidate_alphas = material_alphas[name]
            density, _, _ = fast_helmholtz.optimize_multi_frequency(
                candidate_solver, target_k, candidate_alphas[targets], candidate_initial,
                V_obj=V_obj, numb_iter=iterations, source=SOURCE, sound_speed_m_s=C,
            )
            binary_density = fast_helmholtz.binarize_chi(density, candidate_domain, V_obj)
            costs = evaluate_spectrum(candidate_solver, candidate_domain, binary_density, wavenumbers, candidate_alphas)
            reference = evaluate_spectrum(candidate_solver, candidate_domain, candidate_full, wavenumbers, candidate_alphas)
            candidates.append({"level": level, "material": name, "target_fraction": V_obj,
                               "robin_nodes": int(candidate_robin.sum()), "covered_nodes": int(binary_density.sum()),
                               "J_band_mean": mean_cost(frequencies, costs), "J_max": float(costs.max()),
                               "J_full_band_mean": mean_cost(frequencies, reference)})
            print("Candidat", level, name, ": coût moyen =", candidates[-1]["J_band_mean"])

    with (OUTPUT_DIR / "tableau_synthese_produits.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(candidates[0]))
        writer.writeheader()
        writer.writerows(candidates)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.9))
    labels = [f"Niveau {candidate['level']}\n{candidate['material'].replace('_', ' ').title()}" for candidate in candidates]
    positions = np.arange(len(candidates))
    axes[0].bar(positions, [item["J_band_mean"] for item in candidates], label="Répartition binaire")
    axes[0].plot(positions, [item["J_full_band_mean"] for item in candidates], "o--", label="Paroi entièrement garnie")
    axes[0].set(ylabel="Coût moyen sur la bande", title="Comparaison des configurations pour le RER B")
    axes[0].legend(fontsize=8)
    axes[1].bar(positions, [item["covered_nodes"] for item in candidates], color="tab:orange")
    axes[1].set(ylabel="Nombre de points garnis", title="Quantité discrète de matériau utilisée")
    for ax in axes:
        ax.set_xticks(positions, labels, rotation=50, ha="right", fontsize=7)
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig_j4_3_tableau_de_bord_produits_resonics.jpg", dpi=160)
    plt.close(fig)
    np.savez(OUTPUT_DIR / "data_jour4.npz", frequencies=frequencies, domain=domain,
             chi_initial=initial, chi_continuous=continuous, chi_binary=binary,
             initial_costs=initial_costs, continuous_costs=continuous_costs,
             binary_costs=binary_costs, mixed_costs=mixed_costs, full_costs=full_costs,
             target_indices=targets, history=history)
    print("Les comparaisons conservent la fraction nodale, dont la quantité totale dépend du niveau.")
    return {"candidates": candidates, "history": history, "target_indices": targets,
            "continuous": continuous, "binary": binary, "source_costs": source_costs,
            "continuous_costs": continuous_costs, "binary_costs": binary_costs}


if __name__ == "__main__":
    run_day4_studies()
