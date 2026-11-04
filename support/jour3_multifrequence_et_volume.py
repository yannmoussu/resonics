# -*- coding: utf-8 -*-
"""
Fichier : jour3_multifrequence_et_volume.py
Implémentation stricte des 3 consignes du Jour 3 (EI ST5) avec :
- Source acoustique : Source du RER B (preprocessing.source_rer_b du dossier support)
- Matériau poreux : Ouate de Polyester (MATERIAUX["OUATE_POLYESTER"] du dossier support)

Consignes du Jour 3 :
1. Analyser les résultats obtenus au Jour 2 (distributions optimisées à une fréquence) pour
   comparer leurs performances sur toute la plage de fréquences fixée [50 Hz, 3000 Hz],
   et comparer avec un mur totalement absorbant (chi = 1).
2. Optimiser l'énergie simultanément à plusieurs fréquences différentes (multi-fréquence
   couvrant les composantes de la source RER B).
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


def evaluate_spectrum(solver, domain_omega, chi, k_vals, Alphas, source_amps):
    """Calcule le spectre d'énergie J(f) pondéré par la source RER B sur toute la grille fréquentielle."""
    E_spec = np.zeros_like(k_vals)
    for i, kw in enumerate(k_vals):
        alpha_rob = preprocessing.set2zero(Alphas[i] * chi, domain_omega)
        u = solver.solve(kw, alpha_rob) * source_amps[i]
        E_spec[i] = solver.compute_energy(u)
    return E_spec


def run_day3_studies():
    N = 64
    M = 2 * N
    spacestep = 1.0 / N
    c0 = 343.0    # Célérité du son dans support/compute_alpha.py et support/processing.py
    V_obj = 0.30  # Volume de référence de 30%

    # Plage de fréquences [50 Hz, 3000 Hz] couvrant les 3 composantes de la source RER B
    freqs = np.linspace(50.0, 3000.0, 237)  # Pas de 12.5 Hz
    k_vals = 2.0 * np.pi * freqs / c0
    rer_b_amps = np.array([preprocessing.source_rer_b(f) for f in freqs], dtype=np.float64)
    Alphas_ouate = compute_alpha.compute_alpha(k_vals, material_key="OUATE_POLYESTER", c0=c0)

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
    #           fréquences fixée [50 Hz, 3000 Hz] et comparer avec le mur
    #           totalement absorbant (chi = 1, Ouate de Polyester, Source RER B)
    # =========================================================================
    print("=== [Jour 3 - Tâche 1] Analyse sur [50 Hz, 3000 Hz] des distributions optimisées au Jour 2 vs mur totalement absorbant (chi = 1) ===")

    for lvl in [0, 1, 2]:
        dom, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=lvl)
        f_pde, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
        f_dir[0, 0:N] = 1.0
        slv = fast_helmholtz.FastHelmholtzSolver(dom, spacestep, f_pde, f_dir, f_neu, f_rob)
        solvers_lvl[lvl] = slv
        domains_lvl[lvl] = dom

        chi0_raw = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), dom)
        chi0 = fast_helmholtz.project_chi(chi0_raw, dom, V_obj=V_obj)
        chi0_lvl[lvl] = chi0

        chi_full = np.zeros((M, N), dtype=np.float64)
        chi_full[dom == _env.NODE_ROBIN] = 1.0

        E_init = evaluate_spectrum(slv, dom, chi0, k_vals, Alphas_ouate, rer_b_amps)
        E_full = evaluate_spectrum(slv, dom, chi_full, k_vals, Alphas_ouate, rer_b_amps)
        E_init_lvl[lvl] = E_init
        E_full_lvl[lvl] = E_full

        # Fréquences problématiques (maxima locaux du RER B) optimisées au Jour 2
        p_idx, p_f, _, _ = find_local_maxima(freqs, k_vals, E_full, min_prominence_ratio=0.005)
        mask_bf = (p_f >= 150.0) & (p_f <= 450.0)
        if lvl == 0:
            idx_bf = p_idx[mask_bf][np.argmax(E_full[p_idx[mask_bf]])]
        else:
            idx_bf = p_idx[mask_bf][np.argmax(E_full[p_idx[mask_bf]] * E_init[p_idx[mask_bf]])]

        mask_hf = (p_f >= 500.0) & (p_f <= 1150.0)
        if lvl == 0:
            idx_hf = p_idx[mask_hf][np.argmax(E_full[p_idx[mask_hf]])]
        else:
            idx_hf = p_idx[mask_hf][np.argmax(E_full[p_idx[mask_hf]] * E_init[p_idx[mask_hf]])]

        # Optimisation mono-fréquence sur le pic BF (Moteur) et le pic MF (Roulement)
        chi_bf_cont, _, _, _ = fast_helmholtz.optimize_single_frequency(
            slv, k_vals[idx_bf], Alphas_ouate[idx_bf], chi0, V_obj=V_obj, mu_init=5.0, numb_iter=75
        )
        chi_bf = fast_helmholtz.binarize_chi(
            chi_bf_cont, dom, V_obj=V_obj, solver=slv, wavenumber=k_vals[idx_bf], Alpha=Alphas_ouate[idx_bf]
        )

        chi_hf_cont, _, _, _ = fast_helmholtz.optimize_single_frequency(
            slv, k_vals[idx_hf], Alphas_ouate[idx_hf], chi0, V_obj=V_obj, mu_init=5.0, numb_iter=75
        )
        chi_hf = fast_helmholtz.binarize_chi(
            chi_hf_cont, dom, V_obj=V_obj, solver=slv, wavenumber=k_vals[idx_hf], Alpha=Alphas_ouate[idx_hf]
        )

        E_spec_bf = evaluate_spectrum(slv, dom, chi_bf, k_vals, Alphas_ouate, rer_b_amps)
        E_spec_hf = evaluate_spectrum(slv, dom, chi_hf, k_vals, Alphas_ouate, rer_b_amps)

        mono_opt_lvl[lvl] = {
            "f_bf": freqs[idx_bf], "idx_bf": idx_bf, "chi_bf": chi_bf, "E_bf": E_spec_bf,
            "f_hf": freqs[idx_hf], "idx_hf": idx_hf, "chi_hf": chi_hf, "E_hf": E_spec_hf
        }

        print(f"  [Level {lvl}] Sur [50, 3000] Hz : J_moy(chi_0, 30%) = {np.mean(E_init):.3f} | "
              f"J_moy(opt {freqs[idx_bf]:.0f} Hz) = {np.mean(E_spec_bf):.3f} | "
              f"J_moy(opt {freqs[idx_hf]:.0f} Hz) = {np.mean(E_spec_hf):.3f} | "
              f"J_moy(chi=1, 100%) = {np.mean(E_full):.3f}")

    fig, axes = plt.subplots(1, 3, figsize=(16.8, 5.2), dpi=120)
    for idx, lvl in enumerate([0, 1, 2]):
        ax = axes[idx]
        m_res = mono_opt_lvl[lvl]
        ax.semilogy(freqs, np.maximum(E_init_lvl[lvl], 1e-5), color="tab:gray", ls="--", lw=1.4, alpha=0.8,
                    label=f"Initiale $\\chi_0$ ($30\\%$)")
        ax.semilogy(freqs, np.maximum(m_res["E_bf"], 1e-5), color="tab:blue", lw=1.9,
                    label=f"Opt. Jour 2 ({m_res['f_bf']:.0f} Hz)")
        ax.semilogy(freqs, np.maximum(m_res["E_hf"], 1e-5), color="tab:purple", lw=1.8, ls="-.",
                    label=f"Opt. Jour 2 ({m_res['f_hf']:.0f} Hz)")
        ax.semilogy(freqs, np.maximum(E_full_lvl[lvl], 1e-5), color="tab:green", lw=2.2,
                    label=f"Mur 100% Ouate ($\\chi=1$)")

        # Marquer les deux fréquences où l'optimisation mono-fréquence bat chi = 1
        ax.semilogy(m_res["f_bf"], m_res["E_bf"][m_res["idx_bf"]], "bo", ms=7, zorder=6)
        ax.semilogy(m_res["f_hf"], m_res["E_hf"][m_res["idx_hf"]], "mo", ms=7, zorder=6)

        ax.set_title(f"{lvl_names[lvl]}", fontsize=11.5)
        ax.set_xlabel("Fréquence $f$ (Hz)", fontsize=10.5)
        if idx == 0:
            ax.set_ylabel("Énergie acoustique $J(u)$ (log)", fontsize=11)
        ax.set_ylim(1e-4, 1e2)
        ax.grid(True, which="both", linestyle="--", alpha=0.6)
        ax.legend(fontsize=8.8, loc="upper right")

    plt.suptitle("Jour 3 - Tâche 1 : Analyse sur [50 Hz, 3000 Hz] des distributions optimisées au Jour 2 ($V=30\\%$) face au mur $100\\%$ Ouate ($\\chi=1$) — Source RER B", fontsize=11.8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j3_1_analyse_resultats_jour2_spectre.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 2 : Optimiser l'énergie simultanément à plusieurs fréquences différentes
    #           (couvrant les 3 bandes physiques du RER B : Moteur, Roulement, Crissement)
    # =========================================================================
    print("\n=== [Jour 3 - Tâche 2] Optimisation simultanée à plusieurs fréquences du RER B (V = 30%, Ouate de Polyester) ===")
    multi_opt_lvl = {}
    # Les 4 sous-bandes couvrant les 3 composantes du RER B :
    # 1) Moteur/Ventilation (150-450 Hz), 2) Roulement bas (500-800 Hz),
    # 3) Roulement haut (800-1200 Hz), 4) Crissement (2350-2650 Hz)
    bands = [(150, 450), (500, 800), (800, 1200), (2350, 2650)]

    for lvl in [0, 1, 2]:
        dom = domains_lvl[lvl]
        slv = solvers_lvl[lvl]
        chi0 = chi0_lvl[lvl]
        E_init = E_init_lvl[lvl]
        E_full = E_full_lvl[lvl]

        # Sélection des maxima locaux problématiques dans chaque bande du RER B
        p_idx, p_f, _, p_e = find_local_maxima(freqs, k_vals, E_init, min_prominence_ratio=0.005)
        sel_peaks = []
        for b_i, (b_min, b_max) in enumerate(bands):
            if b_i == 1:
                sel_peaks.append(mono_opt_lvl[lvl]["idx_hf"])
                continue
            mb = (p_f >= b_min) & (p_f <= b_max)
            if np.any(mb):
                sel_peaks.append(p_idx[mb][np.argmax(p_e[mb])])
            else:
                sub = (freqs >= b_min) & (freqs <= b_max)
                sel_peaks.append(np.where(sub)[0][np.argmax(E_init[sub])])
        sel_peaks = np.array(sel_peaks, dtype=int)

        f_multi = freqs[sel_peaks]
        k_multi = k_vals[sel_peaks]
        A_multi = Alphas_ouate[sel_peaks]
        amps_multi = rer_b_amps[sel_peaks]
        E0_multi = E_init[sel_peaks]
        weights = (1.0 / E0_multi) / np.sum(1.0 / E0_multi)

        chi_multi, hist_total, hist_per_freq = fast_helmholtz.optimize_multi_frequency(
            slv, k_multi, A_multi, chi0, weights=weights, source_amps=amps_multi,
            V_obj=V_obj, mu_init=5.0, numb_iter=80
        )
        E_multi_spec = evaluate_spectrum(slv, dom, chi_multi, k_vals, Alphas_ouate, rer_b_amps)

        multi_opt_lvl[lvl] = {
            "sel_peaks": sel_peaks,
            "f_multi": f_multi,
            "chi_multi": chi_multi,
            "hist_total": hist_total,
            "hist_per_freq": hist_per_freq,
            "E_multi_spec": E_multi_spec
        }

        freqs_str = ", ".join([f"{fm:.0f} Hz" for fm in f_multi])
        print(f"  [Level {lvl}] Fréquences RER B optimisées simultanément : [{freqs_str}]")
        print(f"    -> J_moy sur [50, 3000] Hz : Initiale = {np.mean(E_init):.3f} | "
              f"Mono-fréq. = {np.mean(mono_opt_lvl[lvl]['E_hf']):.3f} | "
              f"Multi-fréq. (30%) = {np.mean(E_multi_spec):.3f} | Mur 100% (chi=1) = {np.mean(E_full):.3f}")

    fig, axes = plt.subplots(2, 3, figsize=(16.8, 9.4), dpi=120)
    for idx, lvl in enumerate([0, 1, 2]):
        m_opt = multi_opt_lvl[lvl]
        m_mono = mono_opt_lvl[lvl]

        # Ligne 1 : Convergence simultanée sur les différentes fréquences cibles du RER B
        ax_top = axes[0, idx]
        hist_pf = m_opt["hist_per_freq"]
        n_stop = len(m_opt["hist_total"])
        for m_i, fm in enumerate(m_opt["f_multi"]):
            rel_c = 100.0 * hist_pf[:n_stop, m_i] / hist_pf[0, m_i]
            ax_top.plot(range(n_stop), rel_c, lw=1.9, label=f"{fm:.0f} Hz")
        rel_tot = 100.0 * m_opt["hist_total"] / m_opt["hist_total"][0]
        ax_top.plot(range(n_stop), rel_tot, "k--", lw=2.5, label="Coût pondéré total")
        ax_top.set_title(f"Convergence multi-fréquence - {lvl_names[lvl]}", fontsize=11)
        ax_top.set_xlabel("Itération $k$", fontsize=10)
        if idx == 0:
            ax_top.set_ylabel("Énergie relative $J^{(k)}(\\omega_m)/J^{(0)}(\\omega_m)$ (%)", fontsize=10.5)
        ax_top.grid(True, linestyle="--", alpha=0.6)
        ax_top.legend(fontsize=8.5, loc="upper right")

        # Ligne 2 : Spectre complet J(f) de l'optimisation multi-fréquentielle vs mono-fréquence vs chi=1
        ax_bot = axes[1, idx]
        ax_bot.semilogy(freqs, np.maximum(E_init_lvl[lvl], 1e-5), color="tab:gray", ls="--", lw=1.3, alpha=0.75,
                        label="Initiale $\\chi_0$ (30%)")
        ax_bot.semilogy(freqs, np.maximum(m_mono["E_hf"], 1e-5), color="tab:blue", ls="-.", lw=1.6, alpha=0.85,
                        label=f"Opt. mono ({m_mono['f_hf']:.0f} Hz)")
        ax_bot.semilogy(freqs, np.maximum(m_opt["E_multi_spec"], 1e-5), color="tab:red", lw=2.1,
                        label="Opt. multi-fréquence (30%)")
        ax_bot.semilogy(freqs, np.maximum(E_full_lvl[lvl], 1e-5), color="tab:green", lw=2.0,
                        label="Mur 100% Ouate ($\\chi=1$)")
        for fm in m_opt["f_multi"]:
            ax_bot.axvline(fm, color="tab:red", alpha=0.25, lw=1.1, ls=":")
        ax_bot.set_title(f"Spectre $J(f)$ après opt. multi-fréquence - {lvl_names[lvl]}", fontsize=11)
        ax_bot.set_xlabel("Fréquence $f$ (Hz)", fontsize=10.5)
        if idx == 0:
            ax_bot.set_ylabel("Énergie acoustique $J(u)$ (log)", fontsize=11)
        ax_bot.set_ylim(1e-4, 1e2)
        ax_bot.grid(True, which="both", linestyle="--", alpha=0.6)
        ax_bot.legend(fontsize=8.5, loc="upper right")

    plt.suptitle("Jour 3 - Tâche 2 : Optimisation simultanée de l'énergie à plusieurs fréquences du RER B ($V=30\\%$, Ouate de Polyester)", fontsize=12.2)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j3_2_optimisation_multifrequence.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # TÂCHE 3 : Étudier quelle quantité de matériau poreux (V_obj in [5%, 100%])
    #           donne le résultat le plus optimal (énergie acoustique minimale)
    # =========================================================================
    print("\n=== [Jour 3 - Tâche 3] Étude de la quantité de matériau poreux V_obj minimisant l'énergie acoustique (Source RER B, Ouate de Polyester) ===")
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

        # Maxima locaux d'énergie du mur sous source RER B
        p_idx, p_f, _, _ = find_local_maxima(freqs, k_vals, E_full, min_prominence_ratio=0.005)
        # 1) Pic principal dans la bande Roulement du RER B (mono-fréquence)
        if lvl == 0:
            idx_p1 = int(np.argmin(np.abs(freqs - 750.0)))
            top3 = np.array([int(np.argmin(np.abs(freqs - f_c))) for f_c in [225.0, 575.0, 750.0]], dtype=int)
        else:
            idx_p1 = mono_opt_lvl[lvl]["idx_hf"]
            top3 = p_idx[np.argsort(E_full[p_idx])[::-1][:3]]
        f_mono_lvl[lvl] = freqs[idx_p1]
        k_p1 = k_vals[idx_p1]
        A_p1 = Alphas_ouate[idx_p1]
        amp_p1 = rer_b_amps[idx_p1]

        # 2) Les 3 maxima locaux principaux du RER B (multi-fréquence)
        f_multi_peaks_lvl[lvl] = freqs[top3]
        k_top3 = k_vals[top3]
        A_top3 = Alphas_ouate[top3]
        amps_top3 = rer_b_amps[top3]
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
                j_mono_arr[iv] = float((amp_p1 ** 2) * h_mono[-1])

                _, h_multi, _ = fast_helmholtz.optimize_multi_frequency(
                    slv, k_top3, A_top3, chi0_v, weights=w_top3, source_amps=amps_top3,
                    V_obj=v_val, mu_init=5.0, numb_iter=65
                )
                j_multi_arr[iv] = float(h_multi[-1])

        J_vol_mono_lvl[lvl] = j_mono_arr
        J_vol_multi_lvl[lvl] = j_multi_arr

        idx_min_mono = int(np.argmin(j_mono_arr))
        idx_min_multi = int(np.argmin(j_multi_arr))
        print(f"  [Level {lvl}]")
        print(f"    * Mono-fréquence ({freqs[idx_p1]:.0f} Hz) : Minimum d'énergie à V* = {V_list[idx_min_mono]*100:.0f}% "
              f"(J_min = {j_mono_arr[idx_min_mono]:.4f} vs J(100%, chi=1) = {j_mono_arr[-1]:.4f})")
        print(f"    * Multi-fréquence (3 maxima RER B) : Minimum d'énergie à V* = {V_list[idx_min_multi]*100:.0f}% "
              f"(J_min = {j_multi_arr[idx_min_multi]:.4f} vs J(100%, chi=1) = {j_multi_arr[-1]:.4f})")

    fig, axes = plt.subplots(1, 3, figsize=(16.8, 5.2), dpi=120)
    for idx, lvl in enumerate([0, 1, 2]):
        ax = axes[idx]
        jm = J_vol_mono_lvl[lvl]
        jmul = J_vol_multi_lvl[lvl]
        i_min_m = int(np.argmin(jm))
        i_min_mul = int(np.argmin(jmul))

        ax.plot(V_list * 100, jm, "o-", color="tab:blue", lw=2.2,
                label=f"Opt. mono ({f_mono_lvl[lvl]:.0f} Hz) — Min à $V^*={V_list[i_min_m]*100:.0f}\\%$")
        ax.plot(V_list[i_min_m] * 100, jm[i_min_m], "b*", ms=13, zorder=6)

        ax.plot(V_list * 100, jmul, "s-", color="tab:red", lw=2.2,
                label=f"Opt. multi (3 pics RER B) — Min à $V^*={V_list[i_min_mul]*100:.0f}\\%$")
        ax.plot(V_list[i_min_mul] * 100, jmul[i_min_mul], "r*", ms=13, zorder=6)

        ax.axhline(jmul[-1], color="tab:green", ls=":", lw=1.6, label="Mur 100% Ouate ($\\chi=1$)")
        ax.set_title(f"{lvl_names[lvl]}", fontsize=11.5)
        ax.set_xlabel("Quantité de ouate de polyester $V_{\\mathrm{obj}}$ (%)", fontsize=10.5)
        if idx == 0:
            ax.set_ylabel("Énergie acoustique optimisée $J(\\chi_{\\mathrm{opt}}(V_{\\mathrm{obj}}))$", fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(fontsize=8.6, loc="upper left")

    plt.suptitle("Jour 3 - Tâche 3 : Étude de la quantité optimale de ouate de polyester $V_{\\mathrm{obj}} \\in [5\\%, 100\\%]$ (Source RER B)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j3_3_etude_quantite_optimale_poreux.jpg"), bbox_inches="tight")
    plt.close(fig)

    # Sauvegarde des données pour le Jour 4
    np.savez(
        os.path.join(OUTPUT_DIR, "data_jour3.npz"),
        freqs=freqs,
        k_vals=k_vals,
        rer_b_amps=rer_b_amps,
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
