# -*- coding: utf-8 -*-


# Python packages
import numpy
import scipy
import scipy.sparse
import scipy.sparse.linalg


# MRG packages
import _env
import preprocessing
from preprocessing import set2zero, replace_old_by_new


def is_in_interior_domain(node):
    """
    :param node: node of the grid
    :type node: int64
    :return: boolean
    :rtype: boolean
    """

    if node == _env.NODE_INTERIOR:
        return True
    else:
        return False  # ..warning: can be on the frontier


def is_on_dirichlet_boundary(node):
    """
    :param node: node of the grid
    :type node: int64
    :return: boolean
    :rtype: boolean
    """

    if node == _env.NODE_DIRICHLET:
        return True
    else:
        return False


def is_on_neumann_boundary(node):
    """
    :param node: node of the grid
    :type node: int64
    :return: boolean
    :rtype: boolean
    """

    if node == _env.NODE_NEUMANN:
        return True
    else:
        return False


def is_on_robin_boundary(node):
    """
    :param node: node of the grid
    :type node: int64
    :return: boolean
    :rtype: boolean
    """

    if node == _env.NODE_ROBIN:
        return True
    else:
        return False


def is_on_liner_a_boundary(node):
    """
    :param node: node of the grid
    :type node: int64
    :return: boolean
    :rtype: boolean
    """

    if node == _env.NODE_LINER_A:
        return True
    else:
        return False


def is_on_liner_b_boundary(node):
    """
    :param node: node of the grid
    :type node: int64
    :return: boolean
    :rtype: boolean
    """

    if node == _env.NODE_LINER_B:
        return True
    else:
        return False


def compute_stiffness_matrix(domain, space_step, f, beta_pde):
    """
    This function generates the stiffness matrix.

    :param domain:
    :param space_step:
    :param f:
    :param beta_pde:
    :return:
    """

    h = space_step
    (M, N) = numpy.shape(domain)
    K = M * N
    mat = scipy.sparse.lil_matrix((K, K), dtype=numpy.complex128)
    rhs = numpy.zeros((K, 1), dtype=numpy.complex128)
    for i in range(0, M):
        for j in range(0, N):
            row = i * N + j
            if is_in_interior_domain(domain[i, j]):
                mat[row, row] = -4.0 * beta_pde[i, j]
                mat[row, row - 1] = 1.0 * beta_pde[i, j - 1]
                mat[row, row + 1] = 1.0 * beta_pde[i, j + 1]
                mat[row, row + N] = 1.0 * beta_pde[i + 1, j]
                mat[row, row - N] = 1.0 * beta_pde[i - 1, j]
                rhs[row] = h ** 2 * f[i, j]
            else:
                mat[row, row] = 1.0
                rhs[row] = 0.0

    return mat, rhs


def compute_mass_matrix(domain, space_step, alpha_pde):
    """
    This function generates the mass matrix.

    :param domain:
    :param space_step:
    :param alpha_pde:
    :return:
    """

    h = space_step
    (M, N) = numpy.shape(domain)
    K = M * N
    mat = scipy.sparse.lil_matrix((K, K), dtype=numpy.complex128)
    rhs = numpy.zeros((K, 1), dtype=numpy.complex128)
    for i in range(0, M):
        for j in range(0, N):
            row = i * N + j
            if is_in_interior_domain(domain[i, j]):
                mat[row, row] = 1.0 * h ** 2 * alpha_pde[i, j]

    return mat, rhs


def compute_vgradu_matrix(domain, space_step, v):
    h = space_step
    (M, N) = numpy.shape(domain)
    K = M * N
    mat = scipy.sparse.lil_matrix((K, K), dtype=numpy.complex128)
    rhs = numpy.zeros((K, 1), dtype=numpy.complex128)
    for i in range(0, M):
        for j in range(0, N):
            row = i * N + j
            if is_in_interior_domain(domain[i, j]):
                mat[row, row] = - 2.0 * h * (v[i, j, 0] + v[i, j, 1])
                mat[row, row + 1] = h * v[i, j, 0]
                mat[row, row + N] = h * v[i, j, 1]
                if not is_in_interior_domain(domain[i + 1, j]):
                    mat[row, row] = 2.0 * h * (v[i, j, 0] - v[i, j, 1])
                    mat[row, row + 1] = 0.0
                    mat[row, row - 1] = -h * v[i, j, 0]
                if not is_in_interior_domain(domain[i, j + 1]):
                    mat[row, row] = 2.0 * h * (-v[i, j, 0] + v[i, j, 1])
                    mat[row, row + N] = 0.0
                    mat[row, row - N] = -h * v[i, j, 1]
            else:
                pass

    return mat, rhs


def compute_dirichlet_condition(domain, f_dir, alpha_dir, beta_pde, mat, rhs):
    """
    This function generate the dirichlet boundary condition.

    :param domain:
    :param g:
    :param alpha_dir:
    :param beta_pde:
    :param mat:
    :param rhs:
    :return:
    """

    (M, N) = numpy.shape(domain)
    for i in range(0, M):
        for j in range(0, N):
            # the interior domain AND the frontiers have to be strictly inside of domain
            if is_in_interior_domain(domain[i, j]):
                north = is_on_dirichlet_boundary(domain[i - 1, j])
                south = is_on_dirichlet_boundary(domain[i + 1, j])
                east = is_on_dirichlet_boundary(domain[i, j + 1])
                west = is_on_dirichlet_boundary(domain[i, j - 1])
                row = i * N + j
                if north:
                    mat[row, row - N] -= beta_pde[i - 1, j]
                    rhs[row] += -f_dir[i - 1, j] / alpha_dir[i - 1, j]
                if south:
                    mat[row, row + N] -= beta_pde[i + 1, j]
                    rhs[row] += -f_dir[i + 1, j] / alpha_dir[i + 1, j]
                if east:
                    mat[row, row + 1] -= beta_pde[i, j + 1]
                    rhs[row] += -f_dir[i, j + 1] / alpha_dir[i, j + 1]
                if west:
                    mat[row, row - 1] -= beta_pde[i, j - 1]
                    rhs[row] += -f_dir[i, j - 1] / alpha_dir[i, j - 1]

    return mat, rhs


def compute_neumann_condition(domain, space_step, f_neu, beta_neu, beta_pde, mat, rhs):
    """
    This function generate the neumann boundary condition.

    :param domain:
    :param space_step:
    :param s_N:
    :param beta_neu:
    :param beta_pde:
    :param mat:
    :param rhs:
    :return:
    """

    h = space_step
    (M, N) = numpy.shape(domain)
    for i in range(0, M):
        for j in range(0, N):
            # the interior domain AND the frontiers have to be strictly inside of domain
            if is_in_interior_domain(domain[i, j]):
                north = is_on_neumann_boundary(domain[i - 1, j])
                south = is_on_neumann_boundary(domain[i + 1, j])
                east = is_on_neumann_boundary(domain[i, j + 1])
                west = is_on_neumann_boundary(domain[i, j - 1])
                row = i * N + j
                if north:
                    mat[row, row - N] -= beta_pde[i - 1, j]
                    mat[row, row] += beta_pde[i, j]
                    rhs[row] += h * f_neu[i - 1, j] / beta_neu[i - 1, j]
                if south:
                    mat[row, row + N] -= beta_pde[i + 1, j]
                    mat[row, row] += beta_pde[i, j]
                    rhs[row] += h * f_neu[i + 1, j] / beta_neu[i + 1, j]
                if east:
                    mat[row, row + 1] -= beta_pde[i, j + 1]
                    mat[row, row] += beta_pde[i, j]
                    rhs[row] += h * f_neu[i, j + 1] / beta_neu[i, j + 1]
                if west:
                    mat[row, row - 1] -= beta_pde[i, j - 1]
                    mat[row, row] += beta_pde[i, j]
                    rhs[row] += h * f_neu[i, j - 1] / beta_neu[i, j - 1]

    return mat, rhs


def compute_robin_condition(domain, space_step, f_rob, alpha_rob, beta_rob, beta_pde, mat, rhs):
    """
    On assemble la condition de Robin avec le signe du polycopié.

    :param domain:
    :param space_step:
    :param f_rob:
    :param alpha_rob:
    :param beta_rob:
    :param beta_pde:
    :param mat:
    :param rhs:
    :return:
    """

    h = space_step
    (M, N) = numpy.shape(domain)
    for i in range(0, M):
        for j in range(0, N):
            # the interior domain AND the frontiers have to be strictly inside of domain
            if is_in_interior_domain(domain[i, j]):
                north = is_on_robin_boundary(domain[i - 1, j])
                south = is_on_robin_boundary(domain[i + 1, j])
                east = is_on_robin_boundary(domain[i, j + 1])
                west = is_on_robin_boundary(domain[i, j - 1])
                row = i * N + j
                if north:
                    mat[row, row - N] -= beta_pde[i - 1, j]
                    mat[row, row] += beta_pde[i, j] - (alpha_rob[i - 1, j] / beta_pde[i, j]) * h / (
                            beta_rob[i - 1, j] + (alpha_rob[i - 1, j] / beta_pde[i, j] * h))
                    rhs[row] += (h / (beta_rob[i - 1, j] + ((alpha_rob[i - 1, j] / beta_pde[i, j]) * h))) * f_rob[
                        i - 1, j]
                if south:
                    mat[row, row + N] -= beta_pde[i + 1, j]
                    mat[row, row] += beta_pde[i, j] - (alpha_rob[i + 1, j] / beta_pde[i, j]) * h / (
                            beta_rob[i + 1, j] + (alpha_rob[i + 1, j] / beta_pde[i, j] * h))
                    rhs[row] += (h / (beta_rob[i + 1, j] + ((alpha_rob[i + 1, j] / beta_pde[i, j]) * h))) * f_rob[
                        i + 1, j]
                if east:
                    mat[row, row + 1] -= beta_pde[i, j + 1]
                    mat[row, row] += beta_pde[i, j] - (alpha_rob[i, j + 1] / beta_pde[i, j]) * h / (
                            beta_rob[i, j + 1] + (alpha_rob[i, j + 1] / beta_pde[i, j] * h))
                    rhs[row] += (h / (beta_rob[i, j + 1] + ((alpha_rob[i, j + 1] / beta_pde[i, j]) * h))) * f_rob[
                        i, j + 1]
                if west:
                    mat[row, row - 1] -= beta_pde[i, j - 1]
                    mat[row, row] += beta_pde[i, j] - (alpha_rob[i, j - 1] / beta_pde[i, j]) * h / (
                            beta_rob[i, j - 1] + (alpha_rob[i, j - 1] / beta_pde[i, j] * h))
                    rhs[row] += (h / (beta_rob[i, j - 1] + ((alpha_rob[i, j - 1] / beta_pde[i, j]) * h))) * f_rob[
                        i, j - 1]

    return mat, rhs


def solve_helmholtz(domain, space_step, omega,
                    f, f_dir, f_neu, f_rob,
                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                    prepared=None):
    """On résout le système complet et on renvoie le champ sur la grille."""
    _, _, field = compute_state(
        domain, space_step, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        prepared=prepared,
    )
    return field



def compute_robin_condition_down(domain, u, space_step, beta_rob, alpha_rob):
    """On évalue la condition de Robin avec la normale extérieure et la pression moyenne.

    :param domain:
    :param u:
    :param space_step:
    :param beta_rob:
    :param alpha_rob:
    :return:
    """

    h = space_step
    (M, N) = numpy.shape(domain)
    value = numpy.zeros((M, N), dtype=numpy.complex128)
    for i in range(0, M):
        for j in range(0, N):
            if is_in_interior_domain(domain[i, j]):
                north = is_on_robin_boundary(domain[i - 1, j])
                south = is_on_robin_boundary(domain[i + 1, j])
                east = is_on_robin_boundary(domain[i, j + 1])
                west = is_on_robin_boundary(domain[i, j - 1])
                if north:
                    value[i - 1, j] += beta_rob[i - 1, j] * (u[i - 1, j] - u[i, j]) / h + alpha_rob[
                        i - 1, j] * (u[i - 1, j] + u[i, j]) / 2
                if south:
                    value[i + 1, j] += beta_rob[i + 1, j] * (u[i + 1, j] - u[i, j]) / h + alpha_rob[
                        i + 1, j] * (u[i + 1, j] + u[i, j]) / 2
                if east:
                    value[i, j + 1] += beta_rob[i, j + 1] * (u[i, j + 1] - u[i, j]) / h + alpha_rob[
                        i, j + 1] * (u[i, j + 1] + u[i, j]) / 2
                if west:
                    value[i, j - 1] += beta_rob[i, j - 1] * (u[i, j - 1] - u[i, j]) / h + alpha_rob[
                        i, j - 1] * (u[i, j - 1] + u[i, j]) / 2

    return value



def compute_robin_condition_up(domain, u, space_step, beta_rob, alpha_rob):
    """On évalue la condition de Robin avec la normale extérieure et la pression moyenne.

    :param domain:
    :param u:
    :param space_step:
    :param beta_rob:
    :param alpha_rob:
    :return:
    """

    h = space_step
    (M, N) = numpy.shape(domain)
    value = numpy.zeros((M, N), dtype=numpy.complex128)
    #for i in range(M - 1, -1, -1):  # la frontière est sur un bord donc on ne regarde que
        # les points qui sont strictement à l'intérieur (i.e d'où le 2:M-2 et 2:N-2)
    #    for j in range(N - 1, -1, -1):
    for i in range(0, M):
        for j in range(0, N):
            if is_in_interior_domain(domain[i, j]):
                north = is_on_robin_boundary(domain[i - 1, j])
                south = is_on_robin_boundary(domain[i + 1, j])
                east = is_on_robin_boundary(domain[i, j + 1])
                west = is_on_robin_boundary(domain[i, j - 1])
                if north:
                    value[i - 1, j] += beta_rob[i - 1, j] * (u[i - 1, j] - u[i, j]) / h + alpha_rob[
                        i - 1, j] * (u[i - 1, j] + u[i, j]) / 2
                if south:
                    value[i + 1, j] += beta_rob[i + 1, j] * (u[i + 1, j] - u[i, j]) / h + alpha_rob[
                        i + 1, j] * (u[i + 1, j] + u[i, j]) / 2
                if east:
                    value[i, j + 1] += beta_rob[i, j + 1] * (u[i, j + 1] - u[i, j]) / h + alpha_rob[
                        i, j + 1] * (u[i, j + 1] + u[i, j]) / 2
                if west:
                    value[i, j - 1] += beta_rob[i, j - 1] * (u[i, j - 1] - u[i, j]) / h + alpha_rob[
                        i, j - 1] * (u[i, j - 1] + u[i, j]) / 2

    return value



def prepare_helmholtz_system(domain_omega, spacestep, f, f_neu,
                             beta_pde, alpha_pde, beta_neu):
    """On conserve les matrices fournies et les données de Neumann qui restent fixes."""
    stiffness, rhs = compute_stiffness_matrix(domain_omega, spacestep, f, beta_pde)
    mass, _ = compute_mass_matrix(domain_omega, spacestep, alpha_pde)
    stiffness, rhs = compute_neumann_condition(
        domain_omega, spacestep, f_neu, beta_neu, beta_pde, stiffness, rhs,
    )
    return stiffness, mass, rhs



def assemble_helmholtz_system(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                              beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                              prepared=None):
    """On complète les matrices fournies avec la source et le coefficient du mur."""
    if prepared is None:
        prepared = prepare_helmholtz_system(
            domain_omega, spacestep, f, f_neu, beta_pde, alpha_pde, beta_neu,
        )
    stiffness, mass, fixed_rhs = prepared
    # On conserve les matrices préparées pour les prochains calculs.
    matrix = (stiffness + omega**2 * mass).tolil()
    rhs = fixed_rhs.copy()
    # On applique les conditions de Dirichlet et de Robin fournies.
    matrix, rhs = compute_dirichlet_condition(
        domain_omega, f_dir, alpha_dir, beta_pde, matrix, rhs,
    )
    matrix, rhs = compute_robin_condition(
        domain_omega, spacestep, f_rob, alpha_rob, beta_rob, beta_pde, matrix, rhs,
    )
    return matrix.tocsr(), rhs.ravel()


def compute_state(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                  beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                  prepared=None):
    """On résout le système complet puis on remet le champ sur la grille."""
    matrix, rhs = assemble_helmholtz_system(
        domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        prepared=prepared,
    )
    state = scipy.sparse.linalg.spsolve(matrix, rhs)
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

