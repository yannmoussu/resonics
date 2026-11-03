# -*- coding: utf-8 -*-
"""
Fichier : jour2_spectre_et_optimisation_mono.py
Implémentation stricte des 4 consignes du Jour 2 (EI ST5) :
1. Étudier l'énergie sur la plage de fréquences choisie [100 Hz, 2000 Hz] pour un mur
   totalement absorbant (chi = 1) de forme plane (level = 0) et définir les maxima locaux.
2. Étudier la même question (spectre d'énergie et maxima locaux) pour différentes formes
   de murs totalement absorbants (level = 0, 1, 2, 3).
3. Comparer l'énergie de la distribution initiale de matériau poreux (chi_0 à 30%, comportant
   des parties absorbantes et des parties réfléchissantes) avec l'énergie du mur totalement
   absorbant (chi = 1).
4. Optimiser numériquement (à V = 30%) pour une ou plusieurs des fréquences les plus
   problématiques (auxquelles l'énergie présente un maximum local).
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

OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour2")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def find_local_maxima(freqs, k_vals, energies, min_prominence_ratio=0.01):
    """
    Détecte les maxima locaux d'une courbe d'énergie J(f).
    Renvoie les indices, fréquences, nombres d'onde et valeurs d'énergie des maxima locaux.
    """
    peaks_idx = []
    e_range = np.max(energies) - np.min(energies)
    for i in range(1, len(energies) - 1):
        if energies[i] > energies[i - 1] and energies[i] >= energies[i + 1]:
            left_min = np.min(energies[max(0, i - 6):i + 1])
            right_min = np.min(energies[i:min(len(energies), i + 7)])
            prom = energies[i] - max(left_min, right_min)
            if prom >= min_prominence_ratio * e_range or energies[i] > 1.05 * np.mean(energies):
                peaks_idx.append(i)
    peaks_idx = np.array(peaks_idx, dtype=int)
    return peaks_idx, freqs[peaks_idx], k_vals[peaks_idx], energies[peaks_idx]


def run_day2_studies():
    # Paramètres de maillage : N = 64 = 4^3 (respecte lambda >= 10*h jusqu'à 2176 Hz et géométrie Koch exacte)
    N = 64
    M = 2 * N
    spacestep = 1.0 / N
    c0 = 340.0
    V_obj = 0.30  # Volume de matériau poreux fixé à 30%

    # Plage de fréquences d'intérêt [100 Hz, 2000 Hz]
    freqs = np.linspace(100.0, 2000.0, 200)
    k_vals = 2.0 * np.pi * freqs / c0

    # Coefficient d'admittance complexe alpha(omega) du matériau poreux retenu au Jour 1 (Fibre de Chanvre)
    Alphas_hemp = compute_alpha.compute_alpha(k_vals, material_key="hemp_fiber", c0=c0)

    # =========================================================================
    # TÂCHE 1 : Énergie sur la plage de fréquences pour un mur plan totalement
    #           absorbant (level = 0, chi = 1) et définition des maxima locaux
    # =========================================================================
    print("=== [Jour 2 - Tâche 1] Mur plan totalement absorbant (level = 0, chi = 1) et maxima locaux ===")
    dom0, x0, y0, _, _ = preprocessing._set_geometry_of_domain(M, N, level=0)
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    f_dir[0, 0:N] = 1.0
    solver0 = fast_helmholtz.FastHelmholtzSolver(dom0, spacestep, f, f_dir, f_neu, f_rob)
    mask_rob0 = (dom0 == _env.NODE_ROBIN)

    E_plane_full = np.zeros_like(freqs)
    for i, kw in enumerate(k_vals):
        alpha_rob = np.zeros((M, N), dtype=np.complex128)
        alpha_rob[mask_rob0] = Alphas_hemp[i]
        u = solver0.solve(kw, alpha_rob)
        E_plane_full[i] = solver0.compute_energy(u)

    p_idx0, p_f0, p_k0, p_e0 = find_local_maxima(freqs, k_vals, E_plane_full)
    print(f"Maxima locaux d'énergie pour le mur plan totalement absorbant (level=0, {len(p_f0)} maxima) :")
    for pf, pk, pe in zip(p_f0, p_k0, p_e0):
        print(f"  -> f_max = {pf:6.1f} Hz (k = {pk:5.2f} m^-1) : J_max = {pe:.4f}")

    fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=120)
    ax.plot(freqs, E_plane_full, lw=2.2, color="tab:green",
            label=f"Mur plan totalement absorbant ($\\mathrm{{level}}=0, \\chi=1$, $\\overline{{J}}={np.mean(E_plane_full):.2f}$)")
    ax.plot(p_f0, p_e0, "ro", ms=6.5, label="Maxima locaux d'énergie")

    for idx_p, (pf, pk, pe) in enumerate(zip(p_f0, p_k0, p_e0)):
        y_off = -3.0 if idx_p == 0 else 2.2
        x_off = 45.0 if idx_p == 0 else 15.0
        ax.annotate(f"{pf:.0f} Hz\n($J={pe:.2f}$)", xy=(pf, pe), xytext=(pf + x_off, pe + y_off),
                    fontsize=8.3, arrowprops=dict(arrowstyle="->", lw=0.9, color="darkred"))

    ax.set_ylim(0, 74)
    ax.set_title("Jour 2 - Tâche 1 : Énergie $J(f)$ pour un mur plan totalement absorbant ($\\mathrm{level}=0, \\chi=1$) et maxima locaux", fontsize=11.5)
    ax.set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    ax.set_ylabel("Énergie acoustique $J(u) = \\int_\\Omega |u|^2 \\, \\mathrm{d}\\Omega$", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(fontsize=9.5, loc="upper right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j2_1_mur_plan_absorbant_maxima.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 2 : Même étude (spectre d'énergie et définition des maxima locaux)
    #           pour différentes formes de murs totalement absorbants (level = 0, 1, 2, 3)
    # =========================================================================
    print("\n=== [Jour 2 - Tâche 2] Différentes formes de murs totalement absorbants (level = 0, 1, 2, 3, chi = 1) ===")
    levels = [0, 1, 2, 3]
    solvers_lvl = {0: solver0}
    domains_lvl = {0: dom0}
    xy_lvl = {0: (x0, y0)}
    energies_full_lvl = {0: E_plane_full}
    peaks_full_lvl = {0: (p_idx0, p_f0, p_k0, p_e0)}

    for lvl in [1, 2, 3]:
        dom, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=lvl)
        f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
        f_dir[0, 0:N] = 1.0
        slv = fast_helmholtz.FastHelmholtzSolver(dom, spacestep, f, f_dir, f_neu, f_rob)
        solvers_lvl[lvl] = slv
        domains_lvl[lvl] = dom
        xy_lvl[lvl] = (x, y)

        mask_rob = (dom == _env.NODE_ROBIN)
        E_curve = np.zeros_like(freqs)
        for i, kw in enumerate(k_vals):
            alpha_rob = np.zeros((M, N), dtype=np.complex128)
            alpha_rob[mask_rob] = Alphas_hemp[i]
            u = slv.solve(kw, alpha_rob)
            E_curve[i] = slv.compute_energy(u)

        energies_full_lvl[lvl] = E_curve
        peaks_full_lvl[lvl] = find_local_maxima(freqs, k_vals, E_curve)

    for lvl in levels:
        E_c = energies_full_lvl[lvl]
        p_idx, p_f, p_k, p_e = peaks_full_lvl[lvl]
        peaks_str = ", ".join([f"{pf:.0f} Hz (J={pe:.2f})" for pf, pe in zip(p_f[:5], p_e[:5])])
        print(f"  Level {lvl} : E_moy = {np.mean(E_c):.4f}, E_max = {np.max(E_c):.4f} | Principaux maxima locaux : {peaks_str}")

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.5), dpi=120)
    lvl_colors = {0: "tab:blue", 1: "tab:orange", 2: "tab:green", 3: "tab:red"}
    lvl_names = {0: "Niveau 0 (Mur plan)", 1: "Niveau 1 (Koch itér. 1)", 2: "Niveau 2 (Koch itér. 2)", 3: "Niveau 3 (Koch itér. 3)"}

    for lvl in levels:
        E_c = energies_full_lvl[lvl]
        p_idx, p_f, p_k, p_e = peaks_full_lvl[lvl]
        axes[0].plot(freqs, E_c, lw=2.0, color=lvl_colors[lvl], label=f"{lvl_names[lvl]} ($\\overline{{J}}={np.mean(E_c):.2f}$)")
        axes[0].plot(p_f, p_e, "o", color=lvl_colors[lvl], ms=4.5)

        axes[1].semilogy(freqs, E_c, lw=2.0, color=lvl_colors[lvl], label=f"{lvl_names[lvl]} ({len(p_f)} maxima locaux)")
        axes[1].semilogy(p_f, p_e, "o", color=lvl_colors[lvl], ms=4.5)

    axes[0].set_title("Énergie $J(f)$ et maxima locaux ($\\chi=1$, échelle linéaire)", fontsize=11.5)
    axes[0].set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    axes[0].set_ylabel("Énergie acoustique $J(u)$", fontsize=11)
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend(fontsize=9.2)

    axes[1].set_title("Énergie $J(f)$ et maxima locaux ($\\chi=1$, échelle logarithmique)", fontsize=11.5)
    axes[1].set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    axes[1].set_ylabel("Énergie acoustique $J(u)$ (log)", fontsize=11)
    axes[1].grid(True, which="both", linestyle="--", alpha=0.6)
    axes[1].legend(fontsize=9.2)

    plt.suptitle("Jour 2 - Tâche 2 : Énergie $J(f)$ et maxima locaux pour différentes formes de murs totalement absorbants ($\\chi=1$)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j2_2_comparaison_formes_fractales.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 3 : Comparer l'énergie de la distribution initiale de matériau poreux
    #           (chi_0 à V_0 = 30%, parties absorbantes + réfléchissantes) avec
    #           l'énergie du mur totalement absorbant (chi = 1)
    # =========================================================================
    print("\n=== [Jour 2 - Tâche 3] Comparaison distribution initiale partielle (chi_0, V_0 = 30%) vs mur totalement absorbant (chi = 1) ===")
    energies_init_v03 = {}
    chi0_v03_lvl = {}

    for lvl in [0, 1, 2]:
        dom = domains_lvl[lvl]
        x, y = xy_lvl[lvl]
        slv = solvers_lvl[lvl]

        # Distribution initiale chi_0 projetée à V_obj = 30%
        chi0_raw = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), dom)
        chi0_v03 = fast_helmholtz.project_chi(chi0_raw, dom, V_obj=V_obj)
        chi0_v03_lvl[lvl] = chi0_v03

        E_v03 = np.zeros_like(freqs)
        for i, kw in enumerate(k_vals):
            alp = Alphas_hemp[i]
            E_v03[i] = slv.compute_energy(slv.solve(kw, preprocessing.set2zero(alp * chi0_v03, dom)))

        energies_init_v03[lvl] = E_v03
        print(f"  Level {lvl} : E_moy(chi_0, V_0=30%) = {np.mean(E_v03):.4f} (E_max = {np.max(E_v03):.2f}) "
              f"vs E_moy(chi=1, 100%) = {np.mean(energies_full_lvl[lvl]):.4f} (E_max = {np.max(energies_full_lvl[lvl]):.2f})")

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.0), dpi=120, sharey=False)
    for idx, lvl in enumerate([0, 1, 2]):
        ax = axes[idx]
        ax.semilogy(freqs, energies_init_v03[lvl], color="tab:red", lw=1.9, ls="--",
                    label=f"Distribution initiale $\\chi_0$ ($V_0=30\\%, \\overline{{J}}={np.mean(energies_init_v03[lvl]):.2f}$)")
        ax.semilogy(freqs, energies_full_lvl[lvl], color="tab:green", lw=2.2,
                    label=f"Mur totalement absorbant ($\\chi=1, \\overline{{J}}={np.mean(energies_full_lvl[lvl]):.2f}$)")
        ax.set_title(f"{lvl_names[lvl]}", fontsize=11.5)
        ax.set_xlabel("Fréquence $f$ (Hz)", fontsize=10.5)
        if idx == 0:
            ax.set_ylabel("Énergie acoustique $J(u)$ (log)", fontsize=11)
        ax.set_ylim(1e-1, 3e2)
        ax.grid(True, which="both", linestyle="--", alpha=0.6)
        ax.legend(fontsize=9.0, loc="upper right")

    plt.suptitle("Jour 2 - Tâche 3 : Comparaison de l'énergie de la distribution initiale ($\\chi_0, V_0 = 30\\%$) avec le mur totalement absorbant ($\\chi=1$)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j2_3_initial_partiel_vs_total.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 4 : Optimiser numériquement (V = 30%) pour une ou plusieurs des
    #           fréquences les plus problématiques (maxima locaux d'énergie)
    # =========================================================================
    print("\n=== [Jour 2 - Tâche 4] Optimisation numérique aux fréquences les plus problématiques (maxima locaux d'énergie) ===")
    opt_results = {}

    for lvl in [0, 1, 2]:
        dom = domains_lvl[lvl]
        slv = solvers_lvl[lvl]
        chi0_v03 = chi0_v03_lvl[lvl]

        # Sélection de 2 maxima locaux d'énergie problématiques identifiés sur le mur (BF/MF et MF/HF)
        p_idx, p_f, _, _ = find_local_maxima(freqs, k_vals, energies_full_lvl[lvl], min_prominence_ratio=0.005)

        mask_bf = (p_f >= 150.0) & (p_f <= 700.0)
        if np.any(mask_bf):
            cand_bf = p_idx[mask_bf]
            # Choix du maximum local combinant forte énergie sur chi=1 et sur chi_0
            idx_bf = cand_bf[np.argmax(energies_full_lvl[lvl][cand_bf] * energies_init_v03[lvl][cand_bf])]
        else:
            sub = (freqs >= 150.0) & (freqs <= 700.0)
            idx_bf = np.where(sub)[0][np.argmax(energies_full_lvl[lvl][sub])]

        mask_hf = (p_f > 700.0) & (p_f <= 1800.0)
        if np.any(mask_hf):
            cand_hf = p_idx[mask_hf]
            idx_hf = cand_hf[np.argmax(energies_full_lvl[lvl][cand_hf])]
        else:
            sub = (freqs > 700.0) & (freqs <= 1800.0)
            idx_hf = np.where(sub)[0][np.argmax(energies_full_lvl[lvl][sub])]

        opt_results[lvl] = {}
        for tag, idx_peak in [("autoroute_BF", idx_bf), ("ferroviaire_HF", idx_hf)]:
            f_target = freqs[idx_peak]
            k_target = k_vals[idx_peak]
            Alpha_target = compute_alpha.compute_alpha(k_target, material_key="hemp_fiber", c0=c0)

            # État initial (chi_0 à V_0 = 30%)
            u0 = slv.solve(k_target, preprocessing.set2zero(Alpha_target * chi0_v03, dom))
            J0 = slv.compute_energy(u0)

            # Optimisation par descente de gradient projeté à V_obj = 30%
            chi_opt, ene_hist, u_opt, grad_opt = fast_helmholtz.optimize_single_frequency(
                slv, k_target, Alpha_target, chi0_v03, V_obj=V_obj, mu_init=5.0, numb_iter=80
            )
            J_opt = ene_hist[-1]
            J_full = energies_full_lvl[lvl][idx_peak]

            gain_init = 100.0 * (J0 - J_opt) / J0
            gain_full = 100.0 * (J_full - J_opt) / J_full
            print(f"  [Level {lvl} - {tag}] f* = {f_target:.1f} Hz (k* = {k_target:.2f}) : "
                  f"J(chi_0, 30%) = {J0:.4f} | J(chi=1, 100%) = {J_full:.4f} -> J(chi_opt, 30%) = {J_opt:.4f} "
                  f"(-{gain_init:.1f}% vs chi_0, -{gain_full:.1f}% vs chi=1)")

            opt_results[lvl][tag] = {
                "f_target": f_target,
                "k_target": k_target,
                "idx_peak": idx_peak,
                "J0_proj": J0,
                "J_opt": J_opt,
                "J_full": J_full,
                "chi0": chi0_v03,
                "chi_opt": chi_opt,
                "u0": u0,
                "u_opt": u_opt,
                "ene_hist": ene_hist
            }

    # Tracé de la Figure 4 du Jour 2 : Convergences et champs optimisés aux fréquences problématiques
    fig, axes = plt.subplots(2, 3, figsize=(16.2, 9.5), dpi=120)

    # Ligne 1 : Courbes de convergence J(u^(k)) pour Level 0, 1, 2 aux 2 maxima locaux étudiés
    for idx_l, lvl in enumerate([0, 1, 2]):
        ax = axes[0, idx_l]
        for tag, col, label_prefix in [("autoroute_BF", "tab:blue", "Max. local 1"), ("ferroviaire_HF", "tab:red", "Max. local 2")]:
            res = opt_results[lvl][tag]
            ax.plot(res["ene_hist"], lw=2.2, color=col,
                    label=f"{label_prefix} ($f^*={res['f_target']:.0f}$ Hz) : $J_0={res['J0_proj']:.2f} \\to J_{{\\mathrm{{opt}}}}={res['J_opt']:.2f}$")
            ax.axhline(res["J_full"], color=col, ls=":", lw=1.5,
                       label=f"Mur 100% absorbant à {res['f_target']:.0f} Hz ($J={res['J_full']:.2f}$)")
        ax.set_title(f"Convergence - {lvl_names[lvl]} ($V=30\\%$)", fontsize=11)
        ax.set_xlabel("Itération $k$", fontsize=10.5)
        ax.set_ylabel("Énergie acoustique $J(u^{(k)})$", fontsize=10.5)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(fontsize=8.3, loc="upper right")

    # Ligne 2 : Champ acoustique |u_0| vs |u_opt| et distribution optimale chi_opt (Niveau 2, f* = 367 Hz)
    res_l2 = opt_results[2]["autoroute_BF"]
    dom2 = domains_lvl[2]
    mask_ext2 = (dom2 == _env.NODE_COMPLEMENTARY)

    u0_amp = np.abs(res_l2["u0"]).copy()
    u0_amp[mask_ext2] = np.nan
    uopt_amp = np.abs(res_l2["u_opt"]).copy()
    uopt_amp[mask_ext2] = np.nan
    vmax_amp = max(np.nanmax(u0_amp), np.nanmax(uopt_amp))

    im0 = axes[1, 0].imshow(u0_amp, cmap="inferno", vmin=0, vmax=vmax_amp, extent=[0, 1, 2, 0])
    axes[1, 0].set_ylim(1.4, 0.0)
    axes[1, 0].set_title(f"Champ initial $|u_0|$ ($\\chi_0, V_0=30\\%$, $f^*={res_l2['f_target']:.0f}$ Hz)\nÉnergie $J(\\chi_0) = {res_l2['J0_proj']:.3f}$", fontsize=11)
    axes[1, 0].set_xlabel("$x$ (m)")
    axes[1, 0].set_ylabel("$y$ (m)")
    fig.colorbar(im0, ax=axes[1, 0], fraction=0.046, pad=0.04, label="$|u(x,y)|$")

    im1 = axes[1, 1].imshow(uopt_amp, cmap="inferno", vmin=0, vmax=vmax_amp, extent=[0, 1, 2, 0])
    axes[1, 1].set_ylim(1.4, 0.0)
    axes[1, 1].set_title(f"Champ optimisé $|u_{{\\mathrm{{opt}}}}|$ ($\\chi_{{\\mathrm{{opt}}}}, V=30\\%$, $f^*={res_l2['f_target']:.0f}$ Hz)\nÉnergie $J(\\chi_{{\\mathrm{{opt}}}}) = {res_l2['J_opt']:.3f} < J(\\chi=1) = {res_l2['J_full']:.3f}$", fontsize=11)
    axes[1, 1].set_xlabel("$x$ (m)")
    axes[1, 1].set_ylabel("$y$ (m)")
    fig.colorbar(im1, ax=axes[1, 1], fraction=0.046, pad=0.04, label="$|u(x,y)|$")

    rob_coords2 = np.argwhere(dom2 == _env.NODE_ROBIN)
    ry = rob_coords2[:, 0] * spacestep
    rx = rob_coords2[:, 1] * spacestep
    chi_vals = res_l2["chi_opt"][dom2 == _env.NODE_ROBIN]

    axes[1, 2].imshow(np.where(mask_ext2, 0.85, 1.0), cmap="gray", vmin=0, vmax=1, extent=[0, 1, 2, 0])
    sc = axes[1, 2].scatter(rx, ry, c=chi_vals, cmap="viridis", vmin=0, vmax=1, s=22, edgecolors="none")
    axes[1, 2].set_ylim(1.4, 0.6)
    axes[1, 2].set_title(f"Distribution optimale $\\chi_{{\\mathrm{{opt}}}}$ sur la frontière\n(Niveau 2, $V=30\\%$, $f^*={res_l2['f_target']:.0f}$ Hz)", fontsize=11)
    axes[1, 2].set_xlabel("$x$ (m)")
    axes[1, 2].set_ylabel("$y$ (m)")
    fig.colorbar(sc, ax=axes[1, 2], fraction=0.046, pad=0.04, label="Densité de poreux $\\chi_{\\mathrm{opt}} \\in [0,1]$")

    plt.suptitle("Jour 2 - Tâche 4 : Optimisation numérique aux fréquences les plus problématiques (maxima locaux d'énergie)", fontsize=12.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j2_4_optimisation_mono_frequence.jpg"), bbox_inches="tight")
    plt.close(fig)

    # Sauvegarde des données pour le Jour 3
    np.savez(
        os.path.join(OUTPUT_DIR, "data_jour2.npz"),
        freqs=freqs,
        k_vals=k_vals,
        energies_full_l0=energies_full_lvl[0],
        energies_full_l1=energies_full_lvl[1],
        energies_full_l2=energies_full_lvl[2],
        energies_init_v03_l0=energies_init_v03[0],
        energies_init_v03_l1=energies_init_v03[1],
        energies_init_v03_l2=energies_init_v03[2],
        chi_opt_l0_hw=opt_results[0]["autoroute_BF"]["chi_opt"],
        chi_opt_l1_hw=opt_results[1]["autoroute_BF"]["chi_opt"],
        chi_opt_l2_hw=opt_results[2]["autoroute_BF"]["chi_opt"],
        chi_opt_l2_rw=opt_results[2]["ferroviaire_HF"]["chi_opt"],
        f_hw_l2=opt_results[2]["autoroute_BF"]["f_target"],
        f_rw_l2=opt_results[2]["ferroviaire_HF"]["f_target"]
    )
    print("\n[Jour 2] Les 4 tâches et les 4 figures correspondantes ont été générées dans", OUTPUT_DIR)


if __name__ == "__main__":
    run_day2_studies()
