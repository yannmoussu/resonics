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
    """On réduit l'énergie en répartissant une quantité fixée de matériau.

    On reçoit la géométrie, les données du problème, le coefficient du matériau,
    un pas initial et la répartition de départ. On renvoie la répartition finale,
    les énergies acceptées, le champ final et sa dérivée par rapport au matériau.
    La quantité imposée est une fraction des points du mur dans cette géométrie.
    Le paramètre omega reçoit le nombre d'onde utilisé par le solveur.
    """
    interior = domain_omega == _env.NODE_INTERIOR
    robin = domain_omega == _env.NODE_ROBIN
    if not numpy.any(robin):
        raise ValueError("Le domaine doit contenir une frontière Robin.")
    if not numpy.isfinite(spacestep) or spacestep <= 0:
        raise ValueError("Le pas spatial doit être positif et fini.")
    if not numpy.isfinite(mu) or mu <= 0:
        raise ValueError("Le pas de descente doit être positif et fini.")
    if not numpy.isfinite(V_obj) or not 0 <= V_obj <= 1:
        raise ValueError("La fraction de matériau doit être entre zéro et un.")
    if numpy.shape(chi) != numpy.shape(domain_omega) or not numpy.isrealobj(chi):
        raise ValueError("La répartition doit être un tableau réel de la taille du domaine.")
    if not numpy.all(numpy.isfinite(chi)) or not numpy.isfinite(Alpha):
        raise ValueError("La répartition et le coefficient doivent être finis.")
    if numpy.any(beta_pde[interior] == 0):
        raise ValueError("Le coefficient de diffusion doit être non nul dans le domaine.")

    target = float(V_obj * numpy.count_nonzero(robin))
    nrows, ncols = domain_omega.shape

    def project_density(proposal):
        """On borne la répartition et on retrouve la quantité de matériau imposée."""
        values = proposal[robin]
        projected = numpy.zeros(domain_omega.shape, dtype=numpy.float64)
        if target == 0:
            return projected
        if target == values.size:
            projected[robin] = 1.0
            return projected

        # On cherche par dichotomie le décalage commun aux valeurs du mur.
        lower = float(values.min() - 1.0)
        upper = float(values.max())
        for _ in range(60):
            shift = (lower + upper) / 2.0
            bounded = numpy.clip(values - shift, 0.0, 1.0)
            if bounded.sum() > target:
                lower = shift
            else:
                upper = shift
        projected[robin] = numpy.clip(values - (lower + upper) / 2.0, 0.0, 1.0)
        return projected

    def compute_state(density):
        """On assemble le système fourni et on calcule le champ et son énergie."""
        # On prépare le coefficient du mur sans modifier les données reçues.
        boundary_coefficient = numpy.zeros_like(alpha_rob, dtype=numpy.complex128)
        boundary_coefficient[robin] = Alpha * density[robin]

        # On reprend les mêmes contributions que dans le solveur fourni.
        matrix, rhs = processing.compute_stiffness_matrix(
            domain_omega, spacestep, f, beta_pde
        )
        mass, _ = processing.compute_mass_matrix(domain_omega, spacestep, alpha_pde)
        matrix = matrix + omega**2 * mass
        matrix, rhs = processing.compute_dirichlet_condition(
            domain_omega, f_dir, alpha_dir, beta_pde, matrix, rhs
        )
        matrix, rhs = processing.compute_neumann_condition(
            domain_omega, spacestep, f_neu, beta_neu, beta_pde, matrix, rhs
        )
        matrix, rhs = processing.compute_robin_condition(
            domain_omega, spacestep, f_rob, boundary_coefficient,
            beta_rob, beta_pde, matrix, rhs
        )
        matrix = matrix.tocsr()
        state = scipy.sparse.linalg.spsolve(matrix, rhs.ravel())
        field = numpy.zeros(domain_omega.shape, dtype=numpy.complex128)
        field[interior] = state.reshape(domain_omega.shape)[interior]
        if not numpy.all(numpy.isfinite(state)):
            return matrix, state, field, numpy.inf
        value = your_compute_objective_function(domain_omega, field, spacestep)
        return matrix, state, field, value

    def compute_gradient(matrix, state, density):
        """On utilise le champ adjoint pour calculer l'effet de chaque point du mur."""
        # On calcule le second membre adjoint à partir du champ dans le fluide.
        adjoint_rhs = numpy.zeros_like(state)
        adjoint_rhs[interior.ravel()] = 2.0 * spacestep**2 * state[interior.ravel()]
        adjoint = scipy.sparse.linalg.spsolve(matrix.conjugate().transpose(), adjoint_rhs)
        if not numpy.all(numpy.isfinite(adjoint)):
            raise ValueError("Le calcul adjoint n'a pas donné de champ fini.")

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
        if not numpy.all(numpy.isfinite(gradient)):
            raise ValueError("Le calcul de la dérivée n'a pas donné de valeurs finies.")
        return gradient

    # On démarre avec une copie admissible et son énergie réellement calculée.
    chi = project_density(numpy.array(chi, dtype=numpy.float64, copy=True))
    matrix, state, u, value = compute_state(chi)
    if not numpy.isfinite(value):
        raise ValueError("Le calcul initial n'a pas donné de champ fini.")
    grad = compute_gradient(matrix, state, chi)
    history = [value]
    stop_reason = "nombre maximal d'itérations atteint"

    # On cherche une amélioration en conservant les bornes et la quantité de matériau.
    for iteration in range(100):
        projected = project_density(chi - grad)
        if numpy.max(numpy.abs(projected - chi)) <= 1e-7:
            stop_reason = "variation projetée suffisamment petite"
            break

        step = mu
        accepted = False
        while step >= 1e-5:
            candidate = project_density(chi - step * grad)
            direction = candidate - chi
            candidate_matrix, candidate_state, candidate_u, candidate_value = compute_state(candidate)

            # On accepte seulement une diminution cohérente avec la direction calculée.
            sufficient_decrease = value + 1e-4 * numpy.sum(grad * direction)
            if numpy.isfinite(candidate_value) and candidate_value <= sufficient_decrease:
                accepted = True
                break
            step /= 2.0

        if not accepted:
            stop_reason = "pas de descente devenu trop petit"
            break

        # On conserve uniquement les étapes acceptées puis on actualise la dérivée.
        chi = candidate
        matrix, state, u, value = candidate_matrix, candidate_state, candidate_u, candidate_value
        history.append(value)
        grad = compute_gradient(matrix, state, chi)
        mu = 1.1 * step
        print("Itération", iteration + 1, ": énergie =", value)

    print("Arrêt de la descente :", stop_reason)
    energy = numpy.asarray(history, dtype=numpy.float64).reshape(-1, 1)
    return chi, energy, u, grad


def your_compute_objective_function(domain_omega, u, spacestep):
    """On calcule le critère à partir du module de pression sur les points intérieurs."""
    if numpy.shape(u) != numpy.shape(domain_omega):
        raise ValueError("Le champ et le domaine doivent avoir la même taille.")
    if not numpy.isfinite(spacestep) or spacestep <= 0:
        raise ValueError("Le pas spatial doit être positif et fini.")
    interior_values = numpy.asarray(u)[domain_omega == _env.NODE_INTERIOR]
    if not numpy.all(numpy.isfinite(interior_values)):
        raise ValueError("Le champ doit être fini sur les points intérieurs.")
    # On multiplie la somme des amplitudes au carré par l'aire représentée par un point.
    return float(spacestep**2 * numpy.sum(numpy.abs(interior_values)**2))


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = 50  # number of points along x-axis
    M = 2 * N  # number of points along y-axis
    level = 1 # level of the fractal
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
    # On limite les fréquences pour garder dix points par longueur d’onde.
    frequencies_hz = numpy.arange(100.0, 1501.0, 50.0)
    results = processing.run_rer_b_frequency_sweep(
        domain_omega, spacestep, frequencies_hz,
        f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi0,
    )
    # On enregistre les deux courbes dans le dossier de ce programme.
    postprocessing.plot_rer_b_frequency_sweep(results)

    print('End.')
