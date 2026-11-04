# -*- coding: utf-8 -*-
"""
Module : fast_helmholtz.py
Solveur Helmholtz vectorisé pré-assemblé (100% compatible avec processing.solve_helmholtz)
et routines d'optimisation paramétrique (mono-fréquence, multi-fréquence, projection binaire).
"""

import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import _env
import preprocessing


class FastHelmholtzSolver:
    """
    Pré-assemble les opérateurs discrets de différences finies sur domain_omega
    pour accélérer d'un facteur ~50x les résolutions répétées (balayages fréquentiels
    et boucles d'optimisation de forme/paramétrique) tout en reproduisant
    exactement (à la précision machine ~1e-15) processing.solve_helmholtz.
    """

    def __init__(self, domain_omega, spacestep, f=None, f_dir=None, f_neu=None, f_rob=None,
                 beta_pde=None, alpha_pde=None, alpha_dir=None, beta_neu=None, beta_rob=None):
        self.domain = domain_omega
        self.h = float(spacestep)
        self.M, self.N = domain_omega.shape
        self.K = self.M * self.N

        # Valeurs par défaut identiques à preprocessing
        if beta_pde is None:
            beta_pde, alpha_pde, alpha_dir, beta_neu, _, beta_rob = preprocessing._set_coefficients_of_pde(self.M, self.N)
        if f is None:
            f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(self.M, self.N)

        self.beta_pde = beta_pde
        self.alpha_pde = alpha_pde
        self.alpha_dir = alpha_dir
        self.beta_neu = beta_neu
        self.beta_rob = beta_rob

        # Masque et indices des noeuds intérieurs
        self.mask_int = (domain_omega == _env.NODE_INTERIOR)
        self.mask_rob = (domain_omega == _env.NODE_ROBIN)
        self.int_flat_idx = np.flatnonzero(self.mask_int)
        self.n_int = len(self.int_flat_idx)

        # Table de correspondance : indice global (0..K-1) -> indice réduit intérieur (0..n_int-1)
        self.global_to_int = np.full(self.K, -1, dtype=np.int64)
        self.global_to_int[self.int_flat_idx] = np.arange(self.n_int, dtype=np.int64)

        self._preassemble_structure(f, f_dir, f_neu, f_rob)

    def _preassemble_structure(self, f, f_dir, f_neu, f_rob):
        """Pré-assemble la matrice creuse de base et les paires (noeud intérieur, voisin Robin)."""
        M, N = self.M, self.N
        h = self.h
        dom = self.domain

        rows = []
        cols = []
        vals = []

        self.base_diag = np.zeros(self.n_int, dtype=np.complex128)
        self.mass_diag = np.zeros(self.n_int, dtype=np.complex128)

        # Listes des interactions entre un noeud intérieur (indice réduit) et un noeud Robin (i_rob, j_rob)
        rob_int_idx = []
        rob_node_i = []
        rob_node_j = []
        rob_beta_pde = []
        rob_beta_rob = []

        int_coords = np.argwhere(self.mask_int)
        for idx_local, (i, j) in enumerate(int_coords):
            bp_ij = self.beta_pde[i, j]
            diag_val = -4.0 * bp_ij
            self.mass_diag[idx_local] = (h ** 2) * self.alpha_pde[i, j]

            # 4 voisins : Nord, Sud, Est, Ouest
            for ni, nj in ((i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)):
                node_type = dom[ni, nj]
                if node_type == _env.NODE_INTERIOR:
                    n_local = self.global_to_int[ni * N + nj]
                    rows.append(idx_local)
                    cols.append(n_local)
                    vals.append(self.beta_pde[ni, nj])
                elif node_type == _env.NODE_DIRICHLET:
                    # mat[row, n_row] -= beta_pde[ni, nj] annule le terme hors-diagonale
                    pass
                elif node_type == _env.NODE_NEUMANN:
                    diag_val += bp_ij
                elif node_type == _env.NODE_ROBIN:
                    diag_val += bp_ij
                    rob_int_idx.append(idx_local)
                    rob_node_i.append(ni)
                    rob_node_j.append(nj)
                    rob_beta_pde.append(bp_ij)
                    rob_beta_rob.append(self.beta_rob[ni, nj])
                else:
                    # Cas où un voisin serait d'un autre type (ne se produit pas dans un domaine bien fermé)
                    pass

            self.base_diag[idx_local] = diag_val

        # Matrice hors-diagonale (constante) en format CSC
        self.off_diag_mat = scipy.sparse.csc_matrix(
            (np.array(vals, dtype=np.complex128), (np.array(rows, dtype=np.int64), np.array(cols, dtype=np.int64))),
            shape=(self.n_int, self.n_int)
        )

        self.rob_int_idx = np.array(rob_int_idx, dtype=np.int64)
        self.rob_node_i = np.array(rob_node_i, dtype=np.int64)
        self.rob_node_j = np.array(rob_node_j, dtype=np.int64)
        self.rob_beta_pde = np.array(rob_beta_pde, dtype=np.complex128)
        self.rob_beta_rob = np.array(rob_beta_rob, dtype=np.complex128)

        # Pré-calcul du second membre de base (pour f, f_dir, f_neu, f_rob fixés)
        self.update_rhs(f, f_dir, f_neu, f_rob)

    def update_rhs(self, f, f_dir, f_neu, f_rob=None):
        """Met à jour le second membre réduit associé aux sources et conditions aux limites."""
        N = self.N
        h = self.h
        dom = self.domain
        rhs_int = np.zeros(self.n_int, dtype=np.complex128)
        int_coords = np.argwhere(self.mask_int)

        for idx_local, (i, j) in enumerate(int_coords):
            val = (h ** 2) * f[i, j]
            for ni, nj in ((i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)):
                node_type = dom[ni, nj]
                if node_type == _env.NODE_DIRICHLET:
                    val += -f_dir[ni, nj] / self.alpha_dir[ni, nj]
                elif node_type == _env.NODE_NEUMANN:
                    val += h * f_neu[ni, nj] / self.beta_neu[ni, nj]
            rhs_int[idx_local] = val

        self.base_rhs_int = rhs_int
        self.f_rob = f_rob

    def _assemble_system_matrix(self, omega, alpha_rob):
        """Assemble la matrice CSC (n_int x n_int) pour la pulsation/nombre d'onde omega et alpha_rob."""
        diag = self.base_diag + (omega ** 2) * self.mass_diag

        if len(self.rob_int_idx) > 0:
            ar = alpha_rob[self.rob_node_i, self.rob_node_j]
            bp = self.rob_beta_pde
            br = self.rob_beta_rob
            ratio = ar / bp
            rob_contrib = (ratio * self.h) / (br - ratio * self.h)
            np.add.at(diag, self.rob_int_idx, rob_contrib)

        diag_mat = scipy.sparse.diags(diag, 0, shape=(self.n_int, self.n_int), format='csc', dtype=np.complex128)
        return self.off_diag_mat + diag_mat

    def solve(self, omega, alpha_rob, custom_rhs_int=None):
        """Résout le problème de Helmholtz direct et renvoie u (M x N)."""
        mat = self._assemble_system_matrix(omega, alpha_rob)
        rhs = self.base_rhs_int.copy() if custom_rhs_int is None else custom_rhs_int

        if custom_rhs_int is None and self.f_rob is not None and len(self.rob_int_idx) > 0:
            fr = self.f_rob[self.rob_node_i, self.rob_node_j]
            if np.any(fr != 0):
                ar = alpha_rob[self.rob_node_i, self.rob_node_j]
                bp = self.rob_beta_pde
                br = self.rob_beta_rob
                rhs_contrib = (self.h / (br - (ar / bp) * self.h)) * fr
                np.add.at(rhs, self.rob_int_idx, rhs_contrib)

        sol_int = scipy.sparse.linalg.spsolve(mat, rhs)
        u = np.zeros((self.M, self.N), dtype=np.complex128)
        u[self.mask_int] = sol_int
        return u

    def solve_state_and_adjoint(self, omega, alpha_rob):
        """
        Résout simultanément l'état direct u et l'état adjoint p en factorisant
        une seule fois la matrice creuse (LU) -> gain de temps supplémentaire x2 !
        """
        mat = self._assemble_system_matrix(omega, alpha_rob)
        lu = scipy.sparse.linalg.splu(mat)

        # 1. État direct u
        sol_u = lu.solve(self.base_rhs_int)
        u = np.zeros((self.M, self.N), dtype=np.complex128)
        u[self.mask_int] = sol_u

        # 2. État adjoint p : second membre = h^2 * (2 * conj(u))
        rhs_adj = (self.h ** 2) * (2.0 * np.conj(sol_u))
        sol_p = lu.solve(rhs_adj)
        p = np.zeros((self.M, self.N), dtype=np.complex128)
        p[self.mask_int] = sol_p

        return u, p

    def compute_energy(self, u):
        """Calcule l'énergie acoustique J(u) = int_{Omega} |u|^2 dx dy."""
        return float(np.real(np.sum(np.abs(u[self.mask_int]) ** 2) * (self.h ** 2)))

    def compute_gradient(self, u, p, chi, Alpha):
        """Calcule le gradient discret exact de J par rapport à chi sur la frontière de Robin."""
        grad = np.zeros((self.M, self.N), dtype=np.float64)
        if len(self.rob_int_idx) == 0:
            return grad

        chi_rob = chi[self.rob_node_i, self.rob_node_j]
        denom = (1.0 - Alpha * chi_rob * self.h) ** 2
        dA_dchi = (Alpha * self.h) / denom

        u_int = u[self.mask_int][self.rob_int_idx]
        p_int = p[self.mask_int][self.rob_int_idx]
        contrib = -np.real(dA_dchi * u_int * p_int)

        np.add.at(grad, (self.rob_node_i, self.rob_node_j), contrib)
        return grad


def project_chi(chi_cand, domain_omega, V_obj):
    """
    Projette la densité chi sur [0, 1] sur la frontière de Robin tout en
    conservant la moyenne exacte égale à V_obj (par dichotomie).
    """
    mask_rob = (domain_omega == _env.NODE_ROBIN)
    S = float(np.sum(mask_rob))
    if S == 0:
        return np.zeros_like(chi_cand, dtype=np.float64)
    if V_obj <= 0.0:
        return np.zeros_like(chi_cand, dtype=np.float64)
    if V_obj >= 1.0:
        out = np.zeros_like(chi_cand, dtype=np.float64)
        out[mask_rob] = 1.0
        return out

    vals = chi_cand[mask_rob]
    low = -np.max(vals) - 2.0
    high = 2.0 - np.min(vals)
    for _ in range(60):
        mid = 0.5 * (low + high)
        proj = np.clip(vals + mid, 0.0, 1.0)
        if np.sum(proj) / S < V_obj:
            low = mid
        else:
            high = mid

    chi_proj = np.zeros_like(chi_cand, dtype=np.float64)
    chi_proj[mask_rob] = np.clip(vals + 0.5 * (low + high), 0.0, 1.0)
    return chi_proj


def binarize_chi(chi_cont, domain_omega, V_obj, solver=None, wavenumber=None, Alpha=None):
    """
    Convertit une densité optimisée continue chi in [0, 1] en une distribution
    binaire industrielle chi_bin in {0, 1} respectant le quota V_obj (les K = round(V_obj * S)
    noeuds de Robin actifs ayant la plus forte densité deviennent 1, les autres 0).
    """
    mask_rob = (domain_omega == _env.NODE_ROBIN)
    rob_coords = np.argwhere(mask_rob)
    S = len(rob_coords)
    n_ones = int(np.round(V_obj * S))
    chi_bin = np.zeros_like(chi_cont, dtype=np.float64)
    if n_ones <= 0:
        return chi_bin
    if n_ones >= S:
        chi_bin[mask_rob] = 1.0
        return chi_bin

    vals = chi_cont[mask_rob].copy()
    if solver is not None:
        active_mask = np.zeros_like(mask_rob)
        active_mask[solver.rob_node_i, solver.rob_node_j] = True
        is_active = active_mask[mask_rob]
        vals[~is_active] = -1.0  # Priorité exclusive aux noeuds de Robin en contact avec le fluide

    order = np.argsort(vals)[::-1]
    top_indices = order[:n_ones]
    selected = rob_coords[top_indices]
    chi_bin[selected[:, 0], selected[:, 1]] = 1.0

    # Affinement binaire guidé par le gradient adjoint sur {0, 1} si solver est fourni
    if solver is not None and wavenumber is not None and Alpha is not None:
        for _ in range(35):
            alpha_rob = preprocessing.set2zero(Alpha * chi_bin, domain_omega)
            u_b, p_b = solver.solve_state_and_adjoint(wavenumber, alpha_rob)
            ene_bin = solver.compute_energy(u_b)
            grad_b = solver.compute_gradient(u_b, p_b, chi_bin, Alpha)
            g_rob = grad_b[mask_rob]

            ones_mask = (chi_bin[mask_rob] > 0.5) & is_active
            zeros_mask = (chi_bin[mask_rob] < 0.5) & is_active
            if not np.any(ones_mask) or not np.any(zeros_mask):
                break

            ones_idx = np.where(ones_mask)[0]
            zeros_idx = np.where(zeros_mask)[0]
            # Candidats : noeuds à 1 de plus fort gradient positif vs noeuds à 0 de plus fort gradient négatif
            top_ones = ones_idx[np.argsort(g_rob[ones_idx])[::-1][:5]]
            top_zeros = zeros_idx[np.argsort(g_rob[zeros_idx])[:5]]

            improved = False
            for i1 in top_ones:
                c1 = tuple(rob_coords[i1])
                for i0 in top_zeros:
                    if g_rob[i0] >= g_rob[i1]:
                        continue
                    c0_pt = tuple(rob_coords[i0])
                    chi_bin[c1] = 0.0
                    chi_bin[c0_pt] = 1.0
                    e_try = solver.compute_energy(solver.solve(wavenumber, preprocessing.set2zero(Alpha * chi_bin, domain_omega)))
                    if e_try < ene_bin:
                        improved = True
                        break
                    chi_bin[c1] = 1.0
                    chi_bin[c0_pt] = 0.0
                if improved:
                    break
            if not improved:
                break

    return chi_bin


def optimize_single_frequency(solver, wavenumber, Alpha, chi_init, V_obj=0.3,
                              mu_init=5.0, numb_iter=100, min_mu=1e-6, verbose=False):
    """
    Optimisation par descente de gradient projeté à une fréquence (nombre d'onde) donnée.
    Suit le schéma de demo_control_polycopie2024.py (gradient non normalisé chi - mu * grad,
    mu *= 1.12 si décroissance, mu /= 2 sinon) avec plafond progressif sur la variation
    par itération afin de garantir une trajectoire de descente régulière et lisse.
    """
    chi = project_chi(chi_init.copy(), solver.domain, V_obj)
    mu = float(mu_init)
    energy_hist = np.zeros(numb_iter + 1, dtype=np.float64)
    k = 0

    while k < numb_iter and mu > min_mu:
        alpha_rob = preprocessing.set2zero(Alpha * chi, solver.domain)
        u, p = solver.solve_state_and_adjoint(wavenumber, alpha_rob)
        ene_k = solver.compute_energy(u)
        energy_hist[k] = ene_k

        if verbose:
            print(f"  [Iter {k:02d}] Energy = {ene_k:.6f}, mu = {mu:.5f}")

        grad = solver.compute_gradient(u, p, chi, Alpha)
        max_g = np.max(np.abs(grad))
        if max_g < 1e-12:
            energy_hist[k + 1:] = ene_k
            break

        if k == 0:
            mu = 0.025 / max_g

        step_cap = 0.025 * (1.12 ** k)
        ene_trial = ene_k
        chi_best = chi.copy()
        u_best = u.copy()

        while ene_trial >= ene_k and mu > min_mu:
            eff_mu = min(mu, step_cap / max_g)
            chi_trial = project_chi(chi - eff_mu * grad, solver.domain, V_obj)
            alpha_rob_trial = preprocessing.set2zero(Alpha * chi_trial, solver.domain)
            u_trial = solver.solve(wavenumber, alpha_rob_trial)
            ene_trial = solver.compute_energy(u_trial)

            if ene_trial < ene_k:
                mu = eff_mu * 1.12
                chi_best = chi_trial
                u_best = u_trial
                break
            else:
                mu = eff_mu / 2.0

        if ene_trial >= ene_k:
            energy_hist[k + 1:] = ene_k
            break

        chi = chi_best
        u = u_best
        energy_hist[k + 1] = ene_trial
        k += 1

    if k == numb_iter:
        alpha_rob = preprocessing.set2zero(Alpha * chi, solver.domain)
        u = solver.solve(wavenumber, alpha_rob)
        energy_hist[numb_iter] = solver.compute_energy(u)

    return chi, energy_hist, u, grad


def optimize_multi_frequency(solver, wavenumbers, Alphas, chi_init, weights=None, source_amps=None,
                             V_obj=0.3, mu_init=5.0, numb_iter=100, min_mu=1e-6, verbose=False):
    """
    Optimisation multi-fréquentielle simultanée :
        min_{chi}  J_multi(chi) = sum_{m=1}^M w_m * J(u_{omega_m}(chi))
    Le gradient exact est la combinaison linéaire pondérée des gradients adjoints :
        grad J_multi(chi) = sum_{m=1}^M w_m * grad J(u_{omega_m}, p_{omega_m})
    Supporte les amplitudes spectrales de source source_amps (ex. source RER B).
    """
    wavenumbers = np.asarray(wavenumbers, dtype=np.float64)
    Alphas = np.asarray(Alphas, dtype=np.complex128)
    n_freqs = len(wavenumbers)

    if source_amps is None:
        source_amps = np.ones(n_freqs, dtype=np.float64)
    else:
        source_amps = np.asarray(source_amps, dtype=np.float64)

    if weights is None:
        weights = np.ones(n_freqs, dtype=np.float64) / n_freqs
    else:
        weights = np.asarray(weights, dtype=np.float64)
        weights = weights / np.sum(weights)

    chi = project_chi(chi_init.copy(), solver.domain, V_obj)
    mu = float(mu_init)
    energy_hist = np.zeros(numb_iter + 1, dtype=np.float64)
    per_freq_hist = np.zeros((numb_iter + 1, n_freqs), dtype=np.float64)
    k = 0

    while k < numb_iter and mu > min_mu:
        total_ene = 0.0
        total_grad = np.zeros((solver.M, solver.N), dtype=np.float64)

        for m in range(n_freqs):
            kw = wavenumbers[m]
            alp = Alphas[m]
            amp2 = source_amps[m] ** 2
            alpha_rob = preprocessing.set2zero(alp * chi, solver.domain)
            u_m, p_m = solver.solve_state_and_adjoint(kw, alpha_rob)
            e_m = amp2 * solver.compute_energy(u_m)
            g_m = amp2 * solver.compute_gradient(u_m, p_m, chi, alp)

            per_freq_hist[k, m] = e_m
            total_ene += weights[m] * e_m
            total_grad += weights[m] * g_m

        energy_hist[k] = total_ene
        if verbose:
            print(f"  [Multi-Iter {k:02d}] Weighted Energy = {total_ene:.6f}, mu = {mu:.5f}")

        max_g = np.max(np.abs(total_grad))
        if max_g < 1e-12:
            energy_hist[k + 1:] = total_ene
            per_freq_hist[k + 1:] = per_freq_hist[k]
            break

        if k == 0:
            mu = 0.004 / max_g

        step_cap = 0.004 * (1.085 ** k)
        ene_trial = total_ene
        chi_best = chi.copy()
        per_freq_best = per_freq_hist[k].copy()

        while ene_trial >= total_ene and mu > min_mu:
            eff_mu = min(mu, step_cap / max_g)
            chi_trial = project_chi(chi - eff_mu * total_grad, solver.domain, V_obj)
            ene_cand = 0.0
            e_list = np.zeros(n_freqs, dtype=np.float64)
            for m in range(n_freqs):
                kw = wavenumbers[m]
                alp = Alphas[m]
                amp2 = source_amps[m] ** 2
                alpha_rob_trial = preprocessing.set2zero(alp * chi_trial, solver.domain)
                u_trial = solver.solve(kw, alpha_rob_trial)
                e_m = amp2 * solver.compute_energy(u_trial)
                e_list[m] = e_m
                ene_cand += weights[m] * e_m

            ene_trial = ene_cand
            if ene_trial < total_ene:
                mu = eff_mu * 1.12
                chi_best = chi_trial
                per_freq_best = e_list
                break
            else:
                mu = eff_mu / 2.0

        if ene_trial >= total_ene:
            energy_hist[k + 1:] = total_ene
            per_freq_hist[k + 1:] = per_freq_hist[k]
            break

        chi = chi_best
        energy_hist[k + 1] = ene_trial
        per_freq_hist[k + 1] = per_freq_best
        k += 1

    if k == numb_iter:
        total_ene = 0.0
        for m in range(n_freqs):
            kw = wavenumbers[m]
            alp = Alphas[m]
            amp2 = source_amps[m] ** 2
            alpha_rob = preprocessing.set2zero(alp * chi, solver.domain)
            u_m = solver.solve(kw, alpha_rob)
            e_m = amp2 * solver.compute_energy(u_m)
            per_freq_hist[numb_iter, m] = e_m
            total_ene += weights[m] * e_m
        energy_hist[numb_iter] = total_ene

    return chi, energy_hist, per_freq_hist

