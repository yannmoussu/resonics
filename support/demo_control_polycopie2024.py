# -*- coding: utf-8 -*-


# Python packages
import numpy
import os
import sys
import time
import json
from pathlib import Path


# MRG packages
import _env
import preprocessing
import processing
import postprocessing
from compute_alpha import compute_alpha, MATERIAUX
from preprocessing import project_density
from processing import compute_state, compute_adjoint, compute_gradient


# On choisit la source commune au champ initial, à la descente et aux fréquences.
SOURCE = preprocessing.source_rer_b
# SOURCE = preprocessing.source_constant
MATERIAL_NAME = "OUATE_POLYESTER"
CAR_MAT = MATERIAUX[MATERIAL_NAME]
ALPHA0 = [50.0, -50.0]  # On donne les parties réelle et imaginaire du point initial.
OMEGA = 3430.0  # On exprime la pulsation en radians par seconde.
C = 343.0  # On exprime la célérité en mètres par seconde.

# On choisit une étude ou l’ensemble des comparaisons.
# Les choix sont demo, trois_pics, spectre_complet, materiaux_validation, monofrequence,
# multifrequence, comparaison_dispositifs et tous.
ETUDE = "spectre_complet"
N_POINTS = 128
FREQUENCES_HZ = numpy.arange(50.0, 3501.0, 50.0)
N_ITERATIONS = 80
FRACTION_GARNIE = 0.30
QUANTITES = [0.10, 0.30, 0.50, 0.70, 1.0]
MATERIAUX_A_COMPARER = ["MELAMINE", "LAINE_VERRE", "OUATE_POLYESTER"]

# On règle les contrôles de précision en fréquence séparément du pas de descente.
FREQUENCY_INTEGRAL_TOLERANCE = 0.01
FREQUENCY_PEAK_TOLERANCE = 0.05
FREQUENCY_MAX_GAP_HZ = 25.0
FREQUENCY_REFINEMENTS = 12
VALIDATION_INITIAL_STEP_HZ = 10.0
VALIDATION_REFINEMENTS = 8
GEOMETRY_LEVEL = 2


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
    energy = numpy.zeros((numb_iter+1, 1), dtype=numpy.float64)
    chi = project_density(chi, domain_omega, V_obj)
    delta = 1e-7
    while k < numb_iter and mu > 10**(-5):
        print('---- iteration number = ', k)
        print('1. computing solution of Helmholtz problem, i.e., u')
        matrix, state, u = compute_state(
            domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi,
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
                beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * candidate,
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
            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi,
        )
        energy[0, 0] = compute_objective_function(domain_omega, u, spacestep)
    energy = energy[:k + 1]

    # On garnit les points dont les densités sont les plus grandes.
    robin = domain_omega == _env.NODE_ROBIN
    order = numpy.argsort(-chi[robin])
    number = int(round(V_obj * len(order)))
    values = numpy.zeros(len(order))
    values[order[:number]] = 1.0
    chi = numpy.zeros((M, N))
    chi[robin] = values

    print('end. computing solution of Helmholtz problem, i.e., u')
    matrix, state, u = compute_state(
        domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi,
    )
    # On ajoute séparément le coût de la répartition binaire.
    ene = compute_objective_function(domain_omega, u, spacestep)
    energy = numpy.vstack((energy, [[ene]]))
    p = compute_adjoint(domain_omega, spacestep, matrix, state)
    grad = compute_gradient(
        domain_omega, spacestep, Alpha, chi, beta_pde, beta_rob, f_rob, p, state,
    )

    return chi, energy, u, grad



def your_optimization_procedure_spectrum(
    domain_omega, spacestep, chi, V_obj, frequencies_hz=None,
    f=None, f_neu=None, f_rob=None,
    beta_pde=None, alpha_pde=None, alpha_dir=None, beta_neu=None, beta_rob=None,
    source=None, car_mat=None, alpha0=None,
    sound_speed_m_s=C, mu=5.0, numb_iter=N_ITERATIONS, alphas=None, weights=None,
):
    """On optimise un seul placement avec les énergies pondérées des fréquences données."""
    frequencies_hz = numpy.asarray(FREQUENCES_HZ if frequencies_hz is None else frequencies_hz, dtype=float)
    source = SOURCE if source is None else source
    car_mat = CAR_MAT if car_mat is None else car_mat
    alpha0 = ALPHA0 if alpha0 is None else alpha0
    if alphas is None:
        alphas = processing.compute_material_coefficients(frequencies_hz, source, car_mat, alpha0)
    if alphas is None:
        return None
    alphas = numpy.asarray(alphas, dtype=complex)
    if alphas.shape != frequencies_hz.shape or not numpy.isfinite(alphas).all():
        print("On fournit un coefficient complexe fini pour chaque fréquence.")
        return None
    if weights is None:
        weights = processing.spectral_quadrature_weights(frequencies_hz)
    solver = processing.FastHelmholtzSolver(
        domain_omega, spacestep, f=f, f_neu=f_neu, f_rob=f_rob,
        beta_pde=beta_pde, alpha_pde=alpha_pde, alpha_dir=alpha_dir,
        beta_neu=beta_neu, beta_rob=beta_rob,
    )
    return processing.optimize_frequency_distribution(
        solver, 2.0 * numpy.pi * frequencies_hz / sound_speed_m_s, alphas, chi,
        weights=weights, V_obj=V_obj, mu_init=mu, numb_iter=numb_iter,
        source=source, sound_speed_m_s=sound_speed_m_s, verbose=True,
    )


def your_optimization_procedure_three_peaks(
    domain_omega, spacestep, chi, V_obj,
    f=None, f_neu=None, f_rob=None,
    beta_pde=None, alpha_pde=None, alpha_dir=None, beta_neu=None, beta_rob=None,
    source=None, car_mat=None, alpha0=None,
    sound_speed_m_s=C, mu=5.0, numb_iter=N_ITERATIONS, alphas=None,
):
    """On conserve la somme des énergies aux trois centres comme comparaison."""
    frequencies = numpy.asarray([part[0] for part in preprocessing.RER_B_GAUSSIANS])
    result = your_optimization_procedure_spectrum(
        domain_omega, spacestep, chi, V_obj, frequencies,
        f, f_neu, f_rob, beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
        source, car_mat, alpha0, sound_speed_m_s, mu, numb_iter, alphas,
        weights=numpy.ones(len(frequencies)),
    )
    if result is None:
        return None
    # On conserve la sortie historique de ce mode et on isole aussi la partie continue.
    result["continuous_energy_history"] = result["energy_history"].copy()
    result["energy_history"] = numpy.vstack((result["energy_history"], [[result["binary_energy"]]]))
    result["energy_by_frequency"] = numpy.vstack((result["energy_by_frequency"], result["binary_energies"]))
    return result


def your_compute_objective_function(domain_omega, u, spacestep):
    """On calcule le critère à partir du module de pression sur les points intérieurs."""
    return processing.compute_objective_function(domain_omega, u, spacestep)


# Les deux noms désignent le même calcul du coût.
compute_objective_function = your_compute_objective_function



def run_three_peaks_optimization():
    """Mode autonome : une descente unique sur la somme des trois pics du RER B."""
    N = N_POINTS
    M = 2 * N
    spacestep = 1.0 / N
    level = 2

    beta_pde, alpha_pde, alpha_dir, beta_neu, _, beta_rob = (
        preprocessing._set_coefficients_of_pde(M, N)
    )
    f, _, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level)
    chi_initial = preprocessing._set_chi(M, N, x, y)
    chi_initial = preprocessing.set2zero(chi_initial, domain_omega)
    robin_count = numpy.count_nonzero(domain_omega == _env.NODE_ROBIN)
    V_obj = float(numpy.sum(chi_initial) / robin_count)

    result = your_optimization_procedure_three_peaks(
        domain_omega, spacestep, chi_initial, V_obj,
        f=f, f_neu=f_neu, f_rob=f_rob,
        beta_pde=beta_pde, alpha_pde=alpha_pde, alpha_dir=alpha_dir,
        beta_neu=beta_neu, beta_rob=beta_rob,
        source=SOURCE, car_mat=CAR_MAT, alpha0=ALPHA0, sound_speed_m_s=C,
        mu=5.0, numb_iter=N_ITERATIONS,
    )

    if result is None:
        return None
    energies = result["energy_history"][:, 0]
    components = result["energy_by_frequency"]
    print("Fréquences étudiées (Hz) :", result["frequencies_hz"])
    print("Énergie J initiale :", energies[0])
    print("Énergie J continue finale :", energies[-2])
    print("Énergie J binaire finale :", energies[-1])
    print("Énergies binaires par fréquence :", components[-1])
    print("Points garnis :", int(numpy.count_nonzero(result["chi"])))

    postprocessing._plot_energy_history(result["energy_history"])
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historique_3_pics.csv")
    steps = numpy.arange(len(energies))
    numpy.savetxt(
        csv_path, numpy.column_stack((steps, components, energies)), delimiter=",",
        header="step,J_200Hz,J_800Hz,J_2500Hz,J_total", comments="",
    )
    return result

def sample_frequency_configurations(frequencies, configurations, solver, source,
                                    car_mat, alpha0, sound_speed, cache):
    """On calcule les énergies manquantes et on conserve les coefficients déjà identifiés."""
    frequencies = numpy.asarray(frequencies, dtype=float)
    missing = [float(frequency) for frequency in frequencies if float(frequency) not in cache["alphas"]]
    if missing:
        values = processing.compute_material_coefficients(missing, source, car_mat, alpha0)
        if values is None:
            return None
        cache["alphas"].update(zip(missing, values))
    for name in configurations:
        cache["energies"].setdefault(name, {})
    for frequency in frequencies:
        frequency = float(frequency)
        pending = [name for name in configurations if frequency not in cache["energies"][name]]
        if not pending:
            continue
        solver.set_source(source, 2.0 * numpy.pi * frequency)
        for name in pending:
            field = solver.solve(2.0 * numpy.pi * frequency / sound_speed,
                                 cache["alphas"][frequency] * configurations[name])
            energy = solver.compute_energy(field)
            if not numpy.isfinite(energy):
                print("Énergie non finie à", frequency, "Hz pour", name)
                return None
            cache["energies"][name][frequency] = energy
    return {name: numpy.asarray([cache["energies"][name][float(frequency)] for frequency in frequencies])
            for name in configurations}


def refine_spectral_grid(frequencies, configurations, solver, source, car_mat,
                         alpha0, sound_speed, cache, refinements, phase):
    """On contrôle les trapèzes par leurs milieux puis on raffine les intervalles sensibles."""
    frequencies = numpy.unique(frequencies)
    history = []
    for iteration in range(refinements + 1):
        middle = (frequencies[:-1] + frequencies[1:]) / 2.0
        probes = numpy.sort(numpy.concatenate((frequencies, middle)))
        values = sample_frequency_configurations(probes, configurations, solver, source,
                                                car_mat, alpha0, sound_speed, cache)
        if values is None:
            return None, history
        widths = numpy.diff(frequencies)
        errors, changes, peak_changes, interval_scores, peak_scores = [], [], [], [], []
        for energies in values.values():
            left, mid, right = energies[:-2:2], energies[1::2], energies[2::2]
            coarse = widths * (left + right) / 2.0
            fine = widths * (left + 2.0 * mid + right) / 4.0
            scale = max(float(numpy.sum(fine)), numpy.finfo(float).tiny)
            scores = numpy.abs(fine - coarse) / scale
            errors.append(float(numpy.sum(scores)))
            changes.append(abs(float(numpy.sum(fine) - numpy.sum(coarse))) / scale)
            peak = max(float(numpy.max(energies)), numpy.finfo(float).tiny)
            peak_changes.append(abs(peak - float(numpy.max(energies[::2]))) / peak)
            interval_scores.append(scores)
            peak_scores.append(numpy.abs(mid - (left + right) / 2.0) / peak)
        error, peak_error = max(errors), max(peak_changes)
        converged = (iteration >= 1 and error <= FREQUENCY_INTEGRAL_TOLERANCE
                     and peak_error <= FREQUENCY_PEAK_TOLERANCE
                     and widths.max() <= FREQUENCY_MAX_GAP_HZ)
        history.append({"phase": phase, "iteration": iteration, "n_points": len(frequencies),
                        "n_probe_points": len(probes), "max_gap_hz": float(widths.max()),
                        "minimum_gap_hz": float(widths.min()), "estimated_integral_error": error,
                        "integral_error": max(changes), "peak_error": peak_error,
                        "converged": bool(converged)})
        print(phase, iteration, ":", len(frequencies), "fréquences, erreur d'intégrale estimée =",
              error, ", variation du maximum =", peak_error, flush=True)
        if converged:
            return frequencies, history
        if iteration == refinements:
            print("La limite de raffinement est atteinte. On conserve le dernier contrôle dans les résultats.")
            return probes, history
        # On garde des points sur toute la bande et on ajoute ceux des zones les moins résolues.
        scores = numpy.max(interval_scores, axis=0)
        order = numpy.argsort(scores)[::-1]
        remaining_budget = FREQUENCY_INTEGRAL_TOLERANCE / 4.0
        number = numpy.searchsorted(numpy.cumsum(scores[order]), max(0.0, scores.sum() - remaining_budget)) + 1
        selected = numpy.zeros(len(widths), dtype=bool)
        selected[order[:number]] = True
        selected |= ((numpy.max(peak_scores, axis=0) > FREQUENCY_PEAK_TOLERANCE)
                     | (widths > FREQUENCY_MAX_GAP_HZ))
        if not selected.any():
            selected[numpy.argmax(numpy.max(interval_scores, axis=0))] = True
        frequencies = numpy.sort(numpy.concatenate((frequencies, middle[selected])))
    return frequencies, history


def run_full_spectrum_optimization(N=None, iterations=None, frequencies_hz=None,
                                   material_name=None, output_dir=None, warm_start=True):
    """On compare le mur initial, les trois pics et une optimisation sur toute la bande."""
    started = time.perf_counter()
    N = N_POINTS if N is None else int(N)
    iterations = N_ITERATIONS if iterations is None else int(iterations)
    material_name = MATERIAL_NAME if material_name is None else material_name
    frequencies = numpy.asarray(FREQUENCES_HZ if frequencies_hz is None else frequencies_hz, dtype=float)
    frequencies = numpy.unique(frequencies)
    if len(frequencies) < 2 or numpy.any(frequencies <= 0):
        print("On fournit au moins deux fréquences positives pour une étude sur la bande.")
        return None
    output_dir = (Path(__file__).resolve().parent / "resultats_spectre_complet" / material_name
                  if output_dir is None else Path(output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    car_mat = MATERIAUX[material_name]
    h = 1.0 / N
    domain, x, y, _, _ = preprocessing._set_geometry_of_domain(2 * N, N, GEOMETRY_LEVEL)
    initial = preprocessing.set2zero(preprocessing._set_chi(2 * N, N, x, y), domain)
    robin_count = numpy.count_nonzero(domain == _env.NODE_ROBIN)
    volume = float(initial.sum() / robin_count)
    highest_frequency = max(float(frequencies[-1]), max(part[0] for part in preprocessing.RER_B_GAUSSIANS))
    spatial_ratio = C / (highest_frequency * h)
    if spatial_ratio < 10:
        print("Attention : le maillage de cet essai représente moins de dix points par longueur d'onde.")

    three = your_optimization_procedure_three_peaks(
        domain, h, initial, volume, source=SOURCE, car_mat=car_mat,
        alpha0=ALPHA0, sound_speed_m_s=C, numb_iter=iterations,
    )
    if three is None:
        return None
    solver = processing.FastHelmholtzSolver(domain, h)
    cache = {"alphas": dict(zip(three["frequencies_hz"], three["alphas"])), "energies": {}}
    references = {"initial": initial, "three_peaks": three["chi"]}
    start_band = three["chi_relaxed"] if warm_start else initial
    training_configurations = {"starting_density": start_band, "three_peaks": three["chi"]}
    grid, sampling_history = refine_spectral_grid(
        frequencies, training_configurations, solver, SOURCE, car_mat, ALPHA0, C,
        cache, FREQUENCY_REFINEMENTS, "optimisation",
    )
    if grid is None:
        return None
    alphas = numpy.asarray([cache["alphas"][float(frequency)] for frequency in grid])
    (output_dir / "echantillonnage_initial.json").write_text(json.dumps(sampling_history, indent=2), encoding="utf-8")
    numpy.savez_compressed(output_dir / "avant_descente.npz", frequencies_hz=grid, alphas=alphas,
                           chi_initial=initial, chi_start_band=start_band, chi_three_peaks=three["chi"], domain=domain)
    print("On optimise une grille fixe de", len(grid), "fréquences couvrant", grid[0], "à", grid[-1], "Hz.", flush=True)
    band = your_optimization_procedure_spectrum(
        domain, h, start_band, volume, grid, source=SOURCE, car_mat=car_mat,
        alpha0=ALPHA0, sound_speed_m_s=C, numb_iter=iterations, alphas=alphas,
    )
    if band is None:
        return None

    numpy.savez_compressed(output_dir / "descente_avant_validation.npz",
                           frequencies_hz=grid, alphas=alphas, chi_initial=initial,
                           chi_continuous=band["chi_relaxed"], chi_binary=band["chi"],
                           energy_history=band["energy_history"], binary_energy=band["binary_energy"],
                           chi_three_peaks=three["chi"], domain=domain)
    # On contrôle les quatre champs avec une autre grille et de nouveaux points intermédiaires.
    configurations = {**references, "band_continuous": band["chi_relaxed"], "band_binary": band["chi"]}
    regular = numpy.arange(frequencies[0], frequencies[-1], VALIDATION_INITIAL_STEP_HZ)
    validation_start = numpy.unique(numpy.concatenate((regular, [frequencies[-1]], (grid[:-1] + grid[1:]) / 2.0)))
    validation_grid, validation_history = refine_spectral_grid(
        validation_start, configurations, solver, SOURCE, car_mat, ALPHA0, C,
        cache, VALIDATION_REFINEMENTS, "validation",
    )
    if validation_grid is None:
        return None
    # On retient aussi tous les milieux déjà testés lors du dernier contrôle.
    validation_grid = numpy.sort(numpy.concatenate((validation_grid, (validation_grid[:-1] + validation_grid[1:]) / 2.0)))
    evaluation = sample_frequency_configurations(validation_grid, configurations, solver,
                                                 SOURCE, car_mat, ALPHA0, C, cache)
    if evaluation is None:
        return None
    width = float(frequencies[-1] - frequencies[0])
    weights = processing.spectral_quadrature_weights(validation_grid, normalise=False)
    initial_integral = float(weights @ evaluation["initial"])
    metrics = {}
    for name, energies in evaluation.items():
        integral = float(weights @ energies)
        peak_index = int(numpy.argmax(energies))
        metrics[name] = {"integral_J": integral, "mean_J": integral / width,
                         "maximum_J": float(energies[peak_index]),
                         "frequency_max_hz": float(validation_grid[peak_index]),
                         "reduction_relative": (initial_integral - integral) / initial_integral
                         if initial_integral > 0 else 0.0}
    parameters = {"N": N, "M": 2 * N, "h_m": h, "geometry_level": GEOMETRY_LEVEL,
                  "material_name": material_name, "material_parameters": list(car_mat),
                  "source_name": SOURCE.__name__, "source_gaussians": list(preprocessing.RER_B_GAUSSIANS),
                  "sound_speed_m_s": C, "V_obj": volume, "robin_points": int(robin_count),
                  "binary_covered_points": int(round(volume * robin_count)),
                  "initialization_band": "three_peaks_continuous" if warm_start else "original_wall",
                  "three_peaks_accepted_iterations": int(three["accepted_steps"]),
                  "total_accepted_iterations": int(three["accepted_steps"] + band["accepted_steps"]),
                  "iterations_requested": iterations, "accepted_iterations": int(band["accepted_steps"]),
                  "frequencies_initial_hz": frequencies.tolist(), "frequencies_optimization_hz": grid.tolist(),
                  "frequencies_validation_hz": validation_grid.tolist(),
                  "optimization_minimum_gap_hz": float(numpy.min(numpy.diff(grid))),
                  "optimization_maximum_gap_hz": float(numpy.max(numpy.diff(grid))),
                  "validation_maximum_gap_hz": float(numpy.max(numpy.diff(validation_grid))),
                  "frequency_integral_tolerance": FREQUENCY_INTEGRAL_TOLERANCE,
                  "frequency_peak_tolerance": FREQUENCY_PEAK_TOLERANCE,
                  "frequency_maximum_gap_target_hz": FREQUENCY_MAX_GAP_HZ,
                  "frequency_refinement_limit": FREQUENCY_REFINEMENTS,
                  "validation_initial_step_hz": VALIDATION_INITIAL_STEP_HZ,
                  "validation_refinement_limit": VALIDATION_REFINEMENTS,
                  "sampling_converged": sampling_history[-1]["converged"],
                  "validation_converged": validation_history[-1]["converged"],
                  "points_per_shortest_wavelength": spatial_ratio, "spatial_resolution_ok": bool(spatial_ratio >= 10),
                  "robin_convention": "plus_alpha", "alpha0": list(ALPHA0),
                  "descent_objective": "moyenne de bande avec poids trapezoidaux normalises",
                  "integral_multiplier_hz": width, "gradient_step_initial": 5.0,
                  "gradient_step_minimum": 1e-5, "density_variation_tolerance": 1e-7,
                  "gradient_step_increase_factor": 1.1, "gradient_step_decrease_factor": 2.0,
                  "elapsed_seconds": time.perf_counter() - started}
    for name, estimate in (("band_continuous", float(band["energy_history"][-1, 0]) * width),
                           ("band_binary", float(band["binary_energy"]) * width)):
        fine = metrics[name]["integral_J"]
        parameters["quadrature_discrepancy_" + name] = abs(estimate - fine) / max(abs(fine), numpy.finfo(float).tiny)
    evaluation["frequencies_hz"] = validation_grid
    evaluation["alphas"] = numpy.asarray([cache["alphas"][float(frequency)] for frequency in validation_grid])
    result = {"domain": domain, "spacestep": h, "chi_initial": initial, "chi_start_band": start_band,
              "three_peaks": three, "band": band, "evaluation": evaluation,
              "metrics": metrics, "parameters": parameters,
              "sampling_history": sampling_history, "validation_history": validation_history}
    postprocessing.plot_full_spectrum_study(result, output_dir)
    print("Résultats enregistrés dans", output_dir, flush=True)
    for name, indicators in metrics.items():
        print(name, ":", indicators, flush=True)
    return result


def run_studies(selection):
    """On lance les calculs choisis puis on transmet leurs résultats aux tracés."""
    if selection not in ("materiaux_validation", "monofrequence", "multifrequence", "comparaison_dispositifs", "tous"):
        print("On choisit demo, materiaux_validation, monofrequence, multifrequence, comparaison_dispositifs ou tous dans ETUDE.")
        return
    if selection in ("materiaux_validation", "tous"):
        result = processing.study_porous_materials(
            FREQUENCES_HZ, SOURCE, ALPHA0, MATERIAUX_A_COMPARER,
        )
        if result is None:
            return
        postprocessing.plot_porous_materials(result)
        result = processing.study_sommerfeld_open_air_vs_reflexive(
            N_POINTS, FREQUENCES_HZ, SOURCE, CAR_MAT, ALPHA0, C,
        )
        if result is None:
            return
        postprocessing.plot_sommerfeld_comparison(result)
        depths = numpy.linspace(0.5, 1.5, 201)
        result = processing.study_boundary_depth_dependence(depths, 200.0, SOURCE, C)
        postprocessing.plot_boundary_depth_dependence(result)
        result = processing.validate_adjoint_gradient(
            N_POINTS, 12, OMEGA, SOURCE, CAR_MAT, ALPHA0, C,
        )
        if result is None:
            return
        postprocessing.plot_gradient_validation(result)
    if selection in ("monofrequence", "tous"):
        result = processing.study_spectra_and_single_frequency_placement(
            N_POINTS, FREQUENCES_HZ, N_ITERATIONS, FRACTION_GARNIE,
            SOURCE, CAR_MAT, ALPHA0, C,
        )
        if result is None:
            return
        postprocessing.plot_spectra_and_single_frequency_placement(result)
    if selection in ("multifrequence", "tous"):
        result = processing.study_multifrequency_placement_and_coverage(
            N_POINTS, FREQUENCES_HZ, N_ITERATIONS, FRACTION_GARNIE,
            QUANTITES, SOURCE, CAR_MAT, ALPHA0, C,
        )
        if result is None:
            return
        postprocessing.plot_multifrequency_placement_and_coverage(result)
    if selection in ("comparaison_dispositifs", "tous"):
        reference = processing.compare_absorber_configurations(
            N_POINTS, FREQUENCES_HZ, N_ITERATIONS, FRACTION_GARNIE,
            SOURCE, CAR_MAT, ALPHA0, C, MATERIAUX_A_COMPARER,
        )
        if reference is None:
            return
        postprocessing.plot_absorber_configuration_comparison(reference)
        fixed_budget = processing.compare_absorber_configurations(
            N_POINTS, FREQUENCES_HZ, N_ITERATIONS, FRACTION_GARNIE,
            SOURCE, CAR_MAT, ALPHA0, C, MATERIAUX_A_COMPARER,
            fixed_covered_nodes=int(round(FRACTION_GARNIE * N_POINTS)),
        )
        if fixed_budget is None:
            return
        combined = processing.combine_comparable_configurations(reference, fixed_budget)
        postprocessing.plot_fixed_budget_comparison(combined)


if __name__ == '__main__' and ETUDE == 'demo':

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = N_POINTS  # On reprend la résolution choisie au début du fichier.
    M = 2 * N  # number of points along y-axis
    level = 2 # level of the fractal
    spacestep = 1.0 / N  # mesh size

    # -- set parameters of the partial differential equation
    omega = OMEGA
    c = C
    wavenumber = omega / c

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
    # On repère les positions le long du bord supérieur.
    y_source = (numpy.arange(N) - (N - 1) / 2) * spacestep
    f_dir[:, :] = 0.0
    f_dir[0, :] = SOURCE(y_source, omega)

    # -- define material density matrix
    chi = preprocessing._set_chi(M, N, x, y)
    chi = preprocessing.set2zero(chi, domain_omega)

    # On identifie le coefficient avant de résoudre le problème acoustique.
    coefficients, success, message = compute_alpha(omega, SOURCE, CAR_MAT, ALPHA0)
    if not success:
        sys.exit("Échec du calcul du coefficient : " + str(message))
    Alpha = coefficients[0] + 1j * coefficients[1]
    print("Coefficient du matériau :", Alpha)
    alpha_rob = Alpha * chi

    # -- set parameters for optimization
    S = 0  # surface of the fractal
    for i in range(0, M):
        for j in range(0, N):
            if domain_omega[i, j] == _env.NODE_ROBIN:
                S += 1
    V_0 = 1  # initial volume of the domain
    V_obj = numpy.sum(numpy.sum(chi)) / S  # constraint on the density
    mu = 5  # initial gradient step
    mu1 = 10**(-5)  # parameter of the volume functional

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
    # On améliore la répartition avec la source et le matériau choisis.
    chi, energy, u, grad = your_optimization_procedure(
        domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        Alpha, mu, chi, V_obj,
    )

    chin = chi.copy()
    un = u.copy()

    # -- plot chi, u, and energy
    postprocessing._plot_uncontroled_solution(u0, chi0)
    # On masque le bord et l’extérieur, dont la pression n’est pas renvoyée.
    initial_pressure = numpy.ma.masked_where(
        domain_omega != _env.NODE_INTERIOR, numpy.abs(u0)
    )
    postprocessing.myimshow(
        initial_pressure[:int(max(y)) + 2],
        title="Module de la pression initiale", colorbar=True,
        cmap="viridis", filename=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "fig_u0_module.png"
        ),
    )
    postprocessing._plot_controled_solution(un, chin)
    err = un - u0
    postprocessing._plot_error(err)
    postprocessing._plot_energy_history(energy)

    # On conserve la répartition initiale pour la courbe fréquentielle de référence.
    # On couvre les trois composantes de la source avec la même grille.
    frequencies_hz = FREQUENCES_HZ
    results = processing.run_rer_b_frequency_sweep(
        domain_omega, spacestep, frequencies_hz,
        f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
        chi0, SOURCE, CAR_MAT, ALPHA0, sound_speed_m_s=C,
    )
    # On enregistre les deux courbes dans le dossier de ce programme.
    if results is not None:
        postprocessing.plot_rer_b_frequency_sweep(results, SOURCE)

    print('End.')


if __name__ == "__main__" and ETUDE == "trois_pics":
    run_three_peaks_optimization()

if __name__ == "__main__" and ETUDE == "spectre_complet":
    run_full_spectrum_optimization()

if __name__ == "__main__" and ETUDE not in ("demo", "trois_pics", "spectre_complet"):
    run_studies(ETUDE)
