# -*- coding: utf-8 -*-


# Python packages
import numpy
import os
import sys


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
CAR_MAT = MATERIAUX["LAINE_ROCHE"]
ALPHA0 = [50.0, -50.0]  # On donne les parties réelle et imaginaire du point initial.
OMEGA = 3430.0  # On exprime la pulsation en radians par seconde.
C = 343.0  # On exprime la célérité en mètres par seconde.

# On choisit une étude ou l’ensemble des comparaisons.
# Les choix sont demo, trois_pics, materiaux_validation, monofrequence,
# multifrequence, comparaison_dispositifs et tous.
ETUDE = "demo"
N_POINTS = 128
FREQUENCES_HZ = numpy.arange(50.0, 3501.0, 50.0)
N_ITERATIONS = 80
FRACTION_GARNIE = 0.30
QUANTITES = [0.10, 0.30, 0.50, 0.70, 1.0]
MATERIAUX_A_COMPARER = ["LAINE_ROCHE", "MELAMINE", "LAINE_VERRE"]


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



def your_optimization_procedure_three_peaks(
    domain_omega, spacestep, chi, V_obj,
    f=None, f_neu=None, f_rob=None,
    beta_pde=None, alpha_pde=None, alpha_dir=None, beta_neu=None, beta_rob=None,
    source=preprocessing.source_rer_b, car_mat=CAR_MAT, alpha0=ALPHA0,
    sound_speed_m_s=C, mu=5.0, numb_iter=N_ITERATIONS, alphas=None,
):
    """Minimise J_200(chi) + J_800(chi) + J_2500(chi) avec un seul mur chi.

    Les trois fréquences viennent des centres de preprocessing.RER_B_GAUSSIANS.
    La source est évaluée à chaque pulsation. Si alphas est omis, Alpha est
    identifié une fois par fréquence et conservé pendant la descente.

    Renvoie un dictionnaire avec chi binaire, chi relaxé, les historiques des
    trois coûts et de leur somme, les trois champs finaux et le gradient total.
    La dernière ligne des historiques est le coût APRES le tri binaire.
    """
    frequencies_hz = numpy.array(
        [centre for centre, largeur, poids in preprocessing.RER_B_GAUSSIANS],
        dtype=numpy.float64,
    )
    wavenumbers = 2.0 * numpy.pi * frequencies_hz / sound_speed_m_s
    if sound_speed_m_s / (frequencies_hz.max() * spacestep) < 10.0:
        print("Attention : moins de 10 points de maillage par longueur d'onde à 2500 Hz.")

    if len(frequencies_hz) != 3:
        raise ValueError("La source RER B doit comporter exactement trois gaussiennes.")
    if not (0.0 <= V_obj <= 1.0):
        raise ValueError("V_obj doit être compris entre 0 et 1.")

    if alphas is None:
        alphas = processing.compute_material_coefficients(
            frequencies_hz, source, car_mat, alpha0,
        )
        if alphas is None:
            raise ValueError("Impossible d'identifier Alpha aux trois fréquences.")
    alphas = numpy.asarray(alphas, dtype=numpy.complex128)
    if alphas.shape != (3,) or not numpy.all(numpy.isfinite(alphas)):
        raise ValueError("Il faut trois coefficients Alpha complexes finis.")

    solver = processing.FastHelmholtzSolver(
        domain_omega, spacestep, f=f, f_neu=f_neu, f_rob=f_rob,
        beta_pde=beta_pde, alpha_pde=alpha_pde, alpha_dir=alpha_dir,
        beta_neu=beta_neu, beta_rob=beta_rob,
    )
    chi = project_density(chi, domain_omega, V_obj)
    mu = float(mu)

    def evaluate(distribution, with_gradient=False):
        """Calcule les trois J, leur gradient total éventuel, et les trois champs."""
        energies = numpy.zeros(3, dtype=numpy.float64)
        total_gradient = numpy.zeros(domain_omega.shape, dtype=numpy.float64)
        fields = {}
        for index, (frequency, wavenumber, Alpha) in enumerate(
            zip(frequencies_hz, wavenumbers, alphas)
        ):
            omega = 2.0 * numpy.pi * frequency
            solver.set_source(source, omega)
            if with_gradient:
                u, p = solver.solve_state_and_adjoint(wavenumber, Alpha * distribution)
                total_gradient += solver.compute_gradient(u, p, distribution, Alpha)
            else:
                u = solver.solve(wavenumber, Alpha * distribution)
            energies[index] = solver.compute_energy(u)
            fields[float(frequency)] = u
        return energies, total_gradient, fields

    initial_energies, _, _ = evaluate(chi)
    history_by_frequency = [initial_energies]
    history_total = [float(numpy.sum(initial_energies))]

    for iteration in range(numb_iter):
        if mu <= 1e-5:
            break
        current_energies, gradient_total, _ = evaluate(chi, with_gradient=True)
        current_total = float(numpy.sum(current_energies))
        accepted = False

        while mu > 1e-5:
            descent = chi - mu * gradient_total
            candidate = project_density(descent, domain_omega, V_obj)
            candidate_energies, _, _ = evaluate(candidate)
            candidate_total = float(numpy.sum(candidate_energies))

            if numpy.isfinite(candidate_total) and candidate_total < current_total:
                variation = numpy.max(numpy.abs(candidate - chi))
                chi = candidate
                history_by_frequency.append(candidate_energies)
                history_total.append(candidate_total)
                mu = mu * 1.1
                accepted = True
                break
            mu = mu / 2.0

        if not accepted:
            break
        print(f"3 pics - étape {iteration + 1} : J_total = {history_total[-1]:.6g}")
        if variation < 1e-7:
            break

    chi_relaxed = chi.copy()
    chi_binary = preprocessing.binarize_chi(chi_relaxed, domain_omega, V_obj)

    # Après le passage en binaire, on recalcule les trois champs et gradients.
    final_energies, final_gradient, final_fields = evaluate(chi_binary, with_gradient=True)
    history_by_frequency.append(final_energies)
    history_total.append(float(numpy.sum(final_energies)))

    return {
        "frequencies_hz": frequencies_hz,
        "alphas": alphas,
        "chi": chi_binary,
        "chi_relaxed": chi_relaxed,
        "energy_history": numpy.asarray(history_total, dtype=numpy.float64).reshape(-1, 1),
        "energy_by_frequency": numpy.asarray(history_by_frequency, dtype=numpy.float64),
        "fields_by_frequency": final_fields,
        "gradient": final_gradient,
    }

def your_compute_objective_function(domain_omega, u, spacestep):
    """On calcule le critère à partir du module de pression sur les points intérieurs."""
    interior_values = numpy.asarray(u)[domain_omega == _env.NODE_INTERIOR]
    return float(spacestep**2 * numpy.sum(numpy.abs(interior_values)**2))


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

    energies = result["energy_history"][:, 0]
    components = result["energy_by_frequency"]
    print("Fréquences étudiées (Hz) :", result["frequencies_hz"])
    print("Coût initial :", energies[0])
    print("Coût relaxé final :", energies[-2])
    print("Coût binaire final :", energies[-1])
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
        selected = processing.evaluate_selected_configuration(combined, SOURCE, C)
        postprocessing.plot_selected_configuration(selected)


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

if __name__ == "__main__" and ETUDE not in ("demo", "trois_pics"):
    run_studies(ETUDE)
