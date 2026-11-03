# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy
import numpy as np
import os
import csv
from pathlib import Path


# MRG packages
import _env
import preprocessing


def myimshow(tab, **kwargs):
    """Customized plot."""

    if 'dpi' in kwargs and kwargs['dpi']:
        dpi = kwargs['dpi']
    else:
        dpi = 100

    # -- create figure
    fig = matplotlib.pyplot.figure(dpi=dpi)
    ax = matplotlib.pyplot.axes()

    if 'title' in kwargs and kwargs['title']:
        title = kwargs['title']
    if 'cmap' in kwargs and kwargs['cmap']:
        cmap = kwargs['cmap']
    else:
        cmap = 'jet'
    #if 'clim' in kwargs and kwargs['clim']:
    #    clim = kwargs['clim']
    if 'vmin' in kwargs and kwargs['vmin']:
        vmin = kwargs['vmin']
    if 'vmax' in kwargs and kwargs['vmax']:
        vmax = kwargs['vmax']

    # -- plot curves
    if 'cmap' in kwargs and kwargs['cmap']:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    else:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    if 'title' in kwargs and kwargs['title']:
        matplotlib.pyplot.title(title)
    else:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    if 'colorbar' in kwargs and kwargs['colorbar']:
        matplotlib.pyplot.colorbar()

#    if 'clim' in kwargs and kwargs['clim']:
#        matplotlib.pyplot.clim(clim)
    if 'vmin' in kwargs and kwargs['vmin']:
        matplotlib.pyplot.clim(vmin, vmax)

    if 'filename' in kwargs and kwargs['filename']:
        output_file = kwargs['filename']
        if not os.path.isabs(output_file):
            output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        (root, ext) = os.path.splitext(output_file)
        matplotlib.pyplot.savefig(root + '_plot' + ext, format=ext[1:])
        matplotlib.pyplot.close()
    else:
        matplotlib.pyplot.show()
        matplotlib.pyplot.close()

    matplotlib.pyplot.close(fig)

    return


def _plot_uncontroled_solution(u, chi):
#def _plot_uncontroled_solution(x_plot, y_plot, x, y, u, chi):

    myimshow(numpy.real(u), title=r'$\operatorname{Re}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_re.jpg')
    myimshow(numpy.imag(u), title=r'$\operatorname{Im}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_im.jpg')
    myimshow(chi, title=r'$\chi_{0}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chi0_re.jpg')
    # k_begin = 0
    # k_end = len(x) - 1
    # for k in range(k_begin, k_end):
    #     x_plot[k] = k
    #     y_plot[k] = chi[int(y[k]), int(x[k])]
    # matplotlib.pyplot.plot(x_plot, y_plot)
    # matplotlib.pyplot.title('$\chi_{0}$ in $\Omega$')
    # matplotlib.pyplot.show()

    return


def _plot_controled_solution(u, chi):
#def _plot_controled_solution(x_plot, y_plot, x, y, u, chi):

    myimshow(numpy.real(u), title=r'$\operatorname{Re}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_re.jpg')
    myimshow(numpy.imag(u), title=r'$\operatorname{Im}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_im.jpg')
    myimshow(chi, title=r'$\chi_{n}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chin_re.jpg')
    # k_begin = 0
    # k_end = len(x) - 1
    # for k in range(k_begin, k_end):
    #     x_plot[k] = k
    #     y_plot[k] = chi[int(y[k]), int(x[k])]
    # matplotlib.pyplot.plot(x_plot, y_plot)
    # matplotlib.pyplot.title('$\chi_{n}$ in $\Omega$')
    # matplotlib.pyplot.show()

    return


def _plot_error(err):

    myimshow(numpy.real(err), title=r'$\operatorname{Re}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err_real.jpg')
    myimshow(numpy.imag(err), title=r'$\operatorname{Im}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err.jpg')

    return

def _plot_energy_history(energy):
    """On trace le coût pendant la descente puis après le passage en binaire."""
    values = numpy.asarray(energy).ravel()
    matplotlib.pyplot.plot(values[:-1], label="Descente continue")
    last = len(values) - 2
    matplotlib.pyplot.plot([last, last], [values[-2], values[-1]], ":", color="tab:orange")
    matplotlib.pyplot.scatter(last, values[-1], marker="s", color="tab:orange",
                              label="Répartition finale binaire", zorder=3)
    matplotlib.pyplot.title("Descente et répartition finale du matériau")
    matplotlib.pyplot.xlabel("Étape acceptée de la descente")
    matplotlib.pyplot.ylabel("Critère d'énergie")
    matplotlib.pyplot.legend()
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig_energy_real.jpg')
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()
    return


def plot_rer_b_frequency_sweep(results, source, output_dir=None):
    """On trace la source choisie et le coût du champ en fonction de la fréquence."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # On crée le dossier demandé avant d’enregistrer les figures.
    os.makedirs(output_dir, exist_ok=True)
    frequencies = results["frequencies_hz"]

    # On trace le spectre au-delà des fréquences simulées sans résoudre Helmholtz.
    spectrum_frequencies = numpy.linspace(0.0, 3500.0, 701)
    spectrum_amplitudes = numpy.array([
        source(0.0, 2.0 * numpy.pi * frequency) for frequency in spectrum_frequencies
    ])
    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(spectrum_frequencies, spectrum_amplitudes)
    ax.axvspan(frequencies[0], frequencies[-1], color="gray", alpha=0.15,
               label="Fréquences calculées")
    ax.set_xlim(0.0, 3500.0)
    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Amplitude relative")
    ax.set_title("Amplitude de la source choisie")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig_rer_b_spectre.png"), dpi=150)
    matplotlib.pyplot.close(fig)

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(frequencies, results["energies"], marker="o", markersize=3)
    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Énergie acoustique numérique")
    ax.set_title("Énergie du domaine selon la fréquence")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig_rer_b_energie.png"), dpi=150)
    matplotlib.pyplot.close(fig)
    return


def plot_porous_materials(results, output_dir=None):
    """On trace et on enregistre les coefficients des matériaux comparés."""
    output_dir = Path(__file__).resolve().parent / "resultats_jour1" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies = results["frequencies"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    columns, names = [frequencies], ["frequency_hz"]
    for name in results["material_names"]:
        alphas = results["alphas"][name]
        axes[0].plot(frequencies, alphas.real, label=name.replace("_", " ").title())
        axes[1].plot(frequencies, alphas.imag, label=name.replace("_", " ").title())
        columns.extend((alphas.real, alphas.imag))
        names.extend((name + "_alpha_real", name + "_alpha_imag"))
    for ax, title in zip(axes, ("Partie réelle du coefficient de Robin", "Partie imaginaire du coefficient de Robin")):
        ax.set(xlabel="Fréquence (Hz)", ylabel="Coefficient de Robin", title=title)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_j1_comparaison_materiaux.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir / "comparaison_materiaux.csv", np.column_stack(columns), delimiter=",", header=",".join(names), comments="")


def plot_sommerfeld_comparison(results, output_dir=None):
    """On trace les réponses des trois parois et les références continues."""
    output_dir = Path(__file__).resolve().parent / "resultats_jour1" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies, energies, theory = results["frequencies"], results["energies"], results["theory"]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for j, label in enumerate(("Paroi réfléchissante", "Sortie ouverte discrète", "Matériau sélectionné")):
        ax.semilogy(frequencies, energies[:, j], label=label)
    ax.semilogy(frequencies, theory[:, 0], "k--", label="Sortie ouverte continue")
    ax.semilogy(frequencies, theory[:, 1], color="gray", linestyle=":", label="Paroi réfléchissante continue")
    ax.set(xlabel="Fréquence (Hz)", ylabel="Coût du champ", title="Réponse du domaine rectangulaire selon sa paroi")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_j1_sommerfeld_vs_reflexif.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir / "comparaison_parois.csv", np.column_stack((frequencies, energies, theory)), delimiter=",", header="frequency_hz,J_reflecting,J_open,J_material,J_open_continuous,J_reflecting_continuous", comments="")


def plot_gradient_validation(results, output_dir=None):
    """On trace la comparaison des gradients et l'effet de la perturbation."""
    output_dir = Path(__file__).resolve().parent / "resultats_jour1" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(results["adjoint"], "o-", label="Adjoint")
    axes[0].plot(results["finite_difference"], "x--", label="Différences finies")
    axes[0].set(xlabel="Point du bord testé", ylabel="Dérivée du coût", title="Comparaison des dérivées")
    axes[0].legend()
    axes[1].loglog(results["steps"], np.maximum(results["errors"], 1e-16), "o-")
    axes[1].set(xlabel="Perturbation de la densité", ylabel="Erreur relative", title="Influence de la perturbation")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_j1_validation_gradient_adjoint.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir / "validation_gradient.csv", np.column_stack((results["chosen_nodes"], results["adjoint"], results["finite_difference"])), delimiter=",", header="row,col,adjoint_derivative,finite_difference_derivative", comments="")


def plot_day2_studies(study_results, output_dir=None):
    """On trace les quatre comparaisons du deuxième jour et on conserve leurs données."""
    if study_results is None:
        return None
    OUTPUT_DIR = str(Path(__file__).resolve().parent / "resultats_jour2" if output_dir is None else output_dir)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    freqs = study_results["frequencies"]
    full, initial = study_results["full"], study_results["initial"]
    results = study_results["optimizations"]
    levels, domains = study_results["levels"], study_results["domains"]
    maxima = study_results["maxima"]
    N = study_results["N"]
    M = 2 * N
    spacestep, V_obj = study_results["spacestep"], study_results["volume_fraction"]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(freqs, full[0], label="Mur plan entièrement garni")
    ax.plot(maxima[0][1], maxima[0][3], "ro", label="Maxima locaux échantillonnés")
    ax.set(xlabel="Fréquence (Hz)", ylabel="Coût acoustique", title="Spectre du mur plan")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_1_mur_plan_absorbant_maxima.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for level in levels:
        axes[0].plot(freqs, full[level], label=f"Niveau {level}")
        axes[1].semilogy(freqs, full[level], label=f"Niveau {level}")
        for ax in axes:
            ax.plot(maxima[level][1], maxima[level][3], ".")
    for ax in axes:
        ax.set(xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend()
    axes[0].set_title("Échelle linéaire")
    axes[1].set_title("Échelle logarithmique")
    fig.suptitle("Spectres des différentes formes de murs entièrement garnis")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_2_comparaison_formes_fractales.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, level in zip(axes, (0, 1, 2)):
        ax.semilogy(freqs, initial[level], "--", label=f"Densité initiale, {V_obj:.0%}")
        ax.semilogy(freqs, full[level], label="Mur entièrement garni")
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_3_initial_partiel_vs_total.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for level in (0, 1, 2):
        ax = axes[0, level]
        for result in results[level]:
            line, = ax.plot(result["ene_hist"], label=f'{result["f_target"]:.0f} Hz, continu')
            ax.plot(len(result["ene_hist"]) - 1, result["J_opt"], "x", color=line.get_color(),
                    label=f'{result["f_target"]:.0f} Hz, binaire')
        ax.set(title=f"Niveau {level}", xlabel="Itération acceptée", ylabel="Coût acoustique")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    # On compare les deux champs avec la même échelle de couleurs.
    result, domain = results[2][0], domains[2]
    extent = [-spacestep / 2, (N - .5) * spacestep, (M - .5) * spacestep, -spacestep / 2]
    vmax = max(np.max(np.abs(result["u0"])), np.max(np.abs(result["u_opt"])))
    ymax = (np.max(np.where(domain == _env.NODE_ROBIN)[0]) + 2) * spacestep
    for ax, field, title in zip(axes[1, :2], (result["u0"], result["u_opt"]), ("Champ initial", "Champ après placement binaire")):
        image = ax.imshow(np.ma.masked_where(domain != _env.NODE_INTERIOR, np.abs(field)),
                          extent=extent, origin="upper", vmin=0, vmax=vmax, cmap="magma")
        ax.set(title=title, xlabel="Position horizontale (m)", ylabel="Distance à la source (m)", ylim=(ymax, 0))
        fig.colorbar(image, ax=ax, label="Module du champ")
    rows, cols = np.where(domain == _env.NODE_ROBIN)
    scatter = axes[1, 2].scatter(cols * spacestep, rows * spacestep,
                                 c=result["chi_opt"][rows, cols], cmap="viridis", vmin=0, vmax=1, s=12)
    axes[1, 2].set(title=f'Placement, niveau 2, {result["f_target"]:.0f} Hz',
                   xlabel="Position horizontale (m)", ylabel="Distance à la source (m)")
    axes[1, 2].invert_yaxis()
    axes[1, 2].set_aspect("equal")
    fig.colorbar(scatter, ax=axes[1, 2], label="Point garni ou nu")
    fig.suptitle("Optimisations à une fréquence et coût après passage au placement binaire")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j2_4_optimisation_mono_frequence.jpg"), dpi=160)
    plt.close(fig)

    np.savez(os.path.join(OUTPUT_DIR, "data_jour2.npz"), **study_results["data"])
    return OUTPUT_DIR


def plot_day3_studies(study_results, output_dir=None):
    """On trace les trois comparaisons du troisième jour et on conserve leurs données."""
    if study_results is None:
        return None
    OUTPUT_DIR = str(Path(__file__).resolve().parent / "resultats_jour3" if output_dir is None else output_dir)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    freqs, studies = study_results["frequencies"], study_results["studies"]
    V_obj = study_results["data"]["volume_fraction"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
    for ax, level in zip(axes, (0, 1, 2)):
        study = studies[level]
        ax.semilogy(freqs, study["initial"], "--", label=f"Densité initiale, {V_obj:.0%}")
        ax.semilogy(freqs, study["full"], color="black", label="Mur entièrement garni")
        for index, spectrum in zip(study["mono_targets"], study["mono_spectra"]):
            line, = ax.semilogy(freqs, spectrum, label=f"Placement à {freqs[index]:.0f} Hz")
            ax.plot(freqs[index], spectrum[index], "o", color=line.get_color())
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
    fig.suptitle("Spectres des placements binaires optimisés à une seule fréquence")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_1_analyse_resultats_jour2_spectre.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for level in (0, 1, 2):
        study = studies[level]
        ax = axes[0, level]
        for column, index in enumerate(study["multi_targets"]):
            ax.plot(study["multi_history_frequencies"][:, column], alpha=.65,
                    label=f"{freqs[index]:.0f} Hz")
        ax.plot(study["multi_history"], "k--", label="Moyenne continue")
        ax.plot(len(study["multi_history"]) - 1,
                np.mean(study["multi_spectrum"][study["multi_targets"]]), "kx", label="Placement binaire")
        ax.set(title=f"Niveau {level}", xlabel="Itération acceptée", ylabel="Coût acoustique")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
        ax = axes[1, level]
        ax.semilogy(freqs, study["initial"], "--", label="Densité initiale")
        for index, spectrum in zip(study["mono_targets"], study["mono_spectra"]):
            ax.semilogy(freqs, spectrum, alpha=.65, label=f"Une fréquence, {freqs[index]:.0f} Hz")
        ax.semilogy(freqs, study["multi_spectrum"], lw=2, label="Plusieurs fréquences")
        ax.semilogy(freqs, study["full"], color="black", label="Mur entièrement garni")
        ax.set(xlabel="Fréquence (Hz)", ylabel="Coût acoustique")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
    fig.suptitle("Optimisation commune à plusieurs fréquences et spectres des placements binaires")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_2_optimisation_multifrequence.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for level in (0, 1, 2):
        study = studies[level]
        percentages = 100 * study["actual_volumes"]
        for ax, costs, full_cost, title in (
            (axes[0, level], study["volume_mono_costs"], study["full"][study["volume_mono_index"]],
             f'Une fréquence, {freqs[study["volume_mono_index"]]:.0f} Hz'),
            (axes[1, level], study["volume_multi_costs"], np.mean(study["full"][study["multi_targets"]]),
             "Plusieurs fréquences"),
        ):
            ax.plot(percentages, costs, "o-", label="Placements binaires")
            ax.axhline(full_cost, color="black", ls="--", label="Mur entièrement garni")
            best = np.argmin(costs)
            ax.plot(percentages[best], costs[best], "r*", ms=10, label="Minimum testé")
            ax.set(xlabel="Part du mur garnie (%)", ylabel="Coût acoustique")
            ax.set_title(f"Niveau {level} — {title}", fontsize=10)
            ax.grid(alpha=.3)
            ax.legend(fontsize=7)
    fig.suptitle("Coûts des placements binaires en fonction de la quantité de matériau")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_3_etude_quantite_optimale_poreux.jpg"), dpi=160)
    plt.close(fig)

    np.savez(os.path.join(OUTPUT_DIR, "data_jour3.npz"), **study_results["data"])
    return OUTPUT_DIR


def plot_day4_studies(results, output_dir=None):
    """On présente les répartitions, les profils incidents et les candidats comparés."""
    output_dir = Path(__file__).resolve().parent / "resultats_jour4" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies, domain = results["frequencies"], results["domain"]
    N, h = results["N"], results["spacestep"]
    M = 2 * N
    binary = results["binary"]
    robin = domain == _env.NODE_ROBIN
    rows, cols = np.where(robin)
    deep = rows >= N

    # On présente les coûts avant et après le passage à une répartition binaire.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7))
    for key, label in (
        ("initial_costs", "Répartition initiale"),
        ("continuous_costs", "Répartition continue optimisée"),
        ("binary_costs", "Répartition binaire"),
        ("mixed_costs", "Répartition binaire mixte testée"),
        ("full_costs", "Paroi entièrement garnie"),
    ):
        axes[0].semilogy(frequencies, results[key], label=label)
    axes[0].set(xlabel="Fréquence (Hz)", ylabel="Coût du champ", title="Coûts des répartitions de matériau")
    axes[0].grid(alpha=0.3)
    axes[0].legend(fontsize=7)
    selected = binary[robin] > 0.5
    axes[1].scatter(cols[~selected] * h, rows[~selected] * h, c="gray", marker="s", s=9, label="Paroi non garnie")
    axes[1].scatter(cols[selected & ~deep] * h, rows[selected & ~deep] * h, c="tab:blue", s=11, label="Matériau sélectionné")
    axes[1].scatter(cols[selected & deep] * h, rows[selected & deep] * h, c="tab:orange", s=11, label=results["alternative_material"].replace("_", " ").title())
    axes[1].set(xlabel="Position horizontale (m)", ylabel="Profondeur (m)", title="Répartition mixte testée")
    axes[1].invert_yaxis()
    axes[1].set_aspect("equal")
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_j4_1_industrialisation_binaire_et_hybride.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir / "comparaison_repartitions.csv", np.column_stack((frequencies, results["initial_costs"], results["continuous_costs"], results["binary_costs"], results["mixed_costs"], results["full_costs"])), delimiter=",", header="frequency_hz,J_initial,J_continuous,J_binary,J_mixed,J_full", comments="")

    # On utilise la même échelle de couleurs pour les deux champs d'un profil donné.
    fig, axes = plt.subplots(2, 3, figsize=(11, 7.5))
    exterior = domain == _env.NODE_COMPLEMENTARY
    for col, profile in enumerate(results["profile_fields"]):
        first_map = np.where(exterior, np.nan, np.abs(profile["initial"]))
        second_map = np.where(exterior, np.nan, np.abs(profile["binary"]))
        maximum = max(np.nanmax(first_map), np.nanmax(second_map), 1e-14)
        fields = ((first_map, profile["initial_cost"], "Initiale"), (second_map, profile["binary_cost"], "Binaire"))
        for row, (values, cost, title) in enumerate(fields):
            image = axes[row, col].imshow(values, vmin=0.0, vmax=maximum, cmap="magma", extent=(0, N * h, M * h, 0))
            axes[row, col].set(title=f"{profile['name']}\n{title}, coût = {cost:.4g}", xlabel="Position horizontale (m)")
            axes[row, col].set_ylim(1.4, 0.0)
            fig.colorbar(image, ax=axes[row, col], fraction=0.046)
    axes[0, 0].set_ylabel("Profondeur (m)")
    axes[1, 0].set_ylabel("Profondeur (m)")
    fig.suptitle(f"Réponses à différents profils incidents à {results['profile_frequency']:g} Hz")
    fig.tight_layout()
    fig.savefig(output_dir / "fig_j4_2_robustesse_sources_ondes.jpg", dpi=160)
    plt.close(fig)
    with (output_dir / "robustesse_sources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("profile", "J_initial", "J_binary"))
        writer.writerows(results["source_costs"])

    # On indique aussi la quantité discrète de matériau employée par chaque candidat.
    candidates = results["candidates"]
    with (output_dir / "tableau_synthese_produits.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(candidates[0]))
        writer.writeheader()
        writer.writerows(candidates)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.9))
    labels = [f"Niveau {candidate['level']}\n{candidate['material'].replace('_', ' ').title()}" for candidate in candidates]
    positions = np.arange(len(candidates))
    axes[0].bar(positions, [item["J_band_mean"] for item in candidates], label="Répartition binaire")
    axes[0].plot(positions, [item["J_full_band_mean"] for item in candidates], "o--", label="Paroi entièrement garnie")
    axes[0].set(ylabel="Coût moyen sur la bande", title="Comparaison des configurations pour le RER B")
    axes[0].legend(fontsize=8)
    axes[1].bar(positions, [item["covered_nodes"] for item in candidates], color="tab:orange")
    axes[1].set(ylabel="Nombre de points garnis", title="Quantité discrète de matériau utilisée")
    for ax in axes:
        ax.set_xticks(positions, labels, rotation=50, ha="right", fontsize=7)
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_j4_3_tableau_de_bord_produits_resonics.jpg", dpi=160)
    plt.close(fig)
    np.savez(output_dir / "data_jour4.npz", frequencies=frequencies, domain=domain,
             chi_initial=results["initial"], chi_continuous=results["continuous"], chi_binary=binary,
             initial_costs=results["initial_costs"], continuous_costs=results["continuous_costs"],
             binary_costs=results["binary_costs"], mixed_costs=results["mixed_costs"], full_costs=results["full_costs"],
             target_indices=results["target_indices"], history=results["history"], N=N,
             source_name=results["source_name"], material_parameters=results["material_parameters"],
             sound_speed_m_s=results["sound_speed_m_s"], iterations_requested=results["iterations_requested"],
             volume_fraction=results["volume_fraction"])
