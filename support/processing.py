# -*- coding: utf-8 -*-


# Python packages
import numpy
import numpy as np
import os
import scipy
import scipy.sparse
import scipy.sparse.linalg


# MRG packages
import _env
import preprocessing
from compute_alpha import compute_alpha, MATERIAUX


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
                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob):
    """
    :param domain:
    :param space_step:
    :param omega:
    :param f:
    :param f_dir:
    :param f_neu:
    :param f_rob:
    :param beta_pde:
    :param alpha_pde:
    :param alpha_dir:
    :param beta_neu:
    :param beta_rob:
    :param alpha_rob:
    :return:
    """

    (M, N) = numpy.shape(domain)
    # -- create stiffness matrix
    mat_temp, rhs_temp = compute_stiffness_matrix(domain, space_step, f, beta_pde)
    mat = mat_temp
    rhs = rhs_temp
    # -- create mass matrix
    mat_temp, rhs_temp = compute_mass_matrix(domain, space_step, alpha_pde)
    mat = mat + omega ** 2 * mat_temp
    rhs = rhs
    # -- create convection (vgradu) matrix
    # <!--
    # v = numpy.zeros((M, N, 2), dtype=numpy.float64)
    # xc = int(M//4) * space_step
    # yc = int(N//2) * space_step
    # for i in range(0, M):
    #     for j in range(0, N):
    #         xi = int(i) * space_step
    #         yi = int(j) * space_step
    #         import math
    #         r = math.sqrt( (xi-xc)**2 + (yi-yc)**2 )
    #         if (xi-xc) == 0:
    #             theta = 0.0
    #         elif (yi-yc) / (xi-xc) < 0:
    #             theta = math.atan( -(yi-yc) / (xi-xc) )
    #         elif (yi-yc) / (xi-xc) > 0:
    #             theta = math.atan( (yi - yc) / (xi - xc))
    #
    #         if r == 0.0:
    #             r = 1.0
    #         costheta = (xi - xc) / r
    #         sintheta = (yi - yc) / r
    #         v[i, j, 0] = costheta
    #         v[i, j, 1] = sintheta
    #
    # xploti, yplotj = numpy.meshgrid(numpy.arange(0, N, 1), numpy.arange(0, M, 1))
    # print(xploti.shape[:], yplotj.shape[:])
    # print(v.shape[:])
    #
    #     # #matplotlib.pyplot.quiver(xploti, yplotj, v[:,:,0], v[:,:,1])
    # fig, ax = matplotlib.pyplot.subplots()
    # ax.set_xlim(0, N)
    # ax.set_ylim(M, 0)
    # q = ax.quiver(xploti, yplotj, v[:,:,0], v[:,:,1], units='xy', scale=0.51, color='red')
    # ax.set_aspect('equal')
    # #matplotlib.pyplot.xlim(-5, 5)
    # #matplotlib.pyplot.ylim(-5, 5)
    # matplotlib.pyplot.show()
    #
    # #exit(-6)
    #
    # mat_temp, rhs_temp = compute_vgradu_matrix(domain, space_step, v)
    # mat = mat + mat_temp
    # rhs = rhs
    # -->

    # -- set dirichlet boundary conditions
    mat, rhs = compute_dirichlet_condition(domain, f_dir, alpha_dir, beta_pde, mat, rhs)
    # -- set neumann boundary conditions boundary conditions
    mat, rhs = compute_neumann_condition(domain, space_step, f_neu, beta_neu, beta_pde, mat, rhs)
    # -- set robin boundary conditions
    mat, rhs = compute_robin_condition(domain, space_step, f_rob, alpha_rob, beta_rob, beta_pde, mat, rhs)

    print(mat.shape[:])

    # -- solve linear system
    sol = scipy.sparse.linalg.spsolve(mat, rhs)

    u = numpy.zeros((M, N), dtype=numpy.complex128)
    # -- map solution to the grid
    # for k in range(M * N):
    #     i = k // N
    #     j = k % N
    #     u[i, j] = sol[k]

    for i in range(0, M):
        for j in range(0, N):
            row = i * N + j
            if is_in_interior_domain(domain[i, j]):
                u[i, j] = sol[row]

    return u


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


def set2zero(alpha, domain_omega):
    """This function is useful during the optimisation procedure. It makes sure
    that the density is null everywhere except on the Robin frontier

    Parameter:
        alpha: Matrix (MxN, dtype=complex), this matrix is the density multiply
        by the coefficient of absorbtion;
        domain_omega: Matrix (MxN), it defines the domain and the shape of the
        Robin frontier.
    """

    (M, N) = numpy.shape(domain_omega)
    for i in range(0, M):
        for j in range(0, N):
            if domain_omega[i, j] != _env.NODE_ROBIN:
                alpha[i, j] = 0

    return alpha


def replace_old_by_new(u, oldvalue, newvalue):

    (M, N) = numpy.shape(u)
    for i in range(M):
        for j in range(N):
            if u[i, j] == oldvalue:
                u[i, j] = newvalue
    return u

def run_rer_b_frequency_sweep(domain_omega, spacestep, frequencies_hz,
                            f, f_dir, f_neu, f_rob, beta_pde, alpha_pde,
                            alpha_dir, beta_neu, beta_rob, chi, g, car_mat,
                            alpha0, sound_speed_m_s=343.0):
    """On calcule le champ avec la source et le matériau choisis à chaque fréquence."""
    frequencies = numpy.asarray(frequencies_hz, dtype=numpy.float64)
    amplitudes = numpy.empty_like(frequencies)
    energies = numpy.empty_like(frequencies)
    alphas = numpy.empty(frequencies.size, dtype=numpy.complex128)
    solutions = {}
    y_source = (numpy.arange(domain_omega.shape[1]) - (domain_omega.shape[1] - 1) / 2) * spacestep

    for ind, frequency_hz in enumerate(frequencies):
        omega = 2.0 * numpy.pi * float(frequency_hz)
        k = omega / sound_speed_m_s
        # On détermine le coefficient du matériau dans la convention du polycopié.
        coefficients, success, message = compute_alpha(omega, g, car_mat, alpha0)
        if not success:
            print("Échec du calcul du coefficient à", frequency_hz, "Hz :", message)
            return None
        Alpha = coefficients[0] + 1j * coefficients[1]
        alphas[ind] = Alpha
        alpha_rob_freq = Alpha * chi

        # On applique le même profil de source au bord supérieur.
        amplitudes[ind] = g(0.0, omega)
        f_dir_freq = numpy.zeros_like(f_dir)
        f_dir_freq[0, :] = g(y_source, omega)
        u_freq = solve_helmholtz(
            domain_omega, spacestep, k, f, f_dir_freq, f_neu, f_rob,
            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob_freq,
        )
        interior = domain_omega == _env.NODE_INTERIOR
        energies[ind] = spacestep**2 * numpy.sum(numpy.abs(u_freq[interior])**2)
        solutions[float(frequency_hz)] = u_freq

    # On intègre les énergies, qui contiennent déjà l'amplitude de la source.
    if frequencies.size > 1:
        band_energy = float(numpy.sum(
            (frequencies[1:] - frequencies[:-1])
            * (energies[1:] + energies[:-1]) / 2.0
        ))
    else:
        band_energy = float(energies[0])
    return {
        "frequencies_hz": frequencies,
        "amplitudes": amplitudes,
        "alphas": alphas,
        "energies": energies,
        "solutions": solutions,
        "band_energy": band_energy,
    }


def compute_state(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                  beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob):
    """On assemble le système fourni et on renvoie le champ calculé."""
    # On reprend les mêmes contributions que dans le solveur fourni.
    matrix, rhs = compute_stiffness_matrix(domain_omega, spacestep, f, beta_pde)
    mass, _ = compute_mass_matrix(domain_omega, spacestep, alpha_pde)
    matrix = matrix + omega**2 * mass
    matrix, rhs = compute_dirichlet_condition(
        domain_omega, f_dir, alpha_dir, beta_pde, matrix, rhs,
    )
    matrix, rhs = compute_neumann_condition(
        domain_omega, spacestep, f_neu, beta_neu, beta_pde, matrix, rhs,
    )
    matrix, rhs = compute_robin_condition(
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


class FastHelmholtzSolver:
    """On conserve les contributions de grille communes aux résolutions successives."""

    def __init__(self, domain_omega, spacestep, f=None, f_dir=None, f_neu=None, f_rob=None,
                 beta_pde=None, alpha_pde=None, alpha_dir=None, beta_neu=None, beta_rob=None):
        """On prépare les coefficients et la correspondance des points intérieurs."""
        self.domain = domain_omega
        self.h = float(spacestep)
        self.M, self.N = domain_omega.shape
        self.K = self.M * self.N
        defaults = preprocessing._set_coefficients_of_pde(self.M, self.N)
        self.beta_pde = defaults[0] if beta_pde is None else beta_pde
        self.alpha_pde = defaults[1] if alpha_pde is None else alpha_pde
        self.alpha_dir = defaults[2] if alpha_dir is None else alpha_dir
        self.beta_neu = defaults[3] if beta_neu is None else beta_neu
        self.beta_rob = defaults[5] if beta_rob is None else beta_rob
        loads = preprocessing._set_rhs_of_pde(self.M, self.N)
        f = loads[0] if f is None else f
        f_dir = loads[1] if f_dir is None else f_dir
        f_neu = loads[2] if f_neu is None else f_neu
        f_rob = loads[3] if f_rob is None else f_rob

        self.mask_int = domain_omega == _env.NODE_INTERIOR
        self.mask_rob = domain_omega == _env.NODE_ROBIN
        self.int_flat_idx = np.flatnonzero(self.mask_int)
        self.n_int = len(self.int_flat_idx)
        self.global_to_int = np.full(self.K, -1, dtype=np.int64)
        self.global_to_int[self.int_flat_idx] = np.arange(self.n_int)
        self._preassemble_structure(f, f_dir, f_neu, f_rob)

    def _preassemble_structure(self, f, f_dir, f_neu, f_rob):
        """On assemble les contributions fixes et on repère les voisins du mur."""
        rows, cols, values = [], [], []
        self.base_diag = np.zeros(self.n_int, dtype=np.complex128)
        self.mass_diag = np.zeros(self.n_int, dtype=np.complex128)
        robin_interior, robin_i, robin_j = [], [], []
        robin_beta_pde, robin_beta_rob = [], []
        for local, (i, j) in enumerate(np.argwhere(self.mask_int)):
            beta = self.beta_pde[i, j]
            diagonal = -4.0 * beta
            self.mass_diag[local] = self.h**2 * self.alpha_pde[i, j]
            for ni, nj in ((i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)):
                label = self.domain[ni, nj]
                if label == _env.NODE_INTERIOR:
                    rows.append(local)
                    cols.append(self.global_to_int[ni * self.N + nj])
                    values.append(self.beta_pde[ni, nj])
                elif label == _env.NODE_NEUMANN:
                    diagonal += beta
                elif label == _env.NODE_ROBIN:
                    diagonal += beta
                    robin_interior.append(local)
                    robin_i.append(ni)
                    robin_j.append(nj)
                    robin_beta_pde.append(beta)
                    robin_beta_rob.append(self.beta_rob[ni, nj])
            self.base_diag[local] = diagonal

        self.off_diag_mat = scipy.sparse.csc_matrix(
            (np.asarray(values, dtype=np.complex128), (rows, cols)),
            shape=(self.n_int, self.n_int),
        )
        self.rob_int_idx = np.asarray(robin_interior, dtype=np.int64)
        self.rob_node_i = np.asarray(robin_i, dtype=np.int64)
        self.rob_node_j = np.asarray(robin_j, dtype=np.int64)
        self.rob_beta_pde = np.asarray(robin_beta_pde, dtype=np.complex128)
        self.rob_beta_rob = np.asarray(robin_beta_rob, dtype=np.complex128)
        self.update_rhs(f, f_dir, f_neu, f_rob)

    def update_rhs(self, f, f_dir, f_neu, f_rob=None):
        """On remplace les données de source et on reconstruit le second membre."""
        self.f = np.asarray(f, dtype=np.complex128).copy()
        self.f_dir = np.asarray(f_dir, dtype=np.complex128).copy()
        self.f_neu = np.asarray(f_neu, dtype=np.complex128).copy()
        self.f_rob = np.zeros(self.domain.shape, dtype=np.complex128) if f_rob is None else np.asarray(f_rob, dtype=np.complex128).copy()
        rhs = np.zeros(self.n_int, dtype=np.complex128)
        for local, (i, j) in enumerate(np.argwhere(self.mask_int)):
            value = self.h**2 * self.f[i, j]
            for ni, nj in ((i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)):
                label = self.domain[ni, nj]
                if label == _env.NODE_DIRICHLET:
                    value -= self.f_dir[ni, nj] / self.alpha_dir[ni, nj]
                elif label == _env.NODE_NEUMANN:
                    value += self.h * self.f_neu[ni, nj] / self.beta_neu[ni, nj]
            rhs[local] = value
        self.base_rhs_int = rhs

    def set_source(self, source, omega):
        """On applique la source choisie à la pulsation courante sur le bord supérieur."""
        coordinates = (np.arange(self.N) - (self.N - 1) / 2) * self.h
        f_dir = np.zeros(self.domain.shape, dtype=np.complex128)
        f_dir[0, :] = source(coordinates, omega)
        self.update_rhs(self.f, f_dir, self.f_neu, self.f_rob)

    def _assemble_system_matrix(self, omega, alpha_rob):
        """On complète la matrice avec le nombre d'onde et le coefficient du mur."""
        diagonal = self.base_diag + omega**2 * self.mass_diag
        ratio = alpha_rob[self.rob_node_i, self.rob_node_j] / self.rob_beta_pde
        contribution = -ratio * self.h / (self.rob_beta_rob + ratio * self.h)
        np.add.at(diagonal, self.rob_int_idx, contribution)
        return self.off_diag_mat + scipy.sparse.diags(diagonal, format='csc')

    def _assemble_rhs(self, alpha_rob):
        """On ajoute les éventuelles sources présentes sur le mur."""
        rhs = self.base_rhs_int.copy()
        ratio = alpha_rob[self.rob_node_i, self.rob_node_j] / self.rob_beta_pde
        wall_load = self.f_rob[self.rob_node_i, self.rob_node_j]
        contribution = self.h * wall_load / (self.rob_beta_rob + ratio * self.h)
        np.add.at(rhs, self.rob_int_idx, contribution)
        return rhs

    def solve(self, omega, alpha_rob, custom_rhs_int=None):
        """On résout le système intérieur et on remet le champ sur la grille."""
        matrix = self._assemble_system_matrix(omega, alpha_rob)
        rhs = self._assemble_rhs(alpha_rob) if custom_rhs_int is None else np.asarray(custom_rhs_int).ravel()
        interior_values = scipy.sparse.linalg.spsolve(matrix, rhs)
        u = np.zeros(self.domain.shape, dtype=np.complex128)
        u[self.mask_int] = interior_values
        return u

    def solve_state_and_adjoint(self, omega, alpha_rob):
        """On calcule le champ puis son adjoint à partir du même système."""
        matrix = self._assemble_system_matrix(omega, alpha_rob)
        factorization = scipy.sparse.linalg.splu(matrix)
        interior_values = factorization.solve(self._assemble_rhs(alpha_rob))
        adjoint_values = factorization.solve(2.0 * self.h**2 * interior_values, trans='H')
        u = np.zeros(self.domain.shape, dtype=np.complex128)
        p = np.zeros(self.domain.shape, dtype=np.complex128)
        u[self.mask_int] = interior_values
        p[self.mask_int] = adjoint_values
        return u, p

    def compute_energy(self, u):
        """On additionne les modules au carré du champ sur les points intérieurs."""
        return float(self.h**2 * np.sum(np.abs(u[self.mask_int])**2))

    def compute_gradient(self, u, p, chi, Alpha):
        """On calcule la dérivée du énergie par rapport à chaque valeur du matériau."""
        gradient = np.zeros(self.domain.shape, dtype=np.float64)
        scale = self.h * Alpha / self.rob_beta_pde
        density = chi[self.rob_node_i, self.rob_node_j]
        denominator = self.rob_beta_rob + scale * density
        matrix_derivative = -scale * self.rob_beta_rob / denominator**2
        load = self.f_rob[self.rob_node_i, self.rob_node_j]
        rhs_derivative = -self.h * load * scale / denominator**2
        interior_u = u[self.mask_int][self.rob_int_idx]
        interior_p = p[self.mask_int][self.rob_int_idx]
        contribution = np.real(np.conj(interior_p) * (rhs_derivative - matrix_derivative * interior_u))
        np.add.at(gradient, (self.rob_node_i, self.rob_node_j), contribution)
        return gradient


def optimize_single_frequency(solver, wavenumber, Alpha, chi_init, V_obj=0.3,
                              mu_init=5.0, numb_iter=100, min_mu=1e-5, verbose=False,
                              source=None, sound_speed_m_s=343.0):
    """On recherche une répartition continue à une fréquence donnée."""
    chi, history, _ = optimize_multi_frequency(
        solver, [wavenumber], [Alpha], chi_init, V_obj=V_obj,
        mu_init=mu_init, numb_iter=numb_iter, min_mu=min_mu, verbose=verbose,
        source=source, sound_speed_m_s=sound_speed_m_s,
    )
    if source is not None:
        solver.set_source(source, wavenumber * sound_speed_m_s)
    u, p = solver.solve_state_and_adjoint(wavenumber, Alpha * chi)
    gradient = solver.compute_gradient(u, p, chi, Alpha)
    return chi, history, u, gradient


def optimize_multi_frequency(solver, wavenumbers, Alphas, chi_init, weights=None,
                             V_obj=0.3, mu_init=5.0, numb_iter=100, min_mu=1e-5, verbose=False,
                             source=None, sound_speed_m_s=343.0):
    """On recherche une même répartition pour plusieurs fréquences pondérées."""
    wavenumbers = np.asarray(wavenumbers, dtype=np.float64)
    Alphas = np.asarray(Alphas, dtype=np.complex128)
    weights = np.ones(len(wavenumbers)) if weights is None else np.asarray(weights, dtype=np.float64)
    weights = weights / weights.sum()
    chi = preprocessing.project_density(chi_init, solver.domain, V_obj)
    mu = float(mu_init)
    costs = np.zeros(len(wavenumbers))
    for m, (wavenumber, Alpha) in enumerate(zip(wavenumbers, Alphas)):
        if source is not None:
            solver.set_source(source, wavenumber * sound_speed_m_s)
        costs[m] = solver.compute_energy(solver.solve(wavenumber, Alpha * chi))
    history = [float(weights @ costs)]
    per_frequency = [costs.copy()]

    for iteration in range(numb_iter):
        if mu <= min_mu:
            break
        gradient = np.zeros(solver.domain.shape)
        for weight, wavenumber, Alpha in zip(weights, wavenumbers, Alphas):
            if source is not None:
                solver.set_source(source, wavenumber * sound_speed_m_s)
            u, p = solver.solve_state_and_adjoint(wavenumber, Alpha * chi)
            gradient += weight * solver.compute_gradient(u, p, chi, Alpha)

        accepted = False
        while mu > min_mu:
            candidate = preprocessing.project_density(chi - mu * gradient, solver.domain, V_obj)
            candidate_costs = np.zeros(len(wavenumbers))
            for m, (wavenumber, Alpha) in enumerate(zip(wavenumbers, Alphas)):
                if source is not None:
                    solver.set_source(source, wavenumber * sound_speed_m_s)
                field = solver.solve(wavenumber, Alpha * candidate)
                candidate_costs[m] = solver.compute_energy(field)
            value = float(weights @ candidate_costs)
            if np.isfinite(value) and value < history[-1]:
                variation = np.max(np.abs(candidate - chi))
                chi = candidate
                history.append(value)
                per_frequency.append(candidate_costs.copy())
                mu *= 1.1
                accepted = True
                break
            mu /= 2.0
        if not accepted:
            break
        if verbose:
            print("Étape", iteration + 1, ": énergie =", history[-1])
        if variation < 1e-7:
            break
    return chi, np.asarray(history), np.asarray(per_frequency)


def find_local_maxima(freqs, k_vals, energies, min_prominence_ratio=0.01):
    """On renvoie les pics dont la hauteur dépasse le seuil relatif indiqué."""
    freqs, k_vals, energies = map(np.asarray, (freqs, k_vals, energies))
    indices = []
    energy_range = np.max(energies) - np.min(energies)
    for i in range(1, len(energies) - 1):
        if energies[i] > energies[i - 1] and energies[i] >= energies[i + 1]:
            left = np.min(energies[max(0, i - 6):i + 1])
            right = np.min(energies[i:min(len(energies), i + 7)])
            prominence = energies[i] - max(left, right)
            if prominence >= min_prominence_ratio * energy_range:
                indices.append(i)
    indices = np.asarray(indices, dtype=int)
    return indices, freqs[indices], k_vals[indices], energies[indices]


def compute_material_coefficients(frequencies, source, car_mat, alpha0):
    """On calcule le coefficient complexe du matériau à chaque fréquence."""
    alphas = []
    for frequency in frequencies:
        # On transmet la pulsation temporelle à la fonction de Joachim.
        pair, success, message = compute_alpha(2.0 * np.pi * frequency,
                                               source, car_mat, alpha0)
        alpha = complex(pair[0], pair[1])
        if not success or not np.isfinite(alpha) or alpha.real <= 0 or alpha.imag >= 0:
            print("Coefficient non validé à", frequency, "Hz pour", car_mat, ":", message)
            return None
        # On conserve directement le signe de la condition de Robin du polycopié.
        alphas.append(alpha)
    return np.asarray(alphas, dtype=np.complex128)


def evaluate_spectrum(solver, domain, chi, k_vals, Alphas, source, sound_speed_m_s):
    """On calcule les énergies avec la source choisie à chaque fréquence."""
    energies = []
    chi_wall = np.where(domain == _env.NODE_ROBIN, chi, 0.0)
    for wavenumber, alpha in zip(k_vals, Alphas):
        solver.set_source(source, wavenumber * sound_speed_m_s)
        u = solver.solve(wavenumber, alpha * chi_wall)
        energies.append(solver.compute_energy(u))
    return np.asarray(energies)


def select_peak_indices(freqs, k_vals, energies, count=2):
    """On retient les pics les plus élevés puis les maxima échantillonnés au besoin."""
    energies = np.asarray(energies)
    peaks = find_local_maxima(freqs, k_vals, energies)[0]
    ranked_peaks = peaks[np.argsort(energies[peaks])[::-1]]
    indices = list(ranked_peaks[:count])
    # Une grille de fréquences courte peut ne contenir aucun maximum intérieur.
    for candidate in np.argsort(energies)[::-1]:
        if len(indices) >= min(count, len(energies)):
            break
        if candidate not in indices:
            indices.append(int(candidate))
    return np.asarray(sorted(indices, key=lambda i: freqs[i]), dtype=int)


def study_porous_materials(frequencies, source, alpha0, material_names):
    """On calcule les coefficients des matériaux choisis aux fréquences indiquées."""
    frequencies = np.asarray(frequencies, dtype=float)
    alphas = {}
    # On compare les matériaux avec la même source et le même point de départ.
    for name in material_names:
        values = compute_material_coefficients(frequencies, source, MATERIAUX[name], alpha0)
        if values is None:
            return None
        alphas[name] = values
    return {"frequencies": frequencies, "alphas": alphas,
            "material_names": tuple(material_names)}


def study_sommerfeld_open_air_vs_reflexive(N, frequencies, source, car_mat,
                                          alpha0, sound_speed_m_s):
    """On compare les réponses des parois réfléchissante, ouverte et poreuse."""
    frequencies = np.asarray(frequencies, dtype=float)
    alphas = compute_material_coefficients(frequencies, source, car_mat, alpha0)
    if alphas is None:
        return None
    domain, _, _, _, _ = preprocessing._set_geometry_of_domain(2 * N, N, level=0)
    solver = FastHelmholtzSolver(domain, 1.0 / N)
    robin = domain == _env.NODE_ROBIN
    energies = np.zeros((len(frequencies), 3))
    theory = np.zeros((len(frequencies), 2))

    for i, frequency in enumerate(frequencies):
        omega = 2.0 * np.pi * frequency
        wavenumber = omega / sound_speed_m_s
        solver.set_source(source, omega)
        # On applique le signe du polycopié à la sortie ouverte.
        for j, alpha in enumerate((0.0, -1j * wavenumber, alphas[i])):
            boundary = np.zeros(domain.shape, dtype=complex)
            boundary[robin] = alpha
            energies[i, j] = solver.compute_energy(solver.solve(wavenumber, boundary))

        # On calcule aussi les solutions continues sur une bande rectangulaire unitaire.
        amplitude_squared = abs(source(0.0, omega)) ** 2
        theory[i, 0] = amplitude_squared
        cosine = np.cos(wavenumber)
        if abs(cosine) > 1e-8:
            theory[i, 1] = amplitude_squared * (0.5 + np.sin(2.0 * wavenumber) / (4.0 * wavenumber)) / cosine**2
        else:
            theory[i, 1] = np.nan
    return {"frequencies": frequencies, "energies": energies, "theory": theory,
            "alphas": alphas, "N": N, "sound_speed_m_s": sound_speed_m_s}


def study_boundary_depth_dependence(depths, frequency_hz, source, sound_speed_m_s):
    """On compare les références ouvertes et réfléchissantes pour des rectangles de même aire."""
    depths = np.asarray(depths, dtype=float)
    area = 1.0
    widths = area/depths
    wavenumber = 2*np.pi*frequency_hz/sound_speed_m_s
    amplitude_squared = abs(source(0.0, 2*np.pi*frequency_hz))**2
    denominator = np.cos(wavenumber*depths)**2
    reflecting = area*amplitude_squared*(.5+np.sin(2*wavenumber*depths)/(4*wavenumber*depths))/denominator
    reflecting = np.where(denominator > 1e-12, reflecting, np.nan)
    return {"depths": depths, "widths": widths, "frequency_hz": frequency_hz,
            "open": np.full_like(depths, area*amplitude_squared), "reflecting": reflecting}


def validate_adjoint_gradient(N, samples, omega, source, car_mat, alpha0,
                              sound_speed_m_s):
    """On vérifie le gradient adjoint en perturbant les densités du mur."""
    alphas = compute_material_coefficients([omega / (2.0 * np.pi)], source, car_mat, alpha0)
    if alphas is None:
        return None
    Alpha = alphas[0]
    domain, _, _, _, _ = preprocessing._set_geometry_of_domain(2 * N, N, level=1)
    solver = FastHelmholtzSolver(domain, 1.0 / N)
    solver.set_source(source, omega)
    # On garde des densités éloignées des bornes pour les perturber dans les deux sens.
    density = np.zeros(domain.shape)
    density[domain == _env.NODE_ROBIN] = 0.3
    wavenumber = omega / sound_speed_m_s
    field, adjoint = solver.solve_state_and_adjoint(wavenumber, Alpha * density)
    gradient = solver.compute_gradient(field, adjoint, density, Alpha)
    nodes = np.argwhere(domain == _env.NODE_ROBIN)
    chosen = nodes[np.linspace(0, len(nodes) - 1, min(samples, len(nodes)), dtype=int)]
    epsilon = 1e-6
    finite_difference, adjoint_values = [], []

    for row, col in chosen:
        # On compare le énergie après une augmentation et après une diminution de densité.
        plus, minus = density.copy(), density.copy()
        plus[row, col] += epsilon
        minus[row, col] -= epsilon
        cost_plus = solver.compute_energy(solver.solve(wavenumber, Alpha * plus))
        cost_minus = solver.compute_energy(solver.solve(wavenumber, Alpha * minus))
        finite_difference.append((cost_plus - cost_minus) / (2.0 * epsilon))
        adjoint_values.append(gradient[row, col])

    finite_difference = np.asarray(finite_difference)
    adjoint_values = np.asarray(adjoint_values)
    error = np.linalg.norm(adjoint_values - finite_difference) / max(np.linalg.norm(finite_difference), 1e-14)
    print("Erreur relative du gradient adjoint :", error)

    # On étudie ensuite la taille de la perturbation au point de dérivée maximale.
    row, col = chosen[np.argmax(np.abs(adjoint_values))]
    steps = np.logspace(-8, -2, 13)
    errors = []
    for step in steps:
        plus, minus = density.copy(), density.copy()
        plus[row, col] += step
        minus[row, col] -= step
        derivative = (solver.compute_energy(solver.solve(wavenumber, Alpha * plus)) - solver.compute_energy(solver.solve(wavenumber, Alpha * minus))) / (2.0 * step)
        errors.append(abs(derivative - gradient[row, col]) / max(abs(gradient[row, col]), 1e-14))
    return {"relative_error": float(error), "adjoint": adjoint_values,
            "finite_difference": finite_difference, "chosen_nodes": chosen,
            "steps": steps, "errors": np.asarray(errors), "omega": omega, "N": N}


def study_spectra_and_single_frequency_placement(N, frequencies, iterations, V_obj, source, car_mat, alpha0, sound_speed_m_s):
    """On calcule les spectres des murs puis on optimise le placement à une fréquence."""
    freqs = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    if len(freqs) == 0 or N < 16 or N % 16 != 0:
        print("Il faut au moins une fréquence et une largeur multiple de seize pour les deux premiers niveaux.")
        return None
    M, spacestep = 2 * N, 1.0 / N
    k_vals = 2.0 * np.pi * freqs / sound_speed_m_s
    Alphas = compute_material_coefficients(freqs, source, car_mat, alpha0)
    if Alphas is None:
        return None
    if sound_speed_m_s / (np.max(freqs) * spacestep) < 10:
        print("Attention, le maillage comporte moins de dix points par longueur d'onde au maximum de fréquence.")

    # On compare les murs entièrement garnis.
    print("Spectres des murs entièrement garnis.")
    levels = [0, 1, 2, 3] if N % 64 == 0 else [0, 1, 2]
    if 3 not in levels:
        print("Le niveau trois est écarté de ce calcul réduit car son motif demande une largeur multiple de soixante-quatre.")
    domains, solvers, coordinates, full, maxima = {}, {}, {}, {}, {}
    for level in levels:
        domain, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
        solver = FastHelmholtzSolver(domain, spacestep)
        domains[level], solvers[level], coordinates[level] = domain, solver, (x, y)
        full[level] = evaluate_spectrum(solver, domain, (domain == _env.NODE_ROBIN).astype(float), k_vals, Alphas, source, sound_speed_m_s)
        maxima[level] = find_local_maxima(freqs, k_vals, full[level])
        print("Niveau", level, ": moyenne des échantillons =", np.mean(full[level]), "; pics en Hz =", maxima[level][1])



    # On fixe la quantité de matériau pour chaque mur.
    print("Répartition initiale et mur entièrement garni.")
    initial, chi_initial = {}, {}
    for level in (0, 1, 2):
        x, y = coordinates[level]
        raw = preprocessing._set_chi(M, N, x, y)
        chi_initial[level] = preprocessing.project_density(raw, domains[level], V_obj)
        initial[level] = evaluate_spectrum(solvers[level], domains[level], chi_initial[level], k_vals, Alphas, source, sound_speed_m_s)

    # On optimise séparément deux fréquences critiques.
    print("Placements à une fréquence.")
    results = {}
    for level in (0, 1, 2):
        results[level] = []
        solver, domain = solvers[level], domains[level]
        indices = select_peak_indices(freqs, k_vals, initial[level], count=2)
        for index in indices:
            solver.set_source(source, 2.0 * np.pi * freqs[index])
            u0 = solver.solve(k_vals[index], Alphas[index] * chi_initial[level])
            continuous, history, _, _ = optimize_single_frequency(
                solver, k_vals[index], Alphas[index], chi_initial[level],
                V_obj=V_obj, numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
            )
            # On mesure aussi le placement constitué uniquement de points garnis ou nus.
            binary = preprocessing.binarize_chi(continuous, domain, V_obj)
            u_binary = solver.solve(k_vals[index], Alphas[index] * binary)
            cost_binary = solver.compute_energy(u_binary)
            results[level].append({
                "f_target": freqs[index], "k_target": k_vals[index], "idx_peak": index,
                "J0_proj": solver.compute_energy(u0), "J_relaxed": history[-1],
                "J_opt": cost_binary, "J_full": full[level][index],
                "chi0": chi_initial[level], "chi_cont": continuous, "chi_opt": binary,
                "u0": u0, "u_opt": u_binary, "ene_hist": history,
            })
            print("Niveau", level, "à", freqs[index], "Hz : initial =", initial[level][index],
                  "; continu =", history[-1], "; binaire =", cost_binary, "; entièrement garni =", full[level][index])


    # On enregistre les valeurs réellement calculées et les paramètres associés.
    data = {"freqs": freqs, "k_vals": k_vals, "Alphas": Alphas, "N": N,
            "iterations_requested": iterations,
            "sound_speed_m_s": sound_speed_m_s, "volume_fraction": V_obj,
            "source_name": source.__name__, "material_parameters": np.asarray(car_mat)}
    for level in levels:
        data[f"energies_full_l{level}"] = full[level]
    for level in (0, 1, 2):
        data[f"energies_initial_l{level}"] = initial[level]
        data[f"chi0_l{level}"] = chi_initial[level]
        for number, result in enumerate(results[level], start=1):
            data[f"chi_opt_l{level}_peak{number}"] = result["chi_opt"]
            data[f"chi_cont_l{level}_peak{number}"] = result["chi_cont"]
            data[f"f_target_l{level}_peak{number}"] = result["f_target"]
            data[f"history_l{level}_peak{number}"] = result["ene_hist"]
            data[f"cost_binary_l{level}_peak{number}"] = result["J_opt"]
    return {"frequencies": freqs, "full": full, "initial": initial, "optimizations": results,
            "levels": levels, "domains": domains, "maxima": maxima, "N": N,
            "spacestep": spacestep, "volume_fraction": V_obj, "data": data}


def study_multifrequency_placement_and_coverage(N, frequencies, iterations, V_obj, quantities, source, car_mat, alpha0, sound_speed_m_s):
    """On optimise le placement sur plusieurs fréquences et on compare les quantités de matériau."""
    freqs = np.arange(50.0, 3501.0, 50.0) if frequencies is None else np.asarray(frequencies, dtype=float)
    volumes = np.asarray([.10, .30, .50, .70, 1.0] if quantities is None else quantities, dtype=float)
    if len(freqs) == 0 or len(volumes) == 0 or N < 16 or N % 16 != 0:
        print("Il faut au moins une fréquence, une quantité et une largeur multiple de seize.")
        return None
    if np.any(volumes <= 0) or np.any(volumes > 1):
        print("Les fractions de mur garni doivent être strictement positives et au plus égales à un.")
        return None
    M, spacestep = 2 * N, 1.0 / N
    k_vals = 2.0 * np.pi * freqs / sound_speed_m_s
    Alphas = compute_material_coefficients(freqs, source, car_mat, alpha0)
    if Alphas is None:
        return None
    if sound_speed_m_s / (np.max(freqs) * spacestep) < 10:
        print("Attention, le maillage comporte moins de dix points par longueur d'onde au maximum de fréquence.")

    # On observe chaque placement sur toute la bande.
    print("Spectres des placements à une fréquence.")
    studies = {}
    for level in (0, 1, 2):
        domain, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
        solver = FastHelmholtzSolver(domain, spacestep)
        raw = preprocessing._set_chi(M, N, x, y)
        chi0 = preprocessing.project_density(raw, domain, V_obj)
        full_wall = (domain == _env.NODE_ROBIN).astype(float)
        full = evaluate_spectrum(solver, domain, full_wall, k_vals, Alphas, source, sound_speed_m_s)
        initial = evaluate_spectrum(solver, domain, chi0, k_vals, Alphas, source, sound_speed_m_s)
        targets = select_peak_indices(freqs, k_vals, initial, count=2)
        mono_spectra, mono_placements, mono_histories = [], [], []
        for index in targets:
            continuous, history, _, _ = optimize_single_frequency(
                solver, k_vals[index], Alphas[index], chi0, V_obj=V_obj,
                numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
            )
            binary = preprocessing.binarize_chi(continuous, domain, V_obj)
            mono_spectra.append(evaluate_spectrum(solver, domain, binary, k_vals, Alphas, source, sound_speed_m_s))
            mono_placements.append(binary)
            mono_histories.append(history)
        studies[level] = {
            "domain": domain, "solver": solver, "raw": raw, "chi0": chi0,
            "full": full, "initial": initial, "mono_targets": targets,
            "mono_spectra": mono_spectra, "mono_placements": mono_placements,
            "mono_histories": mono_histories,
        }


    # On minimise la moyenne sur plusieurs fréquences.
    print("Placements pour plusieurs fréquences.")
    for level in (0, 1, 2):
        study = studies[level]
        targets = select_peak_indices(freqs, k_vals, study["initial"], count=3)
        # Le champ contient déjà l'amplitude de la source à chaque fréquence.
        # On donne donc le même poids aux énergies des fréquences retenues.
        continuous, history, per_frequency = optimize_multi_frequency(
            study["solver"], k_vals[targets], Alphas[targets], study["chi0"],
            V_obj=V_obj, numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
        )
        binary = preprocessing.binarize_chi(continuous, study["domain"], V_obj)
        spectrum = evaluate_spectrum(study["solver"], study["domain"], binary, k_vals, Alphas, source, sound_speed_m_s)
        study.update({"multi_targets": targets, "chi_multi_cont": continuous,
                      "chi_multi": binary, "multi_history": history,
                      "multi_history_frequencies": per_frequency, "multi_spectrum": spectrum})
        print("Niveau", level, ": fréquences cibles en Hz =", freqs[targets],
              "; énergie moyen continu =", history[-1],
              "; énergie moyen binaire =", np.mean(spectrum[targets]))


    # On répète le calcul pour les quantités indiquées.
    print("Étude de la quantité de matériau.")
    for level in (0, 1, 2):
        study = studies[level]
        solver, domain = study["solver"], study["domain"]
        # Les fréquences restent identiques pour toutes les quantités d'un mur.
        mono_index = select_peak_indices(freqs, k_vals, study["initial"], count=1)[0]
        multi_indices = study["multi_targets"]
        mono_costs, multi_costs, actual_volumes = [], [], []
        for volume in volumes:
            if volume == 1.0:
                # Le mur entièrement garni fournit directement cette extrémité.
                mono_costs.append(study["full"][mono_index])
                multi_costs.append(np.mean(study["full"][multi_indices]))
                actual_volumes.append(1.0)
                continue
            chi0 = preprocessing.project_density(study["raw"], domain, volume)
            chi_mono_cont, _, _, _ = optimize_single_frequency(
                solver, k_vals[mono_index], Alphas[mono_index], chi0,
                V_obj=volume, numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
            )
            chi_mono = preprocessing.binarize_chi(chi_mono_cont, domain, volume)
            mono_cost = evaluate_spectrum(solver, domain, chi_mono,
                                           k_vals[[mono_index]], Alphas[[mono_index]], source, sound_speed_m_s)[0]
            chi_multi_cont, _, _ = optimize_multi_frequency(
                solver, k_vals[multi_indices], Alphas[multi_indices], chi0,
                V_obj=volume, numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
            )
            chi_multi = preprocessing.binarize_chi(chi_multi_cont, domain, volume)
            multi_cost = np.mean(evaluate_spectrum(solver, domain, chi_multi,
                                                    k_vals[multi_indices], Alphas[multi_indices], source, sound_speed_m_s))
            mono_costs.append(mono_cost)
            multi_costs.append(multi_cost)
            actual_volumes.append(np.mean(chi_multi[domain == _env.NODE_ROBIN]))
        study.update({"volume_mono_index": mono_index, "volume_mono_costs": np.asarray(mono_costs),
                      "volume_multi_costs": np.asarray(multi_costs), "actual_volumes": np.asarray(actual_volumes)})
        best_mono, best_multi = np.argmin(mono_costs), np.argmin(multi_costs)
        print("Niveau", level, ": parmi les quantités testées, minimum à une fréquence =",
              volumes[best_mono], "; minimum à plusieurs fréquences =", volumes[best_multi])


    # On sauvegarde les résultats de chaque mur pour conserver la trace des comparaisons.
    data = {"freqs": freqs, "k_vals": k_vals, "Alphas": Alphas, "N": N,
            "iterations_requested": iterations,
            "sound_speed_m_s": sound_speed_m_s, "volume_fraction": V_obj, "V_list": volumes,
            "source_name": source.__name__, "material_parameters": np.asarray(car_mat)}
    for level in (0, 1, 2):
        study = studies[level]
        data[f"E_init_spec_l{level}"] = study["initial"]
        data[f"E_full_spec_l{level}"] = study["full"]
        data[f"E_multi_spec_l{level}"] = study["multi_spectrum"]
        data[f"chi_multi_l{level}"] = study["chi_multi"]
        data[f"chi_multi_cont_l{level}"] = study["chi_multi_cont"]
        data[f"multi_frequencies_l{level}"] = freqs[study["multi_targets"]]
        data[f"multi_history_l{level}"] = study["multi_history"]
        data[f"multi_history_frequencies_l{level}"] = study["multi_history_frequencies"]
        data[f"J_vol_l{level}"] = study["volume_mono_costs"]
        data[f"J_multi_vol_l{level}"] = study["volume_multi_costs"]
        data[f"actual_volumes_l{level}"] = study["actual_volumes"]
        data[f"volume_mono_frequency_l{level}"] = freqs[study["volume_mono_index"]]
        for number, (target, spectrum, placement) in enumerate(zip(study["mono_targets"], study["mono_spectra"], study["mono_placements"]), start=1):
            data[f"mono_frequency_l{level}_peak{number}"] = freqs[target]
            data[f"E_mono_spec_l{level}_peak{number}"] = spectrum
            data[f"chi_mono_l{level}_peak{number}"] = placement
    return {"frequencies": freqs, "volumes": volumes, "studies": studies, "data": data}


def mean_cost(frequencies, costs):
    """On calcule le énergie moyen sur la bande de fréquences considérée."""
    if len(frequencies) == 1:
        return float(costs[0])
    return float(np.trapezoid(costs, frequencies) / (frequencies[-1] - frequencies[0]))


def compare_absorber_configurations(N, frequencies, iterations, V_obj, source, car_mat, alpha0,
                     sound_speed_m_s, material_names, fixed_covered_nodes=None):
    """On évalue les répartitions, les profils incidents et les matériaux choisis."""
    frequencies = np.asarray(frequencies, dtype=float)
    wavenumbers = 2.0 * np.pi * frequencies / sound_speed_m_s
    M, h = 2 * N, 1.0 / N
    alphas = compute_material_coefficients(frequencies, source, car_mat, alpha0)
    if alphas is None:
        return None

    # On garde la même source et le même matériau pour les différentes répartitions.
    domain, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=2)
    solver = FastHelmholtzSolver(domain, h)
    robin = domain == _env.NODE_ROBIN
    initial = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), domain)
    initial = preprocessing.project_density(initial, domain, V_obj)
    initial_costs = evaluate_spectrum(solver, domain, initial, wavenumbers, alphas, source, sound_speed_m_s)
    targets = select_peak_indices(frequencies, wavenumbers, initial_costs, count=3)
    target_k = wavenumbers[targets]

    # On optimise aux fréquences choisies dans le spectre initial.
    continuous, history, _ = optimize_multi_frequency(
        solver, target_k, alphas[targets], initial, V_obj=V_obj,
        numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
    )
    binary = preprocessing.binarize_chi(continuous, domain, V_obj)
    full = np.zeros(domain.shape)
    full[robin] = 1.0
    continuous_costs = evaluate_spectrum(solver, domain, continuous, wavenumbers, alphas, source, sound_speed_m_s)
    binary_costs = evaluate_spectrum(solver, domain, binary, wavenumbers, alphas, source, sound_speed_m_s)
    full_costs = evaluate_spectrum(solver, domain, full, wavenumbers, alphas, source, sound_speed_m_s)

    # On teste un second matériau sur la partie basse de la répartition binaire.
    alternative = "MELAMINE" if not np.allclose(car_mat, MATERIAUX["MELAMINE"]) else "LAINE_VERRE"
    other_alphas = compute_material_coefficients(frequencies, source, MATERIAUX[alternative], alpha0)
    if other_alphas is None:
        return None
    rows, cols = np.where(robin)
    deep = rows >= N
    mixed_costs = np.zeros(len(frequencies))
    for i, wavenumber in enumerate(wavenumbers):
        boundary = alphas[i] * binary.astype(complex)
        boundary[rows[deep], cols[deep]] = other_alphas[i] * binary[rows[deep], cols[deep]]
        solver.set_source(source, wavenumber * sound_speed_m_s)
        mixed_costs[i] = solver.compute_energy(solver.solve(wavenumber, boundary))

    # On compare trois profils incidents avec la même somme d'amplitudes au carré.
    test_index = targets[np.argmax(initial_costs[targets])]
    test_k = wavenumbers[test_index]
    amplitude = source(0.0, test_k * sound_speed_m_s)
    dirichlet = domain == _env.NODE_DIRICHLET
    uniform = np.ones(N, dtype=complex)
    localized = np.zeros(N, dtype=complex)
    localized[N // 2] = 1.0
    oblique = np.exp(1j * test_k * np.arange(N) * h * np.sin(np.deg2rad(35.0)))
    profiles = (("Profil uniforme", uniform), ("Excitation localisée", localized), ("Profil de phase oblique", oblique))
    f, _, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    source_costs, profile_fields = [], []
    for name, profile in profiles:
        load = np.zeros(domain.shape, dtype=complex)
        load[0, :] = profile
        norm = np.sqrt(np.mean(np.abs(load[dirichlet]) ** 2))
        load *= amplitude / norm
        solver.update_rhs(f, load, f_neu, f_rob)
        first = solver.solve(test_k, alphas[test_index] * initial)
        second = solver.solve(test_k, alphas[test_index] * binary)
        first_cost = solver.compute_energy(first)
        second_cost = solver.compute_energy(second)
        source_costs.append((name, first_cost, second_cost))
        profile_fields.append({"name": name, "initial": first, "binary": second,
                               "initial_cost": first_cost, "binary_cost": second_cost})
        print(name, ": énergie initial =", first_cost, ", énergie binaire =", second_cost)

    # On compare les matériaux et les niveaux avec le budget de matériau choisi.
    material_alphas = {name: compute_material_coefficients(frequencies, source, MATERIAUX[name], alpha0)
                       for name in material_names}
    if any(values is None for values in material_alphas.values()):
        return None
    candidates = []
    candidate_data = {}
    for level in (0, 1, 2):
        candidate_domain, cx, cy, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
        candidate_solver = FastHelmholtzSolver(candidate_domain, h)
        candidate_initial = preprocessing.set2zero(preprocessing._set_chi(M, N, cx, cy), candidate_domain)
        candidate_robin = candidate_domain == _env.NODE_ROBIN
        candidate_fraction = V_obj
        if fixed_covered_nodes is not None:
            if not 0 < fixed_covered_nodes <= np.count_nonzero(candidate_robin):
                print("Le budget de points garnis doit être positif et tenir sur chaque mur.")
                return None
            candidate_fraction = fixed_covered_nodes / np.count_nonzero(candidate_robin)
        candidate_full = np.zeros(candidate_domain.shape)
        candidate_full[candidate_robin] = 1.0
        for name in material_names:
            candidate_alphas = material_alphas[name]
            density, _, _ = optimize_multi_frequency(
                candidate_solver, target_k, candidate_alphas[targets], candidate_initial,
                V_obj=candidate_fraction, numb_iter=iterations, source=source, sound_speed_m_s=sound_speed_m_s,
            )
            binary_density = preprocessing.binarize_chi(density, candidate_domain, candidate_fraction)
            costs = evaluate_spectrum(candidate_solver, candidate_domain, binary_density, wavenumbers, candidate_alphas, source, sound_speed_m_s)
            reference = evaluate_spectrum(candidate_solver, candidate_domain, candidate_full, wavenumbers, candidate_alphas, source, sound_speed_m_s)
            candidate_data[f"{level}_{name}"] = {
                "domain": candidate_domain, "density": binary_density,
                "initial": preprocessing.project_density(candidate_initial, candidate_domain, candidate_fraction),
                "spectrum": costs, "full_spectrum": reference, "alphas": candidate_alphas,
            }
            candidates.append({"level": level, "material": name, "target_fraction": candidate_fraction,
                               "robin_nodes": int(candidate_robin.sum()), "covered_nodes": int(binary_density.sum()),
                               "J_band_mean": mean_cost(frequencies, costs), "J_max": float(costs.max()),
                               "J_full_band_mean": mean_cost(frequencies, reference)})
            print("Candidat", level, name, ": énergie moyen =", candidates[-1]["J_band_mean"])

    if fixed_covered_nodes is None:
        print("La fraction nodale est commune et la quantité totale dépend du niveau.")
    else:
        print("Le nombre de points garnis est commun à toutes les configurations :", fixed_covered_nodes)
    return {"frequencies": frequencies, "domain": domain, "N": N, "spacestep": h,
            "iterations_requested": iterations, "volume_fraction": V_obj,
            "source_name": source.__name__, "material_parameters": np.asarray(car_mat),
            "sound_speed_m_s": sound_speed_m_s,
            "candidates": candidates, "candidate_data": candidate_data, "fixed_covered_nodes": fixed_covered_nodes, "history": history, "target_indices": targets,
            "initial": initial, "continuous": continuous, "binary": binary,
            "initial_costs": initial_costs, "continuous_costs": continuous_costs,
            "binary_costs": binary_costs, "mixed_costs": mixed_costs, "full_costs": full_costs,
            "alternative_material": alternative, "source_costs": source_costs,
            "profile_fields": profile_fields, "profile_frequency": frequencies[test_index]}



def combine_comparable_configurations(reference_results, fixed_budget_results):
    """On retient les meilleurs placements binaires disponibles au même budget."""
    budget = fixed_budget_results["fixed_covered_nodes"]
    combined = fixed_budget_results.copy()
    combined["candidate_data"] = dict(fixed_budget_results["candidate_data"])
    candidates = []
    for fixed in fixed_budget_results["candidates"]:
        best = dict(fixed)
        best["relaxation"] = "budget_exact"
        for previous in reference_results["candidates"]:
            same_case = previous["level"] == fixed["level"] and previous["material"] == fixed["material"]
            if same_case and previous["covered_nodes"] == budget and previous["J_band_mean"] < best["J_band_mean"]:
                best = dict(previous)
                best["relaxation"] = "fraction_initiale"
                key = f"{fixed['level']}_{fixed['material']}"
                combined["candidate_data"][key] = reference_results["candidate_data"][key]
        candidates.append(best)
    combined["candidates"] = candidates
    return combined



def evaluate_selected_configuration(results, source, sound_speed_m_s):
    """On compare le meilleur placement à un placement initial binaire de même quantité."""
    selected = min(results["candidates"], key=lambda case: case["J_band_mean"])
    key = f"{selected['level']}_{selected['material']}"
    data = results["candidate_data"][key]
    domain = data["domain"]
    h = results["spacestep"]
    frequencies = results["frequencies"]
    wavenumbers = 2*np.pi*frequencies/sound_speed_m_s
    solver = FastHelmholtzSolver(domain, h)
    initial_binary = preprocessing.binarize_chi(data["initial"], domain, selected["covered_nodes"]/selected["robin_nodes"])
    initial_spectrum = evaluate_spectrum(solver, domain, initial_binary, wavenumbers, data["alphas"], source, sound_speed_m_s)
    return {"selected": selected, "domain": domain, "spacestep": h,
            "density": data["density"], "initial_density": initial_binary,
            "frequencies": frequencies, "initial_spectrum": initial_spectrum,
            "spectrum": data["spectrum"], "full_spectrum": data["full_spectrum"]}



def study_fully_covered_materials(N, frequencies, source, alpha0, sound_speed_m_s,
                                  material_names=None, levels=(0, 1, 2)):
    """On compare les matériaux sur les mêmes murs entièrement garnis et avec la même source."""
    frequencies = np.asarray(frequencies, dtype=float)
    names = list(MATERIAUX) if material_names is None else list(material_names)
    wavenumbers = 2.0 * np.pi * frequencies / sound_speed_m_s
    h = 1.0 / N
    energies, coefficients = {}, {}
    solvers, domains = {}, {}
    for level in levels:
        domain, _, _, _, _ = preprocessing._set_geometry_of_domain(2 * N, N, level=level)
        domains[level] = domain
        solvers[level] = FastHelmholtzSolver(domain, h)
    for name in names:
        print("Comparaison des murs entièrement garnis :", name, flush=True)
        alphas = compute_material_coefficients(frequencies, source, MATERIAUX[name], alpha0)
        if alphas is None:
            return None
        coefficients[name] = alphas
        energies[name] = {}
        for level in levels:
            # On garnit chaque point du mur puis on calcule le spectre.
            full = (domains[level] == _env.NODE_ROBIN).astype(float)
            energies[name][level] = evaluate_spectrum(
                solvers[level], domains[level], full, wavenumbers, alphas,
                source, sound_speed_m_s,
            )
    return {"frequencies": frequencies, "energies": energies, "alphas": coefficients,
            "material_names": names, "levels": list(levels), "N": N,
            "source_name": source.__name__, "sound_speed_m_s": sound_speed_m_s,
            "alpha0": list(alpha0), "material_parameters": {name: list(MATERIAUX[name]) for name in names}}
