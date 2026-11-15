# -*- coding: utf-8 -*-


import matplotlib.pyplot
import numpy
import os
import csv
import shutil
from pathlib import Path
from zipfile import BadZipFile
from matplotlib.ticker import LogLocator, ScalarFormatter, NullFormatter


import _env


def myimshow(tab, **kwargs):
    """On affiche un tableau avec les bornes de couleur demandées."""
    fig, ax = matplotlib.pyplot.subplots(dpi=kwargs.get("dpi", 100))
    # On applique la palette et les limites de couleur fournies.
    image = ax.imshow(tab, cmap=kwargs.get("cmap", "jet"),
                      vmin=kwargs.get("vmin"), vmax=kwargs.get("vmax"))
    ax.set_title(kwargs.get("title", ""))
    if kwargs.get("colorbar"):
        fig.colorbar(image, ax=ax)
    # On enregistre l'image si un nom est fourni et on l'affiche sinon.
    if kwargs.get("filename"):
        path = Path(kwargs["filename"])
        if not path.is_absolute():
            path = Path(__file__).resolve().parent/path
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path.with_name(path.stem+"_plot"+path.suffix))
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close(fig)


def _plot_uncontroled_solution(u, chi):
    """On trace les deux parties du champ initial et la répartition initiale du matériau."""
    # On utilise les mêmes limites de couleur pour les deux parties du champ.
    myimshow(numpy.real(u), title=r'$\operatorname{Re}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_re.jpg')
    myimshow(numpy.imag(u), title=r'$\operatorname{Im}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_im.jpg')
    myimshow(chi, title=r'$\chi_{0}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chi0_re.jpg')

    return


def _plot_controled_solution(u, chi):
    """On trace les deux parties du champ final et la répartition finale du matériau."""
    # On utilise les mêmes limites de couleur pour comparer les champs.
    myimshow(numpy.real(u), title=r'$\operatorname{Re}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_re.jpg')
    myimshow(numpy.imag(u), title=r'$\operatorname{Im}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_im.jpg')
    myimshow(chi, title=r'$\chi_{n}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chin_re.jpg')

    return


def _plot_error(err):
    """On trace les deux parties de la différence entre les champs final et initial."""
    myimshow(numpy.real(err), title=r'$\operatorname{Re}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err_real.jpg')
    myimshow(numpy.imag(err), title=r'$\operatorname{Im}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err.jpg')

    return

def _plot_energy_history(energy):
    """On enregistre l'évolution de l'énergie pendant une descente."""
    matplotlib.pyplot.plot(energy)
    matplotlib.pyplot.title('Energy')

    # On crée le dossier de sortie avant l'enregistrement.
    os.makedirs('courbes_energie', exist_ok=True)
    filename = os.path.join('courbes_energie', 'fig_energy_real.jpg')
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()

    return


# On définit les noms affichés et les styles des courbes.
MATERIAL_LABELS = {"MELAMINE": "Mélamine", "LAINE_ROCHE": "Laine de roche",
                   "LAINE_VERRE": "Laine de verre", "OUATE_POLYESTER": "Ouate polyester"}
COLORS = ("tab:blue", "tab:orange", "tab:green", "tab:red")
STYLES = ("-", "--", "-.", ":")
MODE_LABELS = {"mono": "Une fréquence", "resonances": "Pics d'énergie",
               "bande50": "Bande, pas 50 Hz", "bande5": "Bande, pas 5 Hz"}


def _read_result(path):
    """On charge un fichier de résultat lorsqu'il est présent et lisible."""
    if not Path(path).exists():
        return None
    # On ignore les fichiers absents ou dont l'enregistrement n'est pas terminé.
    try:
        with numpy.load(path) as result:
            return dict(result)
    except (OSError, ValueError, EOFError, BadZipFile):
        return None


def _number(value):
    """On écrit les valeurs numériques avec une virgule décimale."""
    return f"{float(value):g}".replace(".", ",")


def _band_text(frequencies):
    """On décrit les bornes et le pas des fréquences effectivement calculées."""
    frequencies = numpy.asarray(frequencies)
    if len(frequencies) == 1:
        return _number(frequencies[0])+" Hz"
    text = _number(frequencies[0])+"–"+_number(frequencies[-1])+" Hz"
    # On indique le pas seulement si les fréquences sont régulièrement espacées.
    intervals = numpy.diff(frequencies)
    if numpy.allclose(intervals, intervals[0]):
        text += " — pas "+_number(intervals[0])+" Hz"
    return text


def _spectrum_metrics(frequencies, energies):
    """On calcule l'énergie moyenne, l'intégrale et le maximum d'un spectre."""
    frequencies, energies = numpy.asarray(frequencies), numpy.asarray(energies)
    # On approche l'intégrale à partir des intervalles entre les fréquences.
    integral = float(numpy.sum((energies[1:]+energies[:-1])*numpy.diff(frequencies)/2))
    mean = integral/(frequencies[-1]-frequencies[0]) if len(frequencies)>1 else float(energies[0])
    index = int(numpy.argmax(energies))
    return mean, integral, float(energies[index]), float(frequencies[index])


def _axes(title, xlabel="Fréquence (Hz)", ylabel="Énergie J"):
    """On crée un graphique avec son titre, ses axes et sa grille."""
    fig, ax = matplotlib.pyplot.subplots(figsize=(9, 4.7), constrained_layout=True)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=.2)
    # On fixe les bornes de la bande lorsqu'il s'agit d'un spectre.
    if xlabel == "Fréquence (Hz)":
        ax.set_xlim(50, 2000)
    return fig, ax


def _save_figure(fig, folder, filename):
    """On enregistre une figure et sa copie dans le dossier des figures de présentation."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder/filename
    # On conserve une image dans les résultats avant d'en créer la copie.
    fig.savefig(path, dpi=160, bbox_inches="tight")
    destination = Path(__file__).resolve().parents[1]/"presentation"
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination/filename)
    matplotlib.pyplot.close(fig)


def _write_csv(path, header, rows):
    """On enregistre les lignes d'un tableau avec leur en-tête."""
    with Path(path).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def _mode_description(mode, result, evaluation_frequencies):
    """On décrit les fréquences et le nombre maximal d'itérations d'une descente."""
    objective = result["frequencies_hz"]
    if mode == "mono":
        text = "Descente à "+_number(objective[0])+" Hz"
    elif mode == "resonances":
        text = f"{len(objective)} pics repérés sur "+_band_text(evaluation_frequencies)
    else:
        text = "Descente sur "+_band_text(objective)
    return text+f" — {int(result.get('max_iterations', 100))} itérations maximum"


def _mode_suffix(mode):
    """On choisit le suffixe du nom de fichier selon le type de descente."""
    return "pas5" if mode == "bande5" else mode


def _draw_contour(ax, reference, level):
    """On reconstruit le contour du domaine et on le dessine à l'échelle."""
    import preprocessing
    domain, h = reference["domain"], float(reference["h"])
    rows, columns = domain.shape
    # On reconstruit les sommets avec le même générateur que le domaine.
    nodes = preprocessing.create_fractal_nodes(
        [numpy.array([[0], [columns]]), numpy.array([[columns], [columns]])], level)
    x, y = preprocessing.create_fractal_coordinates(nodes, domain)
    # On place le domaine en fond et le contour à ses coordonnées physiques.
    ax.imshow(domain == _env.NODE_INTERIOR, cmap="Greys", alpha=.15,
              extent=(-h/2, (columns-.5)*h, (rows-.5)*h, -h/2))
    ax.plot(numpy.asarray(x)*h, numpy.asarray(y)*h, color="tab:blue", lw=1)
    ax.set_aspect("equal")
    ax.set_xlim(-h, columns*h)
    ax.set_ylim((numpy.where(domain == _env.NODE_ROBIN)[0].max()+3)*h, -h)


def _plot_references(folder, references, materials, levels):
    """On trace les références entièrement garnies et les comparaisons des matériaux et des formes."""
    # On trace chaque référence et on marque les maxima locaux enregistrés.
    for name in materials:
        available = references[name]
        for level, result in available.items():
            frequencies, full = result["frequencies_hz"], result["full"]
            title = f"Niveau {level} — {MATERIAL_LABELS[name]}\nMur entièrement garni — "+_band_text(frequencies)
            fig, ax = _axes(title)
            ax.plot(frequencies, full, lw=1.4)
            peaks = result["peaks"].astype(int)
            ax.plot(frequencies[peaks], full[peaks], "o", ms=3, color="tab:orange")
            _save_figure(fig, folder, f"energie_{name}_niveau{level}.png")
            # On compare aussi le placement initial à la paroi entièrement garnie.
            if level == 3:
                title = f"Niveau 3 — {MATERIAL_LABELS[name]}\nRépartition initiale et mur entièrement garni — "+_band_text(frequencies)
                fig, ax = _axes(title)
                ax.plot(frequencies, result["initial"], color="tab:blue", lw=1.4, label="Répartition initiale")
                ax.plot(frequencies, full, color="black", ls="--", lw=1.3, label="Entièrement garni")
                ax.legend()
                _save_figure(fig, folder, f"comparaison_repartition_initiale_{name}_niveau3.png")
            _write_csv(folder/name/f"spectre_niveau{level}.csv",
                       ("frequence_hz", "J_initial", "J_entierement_garni"),
                       zip(frequencies, result["initial"], full))
            _write_csv(folder/name/f"maxima_niveau{level}.csv",
                       ("frequence_hz", "J_maximum_local"), zip(frequencies[peaks], full[peaks]))
        if available:
            found = [level for level in levels if level in available]
            first = available[found[0]]
            title = MATERIAL_LABELS[name]+" — niveaux "+", ".join(map(str, found))+"\nMur entièrement garni — "+_band_text(first["frequencies_hz"])
            fig, ax = _axes(title)
            for level, color, style in zip(found, COLORS, STYLES):
                result = available[level]
                ax.plot(result["frequencies_hz"], result["full"], color=color, ls=style, lw=1.4, label=f"Niveau {level}")
            ax.legend()
            _save_figure(fig, folder, f"geometrie_energie_{name}.png")
    # On rassemble les matériaux disponibles sur le mur plan.
    plane = [name for name in materials if 0 in references[name]]
    if plane:
        title = "Niveau 0 — "+", ".join(MATERIAL_LABELS[name] for name in plane)+"\nMur entièrement garni — "+_band_text(references[plane[0]][0]["frequencies_hz"])
        fig, ax = _axes(title)
        for name, color, style in zip(plane, COLORS, STYLES):
            result = references[name][0]
            frequencies, peaks = result["frequencies_hz"], result["peaks"].astype(int)
            ax.plot(frequencies, result["full"], color=color, ls=style, lw=1.4, label=MATERIAL_LABELS[name])
            ax.plot(frequencies[peaks], result["full"][peaks], "o", color=color, ms=2.5)
        ax.legend()
        _save_figure(fig, folder, "comparaison_mur_plan.png")
    # On résume l'influence de la géométrie par l'énergie moyenne de chaque spectre.
    present = [name for name in materials if references[name]]
    if not present:
        return
    first = next(iter(references[present[0]].values()))
    title = ", ".join(MATERIAL_LABELS[name] for name in present)+"\nMurs entièrement garnis — niveaux "+", ".join(map(str, levels))+" — "+_band_text(first["frequencies_hz"])
    fig, ax = _axes(title, "Niveau de fractale", "Énergie J moyenne sur la bande")
    records = []
    for name, color, style, marker in zip(present, COLORS, STYLES, ("o", "s", "^", "D")):
        found = [level for level in levels if level in references[name]]
        means = [_spectrum_metrics(references[name][level]["frequencies_hz"], references[name][level]["full"])[0] for level in found]
        ax.plot(found, means, color=color, ls=style, marker=marker, lw=1.7, ms=5, label=MATERIAL_LABELS[name])
        records.extend(zip([name]*len(found), found, means))
    ax.set_xticks(levels)
    ax.set_ylim(bottom=0)
    ax.legend()
    _save_figure(fig, folder, "influence_geometrie_energie.png")
    _write_csv(folder/"influence_geometrie_energie.csv", ("materiau", "niveau", "J_moyenne"), records)


def _plot_geometries(folder, references, materials, levels):
    """On dessine les contours disponibles séparément puis côte à côte."""
    selected = {level: next((references[name][level] for name in materials if level in references[name]), None)
                for level in levels}
    selected = {level: result for level, result in selected.items() if result is not None}
    if not selected:
        return
    # On enregistre d'abord une image pour chaque contour disponible.
    for level, result in selected.items():
        fig, ax = _axes(f"Contour du mur — niveau {level}", "Position horizontale (m)", "Position verticale (m)")
        _draw_contour(ax, result, level)
        _save_figure(fig, folder, f"geometrie_niveau{level}.png")
    # On utilise ensuite un même repère vertical pour comparer les formes.
    fig, axes = matplotlib.pyplot.subplots(1, len(selected), figsize=(10, 3.8), sharey=True, constrained_layout=True)
    maximum = max((numpy.where(result["domain"] == _env.NODE_ROBIN)[0].max()+3)*float(result["h"]) for result in selected.values())
    for ax, (level, result) in zip(numpy.atleast_1d(axes), selected.items()):
        _draw_contour(ax, result, level)
        ax.set(title=f"Niveau {level}", xlabel="Position (m)", ylim=(maximum, -float(result["h"])))
    numpy.atleast_1d(axes)[0].set_ylabel("Position verticale (m)")
    fig.suptitle("Contours des murs — niveaux "+", ".join(map(str, selected)))
    _save_figure(fig, folder, "comparaison_geometries.png")


def _plot_quantities(folder, references, materials, levels):
    """On compare l'énergie obtenue quand on allonge la portion garnie."""
    for name in materials:
        # On charge les fractions et les énergies calculées pour chaque niveau.
        quantities = {level: _read_result(folder/name/f"quantite_niveau{level}.npz") for level in levels}
        quantities = {level: result for level, result in quantities.items() if result is not None}
        if not quantities or not references[name]:
            continue
        first = next(iter(references[name].values()))
        title = MATERIAL_LABELS[name]+" — niveaux "+", ".join(map(str, quantities))+"\nAllongement de la portion initiale — "+_band_text(first["frequencies_hz"])
        fig, ax = _axes(title, "Part du mur garnie (%)", "Énergie J moyenne sur la bande")
        for (level, result), color, style in zip(quantities.items(), COLORS, STYLES):
            ax.plot(100*result["fractions"], result["energies"], "o", color=color, ls=style, lw=1.3, ms=3, label=f"Niveau {level}")
            _write_csv(folder/name/f"quantite_niveau{level}.csv", ("fraction_garnie", "J_moyenne"), zip(result["fractions"], result["energies"]))
        ax.legend()
        _save_figure(fig, folder, f"quantite_{name}.png")


def _plot_density(folder, reference, result, name, mode, title):
    """On distingue les points garnis et les points réfléchissants du mur."""
    fig, ax = _axes(title, "Position horizontale (m)", "Position verticale (m)")
    rows, cols = numpy.where(reference["domain"] == _env.NODE_ROBIN)
    # On sépare les points garnis des points laissés réfléchissants.
    present = result["chi"][rows, cols].astype(bool)
    h = float(reference["h"])
    for mask, label, color in ((~present, "Réfléchissant", ".6"), (present, "Matériau poreux", "tab:blue")):
        ax.scatter(cols[mask]*h, rows[mask]*h, s=12, marker="s", color=color, label=label)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.legend()
    _save_figure(fig, folder, f"repartition_{name}_niveau3_{_mode_suffix(mode)}.png")


def _plot_mode(folder, name, mode, result, spectrum, reference, validation):
    """On trace l'historique d'une descente, les spectres et la répartition finale."""
    description = _mode_description(mode, result, spectrum["frequencies_hz"])
    title = f"Niveau 3 — {MATERIAL_LABELS[name]}\n"+description
    fig, ax = _axes(title, "Itération acceptée", "Énergie J du critère de descente")
    # On distingue l'historique continu du résultat après passage au binaire.
    ax.plot(numpy.arange(len(result["history"])), result["history"], lw=1.5, label="Descente")
    ax.plot(len(result["history"])-1, result["binary_energy"], "x", ms=7, color="black", label="Mur binaire")
    ax.legend()
    _save_figure(fig, folder, f"descente_{name}_niveau3_{_mode_suffix(mode)}.png")
    _write_csv(folder/name/f"historique_{mode}.csv", ("iteration_acceptee", "J_critere_continu"), enumerate(result["history"]))
    # On compare les spectres initial, entièrement garni et binaire sur la même grille.
    fig, ax = _axes(title+"\nÉvaluation : "+_band_text(spectrum["frequencies_hz"]))
    frequencies = spectrum["frequencies_hz"]
    ax.plot(frequencies, spectrum["initial"], color=".55", lw=1.1, label="Initial")
    ax.plot(frequencies, spectrum["full"], color="black", ls="--", lw=1.1, label="Entièrement garni")
    ax.plot(frequencies, spectrum["binary"], color="tab:blue", lw=1.4, label="Après descente et binarisation")
    ax.legend()
    _save_figure(fig, folder, f"spectre_optimise_{name}_niveau3_{_mode_suffix(mode)}.png")
    _write_csv(folder/name/f"spectre_{mode}.csv", ("frequence_hz", "J_initial", "J_entierement_garni", "J_binaire"),
               zip(frequencies, spectrum["initial"], spectrum["full"], spectrum["binary"]))
    _write_csv(folder/name/f"frequences_objectif_{mode}.csv", ("frequence_hz", "poids"), zip(result["frequencies_hz"], result["weights"]))
    if reference is not None:
        _plot_density(folder, reference, result, name, mode, title)
    # On ajoute le contrôle calculé sur la grille de fréquences plus fine.
    if validation is not None:
        fig, ax = _axes(title+"\nContrôle : "+_band_text(validation["frequencies_hz"]))
        frequencies = validation["frequencies_hz"]
        ax.plot(frequencies, validation["initial"], color=".55", lw=1.1, label="Initial")
        ax.plot(frequencies, validation["binary"], color="tab:blue", lw=1.4, label="Après descente et binarisation")
        ax.legend()
        filename = f"validation_spectre_{name}_niveau3_{_mode_suffix(mode)}.png"
        _save_figure(fig, folder, filename)
        _write_csv(folder/name/f"validation_{mode}.csv", ("frequence_hz", "J_initial", "J_binaire"),
                   zip(frequencies, validation["initial"], validation["binary"]))


def _plot_material_modes(folder, name, results, spectra):
    """On compare les spectres des murs binaires obtenus par plusieurs méthodes."""
    available = [mode for mode in MODE_LABELS if mode in results and mode in spectra]
    if not available:
        return
    first = spectra[available[0]]
    title = f"Niveau 3 — {MATERIAL_LABELS[name]}\nMurs binaires après descente — 100 itérations maximum\nÉvaluation : "+_band_text(first["frequencies_hz"])
    fig, ax = _axes(title)
    for mode, color, style in zip(available, COLORS, STYLES):
        spectrum = spectra[mode]
        # On superpose seulement les résultats évalués aux mêmes fréquences.
        if not numpy.array_equal(spectrum["frequencies_hz"], first["frequencies_hz"]):
            continue
        ax.plot(spectrum["frequencies_hz"], spectrum["binary"], color=color, ls=style, lw=1.4, label=("Une fréquence : "+_number(results[mode]["frequencies_hz"][0])+" Hz") if mode == "mono" else MODE_LABELS[mode])
    ax.legend()
    _save_figure(fig, folder, f"comparaison_spectres_modes_{name}.png")


def _plot_mode_materials(folder, mode, materials, results, spectra, validations):
    """On compare les matériaux pour une même méthode de descente."""
    available = [name for name in materials if mode in results[name] and mode in spectra[name]]
    if not available:
        return
    first_name = available[0]
    first = spectra[first_name][mode]
    description = _mode_description(mode, results[first_name][mode], first["frequencies_hz"])
    if mode == "mono":
        description = "Descentes à une fréquence — 100 itérations maximum"
    elif mode == "resonances":
        description = "Pics repérés sur "+_band_text(first["frequencies_hz"])+" — 100 itérations maximum"
    title = "Niveau 3 — "+", ".join(MATERIAL_LABELS[name] for name in available)+"\n"+description
    fig, ax = _axes(title, "Itération acceptée", "Énergie J du critère de descente")
    for name, color, style in zip(available, COLORS, STYLES):
        result = results[name][mode]
        label = MATERIAL_LABELS[name]
        if mode == "mono":
            label += " ("+_number(result["frequencies_hz"][0])+" Hz)"
        ax.plot(numpy.arange(len(result["history"])), result["history"], color=color, ls=style, lw=1.4, label=label)
    # On utilise une échelle logarithmique si tous les critères restent positifs.
    if all(numpy.all(results[name][mode]["history"] > 0) for name in available):
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1, 2, 5)))
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_ylabel("Énergie J du critère (échelle log)")
    ax.legend()
    suffix = _mode_suffix(mode)
    _save_figure(fig, folder, f"comparaison_descentes_niveau3_{suffix}.png")
    fig, ax = _axes(title+"\nÉvaluation : "+_band_text(first["frequencies_hz"]))
    for name, color, style in zip(available, COLORS, STYLES):
        spectrum = spectra[name][mode]
        ax.plot(spectrum["frequencies_hz"], spectrum["binary"], color=color, ls=style, lw=1.4, label=MATERIAL_LABELS[name])
    ax.legend()
    _save_figure(fig, folder, f"comparaison_spectres_niveau3_{suffix}.png")
    # On rassemble les contrôles plus fins disponibles pour les matériaux.
    fine = [name for name in available if mode in validations[name]]
    if fine:
        first = validations[fine[0]][mode]
        title = "Niveau 3 — "+", ".join(MATERIAL_LABELS[name] for name in fine)+"\n"+description+"\nContrôle : "+_band_text(first["frequencies_hz"])
        fig, ax = _axes(title)
        for name, color, style in zip(fine, COLORS, STYLES):
            spectrum = validations[name][mode]
            ax.plot(spectrum["frequencies_hz"], spectrum["binary"], color=color, ls=style, lw=1.4, label=MATERIAL_LABELS[name])
        ax.legend()
        _save_figure(fig, folder, f"validation_spectres_niveau3_{suffix}.png")


def plot_all_results(folder, materials, levels, modes=("mono", "resonances", "bande50", "bande5")):
    """On charge les résultats disponibles puis on produit les figures et les tableaux."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    materials, levels = list(materials), list(levels)
    # On regroupe les références par matériau et par niveau.
    references = {name: {level: _read_result(folder/name/f"niveau{level}.npz") for level in levels} for name in materials}
    references = {name: {level: result for level, result in found.items() if result is not None} for name, found in references.items()}
    _plot_coefficients(folder, materials)
    _plot_references(folder, references, materials, levels)
    _plot_geometries(folder, references, materials, levels)
    _plot_quantities(folder, references, materials, levels)
    # On rassemble les descentes et les lignes des bilans numériques.
    results, spectra, validations, records, refined = {}, {}, {}, [], []
    for name in materials:
        results[name], spectra[name], validations[name] = {}, {}, {}
        for mode in modes:
            result = _read_result(folder/name/f"descente_{mode}.npz")
            spectrum = _read_result(folder/name/f"spectre_{mode}.npz")
            validation = _read_result(folder/name/f"validation_{mode}.npz")
            if result is None or spectrum is None:
                continue
            results[name][mode], spectra[name][mode] = result, spectrum
            if validation is not None:
                validations[name][mode] = validation
            _plot_mode(folder, name, mode, result, spectrum, references[name].get(3), validation)
            # On mesure le gain en comparant les spectres initial et binaire.
            initial = _spectrum_metrics(spectrum["frequencies_hz"], spectrum["initial"])
            binary = _spectrum_metrics(spectrum["frequencies_hz"], spectrum["binary"])
            gain = 100*(1-binary[0]/initial[0]) if initial[0] else None
            records.append((name, mode, int(result["accepted_steps"]), initial[0], binary[0], binary[1], gain, binary[2], binary[3], float(result["chi"].sum())))
            if validation is not None:
                # On mesure également les changements sur la grille de contrôle plus fine.
                fine_initial = _spectrum_metrics(validation["frequencies_hz"], validation["initial"])
                fine_binary = _spectrum_metrics(validation["frequencies_hz"], validation["binary"])
                fine_gain = 100*(1-fine_binary[0]/fine_initial[0]) if fine_initial[0] else None
                mean_change = 100*(fine_binary[0]/binary[0]-1) if binary[0] else None
                peak_change = 100*(fine_binary[2]/binary[2]-1) if binary[2] else None
                refined.append((name, mode, fine_initial[0], fine_binary[0], fine_binary[1], fine_gain, fine_binary[2], fine_binary[3], mean_change, peak_change))
        _plot_material_modes(folder, name, results[name], spectra[name])
    for mode in modes:
        _plot_mode_materials(folder, mode, materials, results, spectra, validations)
    _plot_legacy_figures(folder, references, results)
    # On conserve les indicateurs dans des tableaux de données.
    if records:
        _write_csv(folder/"bilan_descentes.csv", ("materiau", "etude", "iterations_acceptees", "J_initial_moyenne", "J_binaire_moyenne", "J_binaire_integrale", "gain_pourcent", "J_max", "frequence_max_hz", "points_garnis"), records)
    if refined:
        _write_csv(folder/"verification_pas_frequentiel.csv", ("materiau", "etude", "J_initial_moyenne", "J_binaire_moyenne", "J_binaire_integrale", "gain_pourcent", "J_max", "frequence_max_hz", "ecart_moyenne_pourcent", "hausse_max_pourcent"), refined)
    return folder


def _plot_legacy_figures(folder, references, results):
    """On trace le spectre de source, le spectre énergétique initial et un historique de descente."""
    import preprocessing
    # On trace la source sur une plage plus large que la bande étudiée.
    frequencies = numpy.arange(0.0, 3501.0, 5.0)
    amplitudes = [preprocessing.amplitude_rer_b(value) for value in frequencies]
    fig, ax = _axes("Source RER B — amplitude relative\nPlage étudiée : 50–2000 Hz", ylabel="Amplitude relative")
    ax.plot(frequencies, amplitudes, color="tab:blue", lw=1.5, label="Source")
    ax.axvspan(50, 2000, color=".6", alpha=.15, label="Plage étudiée")
    ax.set_xlim(0, 3500)
    ax.set_ylim(bottom=0)
    ax.legend()
    _save_figure(fig, folder, "fig_rer_b_spectre.png")
    name = "OUATE_POLYESTER"
    reference = references.get(name, {}).get(3)
    if reference is not None:
        fig, ax = _axes("Niveau 3 — Ouate polyester — répartition initiale\n"+_band_text(reference["frequencies_hz"]))
        ax.plot(reference["frequencies_hz"], reference["initial"], color="tab:blue", lw=1.4)
        _save_figure(fig, folder, "fig_rer_b_energie.png")
    result = results.get(name, {}).get("mono")
    if result is not None and reference is not None:
        title = "Niveau 3 — Ouate polyester\n"+_mode_description("mono", result, reference["frequencies_hz"])
        fig, ax = _axes(title, "Itération acceptée", "Énergie J")
        ax.plot(numpy.arange(len(result["history"])), result["history"], color="tab:blue", lw=1.4, label="Descente")
        ax.plot(len(result["history"])-1, result["binary_energy"], "x", color="black", ms=7, label="Mur binaire")
        ax.legend()
        _save_figure(fig, folder, "fig_energy_real.jpg")


def _plot_coefficients(folder, materials):
    """On trace le rapport entre la partie réelle et la valeur absolue de la partie imaginaire."""
    coefficients = {name: _read_result(folder/name/"coefficients.npz") for name in materials}
    coefficients = {name: values for name, values in coefficients.items() if values is not None}
    if not coefficients:
        return
    first = next(iter(coefficients.values()))
    title = ", ".join(MATERIAL_LABELS[name] for name in coefficients)+"\nCoefficient de paroi, profil uniforme — "+_band_text(first["frequencies_hz"])
    fig, ax = _axes(title, ylabel="Re(α) / |Im(α)|")
    for (name, values), color, style in zip(coefficients.items(), COLORS, STYLES):
        alpha = values["alphas"]
        # On utilise la valeur absolue de la partie imaginaire au dénominateur.
        ratio = numpy.divide(alpha.real, numpy.abs(alpha.imag),
                             out=numpy.full(alpha.shape, numpy.nan), where=numpy.abs(alpha.imag)>0)
        ax.plot(values["frequencies_hz"], ratio, color=color, ls=style, lw=1.4, label=MATERIAL_LABELS[name])
        _write_csv(folder/name/"coefficients.csv", ("frequence_hz", "alpha_reel", "alpha_imaginaire", "rapport_reel_module_imaginaire"),
                   zip(values["frequencies_hz"], alpha.real, alpha.imag, ratio))
    ax.legend()
    _save_figure(fig, folder, "rapport_ei.png")
