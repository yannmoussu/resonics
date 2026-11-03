# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import numpy
import os
import sys
import scipy.sparse.linalg


# MRG packages
import _env
import preprocessing
import processing
import postprocessing
from compute_alpha import compute_alpha, MATERIAUX


# On choisit la source commune au champ initial, à la descente et aux fréquences.
SOURCE = preprocessing.source_rer_b
# SOURCE = preprocessing.source_constant
CAR_MAT = MATERIAUX["LAINE_ROCHE"]
ALPHA0 = [50.0, -50.0]  # On donne les parties réelle et imaginaire du point initial.
OMEGA = 3430.0  # On exprime la pulsation en radians par seconde.
C = 343.0  # On exprime la célérité en mètres par seconde.


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


def project_density(proposal, domain_omega, V_obj):
    """On borne les valeurs du mur en conservant la quantité de matériau imposée."""
    robin = domain_omega == _env.NODE_ROBIN
    values = proposal[robin]
    target = float(V_obj * numpy.count_nonzero(robin))
    projected = numpy.zeros(domain_omega.shape, dtype=numpy.float64)
    if target == 0:
        return projected
    if target == values.size:
        projected[robin] = 1.0
        return projected

    # On cherche le décalage commun par dichotomie.
    lower = float(values.min() - 1.0)
    upper = float(values.max())
    for _ in range(60):
        shift = (lower + upper) / 2.0
        if numpy.clip(values - shift, 0.0, 1.0).sum() > target:
            lower = shift
        else:
            upper = shift
    projected[robin] = numpy.clip(values - (lower + upper) / 2.0, 0.0, 1.0)
    return projected


def compute_state(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                  beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob):
    """On assemble le système fourni et on renvoie le champ calculé."""
    # On reprend les mêmes contributions que dans le solveur fourni.
    matrix, rhs = processing.compute_stiffness_matrix(domain_omega, spacestep, f, beta_pde)
    mass, _ = processing.compute_mass_matrix(domain_omega, spacestep, alpha_pde)
    matrix = matrix + omega**2 * mass
    matrix, rhs = processing.compute_dirichlet_condition(
        domain_omega, f_dir, alpha_dir, beta_pde, matrix, rhs,
    )
    matrix, rhs = processing.compute_neumann_condition(
        domain_omega, spacestep, f_neu, beta_neu, beta_pde, matrix, rhs,
    )
    matrix, rhs = processing.compute_robin_condition(
        domain_omega, spacestep, f_rob, alpha_rob, beta_rob, beta_pde, matrix, rhs,
    )
    matrix = matrix.tocsr()
    state = scipy.sparse.linalg.spsolve(matrix, rhs.ravel())
    interior = domain_omega == _env.NODE_INTERIOR
    field = numpy.zeros(domain_omega.shape, dtype=numpy.complex128)
    field[interior] = state.reshape(domain_omega.shape)[interior]
    return matrix, state, field


def compute_adjoint(domain_omega, spacestep, matrix, state):
    """On résout le système adjoint à partir du champ dans le fluide."""
    interior = domain_omega == _env.NODE_INTERIOR
    adjoint_rhs = numpy.zeros_like(state)
    adjoint_rhs[interior.ravel()] = 2.0 * spacestep**2 * state[interior.ravel()]
    return scipy.sparse.linalg.spsolve(matrix.conjugate().transpose(), adjoint_rhs)


def compute_gradient(domain_omega, spacestep, Alpha, density,
                     beta_pde, beta_rob, f_rob, adjoint, state):
    """On calcule l'effet de chaque point du mur à l'aide du champ adjoint."""
    interior = domain_omega == _env.NODE_INTERIOR
    robin = domain_omega == _env.NODE_ROBIN
    ncols = domain_omega.shape[1]

    # On additionne les contributions des voisins intérieurs de chaque point Robin.
    gradient = numpy.zeros(domain_omega.shape, dtype=numpy.float64)
    for i, j in zip(*numpy.nonzero(interior)):
        row = i * ncols + j
        for bi, bj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            if robin[bi, bj]:
                scale = spacestep * Alpha / beta_pde[i, j]
                denominator = beta_rob[bi, bj] + scale * density[bi, bj]
                diagonal_derivative = -scale * beta_rob[bi, bj] / denominator**2
                rhs_derivative = -spacestep * f_rob[bi, bj] * scale / denominator**2
                gradient[bi, bj] += numpy.real(
                    numpy.conjugate(adjoint[row])
                    * (rhs_derivative - diagonal_derivative * state[row])
                )
    return gradient


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = 128  # On affine la grille pour les hautes fréquences.
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
    frequencies_hz = numpy.arange(50.0, 3501.0, 50.0)
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
