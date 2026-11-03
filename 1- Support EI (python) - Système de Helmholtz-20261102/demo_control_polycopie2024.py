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
#import solutions

# ==============================================================================
# Surcharge des fonctions de postprocessing pour ajouter des légendes et axes
# ==============================================================================
import postprocessing

def custom_plot_energy_history(energy):
    """Graphique d'énergie avec axes étiquetés, grille et légende."""
    matplotlib.pyplot.figure(figsize=(8, 5), dpi=100)
    matplotlib.pyplot.plot(energy, color='tab:blue', lw=2, label='Énergie acoustique $J(u)$')
    matplotlib.pyplot.title('Évolution de l\'énergie acoustique au cours des itérations', fontsize=12)
    matplotlib.pyplot.xlabel('Numéro d\'itération ($k$)', fontsize=11)
    matplotlib.pyplot.ylabel('Énergie $J(u) = \\int_{\\Omega} |u|^2 \\, \\mathrm{d}\\Omega$', fontsize=11)
    matplotlib.pyplot.grid(True, linestyle='--', alpha=0.6)
    matplotlib.pyplot.legend(loc='upper right')
    matplotlib.pyplot.tight_layout()
    filename = 'fig_energy_real.jpg'
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()

# Remplacement de la fonction d'origine par notre version enrichie
postprocessing._plot_energy_history = custom_plot_energy_history


# Surcharge optionnelle de myimshow pour ajouter les axes X et Y sur les cartes spatiales
original_myimshow = postprocessing.myimshow

def custom_myimshow(tab, **kwargs):
    """Affiche les matrices 2D avec des labels explicites sur les axes spatiaux."""
    fig = matplotlib.pyplot.figure(dpi=kwargs.get('dpi', 100))
    ax = matplotlib.pyplot.axes()
    
    cmap = kwargs.get('cmap', 'jet')
    im = ax.imshow(tab, cmap=cmap)
    
    if 'title' in kwargs and kwargs['title']:
        ax.set_title(kwargs['title'], fontsize=12)
    
    if kwargs.get('colorbar', False):
        fig.colorbar(im, ax=ax, label='Amplitude / Densité')
        
    if 'vmin' in kwargs and 'vmax' in kwargs:
        im.set_clim(kwargs['vmin'], kwargs['vmax'])
        
    # Ajout des axes spatiaux explicites
    ax.set_xlabel('Coordonneé spatiale $x$ (maillage)', fontsize=10)
    ax.set_ylabel('Coordonneé spatiale $y$ (maillage)', fontsize=10)
    
    if 'filename' in kwargs and kwargs['filename']:
        output_file = kwargs['filename']
        (root, ext) = os.path.splitext(output_file)
        matplotlib.pyplot.savefig(root + '_plot' + ext, format=ext[1:], bbox_inches='tight')
    else:
        matplotlib.pyplot.show()
        
    matplotlib.pyplot.close(fig)
    return

postprocessing.myimshow = custom_myimshow

def compute_exact_discrete_gradient(domain_omega, u, p, chi, Alpha, spacestep):
    """
    Calcule le gradient discret exact de J par rapport à chi en dérivant 
    la formule de compute_robin_condition de processing.py.
    """
    (M, N) = numpy.shape(domain_omega)
    grad = numpy.zeros((M, N), dtype=numpy.float64)
    h = spacestep

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if domain_omega[i, j] == _env.NODE_INTERIOR:
                for (ni, nj) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                    if domain_omega[ni, nj] == _env.NODE_ROBIN:
                        # Dérivée exacte du terme diagonal de Robin par rapport à chi[ni, nj]
                        denom = (1.0 - Alpha * chi[ni, nj] * h) ** 2
                        dA_dchi = (Alpha * h) / denom
                        grad[ni, nj] += -   numpy.real( dA_dchi * u[i, j] * p[i, j] )

    return grad


def your_optimization_procedure(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, mu, chi, V_obj):
    """This function return the optimized density."""

    k = 0
    (M, N) = numpy.shape(domain_omega)
    numb_iter = 100
    energy = numpy.zeros((numb_iter+1, 1), dtype=numpy.float64)
    grad = numpy.zeros((M, N), dtype=numpy.float64)
    zeros_bc = numpy.zeros((M, N), dtype=numpy.complex128)

    while k < numb_iter and mu > 10**(-5):
        print('---- iteration number = ', k)
        print('1. computing solution of Helmholtz problem, i.e., u')
        alpha_rob = preprocessing.set2zero(Alpha * chi, domain_omega)
        u = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)

        print('2. computing solution of adjoint problem, i.e., p')
        # Signe +2.0 car compute_stiffness_matrix utilise (-4, +1, +1, +1, +1)
        f_adj = 2.0 * numpy.conj(u)
        p = processing.solve_helmholtz(domain_omega, spacestep, omega, f_adj, zeros_bc, zeros_bc, zeros_bc,
                            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)

        print('3. computing objective function, i.e., energy')
        energy[k] = your_compute_objective_function(domain_omega, u, spacestep)
        print(f'   -> Current Energy = {energy[k, 0]:.6f}, step mu = {mu:.5f}')

        print('4. computing parametric gradient')
        grad = compute_exact_discrete_gradient(domain_omega, u, p, chi, Alpha, spacestep)

        # Normalisation pour que mu soit d'ordre 1
        norm_g = numpy.max(numpy.abs(grad))
        if norm_g > 1e-12:
            grad_normed = grad / norm_g
        else:
            grad_normed = grad

        ene = energy[k, 0]
        chi_best = chi.copy()
        u_best = u.copy()

        while ene >= energy[k, 0] and mu > 10 ** -5:
            print('    a. computing gradient descent')
            chi_trial = chi - mu * grad_normed

            print('    b. computing projected gradient')
            chi_trial = project_chi(chi_trial, domain_omega, V_obj)

            print('    c. computing solution of Helmholtz problem, i.e., u')
            alpha_rob_trial = preprocessing.set2zero(Alpha * chi_trial, domain_omega)
            u_trial = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob_trial)

            print('    d. computing objective function, i.e., energy (E)')
            ene = your_compute_objective_function(domain_omega, u_trial, spacestep)
            bool_a = (ene < energy[k, 0])
            if bool_a:
                # The step is increased if the energy decreased
                mu = mu * 1.1
                chi_best = chi_trial
                u_best = u_trial
            else:
                # The step is decreased if the energy increased
                mu = mu / 2.0

        # Si aucun pas n'a permis de descendre (convergence atteinte), on sort proprement
        if ene >= energy[k, 0]:
            energy[k+1:] = energy[k, 0]
            break

        chi = chi_best
        u = u_best
        energy[k+1, 0] = ene
        k += 1

    print('end. computing solution of Helmholtz problem, i.e., u')

    return chi, energy, u, grad


def project_chi(chi_cand, domain_omega, V_obj):
    """
    Projette la densité chi sur [0, 1] sur la frontière de Robin tout en 
    conservant la moyenne exacte égale à V_obj (par dichotomie).
    """
    mask_rob = (domain_omega == _env.NODE_ROBIN)
    S = float(numpy.sum(mask_rob))
    vals = chi_cand[mask_rob]

    low = -numpy.max(vals) - 2.0
    high = 2.0 - numpy.min(vals)
    for _ in range(60):
        mid = 0.5 * (low + high)
        proj = numpy.clip(vals + mid, 0.0, 1.0)
        if numpy.sum(proj) / S < V_obj:
            low = mid
        else:
            high = mid

    chi_proj = numpy.zeros_like(chi_cand, dtype=numpy.float64)
    chi_proj[mask_rob] = numpy.clip(vals + 0.5 * (low + high), 0.0, 1.0)
    return chi_proj


def your_compute_objective_function(domain_omega, u, spacestep):
    """
    Calcule l'énergie acoustique : J(u) = \int_{domain_omega} ||u||^2 dx dy
    """
    mask_int = (domain_omega == _env.NODE_INTERIOR)
    energy = numpy.sum(numpy.abs(u[mask_int]) ** 2) * (spacestep ** 2)
    return float(numpy.real(energy))




if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = 50  # number of points along x-axis
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
    V_obj = 0.3  # constraint on the density (30%)
    chi = preprocessing._set_chi(M, N, x, y)
    chi = preprocessing.set2zero(chi, domain_omega)
    chi = project_chi(chi, domain_omega, V_obj)

    # -- define absorbing material
    import compute_alpha
    Alpha = compute_alpha.compute_alpha(wavenumber, material_key="hemp_fiber")
    print("Valeur de Alpha utilisée :", Alpha)
    alpha_rob = Alpha * chi

    # -- set parameters for optimization
    S = 0  # surface of the fractal
    for i in range(0, M):
        for j in range(0, N):
            if domain_omega[i, j] == _env.NODE_ROBIN:
                S += 1
    V_0 = 1  # initial volume of the domain
    V_obj = numpy.sum(numpy.sum(chi)) / S  # constraint on the density (= 0.3)
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
    chi, energy, u, grad = your_optimization_procedure(
        domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
        Alpha, mu, chi, V_obj
    )
    # --- en of optimization

    chin = chi.copy()
    un = u.copy()

    # -- plot chi, u, and energy
    postprocessing._plot_uncontroled_solution(u0, chi0)
    postprocessing._plot_controled_solution(un, chin)
    err = un - u0
    postprocessing._plot_error(err)
    postprocessing._plot_energy_history(energy)

    print('End.')
