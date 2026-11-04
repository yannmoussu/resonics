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
import processing


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
    """On trace l’énergie J pendant la descente puis après le passage en binaire."""
    values = numpy.asarray(energy).ravel()
    matplotlib.pyplot.plot(values[:-1], label="Descente continue")
    last = len(values) - 2
    matplotlib.pyplot.plot([last, last], [values[-2], values[-1]], ":", color="tab:orange")
    matplotlib.pyplot.scatter(last, values[-1], marker="s", color="tab:orange",
                              label="Répartition finale binaire", zorder=3)
    matplotlib.pyplot.title("Descente et répartition finale du matériau")
    matplotlib.pyplot.xlabel("Étape acceptée de la descente")
    matplotlib.pyplot.ylabel("Énergie J")
    matplotlib.pyplot.legend()
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig_energy_real.jpg')
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()
    return


def plot_rer_b_frequency_sweep(results, source, output_dir=None):
    """On trace la source choisie et l’énergie J en fonction de la fréquence."""
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
    fig, ax = matplotlib.pyplot.subplots(figsize=(10.8, 3.6))
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

    fig, ax = matplotlib.pyplot.subplots(figsize=(10.8, 3.6))
    ax.plot(frequencies, results["energies"], marker="o", markersize=3)
    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Énergie J")
    ax.set_title("Énergie J en fonction de la fréquence")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig_rer_b_energie.png"), dpi=150)
    matplotlib.pyplot.close(fig)
    return


def plot_porous_materials(results, output_dir=None):
    """On montre les parties réelle et imaginaire du coefficient pour chaque matériau séparément."""
    output_dir = Path(__file__).resolve().parent / "resultats_materiaux_validation" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies = results["frequencies"]
    names = results["material_names"]
    labels = {"MELAMINE": "Mélamine", "LAINE_VERRE": "Laine de verre", "OUATE_POLYESTER": "Ouate polyester"}
    fig, axes = plt.subplots(1, len(names), figsize=(10.5, 3.8), sharey=True, constrained_layout=True)
    columns, headers = [frequencies], ["frequency_hz"]
    for ax, name in zip(np.atleast_1d(axes), names):
        alphas = results["alphas"][name]
        ax.plot(frequencies, alphas.real, color="#0072B2", lw=1.8, label="Partie réelle")
        ax.plot(frequencies, alphas.imag, color="#D55E00", ls="--", lw=1.8, label="Partie imaginaire")
        ax.axhline(0, color="gray", lw=.7)
        ax.set(title=labels.get(name, name.replace("_", " ").title()), xlabel="Fréquence (Hz)", ylabel="Coefficient de Robin")
        ax.tick_params(labelsize=11)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        ax.grid(alpha=.25)
        ax.legend(fontsize=11)
        columns.extend((alphas.real, alphas.imag))
        headers.extend((name + "_alpha_real", name + "_alpha_imag"))
    fig.savefig(output_dir / "fig_comparaison_materiaux.jpg", dpi=180)
    plt.close(fig)
    np.savetxt(output_dir / "comparaison_materiaux.csv", np.column_stack(columns), delimiter=",", header=",".join(headers), comments="")



def plot_sommerfeld_comparison(results, output_dir=None):
    """On trace les réponses des trois parois et les références continues."""
    output_dir = Path(__file__).resolve().parent / "resultats_materiaux_validation" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies, energies, theory = results["frequencies"], results["energies"], results["theory"]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for j, label in enumerate(("Paroi réfléchissante", "Sortie ouverte discrète", "Matériau de référence")):
        ax.semilogy(frequencies, energies[:, j], label=label)
    ax.semilogy(frequencies, theory[:, 0], "k--", label="Sortie ouverte continue")
    ax.semilogy(frequencies, theory[:, 1], color="gray", linestyle=":", label="Paroi réfléchissante continue")
    ax.set(xlabel="Fréquence (Hz)", ylabel="Énergie J", title="Réponse du domaine rectangulaire selon sa paroi")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_sommerfeld_vs_reflexif.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir / "comparaison_parois.csv", np.column_stack((frequencies, energies, theory)), delimiter=",", header="frequency_hz,J_reflecting,J_open,J_material,J_open_continuous,J_reflecting_continuous", comments="")


def plot_boundary_depth_dependence(results, output_dir=None):
    """On montre la dépendance de l’énergie J à la profondeur pour une aire fixée."""
    output_dir = Path(__file__).resolve().parent/"resultats_materiaux_validation" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.2), constrained_layout=True)
    ax.semilogy(results["depths"], results["open"], label="Sortie ouverte", linewidth=2)
    ax.semilogy(results["depths"], results["reflecting"], label="Paroi réfléchissante", linewidth=2)
    ax.set(xlabel="Profondeur du rectangle (m)", ylabel="Énergie J du modèle continu", title=f"Variation de la forme à aire unitaire, {results['frequency_hz']:g} Hz")
    ax.tick_params(labelsize=11)
    ax.grid(alpha=.3, which="both")
    ax.legend(fontsize=12)
    fig.savefig(output_dir/"fig_cout_profondeur_rectangle.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir/"cout_profondeur_rectangle.csv", np.column_stack([results["depths"], results["widths"], results["open"], results["reflecting"]]), delimiter=",", header="depth_m,width_m,J_open,J_reflecting", comments="")


def plot_gradient_validation(results, output_dir=None):
    """On trace la comparaison des gradients et l'effet de la perturbation."""
    output_dir = Path(__file__).resolve().parent / "resultats_materiaux_validation" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(results["adjoint"], "o-", label="Adjoint")
    axes[0].plot(results["finite_difference"], "x--", label="Différences finies")
    axes[0].set(xlabel="Point du bord testé", ylabel="Dérivée de l’énergie J", title="Comparaison des dérivées")
    axes[0].legend()
    axes[1].loglog(results["steps"], np.maximum(results["errors"], 1e-16), "o-")
    axes[1].set(xlabel="Perturbation de la densité", ylabel="Erreur relative", title="Influence de la perturbation")
    for ax in axes:
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_validation_gradient_adjoint.jpg", dpi=160)
    plt.close(fig)
    np.savetxt(output_dir / "validation_gradient.csv", np.column_stack((results["chosen_nodes"], results["adjoint"], results["finite_difference"])), delimiter=",", header="row,col,adjoint_derivative,finite_difference_derivative", comments="")


def plot_spectra_and_single_frequency_placement(study_results, output_dir=None):
    """On trace les spectres et les placements à une fréquence puis on conserve leurs données."""
    if study_results is None:
        return None
    OUTPUT_DIR = str(Path(__file__).resolve().parent / "resultats_monofrequence" if output_dir is None else output_dir)
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
    ax.set(xlabel="Fréquence (Hz)", ylabel="Énergie J", title="Spectre du mur plan")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_mur_plan_absorbant_maxima.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for level in levels:
        axes[0].plot(freqs, full[level], label=f"Niveau {level}")
        axes[1].semilogy(freqs, full[level], label=f"Niveau {level}")
        for ax in axes:
            ax.plot(maxima[level][1], maxima[level][3], ".")
    for ax in axes:
        ax.set(xlabel="Fréquence (Hz)", ylabel="Énergie J")
        ax.grid(alpha=0.3, which="both")
        ax.legend()
    axes[0].set_title("Échelle linéaire")
    axes[1].set_title("Échelle logarithmique")
    fig.suptitle("Spectres des différentes formes de murs entièrement garnis")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_comparaison_formes_fractales.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, level in zip(axes, (0, 1, 2)):
        ax.semilogy(freqs, initial[level], "--", label=f"Densité initiale, {V_obj:.0%}")
        ax.semilogy(freqs, full[level], label="Mur entièrement garni")
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Énergie J")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_repartition_partielle_et_complete.jpg"), dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for level in (0, 1, 2):
        ax = axes[0, level]
        for result in results[level]:
            line, = ax.plot(result["ene_hist"], label=f'{result["f_target"]:.0f} Hz, continu')
            ax.plot(len(result["ene_hist"]) - 1, result["J_opt"], "x", color=line.get_color(),
                    label=f'{result["f_target"]:.0f} Hz, binaire')
        ax.set(title=f"Niveau {level}", xlabel="Itération acceptée", ylabel="Énergie J")
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
    fig.suptitle("Optimisations à une fréquence et énergie J après passage au placement binaire")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_optimisation_monofrequence.jpg"), dpi=160)
    plt.close(fig)

    np.savez(os.path.join(OUTPUT_DIR, "data_monofrequence.npz"), **study_results["data"])
    plot_single_frequency_details(study_results, OUTPUT_DIR)
    plot_wall_geometries(study_results)
    return OUTPUT_DIR


def plot_multifrequency_placement_and_coverage(study_results, output_dir=None):
    """On trace les placements multifréquences et l’effet de la quantité de matériau."""
    if study_results is None:
        return None
    OUTPUT_DIR = str(Path(__file__).resolve().parent / "resultats_multifrequence" if output_dir is None else output_dir)
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
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Énergie J")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
    fig.suptitle("Spectres des placements binaires optimisés à une seule fréquence")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_spectres_placements_monofrequence.jpg"), dpi=160)
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
        ax.set(title=f"Niveau {level}", xlabel="Itération acceptée", ylabel="Énergie J")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
        ax = axes[1, level]
        ax.semilogy(freqs, study["initial"], "--", label="Densité initiale")
        for index, spectrum in zip(study["mono_targets"], study["mono_spectra"]):
            ax.semilogy(freqs, spectrum, alpha=.65, label=f"Une fréquence, {freqs[index]:.0f} Hz")
        ax.semilogy(freqs, study["multi_spectrum"], lw=2, label="Plusieurs fréquences")
        ax.semilogy(freqs, study["full"], color="black", label="Mur entièrement garni")
        ax.set(xlabel="Fréquence (Hz)", ylabel="Énergie J")
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=7)
    fig.suptitle("Optimisation commune à plusieurs fréquences et spectres des placements binaires")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_optimisation_multifrequence.jpg"), dpi=160)
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
            ax.set(xlabel="Part du mur garnie (%)", ylabel="Énergie J")
            ax.set_title(f"Niveau {level} — {title}", fontsize=10)
            ax.grid(alpha=.3)
            ax.legend(fontsize=7)
    fig.suptitle("Énergies J des placements binaires en fonction de la quantité de matériau")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_cout_quantite_absorbant.jpg"), dpi=160)
    plt.close(fig)

    np.savez(os.path.join(OUTPUT_DIR, "data_multifrequence.npz"), **study_results["data"])
    plot_multifrequency_details(study_results, OUTPUT_DIR)
    plot_coverage_details(study_results, OUTPUT_DIR)
    return OUTPUT_DIR


def plot_absorber_configuration_comparison(results, output_dir=None):
    """On présente les répartitions, les profils incidents et les candidats comparés."""
    output_dir = Path(__file__).resolve().parent / "resultats_comparaison_dispositifs" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies, domain = results["frequencies"], results["domain"]
    N, h = results["N"], results["spacestep"]
    M = 2 * N
    binary = results["binary"]
    robin = domain == _env.NODE_ROBIN
    rows, cols = np.where(robin)
    deep = rows >= N

    # On présente les énergies J avant et après le passage à une répartition binaire.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7))
    for key, label in (
        ("initial_costs", "Répartition initiale"),
        ("continuous_costs", "Répartition continue optimisée"),
        ("binary_costs", "Répartition binaire"),
        ("mixed_costs", "Répartition binaire mixte testée"),
        ("full_costs", "Paroi entièrement garnie"),
    ):
        axes[0].semilogy(frequencies, results[key], label=label)
    axes[0].set(xlabel="Fréquence (Hz)", ylabel="Énergie J", title="Énergie J selon la répartition de matériau")
    axes[0].grid(alpha=0.3)
    axes[0].legend(fontsize=7)
    selected = binary[robin] > 0.5
    axes[1].scatter(cols[~selected] * h, rows[~selected] * h, c="gray", marker="s", s=9, label="Paroi non garnie")
    axes[1].scatter(cols[selected & ~deep] * h, rows[selected & ~deep] * h, c="tab:blue", s=11, label="Matériau de référence")
    axes[1].scatter(cols[selected & deep] * h, rows[selected & deep] * h, c="tab:orange", s=11, label=results["alternative_material"].replace("_", " ").title())
    axes[1].set(xlabel="Position horizontale (m)", ylabel="Profondeur (m)", title="Répartition mixte testée")
    axes[1].invert_yaxis()
    axes[1].set_aspect("equal")
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_repartitions_binaire_et_mixte.jpg", dpi=160)
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
            axes[row, col].set(title=f"{profile['name']}\n{title}, Énergie J = {cost:.4g}", xlabel="Position horizontale (m)")
            axes[row, col].set_ylim(1.4, 0.0)
            fig.colorbar(image, ax=axes[row, col], fraction=0.046)
    axes[0, 0].set_ylabel("Profondeur (m)")
    axes[1, 0].set_ylabel("Profondeur (m)")
    fig.suptitle(f"Réponses à différents profils incidents à {results['profile_frequency']:g} Hz")
    fig.tight_layout()
    fig.savefig(output_dir / "fig_comparaison_profils_sources.jpg", dpi=160)
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
    axes[0].set(ylabel="Énergie J moyenne sur la bande", title="Comparaison des configurations pour le RER B")
    axes[0].legend(fontsize=8)
    axes[1].bar(positions, [item["covered_nodes"] for item in candidates], color="tab:orange")
    axes[1].set(ylabel="Nombre de points garnis", title="Quantité discrète de matériau utilisée")
    for ax in axes:
        ax.set_xticks(positions, labels, rotation=50, ha="right", fontsize=7)
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_comparaison_dispositifs_resonics.jpg", dpi=160)
    plt.close(fig)
    plot_source_profile_costs(results, output_dir)
    np.savez(output_dir / "data_comparaison_dispositifs.npz", frequencies=frequencies, domain=domain,
             chi_initial=results["initial"], chi_continuous=results["continuous"], chi_binary=binary,
             initial_costs=results["initial_costs"], continuous_costs=results["continuous_costs"],
             binary_costs=results["binary_costs"], mixed_costs=results["mixed_costs"], full_costs=results["full_costs"],
             target_indices=results["target_indices"], history=results["history"], N=N,
             source_name=results["source_name"], material_parameters=results["material_parameters"],
             sound_speed_m_s=results["sound_speed_m_s"], iterations_requested=results["iterations_requested"],
             volume_fraction=results["volume_fraction"])


def plot_single_frequency_details(study_results, output_dir=None):
    """On présente les historiques, les champs et le placement à une fréquence."""
    if study_results is None:
        return None
    output_dir = Path(__file__).resolve().parent / "resultats_monofrequence" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    optimizations = study_results["optimizations"]

    # On distingue les énergies J continues et les énergies J mesurées après le tri binaire.
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.5), constrained_layout=True)
    for ax, level in zip(axes, (0, 1, 2)):
        for result in optimizations[level]:
            history = np.asarray(result["ene_hist"]).ravel()
            iterations = np.arange(len(history))
            frequency = result["f_target"]
            line, = ax.plot(iterations, history, linewidth=2,
                            label=f"Continu, {frequency:g} Hz")
            ax.plot(iterations[-1], result["J_opt"], "x", markersize=9,
                    markeredgewidth=2, color=line.get_color(),
                    label=f"Binaire, {frequency:g} Hz")
        ax.set_title(f"Niveau {level}", fontsize=13)
        ax.set_xlabel("Itération acceptée", fontsize=12)
        ax.set_ylabel("Énergie J", fontsize=12)
        ax.tick_params(labelsize=11)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=11)
    fig.savefig(output_dir / "fig_historiques_monofrequence.jpg", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # On utilise la même échelle de couleurs pour les deux champs.
    result = optimizations[2][0]
    domain = study_results["domains"][2]
    M, N = domain.shape
    h = study_results["spacestep"]
    interior = domain == _env.NODE_INTERIOR
    extent = (-h / 2, (N - 0.5) * h, (M - 0.5) * h, -h / 2)
    ymax = (np.max(np.where(domain == _env.NODE_ROBIN)[0]) + 2) * h
    maximum = max(np.max(np.abs(result["u0"][interior])),
                  np.max(np.abs(result["u_opt"][interior])), 1e-14)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.5), constrained_layout=True)
    for ax, field, title in zip(axes[:2], (result["u0"], result["u_opt"]),
                                ("Champ initial", "Champ après tri binaire")):
        values = np.ma.masked_where(~interior, np.abs(field))
        image = ax.imshow(values, extent=extent, origin="upper", cmap="magma",
                          vmin=0, vmax=maximum, interpolation="nearest")
        ax.set_title(title, fontsize=13)
        colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.025)
        colorbar.set_label("Module du champ", fontsize=11)
        colorbar.ax.tick_params(labelsize=11)

    # On repère les points garnis sur le contour du domaine.
    axes[2].imshow(np.ma.masked_where(~interior, np.full(domain.shape, 0.93)),
                   extent=extent, origin="upper", cmap="gray", vmin=0, vmax=1,
                   interpolation="nearest")
    rows, cols = np.where(domain == _env.NODE_ROBIN)
    scatter = axes[2].scatter(cols * h, rows * h, c=result["chi_opt"][rows, cols],
                              cmap="viridis", vmin=0, vmax=1, s=15)
    axes[2].set_title("Placement binaire", fontsize=13)
    colorbar = fig.colorbar(scatter, ax=axes[2], fraction=0.046, pad=0.025, ticks=[0, 1])
    colorbar.ax.set_yticklabels(["Nu", "Garni"], fontsize=11)
    for ax in axes:
        ax.set_xlabel("Position horizontale (m)", fontsize=12)
        ax.set_ylabel("Distance à la source (m)", fontsize=12)
        ax.set_xlim(-h / 2, (N - 0.5) * h)
        ax.set_ylim(ymax, 0)
        ax.tick_params(labelsize=11)
        ax.set_aspect("equal")
    fig.suptitle(f"Champs et placement à {result['f_target']:g} Hz — niveau 2", fontsize=14)
    fig.savefig(output_dir / "fig_champs_placement_monofrequence.jpg", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(output_dir)


def plot_multifrequency_details(study_results, output_dir=None):
    """On présente la descente multifréquence et le spectre du placement obtenu."""
    if study_results is None:
        return None
    output_dir = Path(__file__).resolve().parent / "resultats_multifrequence" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies = np.asarray(study_results["frequencies"])
    study = study_results["studies"][2]
    targets = np.asarray(study["multi_targets"], dtype=int)
    history = np.asarray(study["multi_history"]).ravel()
    iterations = np.arange(len(history))

    # On montre les énergies J individuels et la moyenne utilisée pendant la descente.
    fig, ax = plt.subplots(figsize=(8.5, 4.5), constrained_layout=True)
    for column, index in enumerate(targets):
        ax.plot(iterations, study["multi_history_frequencies"][:, column],
                linewidth=1.9, alpha=0.85, label=f"{frequencies[index]:g} Hz")
    ax.plot(iterations, history, "k--", linewidth=2.5, label="Moyenne continue")
    ax.plot(iterations[-1], np.mean(study["multi_spectrum"][targets]), "kx",
            markersize=10, markeredgewidth=2, label="Moyenne après tri binaire")
    ax.set_title("Historique multifréquence — niveau 2", fontsize=14)
    ax.set_xlabel("Itération acceptée", fontsize=12)
    ax.set_ylabel("Énergie J", fontsize=12)
    ax.tick_params(labelsize=11)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=11)
    fig.savefig(output_dir / "fig_historique_multifrequence.jpg", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # On évalue les différents placements sur la même bande de fréquences.
    fig, ax = plt.subplots(figsize=(8.5, 4.5), constrained_layout=True)
    ax.semilogy(frequencies, study["initial"], "--", color="gray", linewidth=1.8,
                label="Répartition initiale")
    for index, spectrum in zip(study["mono_targets"], study["mono_spectra"]):
        ax.semilogy(frequencies, spectrum, linewidth=1.8,
                    label=f"Placement à {frequencies[index]:g} Hz")
    ax.semilogy(frequencies, study["multi_spectrum"], linewidth=2.5,
                label="Placement multifréquence")
    ax.semilogy(frequencies, study["full"], color="black", linewidth=1.8,
                label="Mur entièrement garni")
    ax.set_title("Spectres des placements — niveau 2", fontsize=14)
    ax.set_xlabel("Fréquence (Hz)", fontsize=12)
    ax.set_ylabel("Énergie J", fontsize=12)
    ax.tick_params(labelsize=11)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=11, loc="lower left")
    fig.savefig(output_dir / "fig_spectre_multifrequence.jpg", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(output_dir)



def plot_wall_geometries(study_results, output_dir=None):
    """On représente les domaines d'air et leurs frontières sur la même échelle."""
    output_dir = Path(__file__).resolve().parent if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    levels = study_results["levels"]
    h = study_results["spacestep"]
    fig, axes = plt.subplots(1, len(levels), figsize=(12, 4.8), sharex=True, sharey=True, squeeze=False)
    for ax, level in zip(axes.ravel(), levels):
        domain = study_results["domains"][level]
        M, N = domain.shape
        air = np.ma.masked_where(domain != _env.NODE_INTERIOR, np.ones(domain.shape))
        ax.imshow(air, extent=(-h/2, (N-.5)*h, (M-.5)*h, -h/2), cmap="Blues", vmin=0, vmax=3, interpolation="nearest")
        rows, cols = np.where(domain == _env.NODE_ROBIN)
        ax.scatter(cols*h, rows*h, color="tab:red", s=2, label="Paroi de Robin")
        ax.plot([0, N*h], [0, 0], color="tab:blue", lw=2, label="Source imposée")
        ax.set(title=f"Niveau {level}", xlabel="Position horizontale (m)", xlim=(-.03, 1.03), ylim=(1.4, -.05), aspect="equal")
        ax.grid(alpha=.15)
    axes[0, 0].set_ylabel("Distance à la source (m)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=(0, .15, 1, 1))
    fig.savefig(output_dir/"fig_geometries.png", dpi=180)
    plt.close(fig)


def plot_fixed_budget_comparison(results, output_dir=None):
    """On compare les énergies moyennes et maximales à nombre de points garnis identique."""
    output_dir = Path(__file__).resolve().parent / "resultats_comparaison_dispositifs" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates = results["candidates"]
    positions = np.arange(len(candidates))
    material_labels = {"MELAMINE": "Mélamine", "LAINE_VERRE": "Laine de verre", "OUATE_POLYESTER": "Ouate polyester"}
    material_colors = {"MELAMINE": "#0072B2", "LAINE_VERRE": "#D55E00", "OUATE_POLYESTER": "#009E73"}
    labels = [f"Niveau {case['level']} — {material_labels.get(case['material'], case['material'])}" for case in candidates]
    colors = [material_colors.get(case["material"], "tab:blue") for case in candidates]
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2), sharey=True, constrained_layout=True)
    axes[0].barh(positions, [case["J_band_mean"] for case in candidates], color=colors)
    axes[0].plot([case["J_full_band_mean"] for case in candidates], positions, "ko", ms=5, label="Entièrement garni")
    axes[0].set_title("Moyenne sur la bande", fontsize=14)
    axes[0].legend(fontsize=11)
    axes[1].barh(positions, [case["J_max"] for case in candidates], color=colors)
    axes[1].set_title("Maximum échantillonné", fontsize=14)
    for ax in axes:
        ax.set_yticks(positions, labels, fontsize=11)
        ax.set_xlabel("Énergie J", fontsize=13)
        ax.tick_params(axis="x", labelsize=11)
        ax.grid(axis="x", alpha=.25)
    axes[0].invert_yaxis()
    fig.suptitle(f"Comparaison avec {results['fixed_covered_nodes']} points garnis par configuration", fontsize=14)
    fig.savefig(output_dir / "fig_comparaison_budget_identique.jpg", dpi=180)
    fig.savefig(output_dir / "fig_budget_commun_trois_materiaux.png", dpi=180)
    plt.close(fig)
    with (output_dir / "comparaison_budget_identique.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(candidates[0]))
        writer.writeheader()
        writer.writerows(candidates)



def plot_coverage_details(study_results, output_dir=None):
    """On montre l'effet de la quantité de matériau sur les critères du niveau deux."""
    output_dir = Path(__file__).resolve().parent/"resultats_multifrequence" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    study = study_results["studies"][2]
    frequencies = study_results["frequencies"]
    quantity = 100*study["actual_volumes"]
    full = study["full"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), constrained_layout=True)
    cases = [(study["volume_mono_costs"], full[study["volume_mono_index"]], f"Une fréquence, {frequencies[study['volume_mono_index']]:g} Hz"),
             (study["volume_multi_costs"], np.mean(full[study["multi_targets"]]), "Moyenne des trois cibles")]
    for ax, (costs, reference, title) in zip(axes, cases):
        ax.plot(quantity, costs, "o-", lw=2, label="Placements binaires")
        ax.axhline(reference, color="black", linestyle="--", label="Mur entièrement garni")
        best = int(np.argmin(costs))
        ax.plot(quantity[best], costs[best], "r*", ms=13, label="Minimum testé")
        ax.set_title(title, fontsize=13)
        ax.set_xlabel("Points garnis (%)", fontsize=12)
        ax.set_ylabel("Énergie J", fontsize=12)
        ax.tick_params(labelsize=11)
        ax.grid(alpha=.3)
        ax.legend(fontsize=10)
    fig.savefig(output_dir/"fig_quantite_niveau_deux.jpg", dpi=160)
    plt.close(fig)


def plot_source_profile_costs(results, output_dir=None):
    """On compare les énergies J des trois profils avant et après le placement binaire."""
    output_dir = Path(__file__).resolve().parent/"resultats_comparaison_dispositifs" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    costs = results["source_costs"]
    positions = np.arange(len(costs))
    fig, ax = plt.subplots(figsize=(9.5, 4.3), constrained_layout=True)
    ax.bar(positions-.18, [row[1] for row in costs], width=.36, label="Placement initial")
    ax.bar(positions+.18, [row[2] for row in costs], width=.36, label="Placement binaire")
    ax.set_xticks(positions, [row[0] for row in costs], fontsize=12)
    ax.set_ylabel("Énergie J", fontsize=12)
    ax.set_title(f"Effet du profil d'entrée à {results['profile_frequency']:g} Hz", fontsize=13)
    ax.tick_params(axis="y", labelsize=11)
    ax.grid(axis="y", alpha=.3)
    ax.legend(fontsize=11)
    fig.savefig(output_dir/"fig_cout_profils_sources.jpg", dpi=160)
    plt.close(fig)



def plot_selected_configuration(results, output_dir=None):
    """On présente le placement retenu et ses spectres à quantité comparable."""
    output_dir = Path(__file__).resolve().parent/"resultats_comparaison_dispositifs" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    domain = results["domain"]
    h = results["spacestep"]
    rows, cols = np.where(domain == _env.NODE_ROBIN)
    chosen = results["density"][rows, cols] > .5
    fig, axes = plt.subplots(2, 1, figsize=(10.8, 5.2), gridspec_kw={"height_ratios": [1, 3]}, constrained_layout=True)
    axes[0].scatter(cols[~chosen]*h, rows[~chosen]*h, c="lightgray", marker="s", s=22, label="Paroi réfléchissante")
    axes[0].scatter(cols[chosen]*h, rows[chosen]*h, c="tab:orange", marker="s", s=22, label="Absorbant")
    axes[0].set(xlabel="Position le long du mur (m)", title="Placement binaire retenu", yticks=[])
    axes[0].legend(fontsize=11, loc="upper left", ncol=2)
    for field, label, style in [("initial_spectrum", "Placement initial binaire", "--"), ("spectrum", "Placement retenu", "-"), ("full_spectrum", "Paroi entièrement garnie", ":")]:
        axes[1].plot(results["frequencies"], results[field], style, label=label, linewidth=1.8)
    axes[1].set(xlabel="Fréquence (Hz)", ylabel="Énergie J", title="Spectres du dispositif et des références")
    axes[1].grid(alpha=.3)
    axes[1].legend(fontsize=11)
    axes[1].tick_params(labelsize=11)
    fig.savefig(output_dir/"fig_dispositif_retenu.jpg", dpi=160)
    plt.close(fig)
    np.savez(output_dir/"dispositif_retenu.npz", frequencies=results["frequencies"],
             domain=domain, density=results["density"], initial_density=results["initial_density"],
             initial_spectrum=results["initial_spectrum"], spectrum=results["spectrum"], full_spectrum=results["full_spectrum"])



def plot_material_energy_comparison(results, retained_materials, output_dir=None):
    """On sépare les courbes par matériau pour comparer leurs pics sans les superposer."""
    import json
    output_dir = Path(__file__).resolve().parent / "resultats_comparaison_materiaux" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 13, "axes.labelsize": 13, "xtick.labelsize": 11, "ytick.labelsize": 11})
    frequencies = results["frequencies"]
    names = results["material_names"]
    retained = list(retained_materials)
    labels = {"MELAMINE": "Mélamine", "LAINE_VERRE": "Laine de verre", "OUATE_POLYESTER": "Ouate polyester"}
    colors = {"MELAMINE": "#0072B2", "LAINE_VERRE": "#D55E00", "OUATE_POLYESTER": "#009E73"}
    columns, headers, arrays = [frequencies], ["frequency_hz"], {"frequencies_hz": frequencies}
    summary = {key: results[key] for key in ("N", "source_name", "sound_speed_m_s", "alpha0", "material_parameters")}
    summary.update({"frequency_step_hz": float(np.min(np.diff(frequencies))), "retained_materials": retained,
                    "robin_convention": "normal_derivative + alpha * density * field = 0", "full_wall": {}})
    for level in results["levels"]:
        # On utilise les mêmes limites verticales pour les matériaux d'un même niveau.
        peak = max(float(np.max(results["energies"][name][level])) for name in names)
        fig, axes = plt.subplots(2, 4, figsize=(14, 6.2), sharex=True, sharey=True, constrained_layout=True)
        for ax, name in zip(axes.flat, names):
            energy = results["energies"][name][level]
            color = colors.get(name, "#777777")
            ax.plot(frequencies, energy, color=color, lw=1.4)
            ax.set(title=labels.get(name, name.replace("_", " ").title()), xlim=(50, 3500), ylim=(0, peak * 1.08))
            ax.grid(alpha=.22)
            ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
            ax.set_xlabel("Fréquence (Hz)")
            ax.set_ylabel("Énergie J")
        for ax in list(axes.flat)[len(names):]:
            ax.axis("off")
        fig.suptitle(f"Énergie J des murs entièrement garnis — niveau {level}", fontsize=14)
        fig.savefig(output_dir / f"fig_energie_tous_materiaux_niveau{level}.png", dpi=180)
        plt.close(fig)
        fig, axes = plt.subplots(1, len(retained), figsize=(10.5, 3.8), sharex=True, sharey=True, constrained_layout=True)
        peak = max(float(np.max(results["energies"][name][level])) for name in retained)
        for ax, name in zip(np.atleast_1d(axes), retained):
            energy = results["energies"][name][level]
            ax.plot(frequencies, energy, color=colors[name], lw=1.6)
            maxima = processing.find_local_maxima(frequencies, 2 * np.pi * frequencies / results["sound_speed_m_s"], energy)
            ax.plot(maxima[1], maxima[3], "o", color=colors[name], ms=3)
            ax.set(title=labels[name], xlabel="Fréquence (Hz)", ylabel="Énergie J", xlim=(50, 3500), ylim=(0, peak * 1.08))
            ax.grid(alpha=.22)
            ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        fig.suptitle(f"Énergie J des trois matériaux étudiés — mur entièrement garni, niveau {level}", fontsize=13)
        fig.savefig(output_dir / f"fig_energie_trois_materiaux_niveau{level}.png", dpi=180)
        plt.close(fig)
        summary["full_wall"][str(level)] = {}
        for name in names:
            energy = results["energies"][name][level]
            index = int(np.argmax(energy))
            summary["full_wall"][str(level)][name] = {"J_band_mean": processing.mean_cost(frequencies, energy),
                         "J_max": float(energy[index]), "f_J_max_hz": float(frequencies[index])}
            columns.append(energy)
            headers.append(f"J_level{level}_{name}")
            arrays[f"J_level{level}_{name}"] = energy
    for name in names:
        arrays[f"alpha_{name}"] = results["alphas"][name]
    np.savetxt(output_dir / "energies_materiaux.csv", np.column_stack(columns), delimiter=",", header=",".join(headers), comments="")
    np.savez(output_dir / "energies_materiaux.npz", **arrays)
    (output_dir / "comparaison_materiaux.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    positions = np.arange(len(names))
    for offset, level in enumerate(results["levels"]):
        axes[0].bar(positions + (offset - 1) * .25, [summary["full_wall"][str(level)][name]["J_band_mean"] for name in names], width=.25, label=f"Niveau {level}")
        axes[1].bar(positions + (offset - 1) * .25, [summary["full_wall"][str(level)][name]["J_max"] for name in names], width=.25, label=f"Niveau {level}")
    for ax, title in zip(axes, ("Énergie J moyenne sur la bande", "Énergie J maximale échantillonnée")):
        ax.set_xticks(positions, [labels.get(name, name.replace("_", " ").title()) for name in names], rotation=35, ha="right", fontsize=11)
        ax.set_title(title)
        ax.set_ylabel("Énergie J")
        ax.legend(fontsize=11)
        ax.grid(axis="y", alpha=.2)
    fig.savefig(output_dir / "fig_bilan_materiaux.png", dpi=180)
    plt.close(fig)
    return summary



def plot_retained_material_studies(material_data=None, output_dir=None):
    """On compare les trois matériaux en séparant leurs courbes et leurs fréquences cibles."""
    output_dir = Path(__file__).resolve().parent / "resultats_comparaison_materiaux" if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if material_data is None:
        material_data = {}
        for name in ("MELAMINE", "LAINE_VERRE", "OUATE_POLYESTER"):
            mono_path = output_dir / name / "monofrequence" / "data_monofrequence.npz"
            multi_path = output_dir / name / "multifrequence" / "data_multifrequence.npz"
            if not mono_path.exists() or not multi_path.exists():
                print("On lance d'abord les études monofréquences et multifréquences pour", name)
                return None
            material_data[name] = {"mono": dict(np.load(mono_path)), "multi": dict(np.load(multi_path))}
    names = list(material_data)
    labels = {"MELAMINE": "Mélamine", "LAINE_VERRE": "Laine de verre", "OUATE_POLYESTER": "Ouate polyester"}
    colors = {"MELAMINE": "#0072B2", "LAINE_VERRE": "#D55E00", "OUATE_POLYESTER": "#009E73"}
    plt.rcParams.update({"font.size": 13, "axes.labelsize": 13, "xtick.labelsize": 11, "ytick.labelsize": 11})
    level = 2
    # On conserve la même échelle verticale pour chaque comparaison de spectres.
    spectra = [material_data[name]["multi"][f"E_init_spec_l{level}"] for name in names]
    max_energy = max(float(np.max(values)) for values in spectra)
    for mode, filename in (("initial", "fig_repartition_initiale_trois_materiaux.png"),
                           ("mono", "fig_spectres_mono_trois_materiaux.png"),
                           ("multi", "fig_spectres_multi_trois_materiaux.png")):
        fig, axes = plt.subplots(1, len(names), figsize=(10.5, 4), sharex=True, sharey=True, constrained_layout=True)
        for ax, name in zip(np.atleast_1d(axes), names):
            data = material_data[name]["multi"]
            frequencies = data["freqs"]
            ax.plot(frequencies, data[f"E_init_spec_l{level}"], ls="--", color="#777777", lw=1.5, label="Densité initiale")
            ax.plot(frequencies, data[f"E_full_spec_l{level}"], color="black", ls=":", lw=1.8, label="Entièrement garni")
            if mode == "mono":
                target = float(data[f"mono_frequency_l{level}_peak1"])
                ax.plot(frequencies, data[f"E_mono_spec_l{level}_peak1"], color=colors[name], lw=1.8, marker="o", ms=3, markevery=5, label=f"Placement à {target:g} Hz")
            if mode == "multi":
                targets = data[f"multi_frequencies_l{level}"]
                ax.plot(frequencies, data[f"E_multi_spec_l{level}"], color=colors[name], lw=1.8, marker="s", ms=3, markevery=5, label="Placement multifréquence")
                ax.set_title(labels[name] + "\nCibles : " + ", ".join(f"{f:g}" for f in targets) + " Hz", fontsize=11)
            else:
                ax.set_title(labels[name], fontsize=13)
            ax.set(xlabel="Fréquence (Hz)", ylabel="Énergie J", xlim=(50, 3500), ylim=(0, max_energy * 1.08))
            ax.legend(fontsize=11, loc="upper right")
            ax.grid(alpha=.22)
            ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        fig.savefig(output_dir / filename, dpi=180)
        plt.close(fig)
    # On montre uniquement les énergies acceptées, puis le contrôle du placement binaire.
    for mode, filename in (("mono", "fig_historiques_mono_trois_materiaux.png"),
                           ("multi", "fig_historiques_multi_trois_materiaux.png")):
        fig, axes = plt.subplots(1, len(names), figsize=(10.5, 3.8), constrained_layout=True)
        for ax, name in zip(np.atleast_1d(axes), names):
            data = material_data[name][mode]
            if mode == "mono":
                history = data[f"history_l{level}_peak1"]
                binary = float(data[f"cost_binary_l{level}_peak1"])
                targets = [float(data[f"f_target_l{level}_peak1"])]
            else:
                history = data[f"multi_history_l{level}"]
                targets = data[f"multi_frequencies_l{level}"]
                indices = [int(np.argmin(abs(data["freqs"] - frequency))) for frequency in targets]
                binary = float(np.mean(data[f"E_multi_spec_l{level}"][indices]))
            if mode == "multi":
                individual = data[f"multi_history_frequencies_l{level}"]
                for column, frequency in enumerate(targets):
                    ax.plot(individual[:, column], lw=1.1, alpha=.65, label=f"{frequency:g} Hz")
                ax.plot(np.arange(len(history)), history, "k--", lw=2, label="Moyenne continue")
            else:
                ax.plot(np.arange(len(history)), history, color=colors[name], lw=2, label="Densité continue")
            ax.plot(len(history) - 1, binary, "x", color="black", ms=8, mew=2, label="Placement binaire")
            ax.set_title(labels[name] + "\n" + ", ".join(f"{f:g}" for f in targets) + " Hz", fontsize=11)
            ax.set(xlabel="Itération acceptée", ylabel="Énergie J" if mode == "mono" else "Énergie J moyenne des cibles")
            ax.grid(alpha=.25)
            ax.legend(fontsize=11)
        fig.savefig(output_dir / filename, dpi=180)
        plt.close(fig)
    # On précise les cibles propres à chaque matériau pour interpréter l'étude de quantité.
    fig, axes = plt.subplots(len(names), 2, figsize=(11.5, 8.5), constrained_layout=True)
    for row, name in enumerate(names):
        data = material_data[name]["multi"]
        volume = 100 * data[f"actual_volumes_l{level}"]
        mono_target = float(data[f"volume_mono_frequency_l{level}"])
        multi_targets = data[f"multi_frequencies_l{level}"]
        mono_index = int(np.argmin(abs(data["freqs"] - mono_target)))
        multi_indices = [int(np.argmin(abs(data["freqs"] - frequency))) for frequency in multi_targets]
        for col, (energy, reference, description) in enumerate((
            (data[f"J_vol_l{level}"], data[f"E_full_spec_l{level}"][mono_index], f"{mono_target:g} Hz"),
            (data[f"J_multi_vol_l{level}"], np.mean(data[f"E_full_spec_l{level}"][multi_indices]), ", ".join(f"{f:g}" for f in multi_targets) + " Hz"),
        )):
            ax = axes[row, col]
            ax.plot(volume, energy, "o-", color=colors[name], lw=1.8, label="Placement binaire")
            ax.axhline(reference, ls="--", color="black", label="Entièrement garni")
            ax.set(title=f"{labels[name]} — {description}", xlabel="Part du mur garnie (%)", ylabel="Énergie J" if col == 0 else "Énergie J moyenne des cibles")
            ax.grid(alpha=.22)
            ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
            ax.legend(fontsize=11)
    fig.savefig(output_dir / "fig_quantites_trois_materiaux.png", dpi=180)
    plt.close(fig)
    # On agrandit aussi les deux comparaisons de quantité pour chaque matériau.
    for name in names:
        data = material_data[name]["multi"]
        volume = 100 * data[f"actual_volumes_l{level}"]
        mono_target = float(data[f"volume_mono_frequency_l{level}"])
        multi_targets = data[f"multi_frequencies_l{level}"]
        mono_index = int(np.argmin(abs(data["freqs"] - mono_target)))
        multi_indices = [int(np.argmin(abs(data["freqs"] - frequency))) for frequency in multi_targets]
        fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8), constrained_layout=True)
        for ax, energy, reference, description in (
            (axes[0], data[f"J_vol_l{level}"], data[f"E_full_spec_l{level}"][mono_index], f"Une fréquence : {mono_target:g} Hz"),
            (axes[1], data[f"J_multi_vol_l{level}"], np.mean(data[f"E_full_spec_l{level}"][multi_indices]), "Cibles : " + ", ".join(f"{f:g}" for f in multi_targets) + " Hz"),
        ):
            ax.plot(volume, energy, "o-", color=colors[name], lw=2, label="Placement binaire")
            ax.axhline(reference, ls="--", color="black", label="Entièrement garni")
            ax.set(title=description, xlabel="Part du mur garnie (%)", ylabel="Énergie J")
            ax.tick_params(labelsize=11)
            ax.grid(alpha=.25)
            ax.legend(fontsize=11)
        axes[1].set_ylabel("Énergie J moyenne des cibles")
        fig.suptitle(labels[name] + " — niveau 2", fontsize=14)
        fig.savefig(output_dir / f"fig_quantites_{name}.png", dpi=180)
        plt.close(fig)
    # On évalue toutes les répartitions sur une bande identique.
    fig, axes = plt.subplots(1, len(names), figsize=(10.5, 4), sharey=True, constrained_layout=True)
    rows = []
    for ax, name in zip(np.atleast_1d(axes), names):
        data = material_data[name]["multi"]
        frequencies = data["freqs"]
        cases = [("Initiale", data[f"E_init_spec_l{level}"]),
                 ("Une fréquence", data[f"E_mono_spec_l{level}_peak1"]),
                 ("Plusieurs fréquences", data[f"E_multi_spec_l{level}"]),
                 ("Entièrement garni", data[f"E_full_spec_l{level}"])]
        means = [processing.mean_cost(frequencies, values) for label, values in cases]
        ax.bar(np.arange(len(cases)), means, color=["#AAAAAA", colors[name], colors[name], "#333333"], hatch=["", "//", "", ""])
        ax.set_xticks(np.arange(len(cases)), [label for label, values in cases], rotation=25, ha="right", fontsize=11)
        ax.set(title=labels[name], ylabel="Énergie J moyenne sur la bande")
        ax.grid(axis="y", alpha=.22)
        for (label, values), mean in zip(cases, means):
            index = int(np.argmax(values))
            rows.append({"material": name, "level": level, "placement": label, "J_band_mean": mean,
                         "J_max": float(values[index]), "f_J_max_hz": float(frequencies[index])})
    fig.savefig(output_dir / "fig_bilan_placements_trois_materiaux.png", dpi=180)
    plt.close(fig)
    with (output_dir / "indicateurs_placements.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows
