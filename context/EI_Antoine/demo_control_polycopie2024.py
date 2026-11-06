# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import numpy
import os


# MRG packages
import _env
import preprocessing
import processing
import postprocessing
import compute_alpha
#import solutions

def compute_chi_1(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, chi):
    
    alpha_rob = Alpha * chi
    u = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
    energy = your_compute_objective_function(domain_omega, u, spacestep)
    return energy


def plot_energy_frequency_one_material(domain_omega, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
                                       beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                                       chi, g_source, name, material, level, save=True, annotate=True):
    
    print('Material %s' % name)
    wavenumbers = 2.0 * numpy.pi * frequencies / c
    energies = numpy.zeros(len(wavenumbers))
    alpha0 = compute_alpha.Alpha0
    for n, k in enumerate(wavenumbers):
        # Alpha optimal à la pulsation omega = c * k, initialisé avec l'Alpha de la fréquence précédente
        alpha_opt, success, message = compute_alpha.compute_alpha(c * k, g_source, material, alpha0)
        if not success:
            print('compute_alpha (f = %g Hz) : %s' % (frequencies[n], message))
        alpha0 = alpha_opt
        Alpha_k = alpha_opt[0] + alpha_opt[1] * 1j
        # source RER B imposée sur le bord supérieur
        f_dir_freq = numpy.zeros_like(f_dir)
        f_dir_freq[0, :] = preprocessing.source_rer_b(frequencies[n])
        energies[n] = compute_chi_1(domain_omega, spacestep, k, f, f_dir_freq, f_neu, f_rob,
                                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                                    Alpha_k, chi)
    line, = matplotlib.pyplot.plot(frequencies, energies, label=name)

    # -- maxima locaux de l'énergie (pics), marqués par une croix avec leur fréquence
    peaks = [n for n in range(1, len(energies) - 1)
             if energies[n] > energies[n - 1] and energies[n] > energies[n + 1]]
    matplotlib.pyplot.plot(frequencies[peaks], energies[peaks], 'x', color=line.get_color())
    for n in (peaks if annotate else []):
        if frequencies[n] > 1350.0:  # pas d'étiquette pour les pics au-dessus de 1350 Hz
            continue
        matplotlib.pyplot.annotate('%g Hz' % frequencies[n], (frequencies[n], energies[n]),
                                   textcoords='offset points', xytext=(0, 5), ha='center', fontsize=7)
    print('%s : pics d\'énergie aux fréquences (Hz) %s' % (name, frequencies[peaks]))

    if save:
        matplotlib.pyplot.xlabel('frequency f (Hz)')
        matplotlib.pyplot.ylabel('energy J')
        matplotlib.pyplot.title('Energy vs frequency, fractal level %d, %s, $\\chi = 1$' % (level, name))
        matplotlib.pyplot.legend()
        os.makedirs('courbes_energie', exist_ok=True)
        matplotlib.pyplot.savefig(os.path.join('courbes_energie', 'fig_energy_frequency_level%d_%s.jpg' % (level, name)))
        matplotlib.pyplot.close()

    return energies, frequencies[peaks]


def plot_energy_frequency_all_materials(domain_omega, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
                                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                                        chi, g_source, level):
    
    for name, material in compute_alpha.MATERIAUX.items():
        plot_energy_frequency_one_material(domain_omega, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
                                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                                           chi, g_source, name, material, level, save=False)

    matplotlib.pyplot.xlabel('frequency f (Hz)')
    matplotlib.pyplot.ylabel('energy J')
    matplotlib.pyplot.title('Energy vs frequency, fractal level %d, $\\chi = 1$' % level)
    matplotlib.pyplot.legend()
    os.makedirs('courbes_energie', exist_ok=True)
    matplotlib.pyplot.savefig(os.path.join('courbes_energie', 'fig_energy_frequency_level%d.jpg' % level))
    matplotlib.pyplot.close()


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

    (M, N) = numpy.shape(domain_omega)
    k_max = 100  # nombre maximal d'itérations
    delta = 1e-5  # critère d'arrêt |chi_{n+1} - chi_n| < delta
    robin = domain_omega == _env.NODE_ROBIN
    S = numpy.sum(robin)  # nombre de noeuds de Robin
    energy = numpy.zeros((k_max + 1, 1), dtype=numpy.float64)

    n = 0
    u = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                   beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi)
    energy[n, 0] = your_compute_objective_function(domain_omega, u, spacestep)
    variation = 1.0

    while variation >= delta and n < k_max and mu > 1e-10:
        alpha_rob = Alpha * chi

        # -- problème adjoint (7.39)
        p = processing.solve_helmholtz(domain_omega, spacestep, omega, -2.0 * numpy.conj(u),
                                       numpy.zeros((M, N), dtype=numpy.complex128), f_neu, f_rob,
                                       beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)

        # -- valeurs de u et p sur Gamma : le solveur les laisse à 0 sur le bord, on les déduit du
        # -- voisin intérieur par la condition de Robin discrète u_b = u_i / (1 - alpha_rob h)
        u_gamma = numpy.zeros((M, N), dtype=numpy.complex128)
        p_gamma = numpy.zeros((M, N), dtype=numpy.complex128)
        for (i, j) in numpy.argwhere(robin):
            for (a, b) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= a < M and 0 <= b < N and domain_omega[a, b] == _env.NODE_INTERIOR:
                    u_gamma[i, j] = u[a, b] / (1.0 - alpha_rob[i, j] * spacestep)
                    p_gamma[i, j] = p[a, b] / (1.0 - alpha_rob[i, j] * spacestep)

        # -- gradient : -Re(alpha u p) or ici la convention sur le alpha n'est pas la même donc -alpha
        grad = numpy.real(Alpha * u_gamma * p_gamma)

        # -- chi_{n+1} = max(0, min(chi_n - mu grad + l, 1)), l par dichotomie pour respecter beta
        chi_tilde = chi - mu * grad

        # -- dichotomie pour trouver l pour la projection sur U_ab* en respectant le volume
        l_min, l_max = -1.0 - numpy.max(numpy.abs(chi_tilde)), 1.0 + numpy.max(numpy.abs(chi_tilde))
        for _ in range(60):
            l = (l_min + l_max) / 2.0
            chi_new = preprocessing.set2zero(numpy.maximum(0.0, numpy.minimum(chi_tilde + l, 1.0)), domain_omega)
            if numpy.sum(chi_new) / S > V_obj:
                l_max = l
            else:
                l_min = l

        u_new = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi_new)
        energy_new = your_compute_objective_function(domain_omega, u_new, spacestep)

        # -- calcul du step pour la descente de gradient
        if energy_new < energy[n, 0]:
            mu = mu + 0.001
            variation = numpy.max(numpy.abs(chi_new - chi))
            chi, u = chi_new, u_new
            n += 1
            energy[n, 0] = energy_new
        else:
            mu = mu / 2.0

    # -- projection finale sur U_ad(beta) : les plus grandes valeurs de chi valent 1, les autres 0
    nodes = numpy.argwhere(robin)[numpy.argsort(-chi[robin], kind='stable')]
    chi = numpy.zeros((M, N), dtype=numpy.float64)
    for (i, j) in nodes[:int(round(V_obj * S))]:
        chi[i, j] = 1.0
    u = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                   beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi)

    return chi, energy, u, grad


def your_multifrequency_optimization(domain_omega, spacestep, frequencies, c, f, f_neu, f_rob,
                                     beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                                     material, g_source, mu, chi, V_obj):

    (M, N) = numpy.shape(domain_omega)
    k_max = 100  # nombre maximal d'itérations
    delta = 1e-5  # critère d'arrêt |chi_{n+1} - chi_n| < delta
    robin = domain_omega == _env.NODE_ROBIN
    S = numpy.sum(robin)  # nombre de noeuds de Robin
    energy = numpy.zeros((k_max + 1, 1), dtype=numpy.float64)

    # -- poids des trapèzes, divisés par la largeur de la bande : J^ est alors l'énergie
    # -- moyenne sur les fréquences, même minimum mais gradient à la même échelle qu'à une fréquence
    n_f = len(frequencies)
    weights = numpy.ones(n_f)
    if n_f > 1:
        weights = numpy.zeros(n_f)
        for j in range(n_f - 1):
            weights[j] += (frequencies[j + 1] - frequencies[j]) / 2.0
            weights[j + 1] += (frequencies[j + 1] - frequencies[j]) / 2.0
        weights = weights / (frequencies[-1] - frequencies[0])

    # -- nombre d'onde, Alpha et source RER B pour chaque fréquence (comme dans
    # -- plot_energy_frequency_one_material)
    wavenumbers = 2.0 * numpy.pi * frequencies / c
    Alphas = []
    f_dirs = []
    alpha0 = compute_alpha.Alpha0
    for j in range(n_f):
        alpha_opt, success, message = compute_alpha.compute_alpha(c * wavenumbers[j], g_source, material, alpha0)
        if not success:
            print('compute_alpha (f = %g Hz) : %s' % (frequencies[j], message))
        alpha0 = alpha_opt
        Alphas.append(alpha_opt[0] + alpha_opt[1] * 1j)
        f_dir_j = numpy.zeros((M, N), dtype=numpy.complex128)
        f_dir_j[0, :] = preprocessing.source_rer_b(frequencies[j])
        f_dirs.append(f_dir_j)

    # -- solutions et énergie totale pour chi_0
    us = [processing.solve_helmholtz(domain_omega, spacestep, wavenumbers[j], f, f_dirs[j], f_neu, f_rob,
                                     beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alphas[j] * chi)
          for j in range(n_f)]
    n = 0
    energy[n, 0] = sum(weights[j] * your_compute_objective_function(domain_omega, us[j], spacestep)
                       for j in range(n_f))
    variation = 1.0

    while variation >= delta and n < k_max and mu > 1e-10:
        # -- gradient de J^ : somme pondérée des gradients à chaque fréquence
        grad = numpy.zeros((M, N), dtype=numpy.float64)
        for j in range(n_f):
            alpha_rob = Alphas[j] * chi
            p = processing.solve_helmholtz(domain_omega, spacestep, wavenumbers[j], -2.0 * numpy.conj(us[j]),
                                           numpy.zeros((M, N), dtype=numpy.complex128), f_neu, f_rob,
                                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
            u_gamma = numpy.zeros((M, N), dtype=numpy.complex128)
            p_gamma = numpy.zeros((M, N), dtype=numpy.complex128)
            for (i, l) in numpy.argwhere(robin):
                for (a, b) in [(i - 1, l), (i + 1, l), (i, l - 1), (i, l + 1)]:
                    if 0 <= a < M and 0 <= b < N and domain_omega[a, b] == _env.NODE_INTERIOR:
                        u_gamma[i, l] = us[j][a, b] / (1.0 - alpha_rob[i, l] * spacestep)
                        p_gamma[i, l] = p[a, b] / (1.0 - alpha_rob[i, l] * spacestep)
            grad += weights[j] * numpy.real(Alphas[j] * u_gamma * p_gamma)

        # -- chi_{n+1} = max(0, min(chi_n - mu grad + l, 1)), l par dichotomie pour respecter beta
        chi_tilde = chi - mu * grad
        l_min, l_max = -1.0 - numpy.max(numpy.abs(chi_tilde)), 1.0 + numpy.max(numpy.abs(chi_tilde))
        for _ in range(60):
            l = (l_min + l_max) / 2.0
            chi_new = preprocessing.set2zero(numpy.maximum(0.0, numpy.minimum(chi_tilde + l, 1.0)), domain_omega)
            if numpy.sum(chi_new) / S > V_obj:
                l_max = l
            else:
                l_min = l

        us_new = [processing.solve_helmholtz(domain_omega, spacestep, wavenumbers[j], f, f_dirs[j], f_neu, f_rob,
                                             beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alphas[j] * chi_new)
                  for j in range(n_f)]
        energy_new = sum(weights[j] * your_compute_objective_function(domain_omega, us_new[j], spacestep)
                         for j in range(n_f))

        # -- calcul du pas pour la descente de gradient
        if energy_new < energy[n, 0]:
            mu = mu + 0.001
            variation = numpy.max(numpy.abs(chi_new - chi))
            chi, us = chi_new, us_new
            n += 1
            energy[n, 0] = energy_new
        else:
            mu = mu / 2.0

    # -- projection finale sur U_ab(beta) : les plus grandes valeurs de chi valent 1, les autres 0
    nodes = numpy.argwhere(robin)[numpy.argsort(-chi[robin], kind='stable')]
    chi = numpy.zeros((M, N), dtype=numpy.float64)
    for (i, j) in nodes[:int(round(V_obj * S))]:
        chi[i, j] = 1.0

    return chi, energy


def your_band_optimization(domain_omega, spacestep, frequencies, c, f, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                           material, g_source, mu, chi, V_obj):

    (M, N) = numpy.shape(domain_omega)
    k_max = 100  # nombre maximal d'itérations
    delta = 1e-5  # critère d'arrêt |chi_{n+1} - chi_n| < delta
    a = 8.0  # paramètre projection sigmoïde
    robin = domain_omega == _env.NODE_ROBIN
    S = numpy.sum(robin)  # nombre de noeuds de Robin
    energy = numpy.zeros((k_max + 1, 1), dtype=numpy.float64)

    # -- poids des trapèzes, divisés par la largeur de la bande (énergie moyenne sur I)
    n_f = len(frequencies)
    weights = numpy.zeros(n_f)
    for j in range(n_f - 1):
        weights[j] += (frequencies[j + 1] - frequencies[j]) / 2.0
        weights[j + 1] += (frequencies[j + 1] - frequencies[j]) / 2.0
    weights = weights / (frequencies[-1] - frequencies[0])

    # -- nombre d'onde, Alpha et source RER B pour chaque fréquence
    wavenumbers = 2.0 * numpy.pi * frequencies / c
    Alphas = []
    f_dirs = []
    alpha0 = compute_alpha.Alpha0
    for j in range(n_f):
        alpha_opt, success, message = compute_alpha.compute_alpha(c * wavenumbers[j], g_source, material, alpha0)
        if not success:
            print('compute_alpha (f = %g Hz) : %s' % (frequencies[j], message))
        alpha0 = alpha_opt
        Alphas.append(alpha_opt[0] + alpha_opt[1] * 1j)
        f_dir_j = numpy.zeros((M, N), dtype=numpy.complex128)
        f_dir_j[0, :] = preprocessing.source_rer_b(frequencies[j])
        f_dirs.append(f_dir_j)

    # -- meilleur point accepté chi_n ; à k = 0, grad = 0 donc on évalue P(chi_0)
    chi_best = chi.copy()
    grad = numpy.zeros((M, N), dtype=numpy.float64)
    energy_best = numpy.inf

    for k in range(k_max + 1):
        # -- chi_{n+1} = P(chi_n - mu J^'(chi_n)), projection sigmoïde : Phi(chi + l) avec
        # -- Phi(x) = 1 / (1 + exp(-a (x - 1/2))), l par dichotomie pour respecter beta
        chi_tilde = chi_best - mu * grad
        l_min, l_max = -5.0 - numpy.max(numpy.abs(chi_tilde)), 5.0 + numpy.max(numpy.abs(chi_tilde))
        for _ in range(60):
            l = (l_min + l_max) / 2.0
            chi = preprocessing.set2zero(1.0 / (1.0 + numpy.exp(-a * (chi_tilde + l - 0.5))), domain_omega)
            if numpy.sum(chi) / S > V_obj:
                l_max = l
            else:
                l_min = l

        us = [processing.solve_helmholtz(domain_omega, spacestep, wavenumbers[j], f, f_dirs[j], f_neu, f_rob,
                                         beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alphas[j] * chi)
              for j in range(n_f)]
        energy_k = sum(weights[j] * your_compute_objective_function(domain_omega, us[j], spacestep)
                       for j in range(n_f))

        # -- si l'énergie remonte, on divise le pas par 2 et on repart de chi_n
        if energy_k >= energy_best:
            mu = mu / 2.0
            energy[k, 0] = energy_best
            if mu < 1e-10:
                break
            continue
        variation = numpy.max(numpy.abs(chi - chi_best))
        chi_old, grad_old = chi_best, grad
        chi_best, energy_best = chi, energy_k
        energy[k, 0] = energy_best
        if variation < delta:
            break

        # -- gradient de J^ : somme pondérée des gradients à chaque fréquence
        grad = numpy.zeros((M, N), dtype=numpy.float64)
        for j in range(n_f):
            alpha_rob = Alphas[j] * chi_best
            p = processing.solve_helmholtz(domain_omega, spacestep, wavenumbers[j], -2.0 * numpy.conj(us[j]),
                                           numpy.zeros((M, N), dtype=numpy.complex128), f_neu, f_rob,
                                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
            u_gamma = numpy.zeros((M, N), dtype=numpy.complex128)
            p_gamma = numpy.zeros((M, N), dtype=numpy.complex128)
            for (i, l) in numpy.argwhere(robin):
                for (a_, b) in [(i - 1, l), (i + 1, l), (i, l - 1), (i, l + 1)]:
                    if 0 <= a_ < M and 0 <= b < N and domain_omega[a_, b] == _env.NODE_INTERIOR:
                        u_gamma[i, l] = us[j][a_, b] / (1.0 - alpha_rob[i, l] * spacestep)
                        p_gamma[i, l] = p[a_, b] / (1.0 - alpha_rob[i, l] * spacestep)
            grad += weights[j] * numpy.real(Alphas[j] * u_gamma * p_gamma)

        if k > 0:
            s = (chi_best - chi_old)[robin]
            y = (grad - grad_old)[robin]
            if numpy.dot(y, y) > 0:
                mu = abs(numpy.dot(s, y)) / numpy.dot(y, y)

    # -- projection finale avec le volume respecté : les plus grandes valeurs valent 1, les autres 0
    nodes = numpy.argwhere(robin)[numpy.argsort(-chi_best[robin], kind='stable')]
    chi = numpy.zeros((M, N), dtype=numpy.float64)
    for (i, j) in nodes[:int(round(V_obj * S))]:
        chi[i, j] = 1.0

    return chi, energy


def your_compute_objective_function(domain_omega, u, spacestep):
    # -- discrete approximation of the integral: sum of |u|^2 * h^2 over the
    # -- nodes of domain_omega
    mask = domain_omega != _env.NODE_COMPLEMENTARY
    energy = numpy.sum(numpy.abs(u[mask])**2) * spacestep**2

    return energy


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = 60  # number of points along x-axis
    M = 2 * N  # number of points along y-axis
    level = 2 # level of the fractal (0 = plane wall)
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
    material = compute_alpha.MATERIAUX["LAINE_ROCHE"]
    g_source = compute_alpha.g1  # onde plane
    alpha_opt, success, message = compute_alpha.compute_alpha(compute_alpha.c0 * wavenumber, g_source,
                                                              material, compute_alpha.Alpha0)
    if not success:
        print('compute_alpha (k = %g) : %s' % (wavenumber, message))
    Alpha = alpha_opt[0] + alpha_opt[1] * 1j
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
    # -- compute optimization
    energy = numpy.zeros((100+1, 1), dtype=numpy.float64)
    chi, energy, u, grad = your_optimization_procedure(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                                                       beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                                                       Alpha, mu, chi, V_obj)
    #chi, energy, u, grad = solutions.optimization_procedure(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
    #                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
    #                    Alpha, mu, chi, V_obj, mu1, V_0)
    # --- en of optimization

    chin = chi.copy()
    un = u.copy()

    # -- étude en fréquence pour une paroi totalement absorbante (chi = 1), pour chaque niveau de fractale
    # bruit de roulement RER B : 250-2000 Hz
    c = 343.0
    frequencies = numpy.linspace(1, 2000.0, 400)  # pas de 5 Hz
    chi_1 = numpy.ones((M,N), dtype=numpy.float64)
    chi_1 = preprocessing.set2zero(chi_1, domain_omega)
    # pour tous les matériaux :
    #plot_energy_frequency_all_materials(domain_omega_k, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
    #                                    beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
    #                                    chi_1, g_source, level_k)
    # pour un seul matériau :
    energies_chi_1, peak_frequencies = plot_energy_frequency_one_material(
        domain_omega, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        chi_1, g_source, "OUATE_POLYESTER", compute_alpha.MATERIAUX["OUATE_POLYESTER"],
        level)

    # -- optimisation multifréquence sur les pics choisis de la courbe chi = 1
    peak_frequencies = numpy.array([270.0, 385.0, 575.0, 725.0, 910.0, 1085.0])
    chi_multi, energy_multi = your_multifrequency_optimization(domain_omega, spacestep, peak_frequencies, c, f, f_neu, f_rob,
                                                               beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                                                               compute_alpha.MATERIAUX["OUATE_POLYESTER"], g_source,
                                                               mu, chi0.copy(), V_obj)

    # -- optimisation sur toute la bande : fréquences régulièrement espacées
    frequencies_band = numpy.linspace(1, 2000.0, 400)  # pas de 5 Hz, pour ne pas manquer les pics
    chi_band, energy_band = your_band_optimization(domain_omega, spacestep, frequencies_band, c, f, f_neu, f_rob,
                                                   beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                                                   compute_alpha.MATERIAUX["OUATE_POLYESTER"], g_source,
                                                   mu, chi0.copy(), V_obj)

    # -- nouvelle figure : chi optimisé sur les pics (chi = 1 en référence)
    os.makedirs('courbes_energie', exist_ok=True)
    matplotlib.pyplot.plot(frequencies, energies_chi_1, label='$\\chi = 1$')
    energies_multi, _ = plot_energy_frequency_one_material(
        domain_omega, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        chi_multi, g_source, '$\\chi$ optimisé sur les pics', compute_alpha.MATERIAUX["OUATE_POLYESTER"],
        level, save=False)
    matplotlib.pyplot.xlabel('frequency f (Hz)')
    matplotlib.pyplot.ylabel('energy J')
    matplotlib.pyplot.title('Energy vs frequency, level %d, optimisation sur les pics' % level)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(os.path.join('courbes_energie', 'fig_energy_frequency_level%d_optimisation_pics.jpg' % level))
    matplotlib.pyplot.close()

    # -- nouvelle figure : chi optimisé sur la bande (chi = 1 en référence), sans la fréquence des pics
    matplotlib.pyplot.plot(frequencies, energies_chi_1, label='$\\chi = 1$')
    energies_band, _ = plot_energy_frequency_one_material(
        domain_omega, spacestep, frequencies, c, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        chi_band, g_source, '$\\chi$ optimisé sur la bande', compute_alpha.MATERIAUX["OUATE_POLYESTER"],
        level, save=False, annotate=False)
    matplotlib.pyplot.xlabel('frequency f (Hz)')
    matplotlib.pyplot.ylabel('energy J')
    matplotlib.pyplot.title('Energy vs frequency, level %d, optimisation sur la bande' % level)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(os.path.join('courbes_energie', 'fig_energy_frequency_level%d_optimisation_bande.jpg' % level))
    matplotlib.pyplot.close()

    # -- énergie totale sur la bande (trapèzes)
    for name_k, energies_k in [('chi = 1', energies_chi_1), ('chi optimisé sur les pics', energies_multi),
                               ('chi optimisé sur la bande', energies_band)]:
        total = numpy.sum((energies_k[1:] + energies_k[:-1]) / 2.0 * numpy.diff(frequencies))
        print('énergie totale %s : %g' % (name_k, total))

    # -- historique de l'énergie de l'optimisation multifréquence
    matplotlib.pyplot.plot(energy_multi[energy_multi[:, 0] > 0])
    matplotlib.pyplot.title('Energy (multifrequency optimization)')
    matplotlib.pyplot.savefig(os.path.join('courbes_energie', 'fig_energy_history_multifreq.jpg'))
    matplotlib.pyplot.close()

    # -- historique de l'énergie de l'optimisation sur la bande
    matplotlib.pyplot.plot(energy_band[energy_band[:, 0] > 0])
    matplotlib.pyplot.title('Energy (band optimization)')
    matplotlib.pyplot.savefig(os.path.join('courbes_energie', 'fig_energy_history_band.jpg'))
    matplotlib.pyplot.close()

    # -- plot chi, u, and energy
    postprocessing._plot_uncontroled_solution(u0, chi0)
    postprocessing._plot_controled_solution(un, chin)
    err = un - u0
    postprocessing._plot_error(err)
    # only the iterations actually computed (the remaining entries of energy are 0)
    postprocessing._plot_energy_history(energy[energy[:, 0] > 0])

    print('End.')