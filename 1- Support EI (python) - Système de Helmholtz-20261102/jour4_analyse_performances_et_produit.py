# -*- coding: utf-8 -*-
"""
Fichier : jour4_analyse_performances_et_produit.py
Implémentation complète du Jour 4 (Startup Resonics - EI ST5) :
1. Poursuite de l'analyse des performances :
   - Passage à l'industrialisation : comparaison densité relaxée continue chi in [0,1]
     vs inclusions binaires manufacturables chi_bin in {0,1} (plan d'usinage des cartouches poreuses).
   - Robustesse vis-à-vis de la nature de la source sonore :
     Onde plane normale vs Onde sphérique (source ponctuelle localisée) vs Onde d'incidence oblique (30°).
   - Étude multi-matériaux (inclusions hybrides combinant deux matériaux poreux vs mono-matériau).
2. Conclusion industrielle : Matrice de décision multi-critères et sélection des produits finaux
   à développer pour l'Autoroute ("ResoWall-Route") et la Voie Ferrée ("ResoWall-Rail").
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

OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour4")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_day4_studies():
    N = 64
    M = 2 * N
    spacestep = 1.0 / N
    c0 = 340.0
    V_obj = 0.30  # Contrainte de volume fixée à 30% de matériau poreux

    freqs = np.linspace(100.0, 2000.0, 160)
    k_vals = 2.0 * np.pi * freqs / c0

    Alphas_hemp = compute_alpha.compute_alpha(k_vals, material_key="hemp_fiber", c0=c0)
    Alphas_rock = compute_alpha.compute_alpha(k_vals, material_key="rock_wool", c0=c0)
    Alphas_mela = compute_alpha.compute_alpha(k_vals, material_key="melamine_foam", c0=c0)

    # =========================================================================
    # ÉTAPE 1 : Industrialisation Binaire (chi in {0,1}) et Combinaison Bi-Matériaux
    # =========================================================================
    print("=== [Jour 4 - Étape 1] Analyse Binaire (0/1) & Inclusions Bi-Matériaux ===")
    dom2, x2, y2, _, _ = preprocessing._set_geometry_of_domain(M, N, level=2)
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    f_dir[0, 0:N] = 1.0
    solver2 = fast_helmholtz.FastHelmholtzSolver(dom2, spacestep, f, f_dir, f_neu, f_rob)
    chi_init2 = preprocessing.set2zero(preprocessing._set_chi(M, N, x2, y2), dom2)

    # Fréquences de résonance cibles pour l'optimisation multi-fréquentielle à V_obj = 35%
    # (correspondant aux pics de résonance identifiés au Jour 3)
    target_freqs = np.array([365.4, 673.2, 832.4, 1416.2, 1670.9])
    target_k = 2.0 * np.pi * target_freqs / c0
    target_Alpha_hemp = compute_alpha.compute_alpha(target_k, material_key="hemp_fiber", c0=c0)

    # Calcul des énergies initiales pour pondérer équitablement
    chi0_v = fast_helmholtz.project_chi(chi_init2, dom2, V_obj=V_obj)
    e0_targets = np.array([
        solver2.compute_energy(solver2.solve(kt, preprocessing.set2zero(at * chi0_v, dom2)))
        for kt, at in zip(target_k, target_Alpha_hemp)
    ])
    weights = (1.0 / e0_targets) / np.sum(1.0 / e0_targets)

    chi_cont, _, _ = fast_helmholtz.optimize_multi_frequency(
        solver2, target_k, target_Alpha_hemp, chi_init2, weights=weights,
        V_obj=V_obj, mu_init=5.0, numb_iter=75
    )
    chi_bin = fast_helmholtz.binarize_chi(chi_cont, dom2, V_obj=V_obj)

    # Construction d'une paroi Hybride Bi-Matériaux (Fibre de Chanvre + Laine de Roche) sur les inclusions binaires :
    # - Dans les cavités profondes de la fractale (y > 1.0 m, ventres de basse fréquence) : Laine de Roche
    # - Sur les crêtes avancées vers la source (y <= 1.0 m, diffraction haute fréquence) : Fibre de Chanvre
    mask_rob2 = (dom2 == _env.NODE_ROBIN)
    rob_i, rob_j = np.where(mask_rob2)
    is_deep_cavity = (rob_i >= N)

    E_refl_spec = np.zeros_like(freqs)
    E_init_spec = np.zeros_like(freqs)
    E_cont_spec = np.zeros_like(freqs)
    E_bin_hemp_spec = np.zeros_like(freqs)
    E_bin_hybrid_spec = np.zeros_like(freqs)
    E_full_spec = np.zeros_like(freqs)

    zero_rob = np.zeros((M, N), dtype=np.complex128)
    chi_full2 = np.zeros((M, N), dtype=np.float64)
    chi_full2[mask_rob2] = 1.0

    for i, kw in enumerate(k_vals):
        ah = Alphas_hemp[i]
        ar = Alphas_rock[i]

        E_refl_spec[i] = solver2.compute_energy(solver2.solve(kw, zero_rob))
        E_init_spec[i] = solver2.compute_energy(solver2.solve(kw, preprocessing.set2zero(ah * chi0_v, dom2)))
        E_cont_spec[i] = solver2.compute_energy(solver2.solve(kw, preprocessing.set2zero(ah * chi_cont, dom2)))
        E_bin_hemp_spec[i] = solver2.compute_energy(solver2.solve(kw, preprocessing.set2zero(ah * chi_bin, dom2)))
        E_full_spec[i] = solver2.compute_energy(solver2.solve(kw, preprocessing.set2zero(ah * chi_full2, dom2)))

        # Matrice alpha_rob hybride bi-matériaux
        alpha_hyb = np.zeros((M, N), dtype=np.complex128)
        for idx_node, (ri, rj) in enumerate(zip(rob_i, rob_j)):
            if chi_bin[ri, rj] > 0.5:
                alpha_hyb[ri, rj] = ar if is_deep_cavity[idx_node] else ah
        E_bin_hybrid_spec[i] = solver2.compute_energy(solver2.solve(kw, alpha_hyb))

    ecart_bin_pct = 100.0 * abs(np.mean(E_bin_hemp_spec) - np.mean(E_cont_spec)) / np.mean(E_cont_spec)
    print(f"  - Énergie moyenne Continue (30%)         : {np.mean(E_cont_spec):.4f}")
    print(f"  - Énergie moyenne Binaire 0/1 Chanvre    : {np.mean(E_bin_hemp_spec):.4f} (écart = {ecart_bin_pct:.2f}%)")
    print(f"  - Énergie moyenne Binaire Bi-Matériaux   : {np.mean(E_bin_hybrid_spec):.4f}")
    print(f"  - Énergie moyenne Mur 100% Absorbant     : {np.mean(E_full_spec):.4f}")

    # Figure 4.1 : Comparaison Continue vs Binaire 0/1 vs Bi-Matériaux + Schéma d'usinage des inclusions
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.4), dpi=120)

    axes[0].plot(freqs, E_init_spec, color="gray", ls="--", lw=1.6, label=f"Initiale non optimisée ($30\\%$, $\\overline{{J}}={np.mean(E_init_spec):.2f}$)")
    axes[0].plot(freqs, E_cont_spec, color="tab:blue", lw=2.2, label=f"Optimisée Continue $\\chi \\in [0,1]$ ($\\overline{{J}}={np.mean(E_cont_spec):.2f}$)")
    axes[0].plot(freqs, E_bin_hemp_spec, color="tab:red", ls="-.", lw=2.1, label=f"Inclusions Binaires $\\chi_{{\\mathrm{{bin}}}} \\in \\{{0,1\\}}$ Chanvre ($\\overline{{J}}={np.mean(E_bin_hemp_spec):.2f}$)")
    axes[0].plot(freqs, E_bin_hybrid_spec, color="tab:purple", lw=2.0, label=f"Inclusions Hybrides Bi-Matériaux ($\\overline{{J}}={np.mean(E_bin_hybrid_spec):.2f}$)")
    axes[0].plot(freqs, E_full_spec, color="tab:green", ls=":", lw=1.9, label=f"Mur 100% absorbant ($\\overline{{J}}={np.mean(E_full_spec):.2f}$)")
    axes[0].set_title("Validation de la binarisation industrielle $\\chi_{\\mathrm{bin}} \\in \\{0,1\\}$ et du bi-matériau ($V=30\\%$)", fontsize=11.5)
    axes[0].set_xlabel("Fréquence $f$ (Hz)", fontsize=11)
    axes[0].set_ylabel("Énergie acoustique $J(u)$", fontsize=11)
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend(fontsize=8.6, loc="upper right")

    # Carte d'usinage industrielle (Béton réfléchissant vs Cartouche Chanvre vs Cartouche Laine de Roche)
    mask_ext2 = (dom2 == _env.NODE_COMPLEMENTARY)
    axes[1].imshow(np.where(mask_ext2, 0.82, 0.97), cmap="gray", vmin=0, vmax=1, extent=[0, 1, 2, 0])

    rx = rob_j * spacestep
    ry = rob_i * spacestep
    mask_concrete = chi_bin[mask_rob2] < 0.5
    mask_hemp_inc = (chi_bin[mask_rob2] >= 0.5) & (~is_deep_cavity)
    mask_rock_inc = (chi_bin[mask_rob2] >= 0.5) & is_deep_cavity

    axes[1].scatter(rx[mask_concrete], ry[mask_concrete], c="#555555", s=24, marker="s", label="Béton réfléchissant ($\\chi=0$, 70%)")
    axes[1].scatter(rx[mask_hemp_inc], ry[mask_hemp_inc], c="#2ca02c", s=34, marker="o", label="Inclusion Fibre de Chanvre ($\\chi=1$, crêtes)")
    axes[1].scatter(rx[mask_rock_inc], ry[mask_rock_inc], c="#d62728", s=34, marker="^", label="Inclusion Laine de Roche ($\\chi=1$, cavités)")
    axes[1].set_ylim(1.42, 0.60)
    axes[1].set_title("Plan d'implantation industriel des cartouches poreuses\n(Module fractal Niveau 2, $30\\%$ d'inclusions absorbantes)", fontsize=11.5)
    axes[1].set_xlabel("Position latérale $x$ (m)", fontsize=11)
    axes[1].set_ylabel("Profondeur $y$ (m)", fontsize=11)
    axes[1].legend(fontsize=9.2, loc="lower right")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j4_1_industrialisation_binaire_et_hybride.jpg"), bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # ÉTAPE 2 : Robustesse vis-à-vis de la source (Onde plane vs Onde sphérique vs Onde oblique)
    # =========================================================================
    print("\n=== [Jour 4 - Étape 2] Analyse de robustesse selon la géométrie de l'onde incidente ===")
    k_rob_test = 2.0 * np.pi * 832.4 / c0  # 832.4 Hz (pic de résonance majeur routier/ferroviaire)
    alp_rob_test = compute_alpha.compute_alpha(k_rob_test, material_key="hemp_fiber", c0=c0)

    # 1. Onde plane normale : f_dir[0, :] = 1.0
    f_d_plane = np.zeros((M, N), dtype=np.complex128)
    f_d_plane[0, 0:N] = 1.0

    # 2. Onde sphérique / source ponctuelle localisée (cf. demo_control_polycopie2024.py l.251-253)
    f_d_sph = np.zeros((M, N), dtype=np.complex128)
    f_d_sph[0, N // 2] = 10.0

    # 3. Onde plane d'incidence oblique (theta = 35 deg)
    theta_inc = np.deg2rad(35.0)
    x_grid = np.arange(N) * spacestep
    f_d_obl = np.zeros((M, N), dtype=np.complex128)
    f_d_obl[0, 0:N] = np.exp(1j * k_rob_test * x_grid * np.sin(theta_inc))

    fig, axes = plt.subplots(2, 3, figsize=(16, 9.2), dpi=120)
    source_cases = [
        ("Onde Plane Normale ($\\theta=0^\\circ$)", f_d_plane),
        ("Onde Sphérique (Source ponctuelle)", f_d_sph),
        ("Onde Oblique ($\\theta=35^\\circ$)", f_d_obl)
    ]

    for col_idx, (src_title, f_dir_case) in enumerate(source_cases):
        solver2.update_rhs(f, f_dir_case, f_neu, f_rob)

        # Champ avec mur réfléchissant ou initial vs mur optimisé binaire
        u_init_case = solver2.solve(k_rob_test, preprocessing.set2zero(alp_rob_test * chi0_v, dom2))
        u_opt_case = solver2.solve(k_rob_test, preprocessing.set2zero(alp_rob_test * chi_bin, dom2))
        u_refl_case = solver2.solve(k_rob_test, zero_rob)

        J_refl_c = solver2.compute_energy(u_refl_case)
        J_init_c = solver2.compute_energy(u_init_case)
        J_opt_c = solver2.compute_energy(u_opt_case)
        att_db = 10.0 * np.log10(J_refl_c / J_opt_c)
        gain_vs_init = 100.0 * (J_init_c - J_opt_c) / J_init_c
        print(f"  * {src_title:36s} : J_refl={J_refl_c:.4f} | J_init={J_init_c:.4f} -> J_opt={J_opt_c:.4f} (-{gain_vs_init:.1f}% vs init, -{att_db:.2f} dB vs réfl.)")

        amp_init = np.abs(u_init_case)
        amp_init[mask_ext2] = np.nan
        amp_opt = np.abs(u_opt_case)
        amp_opt[mask_ext2] = np.nan
        vmax_c = max(np.nanpercentile(amp_init, 99), np.nanpercentile(amp_opt, 99))

        im_top = axes[0, col_idx].imshow(amp_init, cmap="magma", vmin=0, vmax=vmax_c, extent=[0, 1, 2, 0])
        axes[0, col_idx].set_ylim(1.4, 0.0)
        axes[0, col_idx].set_title(f"{src_title}\nParoi Initiale ($J_0 = {J_init_c:.2f}$)", fontsize=10.8)
        fig.colorbar(im_top, ax=axes[0, col_idx], fraction=0.046, pad=0.04)

        im_bot = axes[1, col_idx].imshow(amp_opt, cmap="magma", vmin=0, vmax=vmax_c, extent=[0, 1, 2, 0])
        axes[1, col_idx].set_ylim(1.4, 0.0)
        axes[1, col_idx].set_title(f"Avec Mur Optimisé Resonics ($V=30\\%$)\n$J_{{\\mathrm{{opt}}}} = {J_opt_c:.2f}$ ($-{gain_vs_init:.1f}\\%$ vs init)", fontsize=10.8)
        axes[1, col_idx].set_xlabel("$x$ (m)")
        fig.colorbar(im_bot, ax=axes[1, col_idx], fraction=0.046, pad=0.04)

    axes[0, 0].set_ylabel("Distribution Initiale\n$y$ (m)")
    axes[1, 0].set_ylabel("Mur Optimisé ($30\\%$)\n$y$ (m)")
    plt.suptitle("Jour 4 (1) : Robustesse de la paroi optimisée face à différents types d'ondes incidentes ($f = 832$ Hz)", fontsize=12.8)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j4_2_robustesse_sources_ondes.jpg"), bbox_inches="tight")
    plt.close(fig)

    # Remettre l'onde plane normale par défaut
    solver2.update_rhs(f, f_d_plane, f_neu, f_rob)

    # =========================================================================
    # ÉTAPE 3 : Benchmark Complet & Sélection Finale des Produits à Développer
    # =========================================================================
    print("\n=== [Jour 4 - Étape 3] Matrice de décision multi-critères et sélection des produits ===")
    mask_band_hw = (freqs >= 100.0) & (freqs <= 1600.0)
    mask_band_rw = (freqs >= 250.0) & (freqs <= 2000.0)

    # Évaluer les configurations candidates clés
    candidates = []

    for lvl in [0, 1, 2]:
        dom, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level=lvl)
        slv = fast_helmholtz.FastHelmholtzSolver(dom, spacestep, f, f_d_plane, f_neu, f_rob)
        chi_b = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), dom)
        mask_r = (dom == _env.NODE_ROBIN)

        # Énergie réfléchissante de référence pour ce niveau
        E_ref_lvl = np.array([slv.compute_energy(slv.solve(kw, zero_rob)) for kw in k_vals])

        for mat_key, mat_label, Alphas_mat in [
            ("hemp_fiber", "Fibre de Chanvre", Alphas_hemp),
            ("rock_wool", "Laine de Roche", Alphas_rock),
            ("melamine_foam", "Mousse Mélamine", Alphas_mela)
        ]:
            # Optimiser en multi-fréquence à V = 0.30
            t_Alphas = compute_alpha.compute_alpha(target_k, material_key=mat_key, c0=c0)
            chi_opt_c, _, _ = fast_helmholtz.optimize_multi_frequency(
                slv, target_k, t_Alphas, chi_b, weights=weights, V_obj=V_obj, mu_init=4.5, numb_iter=55
            )
            chi_opt_bin = fast_helmholtz.binarize_chi(chi_opt_c, dom, V_obj=V_obj)

            E_spec_bin = np.array([
                slv.compute_energy(slv.solve(kw, preprocessing.set2zero(Alphas_mat[i] * chi_opt_bin, dom)))
                for i, kw in enumerate(k_vals)
            ])

            # Mur 100% absorbant pour comparaison
            chi_100 = np.zeros((M, N), dtype=np.float64)
            chi_100[mask_r] = 1.0
            E_spec_100 = np.array([
                slv.compute_energy(slv.solve(kw, preprocessing.set2zero(Alphas_mat[i] * chi_100, dom)))
                for i, kw in enumerate(k_vals)
            ])

            J_hw = float(np.mean(E_spec_bin[mask_band_hw]))
            J_rw = float(np.mean(E_spec_bin[mask_band_rw]))
            J_max = float(np.max(E_spec_bin))
            J_100_mean = float(np.mean(E_spec_100))

            # Atténuation moyenne en dB par rapport au mur réfléchissant
            db_hw = float(10.0 * np.log10(np.mean(E_ref_lvl[mask_band_hw]) / J_hw))
            db_rw = float(10.0 * np.log10(np.mean(E_ref_lvl[mask_band_rw]) / J_rw))

            # Pourcentage de la performance d'un mur 100% absorbant atteint avec seulement 30% de matériau
            eff_vs_100 = float(100.0 * (np.mean(E_ref_lvl) - np.mean(E_spec_bin)) / (np.mean(E_ref_lvl) - J_100_mean))

            candidates.append({
                "level": lvl,
                "material_key": mat_key,
                "material": mat_label,
                "V_obj": V_obj,
                "J_hw": J_hw,
                "J_rw": J_rw,
                "J_max": J_max,
                "J_100": J_100_mean,
                "db_hw": db_hw,
                "db_rw": db_rw,
                "eff_vs_100": eff_vs_100
            })
            print(f"  [Candidat Level {lvl} | {mat_label:16s} | V=30%] "
                  f"J_Autoroute={J_hw:.3f} (-{db_hw:.1f} dB) | J_Rail={J_rw:.3f} (-{db_rw:.1f} dB) | "
                  f"J_max={J_max:.3f} | Efficacité vs 100% = {eff_vs_100:.1f}%")

    # Export CSV du tableau comparatif complet
    csv_path = os.path.join(OUTPUT_DIR, "tableau_synthese_produits.csv")
    with open(csv_path, "w", encoding="utf-8") as f_csv:
        f_csv.write("Level,Materiau,Volume_Poreux_Pct,J_moy_Autoroute,J_moy_Ferroviaire,J_max_Pic,Attenuation_Autoroute_dB,Attenuation_Ferroviaire_dB,Ratio_Performance_vs_100pct\n")
        for c in candidates:
            f_csv.write(f"{c['level']},{c['material']},{c['V_obj']*100:.0f},{c['J_hw']:.4f},{c['J_rw']:.4f},{c['J_max']:.4f},{c['db_hw']:.2f},{c['db_rw']:.2f},{c['eff_vs_100']:.1f}\n")

    # Figure 4.3 : Tableau de bord décisionnel des produits Resonics
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.8), dpi=120)

    labels_cand = [f"Niv.{c['level']} - {c['material'].split()[0]}" for c in candidates]
    x_pos = np.arange(len(candidates))
    width = 0.36

    j_hw_vals = [c["J_hw"] for c in candidates]
    j_rw_vals = [c["J_rw"] for c in candidates]
    j_100_vals = [c["J_100"] for c in candidates]

    axes[0].bar(x_pos - width / 2, j_hw_vals, width, color="tab:orange", label="Énergie moyenne Autoroute (100-1600 Hz)")
    axes[0].bar(x_pos + width / 2, j_rw_vals, width, color="tab:purple", label="Énergie moyenne Voie Ferrée (250-2000 Hz)")
    axes[0].plot(x_pos, j_100_vals, "g*--", ms=9, lw=1.5, label="Référence Mur 100% Absorbant ($\\chi=1$)")
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels(labels_cand, rotation=30, ha="right", fontsize=9.5)
    axes[0].set_ylabel("Énergie acoustique moyenne $\\overline{J}$ (plus bas = meilleur)", fontsize=10.5)
    axes[0].set_title("Performance acoustique comparée des 9 prototypes ($V = 30\\%$)", fontsize=11.5)
    axes[0].grid(True, axis="y", linestyle="--", alpha=0.6)
    axes[0].legend(fontsize=9)

    db_hw_vals = [c["db_hw"] for c in candidates]
    db_rw_vals = [c["db_rw"] for c in candidates]
    axes[1].bar(x_pos - width / 2, db_hw_vals, width, color="tab:blue", label="Atténuation Autoroute (dB vs mur béton)")
    axes[1].bar(x_pos + width / 2, db_rw_vals, width, color="tab:red", label="Atténuation Voie Ferrée (dB vs mur béton)")
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(labels_cand, rotation=30, ha="right", fontsize=9.5)
    axes[1].set_ylabel("Gain d'atténuation acoustique $\\Delta L_{\\mathrm{dB}}$ (dB)", fontsize=10.5)
    axes[1].set_title("Gain en décibels (dB) par rapport au tunnel béton non traité", fontsize=11.5)
    axes[1].grid(True, axis="y", linestyle="--", alpha=0.6)
    axes[1].legend(fontsize=9)

    plt.suptitle("Jour 4 (2) : Synthèse décisionnelle pour le choix de la gamme de produits Resonics", fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig_j4_3_tableau_de_bord_produits_resonics.jpg"), bbox_inches="tight")
    plt.close(fig)

    print("\n[Jour 4] Toutes les figures et le tableau CSV de décision ont été générés dans", OUTPUT_DIR)


if __name__ == "__main__":
    run_day4_studies()
