# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import numpy
import os
import scipy.sparse.linalg


# MRG packages
import _env
import preprocessing
import processing
import postprocessing
#import solutions


def your_optimization_procedure(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, mu, chi, V_obj):
    """On répartit une quantité fixée de matériau pour réduire le critère.

    On renvoie la répartition, les coûts acceptés, le champ et le gradient final.
    Le paramètre omega reçoit le nombre d'onde du solveur.
    """
    # On prépare la répartition initiale, son champ et son gradient.
    chi = project_density(chi, domain_omega, V_obj)
    matrix, state, u, value = compute_state(
        domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi,
    )
    grad = compute_gradient(
        domain_omega, spacestep, Alpha, chi, beta_pde, beta_rob, f_rob, matrix, state,
    )
    energy = [value]

    for _ in range(100):
        projected = project_density(chi - grad, domain_omega, V_obj)
        if numpy.max(numpy.abs(projected - chi)) <= 1e-7:
            break

        # On réduit le pas jusqu'à obtenir une diminution suffisante du critère.
        step = mu
        while step >= 1e-5:
            candidate = project_density(chi - step * grad, domain_omega, V_obj)
            candidate_matrix, candidate_state, candidate_u, candidate_value = compute_state(
                domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * candidate,
            )
            limit = value + 1e-4 * numpy.sum(grad * (candidate - chi))
            if numpy.isfinite(candidate_value) and candidate_value <= limit:
                chi, u, value = candidate, candidate_u, candidate_value
                matrix, state = candidate_matrix, candidate_state
                energy.append(value)
                break
            step /= 2.0

        if step < 1e-5:
            break

        # On actualise le gradient après chaque étape acceptée.
        grad = compute_gradient(
            domain_omega, spacestep, Alpha, chi, beta_pde, beta_rob, f_rob, matrix, state,
        )
        mu = 1.1 * step

    return chi, numpy.asarray(energy, dtype=numpy.float64).reshape(-1, 1), u, grad


def your_compute_objective_function(domain_omega, u, spacestep):
    """On calcule le critère à partir du module de pression sur les points intérieurs."""
    interior_values = numpy.asarray(u)[domain_omega == _env.NODE_INTERIOR]
    return float(spacestep**2 * numpy.sum(numpy.abs(interior_values)**2))


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
    """On assemble le système fourni et on renvoie le champ avec son coût."""
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
    value = your_compute_objective_function(domain_omega, field, spacestep)
    if not numpy.all(numpy.isfinite(state)):
        value = numpy.inf
    return matrix, state, field, value


def compute_gradient(domain_omega, spacestep, Alpha, density,
                     beta_pde, beta_rob, f_rob, matrix, state):
    """On calcule l'effet de chaque point du mur à l'aide du champ adjoint."""
    interior = domain_omega == _env.NODE_INTERIOR
    robin = domain_omega == _env.NODE_ROBIN
    ncols = domain_omega.shape[1]

    # On résout le problème adjoint avec le champ dans le fluide.
    adjoint_rhs = numpy.zeros_like(state)
    adjoint_rhs[interior.ravel()] = 2.0 * spacestep**2 * state[interior.ravel()]
    adjoint = scipy.sparse.linalg.spsolve(matrix.conjugate().transpose(), adjoint_rhs)

    # On additionne les contributions des voisins intérieurs de chaque point Robin.
    gradient = numpy.zeros(domain_omega.shape, dtype=numpy.float64)
    for i, j in zip(*numpy.nonzero(interior)):
        row = i * ncols + j
        for bi, bj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            if robin[bi, bj]:
                scale = spacestep * Alpha / beta_pde[i, j]
                denominator = beta_rob[bi, bj] - scale * density[bi, bj]
                diagonal_derivative = scale * beta_rob[bi, bj] / denominator**2
                rhs_derivative = spacestep * f_rob[bi, bj] * scale / denominator**2
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
    kx = -1.0
    ky = -1.0
    wavenumber = numpy.sqrt(kx**2 + ky**2)  # wavenumber
    wavenumber = 10.0

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
    # -- define boundary conditions
    # planar wave defined on top
    f_dir[:, :] = 0.0
    f_dir[0, 0:N] = 1.0
    # spherical wave defined on top
    #f_dir[:, :] = 0.0
    #f_dir[0, int(N/2)] = 10.0

    # -- initialize
    alpha_rob[:, :] = - wavenumber * 1j

    # -- define material density matrix
    chi = preprocessing._set_chi(M, N, x, y)
    chi = preprocessing.set2zero(chi, domain_omega)

    # -- define absorbing material
    Alpha = 10.0 - 10.0 * 1j
    # -- this is the function you have written during your project
    #import compute_alpha
    #Alpha = compute_alpha.compute_alpha(...)
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
    # On améliore la répartition avec le coefficient provisoire du matériau.
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
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi0,
    )
    # On enregistre les deux courbes dans le dossier de ce programme.
    postprocessing.plot_rer_b_frequency_sweep(results)

    print('End.')
