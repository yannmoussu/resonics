# -*- coding: utf-8 -*-
"""On résout les problèmes répétés sur les seuls points intérieurs du domaine."""

import numpy as np
import scipy.sparse
import scipy.sparse.linalg

import _env
import preprocessing
from demo_control_polycopie2024 import project_density as project_chi


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
        """On calcule la dérivée du coût par rapport à chaque valeur du matériau."""
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


def binarize_chi(chi_cont, domain_omega, V_obj):
    """On garnit les points du mur dont les densités sont les plus grandes."""
    robin = domain_omega == _env.NODE_ROBIN
    order = np.argsort(-chi_cont[robin])
    number = int(round(V_obj * len(order)))
    values = np.zeros(len(order))
    values[order[:number]] = 1.0
    binary = np.zeros_like(chi_cont, dtype=np.float64)
    binary[robin] = values
    return binary


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
    chi = project_chi(chi_init, solver.domain, V_obj)
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
            candidate = project_chi(chi - mu * gradient, solver.domain, V_obj)
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
            print("Étape", iteration + 1, ": coût =", history[-1])
        if variation < 1e-7:
            break
    return chi, np.asarray(history), np.asarray(per_frequency)
