# -*- coding: utf-8 -*-
"""On étudie le mur avec les matrices du support et quatre choix de fréquences."""

from pathlib import Path
import time
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
MATERIALS = ["MELAMINE", "LAINE_VERRE", "OUATE_POLYESTER"]
ALPHA0 = [50.0, -50.0]
C = 343.0
OMEGA = 3430.0
N_POINTS = 128
LEVEL = 2
N_ITERATIONS = 10
ETUDE = "bande"
FREQUENCIES_HZ = numpy.arange(50.0, 3501.0, 25.0)
MATERIAL_FREQUENCIES_HZ = numpy.arange(50.0, 3501.0, 10.0)
VOLUMES = [0.10, 0.30, 0.50, 0.70, 1.0]
FREQUENCY_TOLERANCE = 0.01
PEAK_TOLERANCE = 0.05
MAX_FREQUENCY_GAP_HZ = 25.0
MAX_REFINEMENTS = 12

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
    delta = 1e-7
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


def evaluate_distribution(problem, chi, frequency_data, keep_states=False):
    """On résout le système fourni à chaque fréquence et on mesure les énergies."""
    energies, states = [], []
    for wave, alpha, source_values in zip(frequency_data["wavenumbers"], frequency_data["alphas"], frequency_data["sources"]):
        matrix, state, field = processing.compute_state(
            problem["domain"], problem["h"], wave,
            f_dir=dirichlet_load(problem, source_values), alpha_rob=alpha * chi,
            **problem["loads"], **problem["coefficients"], prepared=problem["prepared"],
        )
        energy = your_compute_objective_function(problem["domain"], field, problem["h"])
        if not numpy.isfinite(energy):
            print("Énergie non finie pour le nombre d'onde", wave)
            return None, None
        energies.append(energy)
        if keep_states:
            states.append(state)
    return numpy.asarray(energies), states


def energy_gradient(problem, chi, frequency_data, states, weights):
    """On additionne les gradients fréquentiels obtenus avec les systèmes adjoints."""
    gradient = numpy.zeros(problem["domain"].shape)
    for wave, alpha, values, state, weight in zip(frequency_data["wavenumbers"], frequency_data["alphas"], frequency_data["sources"], states, weights):
        matrix, _ = processing.assemble_helmholtz_system(
            problem["domain"], problem["h"], wave,
            f_dir=dirichlet_load(problem, values), alpha_rob=alpha * chi,
            **problem["loads"], **problem["coefficients"], prepared=problem["prepared"],
        )
        adjoint = compute_adjoint(problem["domain"], problem["h"], matrix, state)
        gradient += weight * compute_gradient(
            problem["domain"], problem["h"], alpha, chi,
            problem["coefficients"]["beta_pde"], problem["coefficients"]["beta_rob"],
            problem["loads"]["f_rob"], adjoint, state,
        )
    return gradient


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
    energies, states = evaluate_distribution(problem, chi, data, keep_states=True)
    if energies is None:
        return None
    history = [float(weights @ energies)]
    for iteration in range(iterations):
        if mu <= 1e-5:
            break
        gradient = energy_gradient(problem, chi, data, states, weights)
        accepted = False
        while mu > 1e-5:
            candidate = project_density(chi - mu * gradient, problem["domain"], problem["V_obj"])
            if numpy.array_equal(candidate, chi):
                break
            candidate_energies, candidate_states = evaluate_distribution(problem, candidate, data, keep_states=True)
            if candidate_energies is None:
                return None
            energy = float(weights @ candidate_energies)
            if energy < history[-1]:
                change = float(numpy.max(numpy.abs(candidate - chi)))
                chi, energies, states = candidate, candidate_energies, candidate_states
                history.append(energy)
                mu *= 1.1
                accepted = True
                break
            mu /= 2.0
        if not accepted:
            break
        print("Étape", iteration + 1, ": Énergie J =", history[-1], flush=True)
        if change < 1e-7:
            break
    chi_relaxed = chi.copy()
    chi = preprocessing.binarize_chi(chi_relaxed, problem["domain"], problem["V_obj"])
    binary_energies, _ = evaluate_distribution(problem, chi, data)
    return {"frequencies_hz": frequencies, "alphas": data["alphas"], "weights": weights,
            "history": numpy.asarray(history), "chi_relaxed": chi_relaxed, "chi": chi,
            "binary_energy": float(weights @ binary_energies), "binary_energies": binary_energies,
            "accepted_steps": len(history) - 1, "mu_final": float(mu)}


def your_three_peaks_optimization(problem, chi=None, iterations=None):
    """On minimise la somme des énergies aux trois centres de la source."""
    frequencies = numpy.asarray([part[0] for part in preprocessing.RER_B_GAUSSIANS])
    return your_multifrequency_optimization(problem, frequencies, chi, numpy.ones(len(frequencies)), iterations=iterations)


def resonance_peaks(frequencies_hz, energies):
    """On repère tous les maxima locaux supérieurs à leurs deux voisins."""
    values = numpy.asarray(energies)
    indices = numpy.flatnonzero((values[1:-1] > values[:-2]) & (values[1:-1] > values[2:])) + 1
    return indices, numpy.asarray(frequencies_hz)[indices]


def your_peak_optimization(problem, frequencies_hz, energies, chi=None, iterations=None):
    """On optimise la somme des énergies à tous les pics repérés sur le spectre."""
    indices, targets = resonance_peaks(frequencies_hz, energies)
    if len(targets) == 0:
        targets = numpy.asarray(frequencies_hz)[[int(numpy.argmax(energies))]]
    return your_multifrequency_optimization(problem, targets, chi, numpy.ones(len(targets)), iterations=iterations)


def your_band_optimization(problem, frequencies_hz, chi=None, iterations=None):
    """On optimise l'énergie de bande avec les poids des trapèzes."""
    weights = preprocessing.trapezoidal_weights(frequencies_hz)
    return your_multifrequency_optimization(problem, frequencies_hz, chi, weights, iterations=iterations)


def compute_spectra(problem, frequencies_hz, distributions):
    """On conserve les évaluations déjà faites pour des répartitions qui restent fixes."""
    frequencies = numpy.asarray(frequencies_hz, dtype=float)
    for name, density in distributions.items():
        saved = problem["spectra"].setdefault(name, {})
        missing = [float(f) for f in frequencies if float(f) not in saved]
        if missing:
            data = prepare_frequencies(problem, missing)
            if data is None:
                return None
            energies, _ = evaluate_distribution(problem, density, data)
            if energies is None:
                return None
            saved.update(zip(missing, energies))
    return {name: numpy.asarray([problem["spectra"][name][float(f)] for f in frequencies]) for name in distributions}


def refine_frequency_sampling(problem, frequencies_hz, distributions, phase, rounds=None):
    """On ajoute les milieux des intervalles dont les trapèzes varient encore sensiblement."""
    frequencies = numpy.unique(frequencies_hz)
    rounds = MAX_REFINEMENTS if rounds is None else rounds
    records = []
    for iteration in range(rounds + 1):
        middle = (frequencies[:-1] + frequencies[1:]) / 2.0
        probes = numpy.sort(numpy.r_[frequencies, middle])
        values = compute_spectra(problem, probes, distributions)
        if values is None:
            return None, records
        widths = numpy.diff(frequencies)
        local_errors, peak_changes = [], []
        for energies in values.values():
            coarse = widths * (energies[:-2:2] + energies[2::2]) / 2.0
            fine = widths * (energies[:-2:2] + 2 * energies[1::2] + energies[2::2]) / 4.0
            local_errors.append(numpy.abs(fine - coarse) / max(float(fine.sum()), numpy.finfo(float).tiny))
            maximum = max(float(energies.max()), numpy.finfo(float).tiny)
            peak_changes.append(abs(maximum - float(energies[::2].max())) / maximum)
        error = max(float(row.sum()) for row in local_errors)
        peak_error = max(peak_changes)
        converged = iteration >= 1 and error <= FREQUENCY_TOLERANCE and peak_error <= PEAK_TOLERANCE and widths.max() <= MAX_FREQUENCY_GAP_HZ
        records.append({"phase": phase, "iteration": iteration, "n_points": len(frequencies),
                        "integral_error": error, "peak_error": peak_error, "converged": bool(converged)})
        print(phase, len(frequencies), "fréquences : écarts", error, peak_error, flush=True)
        if converged or iteration == rounds:
            if not converged:
                print("Le contrôle fréquentiel atteint sa limite de raffinement.", flush=True)
            return probes, records
        scores = numpy.max(local_errors, axis=0)
        order = numpy.argsort(scores)[::-1]
        count = numpy.searchsorted(numpy.cumsum(scores[order]), max(0.0, scores.sum() - FREQUENCY_TOLERANCE / 4)) + 1
        selected = widths > MAX_FREQUENCY_GAP_HZ
        selected[order[:count]] = True
        frequencies = numpy.sort(numpy.r_[frequencies, middle[selected]])
    return frequencies, records


def check_energy_derivative(problem):
    """On compare le gradient adjoint aux différences centrées sur quelques points du mur."""
    density = numpy.zeros(problem["domain"].shape)
    density[problem["domain"] == _env.NODE_ROBIN] = 0.4
    data = prepare_frequencies(problem, [200.0, 800.0, 2500.0])
    energies, states = evaluate_distribution(problem, density, data, keep_states=True)
    gradient = energy_gradient(problem, density, data, states, numpy.ones(3))
    nodes = numpy.argwhere(problem["domain"] == _env.NODE_ROBIN)
    chosen = nodes[numpy.linspace(0, len(nodes) - 1, 12, dtype=int)]
    adjoint, finite = [], []
    epsilon = 1e-6
    for i, j in chosen:
        plus, minus = density.copy(), density.copy()
        plus[i, j] += epsilon
        minus[i, j] -= epsilon
        ep, _ = evaluate_distribution(problem, plus, data)
        em, _ = evaluate_distribution(problem, minus, data)
        finite.append(float((ep.sum() - em.sum()) / (2 * epsilon)))
        adjoint.append(gradient[i, j])
    adjoint, finite = numpy.asarray(adjoint), numpy.asarray(finite)
    return {"adjoint": adjoint, "finite_difference": finite,
            "relative_error": float(numpy.linalg.norm(adjoint - finite) / max(numpy.linalg.norm(finite), 1e-14))}


def material_comparisons(N, frequencies_hz):
    """On compare les trois matériaux sur les murs entièrement garnis."""
    results = {}
    for name in MATERIALS:
        material = {"full": {}, "peaks": {}}
        first = None
        for level in (0, 1, 2):
            problem = make_problem(N, level, name)
            if first is not None:
                problem["alphas"].update(first["alphas"])
                problem["source_values"].update(first["source_values"])
            full = (problem["domain"] == _env.NODE_ROBIN).astype(float)
            data = prepare_frequencies(problem, frequencies_hz)
            energies, _ = evaluate_distribution(problem, full, data)
            material["full"][level] = energies
            material["peaks"][level] = resonance_peaks(frequencies_hz, energies)[0]
            if first is None:
                first = problem
                material["alphas"] = data["alphas"]
            print("Mur entièrement garni :", name, "niveau", level, flush=True)
        results[name] = material
    return results


def quantity_comparison(problem, iterations=None):
    """On compare cinq quantités après optimisation sur les trois centres de la source."""
    values, actual = [], []
    for fraction in VOLUMES:
        modified = dict(problem)
        modified["V_obj"] = fraction
        result = your_three_peaks_optimization(modified, iterations=iterations)
        values.append(result["binary_energy"])
        actual.append(float(result["chi"].sum() / numpy.count_nonzero(problem["domain"] == _env.NODE_ROBIN)))
    return {"fractions": numpy.asarray(actual), "energies": numpy.asarray(values),
            "targets_hz": numpy.asarray([part[0] for part in preprocessing.RER_B_GAUSSIANS])}


def sommerfeld_reference():
    """On compare l'énergie d'un rectangle ouvert à celle d'un rectangle réfléchissant."""
    depths = numpy.linspace(0.5, 1.5, 801)
    frequency = 200.0
    wave = 2 * numpy.pi * frequency / C
    poles = (numpy.pi / 2 + numpy.arange(10) * numpy.pi) / wave
    depths = numpy.unique(numpy.r_[depths, poles[(poles >= .5) & (poles <= 1.5)]])
    amplitude = abs(SOURCE(0.0, 2 * numpy.pi * frequency))**2
    denominator = numpy.cos(wave * depths)**2
    reflecting = amplitude * (.5 + numpy.sin(2 * wave * depths) / (4 * wave * depths)) / numpy.where(denominator > 1e-12, denominator, numpy.nan)
    return {"depths": depths, "open": numpy.full_like(depths, amplitude),
            "reflecting": reflecting, "frequency_hz": frequency}


def run_project(N=None, modes=None, output_dir=None, studies=True):
    """On produit les comparaisons avec les seuls systèmes complets du support."""
    started = time.perf_counter()
    problem = make_problem(N)
    if problem is None:
        return None
    modes = ["mono", "trois_pics", "pics_resonance", "bande"] if modes is None else list(modes)
    study_name = modes[0] if len(modes) == 1 else "comparaison"
    default_folder = Path(__file__).resolve().parent / "resultats_antoine" / f"{problem['material_name']}_N{problem['N']}_{study_name}_{N_ITERATIONS}iterations"
    output_dir = default_folder if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    highest_frequency = max(float(numpy.max(FREQUENCIES_HZ)), max(part[0] for part in preprocessing.RER_B_GAUSSIANS))
    ratio = C / (highest_frequency * problem["h"])
    if ratio < 10:
        print("Essai informatique : moins de dix points par longueur d’onde au maximum de la bande.")
    full = (problem["domain"] == _env.NODE_ROBIN).astype(float)
    references = {"initial": problem["chi_initial"], "full": full}
    scan, records = refine_frequency_sampling(problem, FREQUENCIES_HZ, references, "repérage des pics")
    if scan is None:
        return None
    scan_values = compute_spectra(problem, scan, references)
    numpy.savez_compressed(output_dir / "spectres_reference.npz", frequencies_hz=scan,
                           initial=scan_values["initial"], full=scan_values["full"],
                           alphas=prepare_frequencies(problem, scan)["alphas"],
                           domain=problem["domain"], chi_initial=problem["chi_initial"])
    targets, _ = resonance_peaks(scan, scan_values["initial"])
    if len(targets) == 0:
        targets = numpy.asarray([int(numpy.argmax(scan_values["initial"]))])
    results = {}
    # On conserve une référence aux trois centres pour initialiser les deux recherches plus larges.
    if any(name in modes for name in ("trois_pics", "pics_resonance", "bande")):
        results["trois_pics"] = your_three_peaks_optimization(problem)
        if results["trois_pics"] is None:
            return None
        postprocessing.save_mode(results["trois_pics"], output_dir, "trois_pics")
    if "mono" in modes:
        frequency = float(scan[targets[numpy.argmax(scan_values["initial"][targets])]])
        data = prepare_frequencies(problem, [frequency])
        chi, history, _, _ = your_optimization_procedure(
            problem["domain"], problem["h"], data["wavenumbers"][0],
            f_dir=dirichlet_load(problem, data["sources"][0]), alpha_rob=data["alphas"][0] * problem["chi_initial"],
            Alpha=data["alphas"][0], mu=5.0, chi=problem["chi_initial"], V_obj=problem["V_obj"],
            **problem["loads"], **problem["coefficients"],
        )
        results["mono"] = {"chi": chi, "history": history[:-1, 0], "binary_energy": float(history[-1, 0]),
                           "accepted_steps": len(history) - 2, "frequencies_hz": numpy.asarray([frequency]), "weights": numpy.ones(1)}
        postprocessing.save_mode(results["mono"], output_dir, "mono")
    if "pics_resonance" in modes:
        results["pics_resonance"] = your_peak_optimization(problem, scan, scan_values["initial"], results["trois_pics"]["chi_relaxed"])
        if results["pics_resonance"] is None:
            return None
        postprocessing.save_mode(results["pics_resonance"], output_dir, "pics_resonance")
    if "bande" in modes:
        band_grid, band_records = refine_frequency_sampling(
            problem, FREQUENCIES_HZ,
            {"three_binary": results["trois_pics"]["chi"], "three_continuous": results["trois_pics"]["chi_relaxed"]},
            "choix de la grille de bande",
        )
        records.extend(band_records)
        if band_grid is None:
            return None
        results["bande"] = your_band_optimization(problem, band_grid, results["trois_pics"]["chi_relaxed"])
        if results["bande"] is None:
            return None
        postprocessing.save_mode(results["bande"], output_dir, "bande")
    if any(result is None for result in results.values()):
        return None
    results = {name: results[name] for name in ("mono", "trois_pics", "pics_resonance", "bande") if name in results}
    distributions = dict(references)
    distributions.update({name: result["chi"] for name, result in results.items()})
    validation_start = numpy.unique(numpy.r_[scan, numpy.arange(float(scan[0]), float(scan[-1]), 10.), [float(scan[-1])]])
    grid, validation_records = refine_frequency_sampling(problem, validation_start, distributions, "validation commune")
    records.extend(validation_records)
    if grid is None:
        return None
    spectra = compute_spectra(problem, grid, distributions)
    for name in results:
        results[name]["energies"] = spectra[name]
    parameters = {"N": problem["N"], "h": problem["h"], "h_m": problem["h"], "level": problem["level"],
                  "material_name": problem["material_name"], "source_name": SOURCE.__name__,
                  "V_obj": problem["V_obj"], "iterations": N_ITERATIONS,
                  "robin_points": int(numpy.count_nonzero(problem["domain"] == _env.NODE_ROBIN)),
                  "covered_points": int(results[next(iter(results))]["chi"].sum()),
                  "points_per_shortest_wavelength": ratio, "wavelength_resolution_ok": bool(ratio >= 10), "spatial_convergence_tested": False,
                  "frequency_control_converged": bool(validation_records[-1]["converged"]),
                  "frequency_tolerance": FREQUENCY_TOLERANCE, "peak_tolerance": PEAK_TOLERANCE,
                  "source_gaussians": list(preprocessing.RER_B_GAUSSIANS), "alpha0": list(ALPHA0),
                  "material_parameters": list(MATERIAUX[problem["material_name"]]),
                  "initialization_pics_and_band": "three_peaks_continuous", "linear_system": "support_complet",
                  "elapsed_seconds": time.perf_counter() - started}
    result = {"parameters": parameters, "frequencies_hz": grid, "domain": problem["domain"],
              "h": problem["h"], "chi_initial": problem["chi_initial"], "source": SOURCE,
              "initial": spectra["initial"], "full": spectra["full"], "modes": results,
              "sommerfeld": sommerfeld_reference(), "sampling_history": records}
    if studies:
        result["material_frequencies_hz"] = MATERIAL_FREQUENCIES_HZ
        result["materials"] = material_comparisons(problem["N"], MATERIAL_FREQUENCIES_HZ)
        result["quantities"] = quantity_comparison(problem)
        # On vérifie le calcul différentiel sur une géométrie plus petite et bien résolue à ces fréquences.
        check = make_problem(128, 1)
        result["gradient_check"] = check_energy_derivative(check)
    result["parameters"]["elapsed_seconds"] = time.perf_counter() - started
    postprocessing.plot_comparisons(result, output_dir)
    print("Résultats enregistrés dans", output_dir, flush=True)
    return result


if __name__ == "__main__":
    if ETUDE == "complet":
        run_project()
    elif ETUDE in ("mono", "trois_pics", "pics_resonance", "bande"):
        run_project(modes=[ETUDE], studies=False)
    else:
        print("On choisit mono, trois_pics, pics_resonance, bande ou complet dans ETUDE.")
