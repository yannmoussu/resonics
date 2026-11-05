# -*- coding: utf-8 -*-
"""On compare quatre matériaux et quatre géométries de mur."""

from pathlib import Path
import json
import numpy
import _env
import preprocessing
import processing
import postprocessing
from compute_alpha import compute_alpha, MATERIAUX
from preprocessing import project_density
from processing import compute_state, compute_adjoint, compute_gradient

SOURCE = preprocessing.source_rer_b
MATERIAL_NAME = "OUATE_POLYESTER"
MATERIALS = ["MELAMINE", "LAINE_ROCHE", "LAINE_VERRE", "OUATE_POLYESTER"]
ALPHA0 = [50.0, -50.0]
C = 343.0
OMEGA = 3430.0
N_POINTS = 128
LEVEL = 3
N_ITERATIONS = 100
FREQUENCIES_HZ = numpy.arange(50.0, 3501.0, 5.0)
LEVELS = (0, 1, 2, 3)
VOLUMES = (0.10, 0.30, 0.50, 0.70, 1.0)
DENSITY_TOLERANCE = 1e-5


def your_optimization_procedure(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, mu, chi, V_obj):
    """This function return the optimized density.

    Parameter:
        cf solvehelmholtz's remarks
        Alpha: complex, it corresponds to the absorbtion coefficient;
        mu: float, it is the initial step of the gradient's descent;
        V_obj: float, it characterizes the volume constraint on the density chi.
    """

    k = 0
    (M, N) = numpy.shape(domain_omega)
    numb_iter = 100
    numb_iter = min(numb_iter, N_ITERATIONS)
    energy = numpy.zeros((numb_iter+1, 1), dtype=numpy.float64)
    prepared = processing.prepare_helmholtz_system(
        domain_omega, spacestep, f, f_neu, beta_pde, alpha_pde, beta_neu,
    )
    chi = project_density(chi, domain_omega, V_obj)
    delta = DENSITY_TOLERANCE
    while k < numb_iter and mu > 10**(-5):
        print('---- iteration number = ', k)
        print('1. computing solution of Helmholtz problem, i.e., u')
        matrix, state, u = compute_state(
            domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi, prepared=prepared,
        )
        print('2. computing solution of adjoint problem, i.e., p')
        p = compute_adjoint(domain_omega, spacestep, matrix, state)
        print('3. computing objective function, i.e., energy')
        energy[k, 0] = compute_objective_function(domain_omega, u, spacestep)
        print('4. computing parametric gradient')
        grad = compute_gradient(
            domain_omega, spacestep, Alpha, chi, beta_pde, beta_rob, f_rob, p, state,
        )
        ene = numpy.inf
        bool_a = False
        while ene >= energy[k] and mu > 10 ** -5:
            print('    a. computing gradient descent')
            descent = chi - mu * grad
            print('    b. computing projected gradient')
            candidate = project_density(descent, domain_omega, V_obj)
            print('    c. computing solution of Helmholtz problem, i.e., u')
            _, _, u = compute_state(
                domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * candidate, prepared=prepared,
            )
            print('    d. computing objective function, i.e., energy (E)')
            ene = compute_objective_function(domain_omega, u, spacestep)
            bool_a = ene < energy[k, 0]
            if bool_a:
                # The step is increased if the energy decreased
                mu = mu * 1.1
                variation = numpy.max(numpy.abs(candidate - chi))
                chi = candidate
                energy[k + 1, 0] = ene
                break
            else:
                # The step is decreased is the energy increased
                mu = mu / 2
                ene = numpy.inf
        if not bool_a:
            break
        k += 1
        if variation < delta:
            break

    if k == 0:
        _, _, u = compute_state(
            domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi, prepared=prepared,
        )
        energy[0, 0] = compute_objective_function(domain_omega, u, spacestep)
    energy = energy[:k + 1]

    # On retient les points dont la densité est la plus élevée.
    chi = preprocessing.binarize_chi(chi, domain_omega, V_obj)

    print('end. computing solution of Helmholtz problem, i.e., u')
    matrix, state, u = compute_state(
        domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi, prepared=prepared,
    )
    # On ajoute séparément l’énergie de la répartition binaire.
    ene = compute_objective_function(domain_omega, u, spacestep)
    energy = numpy.vstack((energy, [[ene]]))
    p = compute_adjoint(domain_omega, spacestep, matrix, state)
    grad = compute_gradient(
        domain_omega, spacestep, Alpha, chi, beta_pde, beta_rob, f_rob, p, state,
    )

    return chi, energy, u, grad


def your_compute_objective_function(domain_omega, u, spacestep):
    """On additionne le module au carré de la pression sur les points intérieurs."""
    return float(spacestep**2 * numpy.sum(numpy.abs(u[domain_omega == _env.NODE_INTERIOR])**2))


compute_objective_function = your_compute_objective_function


def make_problem(N=None, level=None, material_name=None, source=None):
    """On prépare le domaine, les données du support et la répartition initiale."""
    N = N_POINTS if N is None else int(N)
    M = 2 * N
    level = LEVEL if level is None else int(level)
    material_name = MATERIAL_NAME if material_name is None else material_name
    source = SOURCE if source is None else source
    spacestep = 1.0 / N
    omega = OMEGA
    wavenumber = omega / C

    # ----------------------------------------------------------------------
    # -- Do not modify this cell, these are the values that you will be assessed against.
    # ----------------------------------------------------------------------
    # --- set coefficients of the partial differential equation
    beta_pde, alpha_pde, alpha_dir, beta_neu, alpha_rob, beta_rob = preprocessing._set_coefficients_of_pde(M, N)

    # -- set right hand sides of the partial differential equation
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)

    # -- set geometry of domain
    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level)

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    coordinates = (numpy.arange(N) - (N - 1) / 2) * spacestep
    f_dir[:] = 0.0
    f_dir[0, :] = source(coordinates, omega)
    chi = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), domain_omega)
    pair, success, message = compute_alpha(omega, source, MATERIAUX[material_name], ALPHA0)
    if not success:
        print("Identification du matériau interrompue :", message)
        return None
    Alpha = complex(*pair)
    alpha_rob = Alpha * chi

    # ----------------------------------------------------------------------
    # -- Do not modify this cell, these are the values that you will be assessed against.
    # ----------------------------------------------------------------------
    # -- compute finite difference solution
    u = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
    chi0 = chi.copy()
    u0 = u.copy()

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    coefficients = {"beta_pde": beta_pde, "alpha_pde": alpha_pde,
                    "alpha_dir": alpha_dir, "beta_neu": beta_neu, "beta_rob": beta_rob}
    loads = {"f": f, "f_neu": f_neu, "f_rob": f_rob}
    prepared = processing.prepare_helmholtz_system(
        domain_omega, spacestep, f, f_neu, beta_pde, alpha_pde, beta_neu,
    )
    robin_count = int(numpy.count_nonzero(domain_omega == _env.NODE_ROBIN))
    return {"domain": domain_omega, "h": spacestep, "N": N, "level": level,
            "source": source, "material_name": material_name, "c": C,
            "coefficients": coefficients, "loads": loads, "prepared": prepared,
            "chi_initial": chi0, "u_initial": u0, "V_obj": float(chi0.sum() / robin_count),
            "alphas": {}, "source_values": {}, "spectra": {}}


def prepare_frequencies(problem, frequencies_hz):
    """On identifie chaque coefficient et on évalue chaque source une seule fois."""
    frequencies = numpy.asarray(frequencies_hz, dtype=float)
    coordinates = (numpy.arange(problem["N"]) - (problem["N"] - 1) / 2) * problem["h"]
    for frequency in frequencies:
        key = float(frequency)
        if key not in problem["alphas"]:
            pair, success, message = compute_alpha(
                2.0 * numpy.pi * key, problem["source"], MATERIAUX[problem["material_name"]], ALPHA0,
            )
            alpha = complex(*pair)
            if not success or not numpy.isfinite(alpha) or alpha.real <= 0 or alpha.imag >= 0:
                print("Coefficient non validé à", key, "Hz :", message)
                return None
            problem["alphas"][key] = alpha
            row = numpy.zeros(problem["N"], dtype=complex)
            row[:] = problem["source"](coordinates, 2.0 * numpy.pi * key)
            problem["source_values"][key] = row
    return {"frequencies_hz": frequencies,
            "wavenumbers": 2.0 * numpy.pi * frequencies / problem["c"],
            "alphas": numpy.asarray([problem["alphas"][float(f)] for f in frequencies]),
            "sources": [problem["source_values"][float(f)] for f in frequencies]}


def dirichlet_load(problem, source_values):
    """On place la source sur le bord supérieur du tableau."""
    f_dir = numpy.zeros(problem["domain"].shape, dtype=complex)
    f_dir[0, :] = source_values
    return f_dir


def evaluate_distribution(problem, chi, frequency_data, weights=None):
    """On calcule les énergies et, si les poids sont fournis, leur gradient pondéré."""
    energies = []
    gradient = numpy.zeros(problem["domain"].shape) if weights is not None else None
    for j, (wave, alpha, source_values) in enumerate(zip(
            frequency_data["wavenumbers"], frequency_data["alphas"], frequency_data["sources"])):
        matrix, state, field, factor = processing.compute_state(
            problem["domain"], problem["h"], wave,
            f_dir=dirichlet_load(problem, source_values), alpha_rob=alpha * chi,
            **problem["loads"], **problem["coefficients"], prepared=problem["prepared"], return_factor=True,
        )
        energy = your_compute_objective_function(problem["domain"], field, problem["h"])
        if not numpy.isfinite(energy):
            print("Énergie non finie pour le nombre d'onde", wave)
            return None, None
        energies.append(energy)
        if weights is not None:
            # On réutilise la factorisation pour résoudre le système adjoint.
            adjoint = compute_adjoint(problem["domain"], problem["h"], matrix, state, factor=factor)
            gradient += weights[j] * compute_gradient(
                problem["domain"], problem["h"], alpha, chi,
                problem["coefficients"]["beta_pde"], problem["coefficients"]["beta_rob"],
                problem["loads"]["f_rob"], adjoint, state,
            )
    return numpy.asarray(energies), gradient


def your_multifrequency_optimization(problem, frequencies_hz, chi=None, weights=None, mu=5.0, iterations=None):
    """On améliore une répartition commune aux fréquences choisies par descente projetée."""
    frequencies = numpy.asarray(frequencies_hz, dtype=float)
    if len(frequencies) == 0 or not numpy.all(numpy.isfinite(frequencies)) or numpy.any(numpy.diff(frequencies) <= 0):
        print("On fournit des fréquences distinctes dans l'ordre croissant.")
        return None
    weights = numpy.ones(len(frequencies)) if weights is None else numpy.asarray(weights, dtype=float)
    if weights.shape != frequencies.shape or not numpy.all(numpy.isfinite(weights)) or numpy.any(weights < 0) or weights.sum() <= 0:
        print("On fournit un poids positif pour chaque fréquence.")
        return None
    iterations = N_ITERATIONS if iterations is None else int(iterations)
    data = prepare_frequencies(problem, frequencies)
    if data is None:
        return None
    chi = problem["chi_initial"] if chi is None else chi
    chi = project_density(chi, problem["domain"], problem["V_obj"])
    energies, gradient = evaluate_distribution(problem, chi, data, weights)
    if energies is None:
        return None
    history = [float(weights @ energies)]
    for iteration in range(iterations):
        if mu <= 1e-5:
            break
        accepted = False
        while mu > 1e-5:
            candidate = project_density(chi - mu * gradient, problem["domain"], problem["V_obj"])
            if numpy.array_equal(candidate, chi):
                break
            candidate_energies, candidate_gradient = evaluate_distribution(problem, candidate, data, weights)
            if candidate_energies is None:
                return None
            energy = float(weights @ candidate_energies)
            if energy < history[-1]:
                change = float(numpy.max(numpy.abs(candidate - chi)))
                chi, energies, gradient = candidate, candidate_energies, candidate_gradient
                history.append(energy)
                mu *= 1.1
                accepted = True
                break
            mu /= 2.0
        if not accepted:
            break
        print(problem["material_name"], "niveau", problem["level"], "étape", iteration + 1,
              ": Énergie J =", history[-1], flush=True)
        if change < DENSITY_TOLERANCE:
            break
    chi_relaxed = chi.copy()
    chi = preprocessing.binarize_chi(chi_relaxed, problem["domain"], problem["V_obj"])
    binary_energies, _ = evaluate_distribution(problem, chi, data)
    return {"frequencies_hz": frequencies, "alphas": data["alphas"], "weights": weights,
            "history": numpy.asarray(history), "chi_relaxed": chi_relaxed, "chi": chi,
            "binary_energy": float(weights @ binary_energies), "binary_energies": binary_energies,
            "accepted_steps": len(history) - 1, "mu_final": float(mu)}


def resonance_peaks(frequencies_hz, energies):
    """On repère tous les maxima locaux supérieurs à leurs deux voisins."""
    values = numpy.asarray(energies)
    indices = numpy.flatnonzero((values[1:-1] > values[:-2]) & (values[1:-1] > values[2:])) + 1
    return indices, numpy.asarray(frequencies_hz)[indices]


def your_band_optimization(problem, frequencies_hz, chi=None, iterations=None):
    """On minimise la moyenne de bande avec les poids des trapèzes."""
    weights = preprocessing.trapezoidal_weights(frequencies_hz)
    return your_multifrequency_optimization(problem, frequencies_hz, chi, weights, iterations=iterations)


def quantity_comparison(problem, data):
    """On augmente la longueur d'une portion garnie centrée sur le contour du mur."""
    _, x, y, _, _ = preprocessing._set_geometry_of_domain(2 * problem["N"], problem["N"], problem["level"])
    nodes = []
    for yy, xx in zip(y[:-1], x[:-1]):
        i, j = int(yy), int(xx)
        if not nodes or (i, j) != nodes[-1]:
            nodes.append((i, j))
    weights = preprocessing.trapezoidal_weights(data["frequencies_hz"])
    fractions, energies = [], []
    for fraction in VOLUMES:
        count = int(round(fraction * len(nodes)))
        start = (len(nodes) - count) // 2
        density = numpy.zeros(problem["domain"].shape)
        for i, j in nodes[start:start + count]:
            density[i, j] = 1.0
        values, _ = evaluate_distribution(problem, density, data)
        fractions.append(float(density.sum() / len(nodes)))
        energies.append(float(weights @ values))
    return numpy.asarray(fractions), numpy.asarray(energies)


def study_material(material_name, output_dir=None):
    """On compare les quatre géométries puis on optimise le niveau choisi."""
    output_dir = Path(__file__).resolve().parent / "resultats" if output_dir is None else Path(output_dir)
    folder = output_dir / material_name
    folder.mkdir(parents=True, exist_ok=True)
    parameters = {"N_points": N_POINTS, "max_iterations": N_ITERATIONS, "levels": list(LEVELS),
                  "optimization_level": LEVEL, "frequencies_hz": FREQUENCIES_HZ.tolist(),
                  "source": SOURCE.__name__, "source_gaussians": list(map(list, preprocessing.RER_B_GAUSSIANS)),
                  "material": material_name, "material_parameters": list(MATERIAUX[material_name]),
                  "c": C, "alpha0": ALPHA0, "density_tolerance": DENSITY_TOLERANCE,
                  "quantity_fractions": list(VOLUMES), "quantity_distribution": "portion_centrale_un_seul_tenant"}
    parameter_file = folder / "parametres.json"
    if parameter_file.exists() and json.loads(parameter_file.read_text()) != parameters:
        print("Les paramètres enregistrés sont différents. On choisit un autre dossier de sortie.")
        return None
    parameter_file.write_text(json.dumps(parameters, ensure_ascii=False, indent=2) + "\n")
    common = None
    for level in LEVELS:
        problem = make_problem(N_POINTS, level, material_name)
        if common is not None:
            problem["alphas"].update(common["alphas"])
            problem["source_values"].update(common["source_values"])
        alpha_file = folder / "coefficients.npz"
        if alpha_file.exists():
            saved = numpy.load(alpha_file)
            for frequency, alpha in zip(saved["frequencies_hz"], saved["alphas"]):
                problem["alphas"][float(frequency)] = complex(alpha)
                row = numpy.zeros(problem["N"], dtype=complex)
                coordinates = (numpy.arange(problem["N"]) - (problem["N"] - 1) / 2) * problem["h"]
                row[:] = problem["source"](coordinates, 2 * numpy.pi * frequency)
                problem["source_values"][float(frequency)] = row
        data = prepare_frequencies(problem, FREQUENCIES_HZ)
        if data is None:
            return None
        numpy.savez_compressed(alpha_file, frequencies_hz=FREQUENCIES_HZ, alphas=data["alphas"])
        common = problem
        reference_file = folder / f"niveau{level}.npz"
        if reference_file.exists():
            reference = dict(numpy.load(reference_file))
        else:
            full = (problem["domain"] == _env.NODE_ROBIN).astype(float)
            full_energies, _ = evaluate_distribution(problem, full, data)
            initial_energies, _ = evaluate_distribution(problem, problem["chi_initial"], data)
            reference = {"frequencies_hz": FREQUENCIES_HZ, "full": full_energies, "initial": initial_energies,
                         "domain": problem["domain"], "chi_initial": problem["chi_initial"], "h": problem["h"]}
            reference["peaks"] = resonance_peaks(FREQUENCIES_HZ, full_energies)[0]
            numpy.savez_compressed(reference_file, **reference)
        postprocessing.plot_reference(reference, material_name, level, output_dir)
        quantity_file = folder / f"quantite_niveau{level}.npz"
        if not quantity_file.exists():
            fractions, energies = quantity_comparison(problem, data)
            numpy.savez_compressed(quantity_file, fractions=fractions, energies=energies)
        print("Références et quantités terminées :", material_name, "niveau", level, flush=True)
        if level == LEVEL:
            mode_file = folder / f"descente_niveau{level}_pas5.npz"
            if mode_file.exists():
                mode = dict(numpy.load(mode_file))
            else:
                mode = your_band_optimization(problem, FREQUENCIES_HZ)
                if mode is None:
                    return None
                numpy.savez_compressed(mode_file, **mode)
            postprocessing.plot_optimization(reference, mode, material_name, level, output_dir)
    return str(folder)


def run_material_comparison(output_dir=None):
    """On calcule les quatre études de matériau puis on trace leurs comparaisons."""
    folder = Path(__file__).resolve().parent / "resultats" if output_dir is None else Path(output_dir)
    for name in MATERIALS:
        if study_material(name, folder) is None:
            return None
    postprocessing.plot_material_comparisons(folder, MATERIALS, LEVELS)
    print("Figures et données enregistrées dans", folder)
    return folder


if __name__ == "__main__":
    run_material_comparison()
