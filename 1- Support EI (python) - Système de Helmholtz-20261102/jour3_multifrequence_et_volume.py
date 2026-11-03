# -*- coding: utf-8 -*-
"""
Fichier : jour3_multifrequence_et_volume.py
Implémentation stricte des 3 consignes du Jour 3 (EI ST5) :
1. Analyser les résultats obtenus au Jour 2 (distributions optimisées à une fréquence) pour
   comparer leurs performances sur toute la plage de fréquences fixée [100 Hz, 2000 Hz],
   et comparer avec un mur totalement absorbant (chi = 1).
2. Optimiser l'énergie simultanément à plusieurs fréquences différentes (multi-fréquence).
3. Étudier quelle quantité de matériau poreux (V_obj in [5%, 100%]) donne le résultat
   le plus optimal (minimisation de l'énergie acoustique J).
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
from jour2_spectre_et_optimisation_mono import find_local_maxima

OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour3")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def evaluate_spectrum(solver, domain_omega, chi, k_vals, Alphas):
    """Calcule le spectre d'énergie J(f) sur toute la grille fréquentielle pour une distribution chi donnée."""
    E_spec = np.zeros_like(k_vals)
    for i, kw in enumerate(k_vals):
        alpha_rob = preprocessing.set2zero(Alphas[i] * chi, domain_omega)
        u = solver.solve(kw, alpha_rob)
        E_spec[i] = solver.compute_energy(u)
    return E_spec


def run_day3_studies():
    N = 64
    M = 2 * N
    spacestep = 1.0 / N
    c0 = 340.0
    V_obj = 0.30  # Volume de référence de 30%

    freqs = np.linspace(100.0, 2000.0, 180)
    k_vals = 2.0 * np.pi * freqs / c0
    Alphas_hemp = compute_alpha.compute_alpha(k_vals, material_key="hemp_fiber", c0=c0)

    lvl_names = {
        0: "Niveau 0 (Mur plan)",
        1: "Niveau 1 (Koch itér. 1)",
        2: "Niveau 2 (Koch itér. 2)"
    }

    solvers_lvl = {}
    domains_lvl = {}
    chi0_lvl = {}
    E_init_lvl = {}
    E_full_lvl = {}
    mono_opt_lvl = {}

    # =========================================================================
    # TÂCHE 1 : Analyser les résultats obtenus au Jour 2 sur toute la plage de
    #           fréquences fixée [100 Hz, 2000 Hz] et comparer avec le mur
    #           totalement absorbant (chi = 1)
    # =========================================================================
    print("=== [Jour 3 - Tâche 1] Analyse sur [100 Hz, 2000 Hz] des distributions optimisées au Jour 2 vs mur totalement absorbant (chi = 1) ===")

    for lvl in [0, 1, 2]:
        dom, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=lvl)
        f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
        f_dir[0, 0:N] = 1.0
        slv = fast_helmholtz.FastHelmholtzSolver(dom, spacestep, f, f_dir, f_neu, f_rob)
        solvers_lvl[lvl] = slv
        domains_lvl[lvl] = dom

        chi0_raw = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), dom)
        chi0 = fast_helmholtz.project_chi(chi0_raw, dom, V_obj=V_obj)
        chi0_lvl[lvl] = chi0

        chi_full = np.zeros((M, N), dtype=np.float64)
        chi_full[dom == _env.NODE_ROBIN] = 1.0

        E_init = evaluate_spectrum(slv, dom, chi0, k_vals, Alphas_hemp)
        E_full = evaluate_spectrum(slv, dom, chi_full, k_vals, Alphas_hemp)
        E_init_lvl[lvl] = E_init
        E_full_lvl[lvl] = E_full

        # Fréquences problématiques (maxima locaux) optimisées au Jour 2
        p_idx, p_f, _, _ = find_local_maxima(freqs, k_vals, E_full, min_prominence_ratio=0.005)
        mask_bf = (p_f >= 150.0) & (p_f <= 700.0)
        idx_bf = p_idx[mask_bf][np.argmax(E_full[p_idx[mask_bf]] * E_init[p_idx[mask_bf]])]
        mask_hf = (p_f > 700.0) & (p_f <= 1800.0)
        idx_hf = p_idx[mask_hf][np.argmax(E_full[p_idx[mask_hf]])]

        chi_bf, _, _, _ = fast_helmholtz.optimize_single_frequency(
            slv, k_vals[idx_bf], Alphas_hemp[idx_bf], chi0, V_obj=V_obj, mu_init=5.0, numb_iter=75
        )
        chi_hf, _, _, _ = fast_helmholtz.optimize_single_frequency(
            slv, k_vals[idx_hf], Alphas_hemp[idx_hf], chi0, V_obj=V_obj, mu_init=5.0, numb_iter=75
        )

        E_spec_bf = evaluate_spectrum(slv, dom, chi_bf, k_vals, Alphas_hemp)
        E_spec_hf = evaluate_spectrum(slv, dom, chi_hf, k_vals, Alphas_hemp)

        mono_opt_lvl[lvl] = {
            "f_bf": freqs[idx_bf], "idx_bf": idx_bf, "chi_bf": chi_bf, "E_bf": E_spec_bf,
            "f_hf": freqs[idx_hf], "idx_hf": idx_hf, "chi_hf": chi_hf, "E_hf": E_spec_hf
        }

        print(f"  [Level {lvl}] Sur [100, 2000] Hz : J_moy(chi_0, 30%) = {np.mean(E_init):.3f} | "
              f"J_moy(opt {freqs[idx_bf]:.0f} Hz) = {np.mean(E_spec_bf):.3f} | "
              f"J_moy(opt {freqs[idx_hf]:.0f} Hz) = {np.mean(E_spec_hf):.3f} | "
              f"J_moy(chi=1, 100%) = {np.mean(E_full):.3f}")

    fig, axes = plt.subplots(1, 3, figsize=(16.8, 5.2), dpi=120)
    for idx, lvl in enumerate([0, 1, 2]):
        ax = axes[idx]
        m_res = mono_opt_lvl[lvl]
        ax.semilogy(freqs, E_init_lvl[lvl], color="tab:gray", ls="--", lw=1.4, alpha=0.8,
                    label=f"Initiale $\\chi_0$ ($30\\%, \\overline{{J}}={np.mean(E_init_lvl[lvl]):.2f}$)")
        ax.semilogy(freqs, m_res["E_bf"], color="tab:blue", lw=1.9,
                    label=f"Opt. Jour 2 à $f_1^*={m_res['f_bf']:.0f}$ Hz ($30\\%, \\overline{{J}}={np.mean(m_res['E_bf']):.2f}$)")
        ax.semilogy(freqs, m_res["E_hf"], color="tab:purple", lw=1.8, ls="-.",
                    label=f"Opt. Jour 2 à $f_2^*={m_res['f_hf']:.0f}$ Hz ($30\\%, \\overline{{J}}={np.mean(m_res['E_hf']):.2f}$)")
        ax.semilogy(freqs, E_full_lvl[lvl], color="tab:green", lw=2.2,
                    label=f"Mur totalement absorbant ($\\chi=1, \\overline{{J}}={np.mean(E_full_lvl[lvl]):.2f}$)")

        # Marquer les deux fréquences où l'optimisation mono-fréquence bat chi = 1
        ax.semilogy(m_res["f_bf"], m_res["E_bf"][m_res["idx_bf"]], "bo", ms=7, zorder=6)
        ax.semilogy(m_res["f_hf"], m_res["E_hf"][m_res["idx_hf"]], "mo", ms=7, zorder=6)

        ax.set_title(f"{lvl_names[lvl]}", fontsize=11.5)
        ax.set_xlabel("Fréquence $f$ (Hz)", fontsize=10.5)
        if idx == 0:
            ax.set_ylabel("Énergie acoustique $J(u)$ (log)", fontsize=11)
        ax.set_ylim(1e-1, 3e2)
        ax.grid(True, which="both", linestyle="--", alpha=0.6)
        ax.legend(fontsize=8.4, loc="upper right")

    plt.suptitle("Jour 3 - Tâche 1 : Analyse sur [100 Hz, 2000 Hz] des distributions optimisées au Jour 2 ($V=30\\%$) face au mur totalement absorbant ($\\chi=1$)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j3_1_analyse_resultats_jour2_spectre.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 2 : Optimiser l'énergie simultanément à plusieurs fréquences différentes
    # =========================================================================
    print("\n=== [Jour 3 - Tâche 2] Optimisation simultanée à plusieurs fréquences différentes (V = 30%) ===")
    multi_opt_lvl = {}
    bands = [(150, 450), (450, 850), (850, 1250), (1250, 1650), (1650, 1980)]

    for lvl in [0, 1, 2]:
        dom = domains_lvl[lvl]
        slv = solvers_lvl[lvl]
        chi0 = chi0_lvl[lvl]
        E_init = E_init_lvl[lvl]
        E_full = E_full_lvl[lvl]

        # Sélection de maxima locaux répartis sur la plage de fréquences
        p_idx, p_f, _, p_e = find_local_maxima(freqs, k_vals, E_init, min_prominence_ratio=0.015)
        sel_peaks = []
        for b_min, b_max in bands:
            mb = (p_f >= b_min) & (p_f < b_max)
            if np.any(mb):
                sel_peaks.append(p_idx[mb][np.argmax(p_e[mb])])
        sel_peaks = np.array(sel_peaks, dtype=int)

        f_multi = freqs[sel_peaks]
        k_multi = k_vals[sel_peaks]
        A_multi = Alphas_hemp[sel_peaks]
        E0_multi = E_init[sel_peaks]
        weights = (1.0 / E0_multi) / np.sum(1.0 / E0_multi)

        chi_multi, hist_total, hist_per_freq = fast_helmholtz.optimize_multi_frequency(
            slv, k_multi, A_multi, chi0, weights=weights, V_obj=V_obj, mu_init=5.0, numb_iter=80
        )
        E_multi_spec = evaluate_spectrum(slv, dom, chi_multi, k_vals, Alphas_hemp)

        multi_opt_lvl[lvl] = {
            "sel_peaks": sel_peaks,
            "f_multi": f_multi,
            "chi_multi": chi_multi,
            "hist_total": hist_total,
            "hist_per_freq": hist_per_freq,
            "E_multi_spec": E_multi_spec
        }

        freqs_str = ", ".join([f"{fm:.0f} Hz" for fm in f_multi])
        print(f"  [Level {lvl}] Fréquences optimisées simultanément : [{freqs_str}]")
        print(f"    -> J_moy sur [100, 2000] Hz : Initiale = {np.mean(E_init):.3f} | "
              f"Mono-fréq. = {np.mean(mono_opt_lvl[lvl]['E_bf']):.3f} | "
              f"Multi-fréq. (30%) = {np.mean(E_multi_spec):.3f} | Mur 100% (chi=1) = {np.mean(E_full):.3f}")

    fig, axes = plt.subplots(2, 3, figsize=(16.8, 9.4), dpi=120)
    for idx, lvl in enumerate([0, 1, 2]):
        m_opt = multi_opt_lvl[lvl]
        m_mono = mono_opt_lvl[lvl]

        # Ligne 1 : Convergence simultanée sur les différentes fréquences cibles
        ax_top = axes[0, idx]
        hist_pf = m_opt["hist_per_freq"]
        n_stop = len(m_opt["hist_total"])
        for m_i, fm in enumerate(m_opt["f_multi"]):
            rel_c = 100.0 * hist_pf[:n_stop, m_i] / hist_pf[0, m_i]
            ax_top.plot(range(n_stop), rel_c, lw=1.8,
                        label=f"$f_{m_i+1}={fm:.0f}$ Hz ($J_0={hist_pf[0, m_i]:.1f} \\to {hist_pf[-1, m_i]:.2f}$)")
        rel_tot = 100.0 * m_opt["hist_total"] / m_opt["hist_total"][0]
        ax_top.plot(range(n_stop), rel_tot, "k--", lw=2.5, label=f"Énergie pondérée totale ($-{100-rel_tot[-1]:.1f}\\%$)")
        ax_top.set_title(f"Convergence multi-fréquentielle - {lvl_names[lvl]}", fontsize=11)
        ax_top.set_xlabel("Itération $k$", fontsize=10)
        if idx == 0:
            ax_top.set_ylabel("Énergie relative $J^{(k)}(\\omega_m)/J^{(0)}(\\omega_m)$ (%)", fontsize=10.5)
        ax_top.grid(True, linestyle="--", alpha=0.6)
        ax_top.legend(fontsize=8.0, loc="upper right")

        # Ligne 2 : Spectre complet J(f) de l'optimisation multi-fréquentielle vs mono-fréquence vs chi=1
        ax_bot = axes[1, idx]
        ax_bot.semilogy(freqs, E_init_lvl[lvl], color="tab:gray", ls="--", lw=1.3, alpha=0.75,
                        label=f"Initiale $\\chi_0$ ($30\\%, \\overline{{J}}={np.mean(E_init_lvl[lvl]):.2f}$)")
        ax_bot.semilogy(freqs, m_mono["E_bf"], color="tab:blue", ls="-.", lw=1.6, alpha=0.85,
                        label=f"Opt. mono-fréq. ($30\\%, \\overline{{J}}={np.mean(m_mono['E_bf']):.2f}$)")
        ax_bot.semilogy(freqs, m_opt["E_multi_spec"], color="tab:red", lw=2.1,
                        label=f"Opt. multi-fréq. ($30\\%, \\overline{{J}}={np.mean(m_opt['E_multi_spec']):.2f}$)")
        ax_bot.semilogy(freqs, E_full_lvl[lvl], color="tab:green", lw=2.0,
                        label=f"Mur 100% absorbant ($\\chi=1, \\overline{{J}}={np.mean(E_full_lvl[lvl]):.2f}$)")
        for fm in m_opt["f_multi"]:
            ax_bot.axvline(fm, color="tab:red", alpha=0.22, lw=1.0, ls=":")
        ax_bot.set_title(f"Spectre $J(f)$ après opt. multi-fréquence - {lvl_names[lvl]}", fontsize=11)
        ax_bot.set_xlabel("Fréquence $f$ (Hz)", fontsize=10.5)
        if idx == 0:
            ax_bot.set_ylabel("Énergie acoustique $J(u)$ (log)", fontsize=11)
        ax_bot.set_ylim(1e-1, 3e2)
        ax_bot.grid(True, which="both", linestyle="--", alpha=0.6)
        ax_bot.legend(fontsize=8.2, loc="upper right")

    plt.suptitle("Jour 3 - Tâche 2 : Optimisation simultanée de l'énergie à plusieurs fréquences différentes ($V=30\\%$)", fontsize=12.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j3_2_optimisation_multifrequence.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 3 : Étudier quelle quantité de matériau poreux (V_obj in [5%, 100%])
    #           donne le résultat le plus optimal (énergie acoustique minimale)
    # =========================================================================
    print("\n=== [Jour 3 - Tâche 3] Étude de la quantité de matériau poreux V_obj minimisant l'énergie acoustique ===")
    V_list = np.array([0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])

    J_vol_mono_lvl = {}
    J_vol_multi_lvl = {}
    f_mono_lvl = {}
    f_multi_peaks_lvl = {}

    for lvl in [0, 1, 2]:
        dom, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=lvl)
        slv = solvers_lvl[lvl]
        chi_base = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), dom)
        E_full = E_full_lvl[lvl]

        # Maxima locaux d'énergie du mur
        p_idx, p_f, _, _ = find_local_maxima(freqs, k_vals, E_full, min_prominence_ratio=0.005)
        # 1) Pic principal (mono-fréquence)
        idx_p1 = p_idx[np.argmax(E_full[p_idx])]
        f_mono_lvl[lvl] = freqs[idx_p1]
        k_p1 = k_vals[idx_p1]
        A_p1 = Alphas_hemp[idx_p1]

        # 2) Les 3 maxima locaux principaux (multi-fréquence)
        top3 = p_idx[np.argsort(E_full[p_idx])[::-1][:3]]
        f_multi_peaks_lvl[lvl] = freqs[top3]
        k_top3 = k_vals[top3]
        A_top3 = Alphas_hemp[top3]
        w_top3 = np.ones(len(top3), dtype=np.float64) / len(top3)

        j_mono_arr = np.zeros_like(V_list)
        j_multi_arr = np.zeros_like(V_list)

        for iv, v_val in enumerate(V_list):
            if v_val >= 0.999:
                j_mono_arr[iv] = float(E_full[idx_p1])
                j_multi_arr[iv] = float(np.mean(E_full[top3]))
            else:
                chi0_v = fast_helmholtz.project_chi(chi_base, dom, V_obj=v_val)
                _, h_mono, _, _ = fast_helmholtz.optimize_single_frequency(
                    slv, k_p1, A_p1, chi0_v, V_obj=v_val, mu_init=5.0, numb_iter=65
                )
                j_mono_arr[iv] = float(h_mono[-1])

                _, h_multi, _ = fast_helmholtz.optimize_multi_frequency(
                    slv, k_top3, A_top3, chi0_v, weights=w_top3, V_obj=v_val, mu_init=5.0, numb_iter=65
                )
                j_multi_arr[iv] = float(h_multi[-1])

        J_vol_mono_lvl[lvl] = j_mono_arr
        J_vol_multi_lvl[lvl] = j_multi_arr

        idx_min_mono = int(np.argmin(j_mono_arr))
        idx_min_multi = int(np.argmin(j_multi_arr))
        print(f"  [Level {lvl}]")
        print(f"    * Mono-fréquence ({freqs[idx_p1]:.0f} Hz) : Minimum d'énergie à V* = {V_list[idx_min_mono]*100:.0f}% "
              f"(J_min = {j_mono_arr[idx_min_mono]:.4f} vs J(100%, chi=1) = {j_mono_arr[-1]:.4f})")
        print(f"    * Multi-fréquence (3 maxima) : Minimum d'énergie à V* = {V_list[idx_min_multi]*100:.0f}% "
              f"(J_min = {j_multi_arr[idx_min_multi]:.4f} vs J(100%, chi=1) = {j_multi_arr[-1]:.4f})")

    fig, axes = plt.subplots(1, 3, figsize=(16.8, 5.2), dpi=120)
    for idx, lvl in enumerate([0, 1, 2]):
        ax = axes[idx]
        jm = J_vol_mono_lvl[lvl]
        jmul = J_vol_multi_lvl[lvl]
        i_min_m = int(np.argmin(jm))
        i_min_mul = int(np.argmin(jmul))

        ax.plot(V_list * 100, jm, "o-", color="tab:blue", lw=2.2,
                label=f"Opt. mono-fréquence ($f^*={f_mono_lvl[lvl]:.0f}$ Hz)\nMin à $V^*={V_list[i_min_m]*100:.0f}\\%$ ($J={jm[i_min_m]:.2f} < J_{{100\\%}}={jm[-1]:.2f}$)")
        ax.plot(V_list[i_min_m] * 100, jm[i_min_m], "b*", ms=13, zorder=6)

        ax.plot(V_list * 100, jmul, "s-", color="tab:red", lw=2.2,
                label=f"Opt. multi-fréquence (3 maxima locaux)\nMin à $V^*={V_list[i_min_mul]*100:.0f}\\%$ ($J={jmul[i_min_mul]:.2f} < J_{{100\\%}}={jmul[-1]:.2f}$)")
        ax.plot(V_list[i_min_mul] * 100, jmul[i_min_mul], "r*", ms=13, zorder=6)

        ax.axhline(jmul[-1], color="tab:green", ls=":", lw=1.6, label=f"Mur 100% absorbant ($\\chi=1, V=100\\%$)")
        ax.set_title(f"{lvl_names[lvl]}", fontsize=11.5)
        ax.set_xlabel("Quantité de matériau poreux $V_{\\mathrm{obj}}$ (%)", fontsize=10.5)
        if idx == 0:
            ax.set_ylabel("Énergie acoustique optimisée $J(\\chi_{\\mathrm{opt}}(V_{\\mathrm{obj}}))$", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(fontsize=8.3, loc="upper left")

    plt.suptitle("Jour 3 - Tâche 3 : Étude de la quantité de matériau poreux $V_{\\mathrm{obj}} \\in [5\\%, 100\\%]$ donnant le résultat le plus optimal", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j3_3_etude_quantite_optimale_poreux.jpg"), bbox_inches="tight")
    plt.close(fig)

    # Sauvegarde des données pour le Jour 4
    np.savez(
        os.path.join(OUTPUT_DIR, "data_jour3.npz"),
        freqs=freqs,
        k_vals=k_vals,
        E_init_spec=E_init_lvl[2],
        E_mono_bf_spec=mono_opt_lvl[2]["E_bf"],
        E_mono_hf_spec=mono_opt_lvl[2]["E_hf"],
        E_multi_spec=multi_opt_lvl[2]["E_multi_spec"],
        E_full_spec=E_full_lvl[2],
        chi_multi=multi_opt_lvl[2]["chi_multi"],
        V_list=V_list,
        J_vol_l0=J_vol_multi_lvl[0],
        J_vol_l1=J_vol_multi_lvl[1],
        J_vol_l2=J_vol_multi_lvl[2]
    )
    print("\n[Jour 3] Les 3 tâches et les 3 figures correspondantes ont été générées dans", OUTPUT_DIR)


if __name__ == "__main__":
    run_day3_studies()
