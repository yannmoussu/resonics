"""On compare les matériaux et on vérifie le modèle et son gradient."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import _env
import compute_alpha
import fast_helmholtz
import preprocessing
from demo_control_polycopie2024 import SOURCE, CAR_MAT, C, OMEGA
from jour2_spectre_et_optimisation_mono import compute_material_coefficients


OUTPUT_DIR = Path(__file__).resolve().parent / "resultats_jour1"


def study_porous_materials(frequencies=None):
    """On compare les coefficients de Robin de trois matériaux disponibles."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    frequencies = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    materials = ("LAINE_ROCHE", "MELAMINE", "LAINE_VERRE")
    results = {}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    # On utilise les caractéristiques du dictionnaire et la même source pour les trois matériaux.
    for name in materials:
        alphas = compute_material_coefficients(frequencies, compute_alpha.MATERIAUX[name])
        if alphas is None:
            plt.close(fig)
            return None
        results[name] = alphas
        axes[0].plot(frequencies, alphas.real, label=name.replace("_", " ").title())
        axes[1].plot(frequencies, alphas.imag, label=name.replace("_", " ").title())

    # On garde les parties réelle et imaginaire séparées pour lire leur signe et leur évolution.
    for ax, title in zip(axes, ("Partie réelle du coefficient de Robin", "Partie imaginaire du coefficient de Robin")):
        ax.set(xlabel="Fréquence (Hz)", ylabel="Coefficient de Robin", title=title)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig_j1_comparaison_materiaux.jpg", dpi=160)
    plt.close(fig)
    columns = [frequencies]
    names = ["frequency_hz"]
    for name in materials:
        columns.extend((results[name].real, results[name].imag))
        names.extend((name + "_alpha_real", name + "_alpha_imag"))
    np.savetxt(OUTPUT_DIR / "comparaison_materiaux.csv", np.column_stack(columns), delimiter=",", header=",".join(names), comments="")
    return {"frequencies": frequencies, "alphas": results}


def study_sommerfeld_open_air_vs_reflexive(N=128, frequencies=None):
    """On compare une paroi réfléchissante, une sortie ouverte et une paroi poreuse."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    frequencies = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    alphas = compute_material_coefficients(frequencies, CAR_MAT)
    if alphas is None:
        return None
    domain, _, _, _, _ = preprocessing._set_geometry_of_domain(2 * N, N, level=0)
    solver = fast_helmholtz.FastHelmholtzSolver(domain, 1.0 / N)
    robin = domain == _env.NODE_ROBIN
    energies = np.zeros((len(frequencies), 3))
    theory = np.zeros((len(frequencies), 2))

    for i, frequency in enumerate(frequencies):
        omega = 2.0 * np.pi * frequency
        wavenumber = omega / C
        solver.set_source(SOURCE, omega)
        # On applique le signe de Robin du polycopié à la sortie ouverte.
        for j, alpha in enumerate((0.0, -1j * wavenumber, alphas[i])):
            boundary = np.zeros(domain.shape, dtype=complex)
            boundary[robin] = alpha
            energies[i, j] = solver.compute_energy(solver.solve(wavenumber, boundary))

        # On compare aux solutions continues sur une bande rectangulaire de dimensions unitaires.
        amplitude_squared = abs(SOURCE(0.0, omega)) ** 2
        theory[i, 0] = amplitude_squared
        cosine = np.cos(wavenumber)
        theory[i, 1] = amplitude_squared * (0.5 + np.sin(2.0 * wavenumber) / (4.0 * wavenumber)) / cosine**2 if abs(cosine) > 1e-8 else np.nan

    fig, ax = plt.subplots(figsize=(9, 4.8))
    for j, label in enumerate(("Paroi réfléchissante", "Sortie ouverte discrète", "Matériau sélectionné")):
        ax.semilogy(frequencies, energies[:, j], label=label)
    ax.semilogy(frequencies, theory[:, 0], "k--", label="Sortie ouverte continue")
    ax.semilogy(frequencies, theory[:, 1], color="gray", linestyle=":", label="Paroi réfléchissante continue")
    ax.set(xlabel="Fréquence (Hz)", ylabel="Coût du champ", title="Réponse du domaine rectangulaire selon sa paroi")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig_j1_sommerfeld_vs_reflexif.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(OUTPUT_DIR / "comparaison_parois.csv", np.column_stack((frequencies, energies, theory)), delimiter=",", header="frequency_hz,J_reflecting,J_open,J_material,J_open_continuous,J_reflecting_continuous", comments="")
    return {"frequencies": frequencies, "energies": energies, "theory": theory}


def validate_adjoint_gradient(N=64, samples=12, omega=OMEGA):
    """On compare le gradient adjoint aux variations du coût après une petite perturbation."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    alphas = compute_material_coefficients([omega / (2.0 * np.pi)], CAR_MAT)
    if alphas is None:
        return None
    Alpha = alphas[0]
    domain, _, _, _, _ = preprocessing._set_geometry_of_domain(2 * N, N, level=1)
    solver = fast_helmholtz.FastHelmholtzSolver(domain, 1.0 / N)
    solver.set_source(SOURCE, omega)
    # On garde des densités éloignées des bornes pour pouvoir les perturber dans les deux sens.
    density = np.zeros(domain.shape)
    density[domain == _env.NODE_ROBIN] = 0.3
    wavenumber = omega / C
    field, adjoint = solver.solve_state_and_adjoint(wavenumber, Alpha * density)
    gradient = solver.compute_gradient(field, adjoint, density, Alpha)
    nodes = np.argwhere(domain == _env.NODE_ROBIN)
    chosen = nodes[np.linspace(0, len(nodes) - 1, min(samples, len(nodes)), dtype=int)]
    epsilon = 1e-6
    finite_difference = []
    adjoint_values = []

    for row, col in chosen:
        # On résout le même problème avec une densité légèrement augmentée puis diminuée.
        plus = density.copy()
        minus = density.copy()
        plus[row, col] += epsilon
        minus[row, col] -= epsilon
        cost_plus = solver.compute_energy(solver.solve(wavenumber, Alpha * plus))
        cost_minus = solver.compute_energy(solver.solve(wavenumber, Alpha * minus))
        finite_difference.append((cost_plus - cost_minus) / (2.0 * epsilon))
        adjoint_values.append(gradient[row, col])

    finite_difference = np.asarray(finite_difference)
    adjoint_values = np.asarray(adjoint_values)
    error = np.linalg.norm(adjoint_values - finite_difference) / max(np.linalg.norm(finite_difference), 1e-14)
    print("Erreur relative du gradient adjoint :", error)

    # On fait ensuite varier la perturbation au point où la dérivée est la plus grande.
    row, col = chosen[np.argmax(np.abs(adjoint_values))]
    steps = np.logspace(-8, -2, 13)
    errors = []
    for step in steps:
        plus = density.copy()
        minus = density.copy()
        plus[row, col] += step
        minus[row, col] -= step
        derivative = (solver.compute_energy(solver.solve(wavenumber, Alpha * plus)) - solver.compute_energy(solver.solve(wavenumber, Alpha * minus))) / (2.0 * step)
        errors.append(abs(derivative - gradient[row, col]) / max(abs(gradient[row, col]), 1e-14))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(adjoint_values, "o-", label="Adjoint")
    axes[0].plot(finite_difference, "x--", label="Différences finies")
    axes[0].set(xlabel="Point du bord testé", ylabel="Dérivée du coût", title="Comparaison des dérivées")
    axes[0].legend()
    axes[1].loglog(steps, np.maximum(errors, 1e-16), "o-")
    axes[1].set(xlabel="Perturbation de la densité", ylabel="Erreur relative", title="Influence de la perturbation")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig_j1_validation_gradient_adjoint.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(OUTPUT_DIR / "validation_gradient.csv", np.column_stack((chosen, adjoint_values, finite_difference)), delimiter=",", header="row,col,adjoint_derivative,finite_difference_derivative", comments="")
    return {"relative_error": float(error), "adjoint": adjoint_values, "finite_difference": finite_difference}


if __name__ == "__main__":
    study_porous_materials()
    study_sommerfeld_open_air_vs_reflexive()
    validate_adjoint_gradient()
