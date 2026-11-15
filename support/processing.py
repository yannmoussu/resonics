# -*- coding: utf-8 -*-


import numpy
import scipy
import scipy.sparse
import scipy.sparse.linalg


import _env


def is_in_interior_domain(node):
    """On indique si le point appartient à l'intérieur du domaine."""

    if node == _env.NODE_INTERIOR:
        return True
    else:
        return False


def is_on_dirichlet_boundary(node):
    """On indique si le point porte une valeur imposée du champ."""

    if node == _env.NODE_DIRICHLET:
        return True
    else:
        return False


def is_on_neumann_boundary(node):
    """On indique si le point porte une dérivée normale imposée."""

    if node == _env.NODE_NEUMANN:
        return True
    else:
        return False


def is_on_robin_boundary(node):
    """On indique si le point appartient au mur avec une condition de Robin."""

    if node == _env.NODE_ROBIN:
        return True
    else:
        return False


def compute_stiffness_matrix(domain, space_step, f, beta_pde):
    """On construit la matrice des différences finies et le chargement volumique."""

    h = space_step
    (M, N) = numpy.shape(domain)
    K = M * N
    # On remplit une matrice creuse ligne par ligne.
    mat = scipy.sparse.lil_matrix((K, K), dtype=numpy.complex128)
    rhs = numpy.zeros((K, 1), dtype=numpy.complex128)
    for i in range(0, M):
        for j in range(0, N):
            # On associe chaque point de la grille à une ligne du système.
            row = i * N + j
            if is_in_interior_domain(domain[i, j]):
                # On relie le point intérieur à ses quatre voisins.
                mat[row, row] = -4.0 * beta_pde[i, j]
                mat[row, row - 1] = 1.0 * beta_pde[i, j - 1]
                mat[row, row + 1] = 1.0 * beta_pde[i, j + 1]
                mat[row, row + N] = 1.0 * beta_pde[i + 1, j]
                mat[row, row - N] = 1.0 * beta_pde[i - 1, j]
                rhs[row] = h ** 2 * f[i, j]
            else:
                # On réserve une ligne identité aux autres points de la grille.
                mat[row, row] = 1.0
                rhs[row] = 0.0

    return mat, rhs


def compute_mass_matrix(domain, space_step, alpha_pde):
    """On construit la matrice diagonale du terme dépendant de la fréquence."""

    h = space_step
    (M, N) = numpy.shape(domain)
    K = M * N
    mat = scipy.sparse.lil_matrix((K, K), dtype=numpy.complex128)
    rhs = numpy.zeros((K, 1), dtype=numpy.complex128)
    for i in range(0, M):
        for j in range(0, N):
            row = i * N + j
            if is_in_interior_domain(domain[i, j]):
                # On remplit uniquement la diagonale des points intérieurs.
                mat[row, row] = 1.0 * h ** 2 * alpha_pde[i, j]

    return mat, rhs


def compute_vgradu_matrix(domain, space_step, v):
    """On construit la matrice d'un terme de transport à partir du champ de vitesse."""
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
                # On adapte les voisins utilisés lorsque le point est proche du bord.
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
    """On reporte les valeurs imposées au bord dans le chargement des points intérieurs."""

    (M, N) = numpy.shape(domain)
    for i in range(0, M):
        for j in range(0, N):

            if is_in_interior_domain(domain[i, j]):
                # On repère les voisins dont la valeur du champ est imposée.
                north = is_on_dirichlet_boundary(domain[i - 1, j])
                south = is_on_dirichlet_boundary(domain[i + 1, j])
                east = is_on_dirichlet_boundary(domain[i, j + 1])
                west = is_on_dirichlet_boundary(domain[i, j - 1])
                row = i * N + j
                # On retire chaque voisin imposé de la matrice et on reporte sa valeur au chargement.
                if north:
                    mat[row, row - N] -= beta_pde[i - 1, j]
                    rhs[row] -= beta_pde[i - 1, j] * f_dir[i - 1, j] / alpha_dir[i - 1, j]
                if south:
                    mat[row, row + N] -= beta_pde[i + 1, j]
                    rhs[row] -= beta_pde[i + 1, j] * f_dir[i + 1, j] / alpha_dir[i + 1, j]
                if east:
                    mat[row, row + 1] -= beta_pde[i, j + 1]
                    rhs[row] -= beta_pde[i, j + 1] * f_dir[i, j + 1] / alpha_dir[i, j + 1]
                if west:
                    mat[row, row - 1] -= beta_pde[i, j - 1]
                    rhs[row] -= beta_pde[i, j - 1] * f_dir[i, j - 1] / alpha_dir[i, j - 1]

    return mat, rhs


def compute_neumann_condition(domain, space_step, f_neu, beta_neu, beta_pde, mat, rhs):
    """On remplace les voisins de Neumann par leur relation avec le point intérieur."""

    h = space_step
    (M, N) = numpy.shape(domain)
    for i in range(0, M):
        for j in range(0, N):

            if is_in_interior_domain(domain[i, j]):
                # On repère les voisins dont la dérivée normale est prescrite.
                north = is_on_neumann_boundary(domain[i - 1, j])
                south = is_on_neumann_boundary(domain[i + 1, j])
                east = is_on_neumann_boundary(domain[i, j + 1])
                west = is_on_neumann_boundary(domain[i, j - 1])
                row = i * N + j
                # On reporte chaque relation de bord dans la diagonale et le chargement.
                if north:
                    mat[row, row - N] -= beta_pde[i - 1, j]
                    mat[row, row] += beta_pde[i - 1, j]
                    rhs[row] -= beta_pde[i - 1, j] * h * f_neu[i - 1, j] / beta_neu[i - 1, j]
                if south:
                    mat[row, row + N] -= beta_pde[i + 1, j]
                    mat[row, row] += beta_pde[i + 1, j]
                    rhs[row] -= beta_pde[i + 1, j] * h * f_neu[i + 1, j] / beta_neu[i + 1, j]
                if east:
                    mat[row, row + 1] -= beta_pde[i, j + 1]
                    mat[row, row] += beta_pde[i, j + 1]
                    rhs[row] -= beta_pde[i, j + 1] * h * f_neu[i, j + 1] / beta_neu[i, j + 1]
                if west:
                    mat[row, row - 1] -= beta_pde[i, j - 1]
                    mat[row, row] += beta_pde[i, j - 1]
                    rhs[row] -= beta_pde[i, j - 1] * h * f_neu[i, j - 1] / beta_neu[i, j - 1]

    return mat, rhs


def compute_robin_condition(domain, space_step, f_rob, alpha_rob, beta_rob, beta_pde, mat, rhs):
    """On prend en compte l'absorption des voisins qui appartiennent au mur."""
    h = space_step
    M, N = domain.shape
    for i in range(M):
        for j in range(N):
            if is_in_interior_domain(domain[i, j]):
                row = i * N + j
                # On traite chaque face reliant un point intérieur au mur.
                for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if is_on_robin_boundary(domain[a, b]):
                        coefficient = beta_pde[a, b]
                        # On utilise la convention où le terme d'absorption est ajouté à la dérivée normale.
                        denominator = beta_rob[a, b] + h * alpha_rob[a, b]
                        # On reporte la relation de bord dans la diagonale et le chargement.
                        mat[row, a * N + b] -= coefficient
                        mat[row, row] += coefficient * beta_rob[a, b] / denominator
                        rhs[row] -= coefficient * h * f_rob[a, b] / denominator
    return mat, rhs


def prepare_helmholtz_system(domain, space_step, beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob):
    """On prépare les matrices et les voisins de bord qui restent fixes."""
    # On assemble les parties fixes avec des chargements nuls.
    zero = numpy.zeros(domain.shape, dtype=numpy.complex128)
    matrix, rhs = compute_stiffness_matrix(domain, space_step, zero, beta_pde)
    mass, _ = compute_mass_matrix(domain, space_step, alpha_pde)
    matrix, rhs = compute_dirichlet_condition(domain, zero, alpha_dir, beta_pde, matrix, rhs)
    matrix, rhs = compute_neumann_condition(domain, space_step, zero, beta_neu, beta_pde, matrix, rhs)
    matrix, rhs = compute_robin_condition(domain, space_step, zero, zero, beta_rob, beta_pde, matrix, rhs)
    # On enregistre une contribution pour chaque voisin de bord rencontré.
    faces = {kind: [[], [], []] for kind in ('dirichlet', 'neumann', 'robin')}
    M, N = domain.shape
    for i, j in numpy.argwhere(domain == _env.NODE_INTERIOR):
        for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            kind = {_env.NODE_DIRICHLET: 'dirichlet', _env.NODE_NEUMANN: 'neumann',
                    _env.NODE_ROBIN: 'robin'}.get(domain[a, b])
            if kind is not None:
                faces[kind][0].append(i * N + j)
                faces[kind][1].append(a * N + b)
                faces[kind][2].append(beta_pde[a, b])
    # On conserve les matrices fixes et les correspondances avec la grille.
    prepared = {'stiffness': matrix.tocsr(), 'mass': mass.tocsr(),
                'interior_mask': (domain == _env.NODE_INTERIOR).ravel(), 'shape': domain.shape}
    prepared['stiffness'].eliminate_zeros()
    for kind, (rows, nodes, coefficients) in faces.items():
        prepared[kind + '_rows'] = numpy.asarray(rows, dtype=int)
        prepared[kind + '_nodes'] = numpy.asarray(nodes, dtype=int)
        prepared[kind + '_coefficients'] = numpy.asarray(coefficients, dtype=complex)
    # On prépare les facteurs multiplicatifs des chargements de bord.
    prepared['dirichlet_factors'] = prepared['dirichlet_coefficients'] / alpha_dir.ravel()[prepared['dirichlet_nodes']]
    prepared['neumann_factors'] = space_step * prepared['neumann_coefficients'] / beta_neu.ravel()[prepared['neumann_nodes']]
    prepared['robin_beta'] = beta_rob.ravel()[prepared['robin_nodes']]
    return prepared


def assemble_helmholtz_system(domain, space_step, omega, f, f_dir, f_neu, f_rob,
                             beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                             prepared=None):
    """On assemble le système avec les données de la fréquence et du placement choisis."""
    if prepared is None:

        # On assemble toutes les contributions lorsqu'aucune préparation n'est fournie.
        matrix, rhs = compute_stiffness_matrix(domain, space_step, f, beta_pde)
        mass, _ = compute_mass_matrix(domain, space_step, alpha_pde)
        matrix = matrix + omega ** 2 * mass
        matrix, rhs = compute_dirichlet_condition(domain, f_dir, alpha_dir, beta_pde, matrix, rhs)
        matrix, rhs = compute_neumann_condition(domain, space_step, f_neu, beta_neu, beta_pde, matrix, rhs)
        matrix, rhs = compute_robin_condition(domain, space_step, f_rob, alpha_rob, beta_rob, beta_pde, matrix, rhs)
        rhs = rhs.ravel()
    else:

        # On réutilise les matrices fixes et on actualise les chargements.
        matrix = prepared['stiffness'] + omega ** 2 * prepared['mass']
        rhs = space_step ** 2 * numpy.asarray(f).ravel() * prepared['interior_mask']
        rhs = rhs.astype(complex)
        # On additionne les contributions lorsqu'un point intervient sur plusieurs faces.
        numpy.add.at(rhs, prepared['dirichlet_rows'],
                     -prepared['dirichlet_factors'] * numpy.asarray(f_dir).ravel()[prepared['dirichlet_nodes']])
        numpy.add.at(rhs, prepared['neumann_rows'],
                     -prepared['neumann_factors'] * numpy.asarray(f_neu).ravel()[prepared['neumann_nodes']])
        # On actualise la diagonale pour le matériau présent sur chaque point du mur.
        rows, nodes = prepared['robin_rows'], prepared['robin_nodes']
        coefficient, beta = prepared['robin_coefficients'], prepared['robin_beta']
        alpha = numpy.asarray(alpha_rob).ravel()[nodes]
        denominator = beta + space_step * alpha
        diagonal = numpy.zeros(domain.size, dtype=complex)
        numpy.add.at(diagonal, rows, -coefficient * space_step * alpha / denominator)
        matrix = matrix + scipy.sparse.diags(diagonal)
        numpy.add.at(rhs, rows, -coefficient * space_step * numpy.asarray(f_rob).ravel()[nodes] / denominator)
    # On prépare le stockage de la matrice pour sa factorisation.
    matrix = matrix.tocsc()
    matrix.eliminate_zeros()
    return matrix, rhs


def solve_helmholtz(domain, space_step, omega,
                    f, f_dir, f_neu, f_rob,
                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                    prepared=None, return_system=False):
    """On résout le champ à partir du nombre d'onde fourni.

    On restitue les valeurs intérieures dans un tableau ayant la forme du domaine.
    On peut aussi renvoyer la matrice et sa factorisation pour le calcul adjoint.
    """
    matrix, rhs = assemble_helmholtz_system(
        domain, space_step, omega, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob, prepared,
    )
    # On factorise la matrice puis on résout le système linéaire.
    factor = scipy.sparse.linalg.splu(matrix)
    sol = factor.solve(rhs)
    # On restitue le champ intérieur dans un tableau de la taille de la grille.
    u = numpy.zeros(domain.shape, dtype=numpy.complex128)
    interior = domain == _env.NODE_INTERIOR
    u[interior] = sol.reshape(domain.shape)[interior]
    # On peut réutiliser la factorisation pour résoudre le problème adjoint.
    if return_system:
        return u, matrix, factor
    return u
