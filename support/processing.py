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



def boundary_neighbours(domain, boundary):
    """On repère chaque voisinage entre un point intérieur et le bord demandé."""
    ncols = domain.shape[1]
    i, j = numpy.nonzero(domain == _env.NODE_INTERIOR)
    rows, nodes = [], []
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        selected = domain[i + di, j + dj] == boundary
        rows.append(i[selected] * ncols + j[selected])
        nodes.append((i[selected] + di) * ncols + j[selected] + dj)
    return numpy.concatenate(rows), numpy.concatenate(nodes)


def prepare_helmholtz_system(domain_omega, spacestep, f, f_neu,
                             beta_pde, alpha_pde, beta_neu):
    """On prépare les matrices fournies et les voisinages qui restent fixes."""
    stiffness, rhs = compute_stiffness_matrix(domain_omega, spacestep, f, beta_pde)
    mass, _ = compute_mass_matrix(domain_omega, spacestep, alpha_pde)
    stiffness, rhs = compute_neumann_condition(
        domain_omega, spacestep, f_neu, beta_neu, beta_pde, stiffness, rhs,
    )
    dr, dn = boundary_neighbours(domain_omega, _env.NODE_DIRICHLET)
    rr, rn = boundary_neighbours(domain_omega, _env.NODE_ROBIN)
    # On supprime une seule fois les coefficients reliant le fluide aux points de bord.
    for rows, nodes in ((dr, dn), (rr, rn)):
        stiffness[rows, nodes] = 0.0
    diagonal = stiffness.diagonal()
    numpy.add.at(diagonal, rr, beta_pde.ravel()[rr])
    stiffness.setdiag(diagonal)
    return {"stiffness": stiffness.tocsr(), "mass": mass.tocsr(), "rhs": rhs.ravel(),
            "dir_rows": dr, "dir_nodes": dn, "rob_rows": rr, "rob_nodes": rn}


def assemble_helmholtz_system(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                              beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                              prepared=None):
    """On applique les mêmes conditions de bord à tous les voisinages repérés."""
    if prepared is None:
        prepared = prepare_helmholtz_system(
            domain_omega, spacestep, f, f_neu, beta_pde, alpha_pde, beta_neu,
        )
    matrix = prepared["stiffness"] + omega**2 * prepared["mass"]
    rhs = prepared["rhs"].copy()
    dr, dn = prepared["dir_rows"], prepared["dir_nodes"]
    rr, rn = prepared["rob_rows"], prepared["rob_nodes"]
    numpy.add.at(rhs, dr, -f_dir.ravel()[dn] / alpha_dir.ravel()[dn])
    scale = spacestep * alpha_rob.ravel()[rn] / beta_pde.ravel()[rr]
    denominator = beta_rob.ravel()[rn] + scale
    diagonal = matrix.diagonal()
    # On additionne les effets des différentes faces d'un même point intérieur.
    numpy.add.at(diagonal, rr, -scale / denominator)
    numpy.add.at(rhs, rr, spacestep * f_rob.ravel()[rn] / denominator)
    matrix.setdiag(diagonal)
    return matrix.tocsr(), rhs


def compute_state(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                  beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                  prepared=None, return_factor=False):
    """On résout le système complet puis on remet le champ sur la grille."""
    matrix, rhs = assemble_helmholtz_system(
        domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        prepared=prepared,
    )
    factor = scipy.sparse.linalg.splu(matrix.tocsc())
    state = factor.solve(rhs)
    interior = domain_omega == _env.NODE_INTERIOR
    field = numpy.zeros(domain_omega.shape, dtype=numpy.complex128)
    field[interior] = state.reshape(domain_omega.shape)[interior]
    if return_factor:
        return matrix, state, field, factor
    return matrix, state, field


def compute_adjoint(domain_omega, spacestep, matrix, state, factor=None):
    """On résout le système adjoint à partir du champ dans le fluide."""
    interior = domain_omega == _env.NODE_INTERIOR
    adjoint_rhs = numpy.zeros_like(state)
    adjoint_rhs[interior.ravel()] = 2.0 * spacestep**2 * state[interior.ravel()]
    if factor is not None:
        return factor.solve(adjoint_rhs, trans="H")
    return scipy.sparse.linalg.spsolve(matrix.conjugate().transpose(), adjoint_rhs)


def compute_gradient(domain_omega, spacestep, Alpha, density,
                     beta_pde, beta_rob, f_rob, adjoint, state):
    """On additionne les effets des faces du mur, y compris aux coins."""
    rows, nodes = boundary_neighbours(domain_omega, _env.NODE_ROBIN)
    scale = spacestep * Alpha / beta_pde.ravel()[rows]
    denominator = beta_rob.ravel()[nodes] + scale * density.ravel()[nodes]
    diagonal_derivative = -scale * beta_rob.ravel()[nodes] / denominator**2
    rhs_derivative = -spacestep * f_rob.ravel()[nodes] * scale / denominator**2
    gradient = numpy.zeros(domain_omega.size)
    numpy.add.at(gradient, nodes, numpy.real(numpy.conjugate(adjoint[rows])
                 * (rhs_derivative - diagonal_derivative * state[rows])))
    return gradient.reshape(domain_omega.shape)
