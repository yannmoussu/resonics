# -*- coding: utf-8 -*-


import matplotlib.pyplot
import numpy
import os


import _env
from processing import is_in_interior_domain, is_on_robin_boundary


def set2zero(alpha, domain_omega):
    """On met à zéro les valeurs qui ne se trouvent pas sur le mur."""

    (M, N) = numpy.shape(domain_omega)
    for i in range(0, M):
        for j in range(0, N):
            # On conserve uniquement les valeurs situées sur la paroi.
            if domain_omega[i, j] != _env.NODE_ROBIN:
                alpha[i, j] = 0

    return alpha


def replace_old_by_new(u, oldvalue, newvalue):
    """On remplace toutes les occurrences d'une valeur dans le tableau fourni."""
    (M, N) = numpy.shape(u)
    for i in range(M):
        for j in range(N):
            if u[i, j] == oldvalue:
                u[i, j] = newvalue
    return u


def _set_coefficients_of_pde(M, N):
    """On crée les tableaux de coefficients constants du domaine et de ses bords."""
    beta_pde = numpy.ones((M, N), dtype=numpy.complex128)
    alpha_pde = numpy.ones((M, N), dtype=numpy.complex128)
    alpha_dir = numpy.ones((M, N), dtype=numpy.complex128)
    beta_neu = numpy.ones((M, N), dtype=numpy.complex128)
    alpha_rob = numpy.ones((M, N), dtype=numpy.complex128)
    beta_rob = numpy.ones((M, N), dtype=numpy.complex128)
    return beta_pde, alpha_pde, alpha_dir, beta_neu, alpha_rob, beta_rob


def _set_rhs_of_pde(M, N):
    """On crée des tableaux de chargement initialement nuls."""
    f = numpy.zeros((M, N), dtype=numpy.complex128)
    f_dir = numpy.zeros((M, N), dtype=numpy.complex128)
    f_neu = numpy.zeros((M, N), dtype=numpy.complex128)
    f_rob = numpy.zeros((M, N), dtype=numpy.complex128)
    return f, f_dir, f_neu, f_rob


def _set_geometry_of_domain(M, N, level=0):
    """On construit les points intérieurs, les bords et la paroi fractale."""
    # On réserve un tableau de codes pour distinguer les zones de la grille.
    domain_omega = numpy.zeros((M, N), dtype=numpy.int64)

    # On marque d'abord l'intérieur puis le cadre extérieur de la grille.
    domain_omega[0:M, 0:N] = _env.NODE_INTERIOR
    domain_omega[0, 0:N] = _env.NODE_DIRICHLET
    domain_omega[M-1, 0:N] = _env.NODE_NEUMANN
    domain_omega[0:M, 0] = _env.NODE_NEUMANN
    domain_omega[0:M, N - 1] = _env.NODE_NEUMANN

    # On place directement une paroi horizontale pour le niveau sans motif.
    if level == 0:
        domain_omega[N, 0:N] = _env.NODE_ROBIN
    else:
        domain_omega[M-1, 0:N] = _env.NODE_NEUMANN

    # On construit les sommets du contour puis tous ses points sur la grille.
    nodes = create_fractal_nodes([numpy.array([[0], [N]]), numpy.array([[N], [N]])], level)
    x, y = create_fractal_coordinates(nodes, domain_omega)
    x_plot = numpy.zeros(len(x) - 1, dtype=numpy.float64)
    y_plot = numpy.zeros(len(x) - 1, dtype=numpy.float64)

    # On attribue la condition de Robin aux points du contour.
    for k in range(0, len(x) - 1):
        domain_omega[int(y[k]), int(x[k])] = _env.NODE_ROBIN
    # On part d'un point sous le mur pour marquer la zone extérieure.
    seed1 = [M-2, N-2]
    domain_omega = partition_domain(domain_omega, seed1)

    return domain_omega, x, y, x_plot, y_plot


def _set_chi(M, N, x, y):
    """On garnit une portion initiale du contour avec une densité uniforme."""
    chi = numpy.zeros((M, N), dtype=numpy.float64)
    # On choisit les indices qui délimitent la portion initialement garnie.
    k_begin = (len(x) - 1) // 5
    k_end = 3 * (len(x) - 1) // 5
    val = 1.0
    for k in range(k_begin, k_end):
        chi[int(y[k]), int(x[k])] = val
    return chi


def create_motif_koch(A, B):
    """On remplace un segment par un motif orthogonal de huit segments."""

    # On construit une rotation d'un quart de tour.
    alpha = numpy.pi / 2.0
    radius = numpy.array([[numpy.cos(alpha), -numpy.sin(alpha)],
                          [numpy.sin(alpha), numpy.cos(alpha)]])
    # On partage le déplacement entre les extrémités en quatre.
    distance = (B - A) / 4.0
    C = A + distance
    D = C + numpy.dot(radius, distance)
    E = D + distance
    F = E - numpy.dot(radius, distance)
    G = F - numpy.dot(radius, distance)
    H = G + distance
    I = H + numpy.dot(radius, distance)

    return [A, C, D, E, F, G, H, I, B]


def create_fractal_nodes(nodes, n_iter):
    """On répète le motif sur chaque segment pour construire les sommets du contour."""

    n = 0
    # On remplace tous les segments par un nouveau motif à chaque niveau.
    while n < n_iter:
        new_nodes = []
        for k in range(len(nodes) - 1):
            a = nodes[k]
            b = nodes[k + 1]
            temp = create_motif_koch(a, b)
            new_nodes = new_nodes + temp
        n += 1
        nodes = new_nodes

    return nodes


def create_fractal_coordinates(nodes, domain):
    """On transforme les sommets du contour en une suite de points de la grille."""

    # On arrondit les sommets pour supprimer les petites erreurs dues aux rotations.
    a = []
    b = []
    for k in range(0, len(nodes)):
        a.append(round(nodes[k][0][0]))
        b.append(round(nodes[k][1][0]))
    current_node = [[a[k], b[k]] for k in range(len(nodes))]
    l = []
    # On parcourt tous les points entre deux sommets successifs.
    for k in range(0, len(current_node) - 1):

        n = current_node[k + 1][0] - current_node[k][0]
        m = current_node[k + 1][1] - current_node[k][1]
        if n > 0:
            for o in range(0, int(n) + 1):
                a = [[current_node[k][0] + o], [current_node[k][1]]]
                l.append(a)
        elif m > 0:
            for o in range(0, int(m) + 1):
                a = [[current_node[k][0]], [current_node[k][1] + o]]
                l.append(a)
        elif m < 0:
            for o in range(0, int(-m) + 1):
                a = [[current_node[k][0]], [current_node[k][1] - o]]
                l.append(a)
        elif n < 0:
            for o in range(0, int(-n) + 1):
                a = [[current_node[k][0] - o], [current_node[k][1]]]
                l.append(a)
    x = []
    y = []
    for k in range(0, len(l)):
        x.append(l[k][0][0])
        y.append(l[k][1][0])

    (M, N) = numpy.shape(domain)

    # On prolonge le contour jusqu'aux côtés de la grille.
    while x[-1] < N:
        x.append(x[-1] + 1)
        y.append(y[-1])

    while x[0] > 0:
        x.insert(0, x[0] - 1)
        y.insert(0, y[0])

    return x, y


def is_on_boundary(node):
    """On indique si le code du point correspond à un bord."""

    if node not in [_env.NODE_ROBIN, _env.NODE_NEUMANN, _env.NODE_DIRICHLET]:
        return 'NOT BOUNDARY'
    else:
        return 'BOUNDARY'


def partition_domain(domain, seed):
    """On propage un marquage depuis un point sans franchir les bords."""

    (M, N) = numpy.shape(domain)
    # On conserve les points à visiter et ceux déjà parcourus.
    Neighbours = [seed]
    Visited = []

    # On écarte une graine placée sur un bord.
    if is_on_boundary(domain[seed[0], seed[1]]) == 'BOUNDARY':
        return 'Error: choose another point for seed'

    else:
        count = 0
        # On traite les points en attente tant que la zone reste accessible.
        while len(Neighbours) > 0:

            i = Neighbours[0][0]
            j = Neighbours[0][1]

            # On ne prend en compte que les voisins présents dans la grille.
            if i == 0:
                if j == 0:
                    south = [i + 1, j]
                    east = [i, j + 1]
                    a = 'Not Exist'
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = 'Not Exist'
                elif j == N - 1:
                    south = [i + 1, j]
                    west = [i, j - 1]
                    a = 'Not Exist'
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = 'Not Exist'
                    d = is_on_boundary(domain[west[0], west[1]])
                else:
                    south = [i + 1, j]
                    west = [i, j - 1]
                    east = [i, j + 1]
                    a = 'Not Exist'
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = is_on_boundary(domain[west[0], west[1]])
            # On traite le bas de la grille.
            elif i == M - 1:
                if j == 0:
                    north = [i - 1, j]
                    east = [i, j + 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = 'Not Exist'
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = 'Not Exist'
                elif j == N - 1:
                    north = [i - 1, j]
                    west = [i, j - 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = 'Not Exist'
                    c = 'Not Exist'
                    d = is_on_boundary(domain[west[0], west[1]])
                else:
                    north = [i - 1, j]
                    west = [i, j - 1]
                    east = [i, j + 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = 'Not Exist'
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = is_on_boundary(domain[west[0], west[1]])
            # On traite le côté droit de la grille.
            elif j == N - 1:
                if i == 0:
                    south = [i + 1, j]
                    west = [i, j - 1]
                    a = 'Not Exist'
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = 'Not Exist'
                    d = is_on_boundary(domain[west[0], west[1]])
                elif i == M - 1:
                    north = [i - 1, j]
                    west = [i, j - 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = 'Not Exist'
                    c = 'Not Exist'
                    d = is_on_boundary(domain[west[0], west[1]])
                else:
                    north = [i - 1, j]
                    south = [i + 1, j]
                    west = [i, j - 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = 'Not Exist'
                    d = is_on_boundary(domain[west[0], west[1]])
            # On traite le côté gauche de la grille.
            elif j == 0:
                if i == 0:
                    south = [i + 1, j]
                    east = [i, j + 1]
                    a = 'Not Exist'
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = 'Not Exist'
                elif i == M - 1:
                    north = [i - 1, j]
                    east = [i, j + 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = 'Not Exist'
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = 'Not Exist'
                else:
                    north = [i - 1, j]
                    south = [i + 1, j]
                    east = [i, j + 1]
                    a = is_on_boundary(domain[north[0], north[1]])
                    b = is_on_boundary(domain[south[0], south[1]])
                    c = is_on_boundary(domain[east[0], east[1]])
                    d = 'Not Exist'

            else:
                north = [i - 1, j]
                south = [i + 1, j]
                east = [i, j + 1]
                west = [i, j - 1]
                a = is_on_boundary(domain[north[0], north[1]])
                b = is_on_boundary(domain[south[0], south[1]])
                c = is_on_boundary(domain[east[0], east[1]])
                d = is_on_boundary(domain[west[0], west[1]])

            # On marque le point comme extérieur puis on le retire de la liste d'attente.
            domain[i, j] = _env.NODE_COMPLEMENTARY
            Neighbours.pop(0)
            Visited.append([i, j])
            count += 1

            # On ajoute les voisins libres qui n'ont pas encore été rencontrés.
            if a == 'NOT BOUNDARY' and north not in Visited and north not in Neighbours:
                Neighbours.append(north)
            if b == 'NOT BOUNDARY' and south not in Visited and south not in Neighbours:
                Neighbours.append(south)
            if c == 'NOT BOUNDARY' and east not in Visited and east not in Neighbours:
                Neighbours.append(east)
            if d == 'NOT BOUNDARY' and west not in Visited and west not in Neighbours:
                Neighbours.append(west)
            # On limite le parcours au nombre de points de la grille.
            if count > M * N:
                return Neighbours, Visited

    return domain


def amplitude_rer_b(frequency_hz):
    """On additionne trois composantes gaussiennes pour obtenir l'amplitude de la source."""
    frequency_hz = float(frequency_hz)

    # Chaque composante possède un centre, une largeur et une amplitude relative.
    composantes = (
        (200.0, 100.0, 1.0),
        (800.0, 350.0, 0.8),
        (2500.0, 150.0, 0.5),
    )
    amplitude = 0.0
    # On additionne les amplitudes des trois contributions à la fréquence demandée.
    for centre, largeur, poids in composantes:
        amplitude += poids * numpy.exp(
            -0.5 * ((frequency_hz - centre) / largeur) ** 2
        )
    return float(amplitude)


def source_rer_b(y, omega):
    """On convertit la pulsation en fréquence puis on évalue la source ferroviaire."""
    return amplitude_rer_b(float(omega) / (2.0 * numpy.pi))


def source_constant(y, omega):
    """On renvoie une source uniforme d'amplitude constante."""
    return 1.0
