# -*- coding: utf-8 -*-
"""
Fichier : jour1_etude_theorique_et_materiaux.py
Compléments numériques du Jour 1 (Startup Resonics - EI ST5) :
1. Étude approfondie des matériaux poreux (modèle JCA : absorption, partie réelle/imaginaire de Alpha, épaisseur).
2. Étude théorique & numérique : Comparaison Paroi Réfléchissante (Neumann) vs Air Libre (Sommerfeld) vs Paroi Poreuse (Robin).
3. Validation numérique du gradient adjoint exact par rapport aux différences finies centrées.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if "MPLCONFIGDIR" not in os.environ:
    os.environ["MPLCONFIGDIR"] = "/tmp/mplconfig"
    os.makedirs("/tmp/mplconfig", exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import _env
import preprocessing
import compute_alpha
import fast_helmholtz

OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour1")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def study_porous_materials():
    """
    Compare les 3 matériaux poreux (Mousse de Mélamine, Laine de Roche, Fibre de Chanvre)
    sur [100 Hz, 2500 Hz] :
      - Coefficient d'absorption acoustique alpha_abs = 1 - |R|^2
      - Parties réelle et imaginaire de Alpha(omega)
      - Influence de l'épaisseur d sur la Fibre de Chanvre
    """
    freqs = np.linspace(100, 2500, 300)
    c0 = 340.0
    k_vals = 2.0 * np.pi * freqs / c0

    colors = {
        "melamine_foam": "tab:blue",
        "hemp_fiber": "tab:green",
        "rock_wool": "tab:red"
    }

    # --- Figure 1 : Absorption et parties réelle / imaginaire de Alpha ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=120)
    ax1, ax2 = axes[0], axes[1]

    for key, mat in compute_alpha.MATERIALS.items():
        Alpha = compute_alpha.compute_alpha(k_vals, material_key=key, c0=c0)
        Z_norm = -1j * k_vals / Alpha
        R = (Z_norm - 1.0) / (Z_norm + 1.0)
        a_abs = 1.0 - np.abs(R) ** 2

        label = f"{mat['name']} ($\\sigma={mat['sigma']/1000:.0f}$ kN$\\cdot$s/m$^4$)"
        ax1.plot(freqs, a_abs, lw=2.2, color=colors[key], label=label)

        ax2.plot(freqs, np.real(Alpha), lw=2.0, color=colors[key], ls="-", label=f"Re($\\alpha$) - {mat['name']}")
        ax2.plot(freqs, np.imag(Alpha), lw=1.8, color=colors[key], ls="--", label=f"Im($\\alpha$) - {mat['name']}")

    ax1.axvspan(400, 1250, color="orange", alpha=0.12, label="Dominante Autoroute (400-1250 Hz)")
    ax1.axvspan(800, 2000, color="purple", alpha=0.10, label="Dominante Ferroviaire (800-2000 Hz)")
    ax1.set_title("Coefficient d'absorption sous incidence normale ($d = 5$ cm)", fontsize=12)
    ax1.set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    ax1.set_ylabel("Absorption $\\alpha_{\\mathrm{abs}} = 1 - |R|^2$ (-)", fontsize=11)
    ax1.set_ylim(0, 1.05)
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(fontsize=9, loc="lower right")

    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_title("Coefficient de Robin complexe $\\alpha(\\omega)$ (Modèle JCA, $d=5$ cm)", fontsize=12)
    ax2.set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    ax2.set_ylabel("$\\mathrm{Re}(\\alpha)$ [>0] et $\\mathrm{Im}(\\alpha)$ [<0] (m$^{-1}$)", fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend(fontsize=8.5, ncol=1, loc="best")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j1_materiaux_jca_complet.jpg"), bbox_inches="tight")
    plt.savefig(os.path.join(BASE_DIR, "fig_comparaison_materiaux.jpg"), bbox_inches="tight")
    plt.close(fig)

    # --- Figure 2 : Influence de l'épaisseur d du matériau poreux (Fibre de Chanvre) ---
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=120)
    thicknesses = [0.02, 0.04, 0.05, 0.08, 0.10]
    orig_d = compute_alpha.MATERIALS["hemp_fiber"]["d"]

    for d_val in thicknesses:
        compute_alpha.MATERIALS["hemp_fiber"]["d"] = d_val
        Alpha = compute_alpha.compute_alpha(k_vals, material_key="hemp_fiber", c0=c0)
        Z_norm = -1j * k_vals / Alpha
        R = (Z_norm - 1.0) / (Z_norm + 1.0)
        a_abs = 1.0 - np.abs(R) ** 2
        lw = 2.8 if abs(d_val - 0.05) < 1e-6 else 1.8
        ax.plot(freqs, a_abs, lw=lw, label=f"Épaisseur $d = {d_val*100:.0f}$ cm" + (" (Référence)" if abs(d_val - 0.05) < 1e-6 else ""))

    compute_alpha.MATERIALS["hemp_fiber"]["d"] = orig_d
    ax.set_title("Influence de l'épaisseur $d$ sur l'absorption (Fibre de Chanvre biosourcée)", fontsize=12)
    ax.set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    ax.set_ylabel("Coefficient d'absorption $\\alpha_{\\mathrm{abs}} = 1 - |R|^2$", fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j1_epaisseur_chanvre.jpg"), bbox_inches="tight")
    plt.close(fig)
    print("[Jour 1] Étude des matériaux poreux enregistrée.")


def study_sommerfeld_open_air_vs_reflexive():
    """
    Étude théorique et numérique du Jour 1 :
    Compare l'énergie acoustique J(k) dans le tunnel (level=0, hauteur L=1m, largeur Lx=1m) :
      1. Frontière réfléchissante (Neumann homogène : du/dn = 0, soit alpha_rob = 0)
      2. Frontière ouverte à l'air libre (Condition de radiation de Sommerfeld : du/dn - i*k*u = 0, soit alpha_rob = -i*k)
      3. Frontière totalement absorbante poreuse (Condition de Robin JCA : alpha_rob = Alpha(k))
    Superpose les solutions analytiques 1D exactes et les résolutions différences finies 2D.
    """
    N = 64
    M = 2 * N
    spacestep = 1.0 / N
    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=0)
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    f_dir[0, 0:N] = 1.0

    solver = fast_helmholtz.FastHelmholtzSolver(domain_omega, spacestep, f, f_dir, f_neu, f_rob)
    mask_rob = (domain_omega == _env.NODE_ROBIN)

    k_vals = np.linspace(0.5, 25.0, 220)
    c0 = 340.0
    freqs = k_vals * c0 / (2.0 * np.pi)

    E_refl_2d = np.zeros_like(k_vals)
    E_open_2d = np.zeros_like(k_vals)
    E_porous_2d = np.zeros_like(k_vals)

    E_refl_1d = np.zeros_like(k_vals)
    E_open_1d = np.ones_like(k_vals)

    L = 1.0

    for idx, kw in enumerate(k_vals):
        # 1. Réfléchissant (alpha_rob = 0)
        alpha_zero = np.zeros((M, N), dtype=np.complex128)
        u_refl = solver.solve(kw, alpha_zero)
        E_refl_2d[idx] = solver.compute_energy(u_refl)

        cos_kL = np.cos(kw * L)
        if abs(cos_kL) > 1e-3:
            E_refl_1d[idx] = (0.5 * L + np.sin(2.0 * kw * L) / (4.0 * kw)) / (cos_kL ** 2)
        else:
            E_refl_1d[idx] = np.nan

        # 2. Air libre - Condition de Sommerfeld (du/dn - i*k*u = 0 => alpha_rob = -i*k)
        alpha_somm = np.zeros((M, N), dtype=np.complex128)
        alpha_somm[mask_rob] = -1j * kw
        u_open = solver.solve(kw, alpha_somm)
        E_open_2d[idx] = solver.compute_energy(u_open)

        # 3. Paroi poreuse (Fibre de chanvre)
        Alpha_jca = compute_alpha.compute_alpha(kw, material_key="hemp_fiber", c0=c0)
        alpha_por = np.zeros((M, N), dtype=np.complex128)
        alpha_por[mask_rob] = Alpha_jca
        u_por = solver.solve(kw, alpha_por)
        E_porous_2d[idx] = solver.compute_energy(u_por)

    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=120)
    ax.semilogy(freqs, E_refl_2d, color="tab:red", lw=2.0, label="Tunnel réfléchissant 2D ($\\alpha = 0$, Neumann)")
    ax.semilogy(freqs, np.clip(E_refl_1d, None, 1e4), color="darkred", lw=1.2, ls=":", label="Théorie analytique 1D réfléchissante : $J(k) = \\frac{L/2 + \\sin(2kL)/(4k)}{\\cos^2(kL)}$")
    ax.semilogy(freqs, E_porous_2d, color="tab:green", lw=2.2, label="Paroi poreuse absorbante 2D (Fibre de chanvre, $\\chi=1$)")
    ax.semilogy(freqs, E_open_2d, color="tab:blue", lw=2.2, label="Frontière ouverte / Air libre 2D (Sommerfeld : $\\partial_n u - iku = 0$)")
    ax.semilogy(freqs, E_open_1d, color="navy", lw=1.4, ls="--", label="Théorie analytique 1D Air libre : $J_{\\mathrm{open}}(k) = |\\Omega| = 1$")

    for n_mode in range(8):
        k_mode = (n_mode + 0.5) * np.pi / L
        f_mode = k_mode * c0 / (2.0 * np.pi)
        if f_mode <= freqs[-1]:
            ax.axvline(f_mode, color="gray", ls="--", lw=0.8, alpha=0.5)
            if n_mode == 0:
                ax.text(f_mode + 10, 200, f"$f_{n_mode} = {f_mode:.0f}$ Hz\n($k=(n+1/2)\\pi$)", fontsize=8.5, color="dimgray")

    ax.set_ylim(1e-1, 1e3)
    ax.set_title("Étude théorique (Jour 1) : Tunnel réfléchissant vs Air libre (Sommerfeld) vs Paroi poreuse", fontsize=12)
    ax.set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    ax.set_ylabel("Énergie acoustique $J(u) = \\int_\\Omega |u|^2 \\, \\mathrm{d}\\Omega$ (échelle log)", fontsize=11)
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend(fontsize=9.2, loc="upper right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j1_sommerfeld_vs_reflexif.jpg"), bbox_inches="tight")
    plt.close(fig)
    print("[Jour 1] Comparaison théorique Sommerfeld (Air libre) vs Réfléchissant enregistrée.")


def validate_adjoint_gradient():
    """
    Vérifie numériquement que le gradient discret obtenu par méthode de l'état adjoint
    coïncide avec les différences finies centrées :
        dJ/dchi_m = (J(chi + eps * e_m) - J(chi - eps * e_m)) / (2 * eps)
    """
    N = 48
    M = 2 * N
    spacestep = 1.0 / N
    wavenumber = 10.0
    level = 1

    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=level)
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    f_dir[0, 0:N] = 1.0

    solver = fast_helmholtz.FastHelmholtzSolver(domain_omega, spacestep, f, f_dir, f_neu, f_rob)
    chi = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), domain_omega)
    chi = fast_helmholtz.project_chi(chi, domain_omega, V_obj=0.3)

    Alpha = compute_alpha.compute_alpha(wavenumber, material_key="hemp_fiber")
    alpha_rob = preprocessing.set2zero(Alpha * chi, domain_omega)

    u, p = solver.solve_state_and_adjoint(wavenumber, alpha_rob)
    grad_adj = solver.compute_gradient(u, p, chi, Alpha)

    rob_coords = np.argwhere(domain_omega == _env.NODE_ROBIN)
    sample_indices = np.linspace(0, len(rob_coords) - 1, 30, dtype=int)
    eps = 1e-6
    grad_fd_sample = np.zeros(len(sample_indices))
    grad_adj_sample = np.zeros(len(sample_indices))

    for idx_s, r_idx in enumerate(sample_indices):
        ri, rj = rob_coords[r_idx]
        grad_adj_sample[idx_s] = grad_adj[ri, rj]

        chi_plus = chi.copy()
        chi_plus[ri, rj] += eps
        u_plus = solver.solve(wavenumber, preprocessing.set2zero(Alpha * chi_plus, domain_omega))
        J_plus = solver.compute_energy(u_plus)

        chi_minus = chi.copy()
        chi_minus[ri, rj] -= eps
        u_minus = solver.solve(wavenumber, preprocessing.set2zero(Alpha * chi_minus, domain_omega))
        J_minus = solver.compute_energy(u_minus)

        grad_fd_sample[idx_s] = (J_plus - J_minus) / (2.0 * eps)

    rel_err = np.linalg.norm(grad_adj_sample - grad_fd_sample) / np.linalg.norm(grad_fd_sample)
    print(f"[Jour 1] Erreur relative Gradient Adjoint vs Différences Finies (eps=1e-6) : {rel_err:.2e}")

    ri0, rj0 = rob_coords[len(rob_coords) // 3]
    eps_list = np.logspace(-8, -1, 15)
    err_eps = []
    J0 = solver.compute_energy(u)
    for ep in eps_list:
        chi_p = chi.copy()
        chi_p[ri0, rj0] += ep
        Jp = solver.compute_energy(solver.solve(wavenumber, preprocessing.set2zero(Alpha * chi_p, domain_omega)))
        df_unilat = (Jp - J0) / ep
        err_eps.append(abs(df_unilat - grad_adj[ri0, rj0]) / abs(grad_adj[ri0, rj0]))

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), dpi=120)
    axes[0].plot(sample_indices, grad_adj_sample, "o-", color="tab:blue", lw=2, label="Gradient Adjoint Exact $\\nabla_\\chi J$")
    axes[0].plot(sample_indices, grad_fd_sample, "x--", color="tab:red", lw=1.8, ms=7, label="Différences Finies Centrées ($\\varepsilon=10^{-6}$)")
    axes[0].set_title(f"Validation spatiale du gradient sur $\\Gamma_{{\\mathrm{{Robin}}}}$ (Erreur rel. = {rel_err:.2e})", fontsize=11)
    axes[0].set_xlabel("Indice du nœud sur la frontière fractale $\\Gamma_{\\mathrm{Robin}}$", fontsize=10.5)
    axes[0].set_ylabel("Dérivée partielle $\\partial J / \\partial \\chi_m$", fontsize=10.5)
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    axes[1].loglog(eps_list, err_eps, "s-", color="tab:purple", lw=2, label="Erreur $|\\frac{J(\\chi+\\varepsilon e_m)-J(\\chi)}{\\varepsilon} - \\nabla_\\chi J_m| / |\\nabla_\\chi J_m|$")
    axes[1].loglog(eps_list, eps_list * (err_eps[-1] / eps_list[-1]), "k--", lw=1.2, label="Pente d'ordre 1 ($\\mathcal{O}(\\varepsilon)$)")
    axes[1].set_title("Convergence de la dérivée directionnelle quand $\\varepsilon \\to 0$", fontsize=11)
    axes[1].set_xlabel("Pas de perturbation $\\varepsilon$", fontsize=10.5)
    axes[1].set_ylabel("Erreur relative", fontsize=10.5)
    axes[1].grid(True, which="both", linestyle="--", alpha=0.6)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j1_validation_gradient_adjoint.jpg"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    study_porous_materials()
    study_sommerfeld_open_air_vs_reflexive()
    validate_adjoint_gradient()
