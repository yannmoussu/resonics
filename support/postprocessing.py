# -*- coding: utf-8 -*-
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
import _env
import preprocessing

plt.rcParams.update({"font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
                     "xtick.labelsize": 10, "ytick.labelsize": 10})


MODE_LABELS = {"mono": "Une fréquence", "trois_pics": "Trois centres",
               "pics_resonance": "Pics de résonance", "bande": "Bande entière"}
MODE_COLORS = {"mono": "#9467BD", "trois_pics": "#D55E00",
               "pics_resonance": "#009E73", "bande": "#0072B2"}
MATERIAL_LABELS = {"MELAMINE": "Mélamine", "LAINE_VERRE": "Laine de verre",
                   "OUATE_POLYESTER": "Ouate polyester"}


def myimshow(tab, **kwargs):
    """On affiche un tableau et on enregistre la figure à l'emplacement demandé."""
    fig, ax = plt.subplots(dpi=kwargs.get("dpi", 100))
    image = ax.imshow(tab, cmap=kwargs.get("cmap", "jet"),
                      vmin=kwargs.get("vmin"), vmax=kwargs.get("vmax"))
    ax.set_title(kwargs.get("title", ""))
    if kwargs.get("colorbar"):
        fig.colorbar(image, ax=ax)
    filename = kwargs.get("filename")
    if filename:
        path = Path(filename)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent / path
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path.with_name(path.stem + "_plot" + path.suffix))
    else:
        plt.show()
    plt.close(fig)


def _plot_solution(u, chi, suffix):
    """On représente le champ et la répartition avec les noms de fichiers du support."""
    state = "initial" if suffix == "0" else "final"
    for values, title, filename in ((np.real(u), "Partie réelle du champ "+state, f"fig_u{suffix}_re.jpg"),
                                    (np.imag(u), "Partie imaginaire du champ "+state, f"fig_u{suffix}_im.jpg"),
                                    (chi, "Répartition initiale" if suffix == "0" else "Répartition finale", f"fig_chi{suffix}_re.jpg")):
        myimshow(values, title=title, colorbar=True, vmin=-1, vmax=1, filename=filename)


def _plot_uncontroled_solution(u, chi):
    """On représente le champ initial et le matériau."""
    _plot_solution(u, chi, "0")


def _plot_controled_solution(u, chi):
    """On représente le champ final et le matériau."""
    _plot_solution(u, chi, "n")


def _plot_error(err):
    """On représente les différences entre les deux champs."""
    myimshow(np.real(err), title="Différence des parties réelles", colorbar=True, filename="fig_err_real.jpg")
    myimshow(np.imag(err), title="Différence des parties imaginaires", colorbar=True, filename="fig_err.jpg")


def _plot_energy_history(energy, binary_energy=None):
    """On représente l'énergie calculée et le résultat binaire lorsqu'il est fourni."""
    values = np.asarray(energy).ravel()
    fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)
    ax.plot(np.arange(len(values)), values, label="Critère de descente")
    if binary_energy is not None:
        ax.plot(len(values)-1, binary_energy, "kx", ms=9, label="Après binarisation")
    ax.set(xlabel="Étape", ylabel="Énergie J", title="Évolution du critère")
    ax.legend()
    ax.grid(alpha=.25)
    _save(fig, Path(__file__).resolve().parent, "fig_energy_real.jpg")


def _save(fig, folder, filename):
    """On enregistre la figure puis on libère sa mémoire."""
    fig.savefig(Path(folder) / filename, dpi=180)
    plt.close(fig)


def _json_value(value):
    """On convertit les valeurs numériques pour les fichiers JSON."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return [value.real, value.imag]
    return str(value)


def _metrics(frequencies, values):
    """On calcule l'intégrale, la moyenne et le maximum du spectre évalué."""
    f, values = np.asarray(frequencies), np.asarray(values)
    area = float(np.sum(np.diff(f) * (values[:-1] + values[1:]) / 2))
    width = float(f[-1] - f[0])
    index = int(np.argmax(values))
    return {"J_integral": area, "J_mean": area/width if width else float(values[0]),
            "J_max": float(values[index]), "f_J_max_hz": float(f[index])}


def _criterion_label(name, mode):
    """On précise le critère effectivement pondéré pour chaque descente."""
    if mode.get("criterion_label"):
        return mode["criterion_label"]
    if name == "bande":
        total = np.sum(mode["weights"])
        span = np.ptp(mode["frequencies_hz"])
        if np.isclose(total, 1.):
            return "moyenne de bande"
        if np.isclose(total, span):
            return "intégrale de bande"
        return "somme pondérée sur la bande"
    return {"mono": "énergie à la cible", "trois_pics": "somme aux trois centres", "pics_resonance": "somme aux pics repérés"}[name]


def save_mode(mode_result, output_dir, name):
    """On conserve les valeurs numériques d'une descente dès qu'elle est terminée."""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    arrays = {}
    for key in ("frequencies_hz", "weights", "history", "chi", "chi_relaxed", "binary_energy", "alphas", "accepted_steps"):
        if key in mode_result and mode_result[key] is not None:
            value = np.asarray(mode_result[key])
            if value.dtype.kind in "biufc":
                arrays[key] = value
    path = folder / ("mode_"+name+".npz")
    np.savez_compressed(path, **arrays)
    return path


def _save_comparison_data(results, folder):
    """On conserve les paramètres, les spectres et les densités de chaque méthode."""
    f = np.asarray(results["frequencies_hz"])
    curves = {"initial": results["initial"], "full": results["full"]}
    curves.update({name: mode["energies"] for name, mode in results["modes"].items()})
    np.savetxt(folder/"spectres.csv", np.column_stack((f, *curves.values())), delimiter=",",
               header="frequency_hz," + ",".join(curves), comments="")
    arrays = {"frequencies_hz": f, "domain": results["domain"], "chi_initial": results["chi_initial"]}
    metrics = {name: _metrics(f, values) for name, values in curves.items()}
    initial = metrics["initial"]["J_integral"]
    for values in metrics.values():
        values["reduction_relative"] = 1-values["J_integral"]/initial if initial else 0.
    modes = {}
    for name, mode in results["modes"].items():
        history = np.asarray(mode["history"]).ravel()
        np.savetxt(folder/f"historique_{name}.csv", np.column_stack((np.arange(len(history)), history)),
                   delimiter=",", header="accepted_step,J_continuous_criterion", comments="")
        modes[name] = {key: mode[key] for key in ("frequencies_hz", "weights", "binary_energy", "accepted_steps")}
        modes[name]["criterion_label"] = _criterion_label(name, mode)
        for key in ("chi", "chi_relaxed", "history", "frequencies_hz", "weights", "alphas"):
            if key in mode and mode[key] is not None:
                arrays[name + "_" + key] = np.asarray(mode[key])
        arrays[name + "_binary_energy"] = np.asarray(mode["binary_energy"])
    arrays.update({"J_"+name: np.asarray(values) for name, values in curves.items()})
    fm = np.asarray(results.get("material_frequencies_hz", f))
    arrays["material_frequencies_hz"] = fm
    for name, material in results.get("materials", {}).items():
        alphas = np.asarray(material["alphas"])
        columns, headers = [fm, alphas.real, alphas.imag], ["frequency_hz", "alpha_real", "alpha_imag"]
        arrays[name + "_alphas"] = alphas
        peaks = []
        for level, values in material["full"].items():
            for index in material.get("peaks", {}).get(level, []):
                peaks.append((int(level), fm[index], values[index]))
            columns.append(values)
            headers.append("J_full_level"+str(level))
            arrays[f"{name}_full_level{level}"] = np.asarray(values)
        np.savetxt(folder/f"pics_{name}.csv", np.asarray(peaks).reshape(-1, 3), delimiter=",",
                   header="level,frequency_hz,J", comments="")
        np.savetxt(folder/f"materiau_{name}.csv", np.column_stack(columns), delimiter=",", header=",".join(headers), comments="")
    if results.get("quantities"):
        q = results["quantities"]
        arrays["quantity_fractions"], arrays["quantity_energies"] = np.asarray(q["fractions"]), np.asarray(q["energies"])
        np.savetxt(folder/"quantites.csv", np.column_stack((q["fractions"], q["energies"])), delimiter=",", header="fraction,J_three_centres_binary", comments="")
    np.savez_compressed(folder/"resultats_comparaisons.npz", **arrays)
    for name, value in (("parametres", results["parameters"]), ("criteres_modes", modes), ("indicateurs", metrics),
                        ("controle_frequences", results.get("sampling_history", [])), ("controle_gradient", results.get("gradient_check", {}))):
        (folder/(name+".json")).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=_json_value)+"\n", encoding="utf-8")
    fields = ["configuration"]+list(next(iter(metrics.values())))
    with (folder/"indicateurs.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for name, values in metrics.items():
            writer.writerow({"configuration": name, **values})
    return metrics


def _plot_source_and_geometries(results, folder):
    """On représente la source choisie et les domaines du support fourni."""
    params = results["parameters"]
    frequencies = np.asarray(results["frequencies_hz"])
    source = results.get("source", getattr(preprocessing, params.get("source_name", ""), None))
    amplitudes = results.get("source_amplitudes")
    if source is not None:
        amplitudes = np.asarray([abs(source(0., 2*np.pi*f)) for f in frequencies])
    if amplitudes is not None:
        fig, ax = plt.subplots(figsize=(10, 3.7), constrained_layout=True)
        ax.plot(frequencies, amplitudes, color="#0072B2", lw=2)
        ax.set(xlabel="Fréquence (Hz)", ylabel="Amplitude relative", title="Amplitude de la source")
        ax.grid(alpha=.25)
        _save(fig, folder, "fig_source_rer_b.png")
    N = int(params["N"])
    h = float(params.get("h", params.get("h_m", 1/N)))
    fig, axes = plt.subplots(1, 3, figsize=(11, 4), constrained_layout=True)
    for level, ax in enumerate(axes):
        domain, _, _, _, _ = preprocessing._set_geometry_of_domain(2*N, N, level)
        air = domain == _env.NODE_INTERIOR
        rows, cols = np.where(domain == _env.NODE_ROBIN)
        ax.imshow(air, cmap="Blues", origin="upper", extent=(-h/2, (N-.5)*h, (2*N-.5)*h, -h/2), alpha=.5)
        ax.scatter(cols*h, rows*h, s=4, color="#D55E00")
        ax.set(title=f"Niveau {level}", xlabel="Position horizontale (m)", ylabel="Position verticale (m)",
               ylim=(max(rows.max(), np.where(air)[0].max())*h+2*h, -h))
    _save(fig, folder, "fig_geometries.png")


def _plot_materials(results, folder):
    """On compare les coefficients et les murs entièrement garnis par matériau."""
    materials = results.get("materials", {})
    if not materials:
        return
    f = np.asarray(results.get("material_frequencies_hz", results["frequencies_hz"]))
    fig, axes = plt.subplots(1, len(materials), figsize=(11, 3.7), squeeze=False, constrained_layout=True)
    for ax, (name, material) in zip(axes.flat, materials.items()):
        alphas = np.asarray(material["alphas"])
        ax.plot(f, alphas.real, label="Partie réelle", color="#0072B2")
        ax.plot(f, alphas.imag, "--", label="Partie imaginaire", color="#D55E00")
        ax.set(title=MATERIAL_LABELS.get(name, name), xlabel="Fréquence (Hz)", ylabel=r"Coefficient de Robin (m$^{-1}$)")
        ax.grid(alpha=.25)
        ax.legend(fontsize=9)
    _save(fig, folder, "fig_coefficients_materiaux.png")
    fig, axes = plt.subplots(1, len(materials), figsize=(11, 3.7), squeeze=False, sharey=True, constrained_layout=True)
    for ax, (name, material) in zip(axes.flat, materials.items()):
        values = material["full"].get(0, material["full"].get("0"))
        ax.plot(f, values, lw=1.6)
        indices = material.get("peaks", {}).get(0, [])
        ax.scatter(f[indices], np.asarray(values)[indices], color="#D55E00", s=18, label="Maxima locaux", zorder=3)
        ax.legend(fontsize=9)
        ax.set(title=MATERIAL_LABELS.get(name, name), xlabel="Fréquence (Hz)", ylabel="Énergie J")
        ax.grid(alpha=.25)
    _save(fig, folder, "fig_spectres_materiaux_niveau0.png")
    name = results["parameters"]["material_name"]
    if name not in materials:
        return
    shapes = materials[name]["full"]
    fig, axes = plt.subplots(1, len(shapes), figsize=(11, 3.7), squeeze=False, sharey=True, constrained_layout=True)
    for ax, (level, values) in zip(axes.flat, sorted(shapes.items(), key=lambda item: int(item[0]))):
        ax.plot(f, values, lw=1.6)
        indices = materials[name].get("peaks", {}).get(level, [])
        ax.scatter(f[indices], np.asarray(values)[indices], color="#D55E00", s=18, label="Maxima locaux", zorder=3)
        ax.legend(fontsize=9)
        ax.set(title=f"Niveau {level}", xlabel="Fréquence (Hz)", ylabel="Énergie J")
        ax.grid(alpha=.25)
    _save(fig, folder, "fig_spectres_formes.png")


def _spectrum_axis(ax, f, curves, logarithmic=False):
    """On conserve les mêmes axes pour confronter des spectres physiques."""
    for values, label, color, style in curves:
        ax.plot(f, values, label=label, color=color, ls=style, lw=1.6)
    ax.set(xlabel="Fréquence (Hz)", ylabel="Énergie J", xlim=(f[0], f[-1]))
    if logarithmic:
        ax.set_yscale("log")
        ax.set_ylabel("Énergie J (échelle logarithmique)")
        positive = np.concatenate([np.asarray(values)[np.asarray(values)>0] for values, *_ in curves])
        if positive.size:
            ax.set_ylim(bottom=max(positive.max()*1e-7, positive.min()))
    ax.grid(alpha=.25, which="both")
    ax.legend(fontsize=9)


def _plot_spectra(results, folder):
    """On compare uniquement les placements binaires aux deux références."""
    f = np.asarray(results["frequencies_hz"])
    reference = [(results["initial"], "Mur initial", "#777777", "--"),
                 (results["full"], "Entièrement garni", "black", ":")]
    fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
    _spectrum_axis(ax, f, reference, logarithmic=True)
    ax.set_title("Répartition initiale et mur entièrement garni")
    _save(fig, folder, "fig_repartition_initiale_complete.png")
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    filenames = {"mono": "mono", "trois_pics": "trois_pics", "pics_resonance": "pics", "bande": "bande"}
    for ax, (name, mode) in zip(axes.flat, results["modes"].items()):
        curves = reference + [(mode["energies"], MODE_LABELS[name], MODE_COLORS[name], "-")]
        _spectrum_axis(ax, f, curves, logarithmic=True)
        ax.set_title(MODE_LABELS[name])
        single, single_ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
        _spectrum_axis(single_ax, f, curves, logarithmic=True)
        single_ax.set_title("Spectre du placement binaire — " + MODE_LABELS[name].lower())
        _save(single, folder, "fig_spectre_"+filenames[name]+".png")
    for ax in list(axes.flat)[len(results["modes"]):]:
        ax.axis("off")
    _save(fig, folder, "fig_spectres_modes.png")
    fig, ax = plt.subplots(figsize=(10.5, 4.3), constrained_layout=True)
    curves = [(mode["energies"], MODE_LABELS[name], MODE_COLORS[name], style)
              for (name, mode), style in zip(((name, mode) for name, mode in results["modes"].items() if name != "mono"), ("-.", "--", "-"))]
    if curves:
        _spectrum_axis(ax, f, curves)
        ax.set_title("Spectres des répartitions binaires optimisées")
        _save(fig, folder, "fig_comparaison_optimisations.png")
    else:
        plt.close(fig)


def _history_axis(ax, name, mode, normalise):
    """On distingue la descente continue du résultat obtenu après binarisation."""
    history = np.asarray(mode["history"]).ravel()
    scale = history[0] if normalise and history[0] else 1.
    ax.plot(np.arange(len(history)), history/scale, color=MODE_COLORS[name], label="Descente continue")
    ax.plot(len(history)-1, mode["binary_energy"]/scale, "kx", ms=8, label="Après binarisation")
    ax.set(xlabel="Étape acceptée", ylabel="Critère rapporté au départ" if normalise else "Énergie J",
           title=MODE_LABELS[name]+" — "+_criterion_label(name, mode))
    plotted = np.r_[history, mode["binary_energy"]] / scale
    if np.all(plotted > 0) and plotted.max() / plotted.min() > 100:
        ax.set_yscale("log")
        ax.set_ylabel(ax.get_ylabel() + " (échelle log)")
    ax.grid(alpha=.25)
    ax.legend(fontsize=9)


def _plot_histories_and_densities(results, folder):
    """On distingue les critères de descente et on montre les portions finales garnies."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    for ax, (name, mode) in zip(axes.flat, results["modes"].items()):
        _history_axis(ax, name, mode, normalise=True)
    for ax in list(axes.flat)[len(results["modes"]):]:
        ax.axis("off")
    _save(fig, folder, "fig_historiques_modes.png")
    band = results["modes"].get("bande")
    if band is not None:
        fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
        _history_axis(ax, "bande", band, normalise=False)
        _save(fig, folder, "fig_descente_bande.png")
    mono = results["modes"].get("mono")
    if mono is not None:
        fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
        _history_axis(ax, "mono", mono, normalise=False)
        _save(fig, folder, "fig_descente_mono.png")
    domain = np.asarray(results["domain"])
    rows, cols = np.where(domain == _env.NODE_ROBIN)
    params = results["parameters"]
    h = float(params.get("h", params.get("h_m", 1/int(params["N"]))))
    densities = [(results["chi_initial"], "Mur initial")]+[(mode["chi"], MODE_LABELS[name]) for name, mode in results["modes"].items()]
    fig, axes = plt.subplots(2, 3, figsize=(11, 6), sharex=True, sharey=True, constrained_layout=True)
    colors = ["#3d1255", "#F0E442"]
    palette = ListedColormap(colors)
    norm = BoundaryNorm([-.5, .5, 1.5], 2)
    for ax, (chi, label) in zip(axes.flat, densities):
        image = ax.scatter(cols*h, rows*h, c=np.asarray(chi)[rows, cols], norm=norm, marker="s", s=17, cmap=palette)
        ax.set(title=label, xlabel="Position horizontale (m)", ylabel="Position verticale (m)",
               ylim=(rows.max()*h+2*h, rows.min()*h-2*h))
        ax.set_aspect("equal")
    for ax in list(axes.flat)[len(densities):]:
        ax.axis("off")
    axes.flat[-1].legend(handles=[Patch(facecolor=colors[0], label="Réfléchissant"),
                                 Patch(facecolor=colors[1], label="Matériau poreux")],
                         loc="center", frameon=False)
    _save(fig, folder, "fig_repartitions_modes.png")


def _plot_controls(results, folder):
    """On représente les contrôles du gradient, des fréquences et de la quantité."""
    check = results.get("gradient_check")
    if check:
        adjoint, finite = np.asarray(check["adjoint"]), np.asarray(check["finite_difference"])
        fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
        ax.plot(finite, "o-", label="Différences centrées")
        ax.plot(adjoint, "x--", label="Adjoint")
        ax.set(xlabel="Point du mur testé", ylabel="Dérivée de l'énergie", title="Contrôle numérique du gradient")
        ax.grid(alpha=.25)
        ax.legend()
        _save(fig, folder, "fig_validation_gradient.png")
    history = results.get("sampling_history", [])
    if history:
        fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), constrained_layout=True)
        for phase in dict.fromkeys(row.get("phase", "contrôle") for row in history):
            records = [row for row in history if row.get("phase", "contrôle") == phase]
            points = [row["n_points"] for row in records]
            axes[0].semilogy(points, [max(row["integral_error"], 1e-16) for row in records], "o-", label=phase)
            axes[1].plot(points, [row["peak_error"] for row in records], "o-", label=phase)
        limits = (results["parameters"].get("frequency_tolerance", .01), results["parameters"].get("peak_tolerance", .05))
        for ax, title, limit in zip(axes, ("Variation relative de l'intégrale", "Variation relative du maximum"), limits):
            ax.axhline(limit, color="black", ls=":", label=f"Seuil {100*limit:g} %")
            ax.set(xlabel="Nombre de fréquences", ylabel="Écart relatif", title=title)
            ax.grid(alpha=.25)
            ax.legend(fontsize=9)
        _save(fig, folder, "fig_convergence_frequence.png")
    quantities = results.get("quantities")
    if quantities:
        fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
        ax.plot(100*np.asarray(quantities["fractions"]), quantities["energies"], "o-", lw=1.8)
        ax.set(xlabel="Part du mur garnie (%)", ylabel="Somme des Énergies J aux trois centres", title="Énergie selon la quantité de matériau")
        ax.grid(alpha=.25)
        _save(fig, folder, "fig_quantites.png")
    theory = results.get("sommerfeld")
    if theory:
        fig, ax = plt.subplots(figsize=(9, 4), constrained_layout=True)
        ax.plot(theory["depths"], theory["open"], label="Sortie ouverte")
        ax.plot(theory["depths"], theory["reflecting"], label="Paroi réfléchissante")
        ax.set(xlabel="Profondeur (m)", ylabel="Énergie J", title=f"Forme du rectangle à {theory['frequency_hz']:g} Hz")
        ax.set_yscale("log")
        ax.grid(alpha=.25)
        ax.legend()
        _save(fig, folder, "fig_sommerfeld_forme.png")


def plot_comparisons(results, output_dir):
    """On enregistre les nouvelles comparaisons calculées avec le support fourni."""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    metrics = _save_comparison_data(results, folder)
    _plot_source_and_geometries(results, folder)
    _plot_materials(results, folder)
    _plot_spectra(results, folder)
    _plot_histories_and_densities(results, folder)
    _plot_controls(results, folder)
    names = ["full"]+list(results["modes"])
    labels = ["Entièrement garni"]+[MODE_LABELS[name] for name in results["modes"]]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), constrained_layout=True)
    for ax, key, title in zip(axes, ("J_integral", "J_max"), ("Énergie intégrée sur la bande", "Maximum de l'énergie sur la bande")):
        ax.bar(np.arange(len(names)), [metrics[name][key] for name in names], color=["#444444"]+[MODE_COLORS[name] for name in results["modes"]])
        ax.set_xticks(np.arange(len(names)), labels, rotation=25, ha="right", fontsize=9)
        ax.set(ylabel="Énergie J", title=title)
        ax.grid(axis="y", alpha=.25)
    _save(fig, folder, "fig_bilan_performances.png")
    return metrics
