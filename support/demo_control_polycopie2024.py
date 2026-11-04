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
# Les choix sont demo, materiaux_validation, monofrequence,
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


def your_compute_objective_function(domain_omega, u, spacestep):
    """On calcule le critère à partir du module de pression sur les points intérieurs."""
    interior_values = numpy.asarray(u)[domain_omega == _env.NODE_INTERIOR]
    return float(spacestep**2 * numpy.sum(numpy.abs(interior_values)**2))


# Les deux noms désignent le même calcul du coût.
compute_objective_function = your_compute_objective_function


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
        result = processing.compare_absorber_configurations(
            N_POINTS, FREQUENCES_HZ, N_ITERATIONS, FRACTION_GARNIE,
            SOURCE, CAR_MAT, ALPHA0, C, MATERIAUX_A_COMPARER,
        )
        if result is None:
            return
        postprocessing.plot_absorber_configuration_comparison(result)


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


if __name__ == "__main__" and ETUDE != "demo":
    run_studies(ETUDE)
