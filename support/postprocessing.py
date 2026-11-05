# -*- coding: utf-8 -*-
import csv
import shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import _env
import preprocessing

MATERIAL_LABELS = {"MELAMINE": "Mélamine", "LAINE_ROCHE": "Laine de roche",
                   "LAINE_VERRE": "Laine de verre", "OUATE_POLYESTER": "Ouate polyester"}
COLORS = ("tab:blue", "tab:orange", "tab:green", "tab:red")
STYLES = ("-", "--", "-.", ":")
plt.rcParams.update({"font.size": 11, "axes.titlesize": 11, "axes.labelsize": 11,
                     "legend.fontsize": 10, "xtick.labelsize": 10, "ytick.labelsize": 10})

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


def save_figure(fig, folder, name):
    """On enregistre le tracé dans le support et sa copie dans la présentation."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    fig.savefig(path, dpi=160, bbox_inches="tight")
    destination = Path(__file__).resolve().parent.parent / "presentation"
    destination.mkdir(exist_ok=True)
    shutil.copy2(path, destination / name)
    plt.close(fig)


def curve_axes(title, xlabel="Fréquence (Hz)", ylabel="Énergie J"):
    """On prépare un seul graphique avec une grille légère."""
    fig, ax = plt.subplots(figsize=(9, 4.7), constrained_layout=True)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=.2)
    return fig, ax


def plot_reference(reference, material, level, folder):
    """On trace l'énergie du mur entièrement garni et ses maxima locaux."""
    f, energy = reference["frequencies_hz"], reference["full"]
    name = MATERIAL_LABELS[material]
    fig, ax = curve_axes(f"Niveau {level} — {name}\nMur entièrement garni — 50–3500 Hz — pas 5 Hz")
    ax.plot(f, energy, lw=1.4)
    values = reference["peaks"]
    ax.plot(f[values], energy[values], "o", ms=3, color="tab:orange")
    save_figure(fig, folder, f"energie_{material}_niveau{level}.png")
    np.savetxt(Path(folder)/material/f"spectre_niveau{level}.csv",
               np.column_stack((f, reference["initial"], energy)), delimiter=",",
               header="frequence_hz,J_initial,J_entierement_garni", comments="")
    np.savetxt(Path(folder)/material/f"maxima_niveau{level}.csv",
               np.column_stack((f[values], energy[values])), delimiter=",",
               header="frequence_hz,J_maximum_local", comments="")


def plot_optimization(reference, mode, material, level, folder):
    """On trace la descente puis le spectre et la répartition du mur binaire."""
    name = MATERIAL_LABELS[material]
    title = f"Niveau {level} — {name} — 50–3500 Hz\nDescente de gradient — pas 5 Hz — 100 itérations maximum"
    fig, ax = curve_axes(title, "Itération acceptée", "Énergie J moyenne sur la bande")
    ax.plot(np.arange(len(mode["history"])), mode["history"], lw=1.5)
    ax.plot(len(mode["history"])-1, mode["binary_energy"], "x", color="black", ms=7)
    save_figure(fig, folder, f"descente_{material}_niveau{level}_pas5.png")
    fig, ax = curve_axes(title)
    f = reference["frequencies_hz"]
    ax.plot(f, reference["initial"], color=".6", lw=1, label="Initial")
    ax.plot(f, reference["full"], color="black", lw=1, ls="--", label="Entièrement garni")
    ax.plot(f, mode["binary_energies"], color="tab:blue", lw=1.4, label="Optimisé")
    ax.legend()
    save_figure(fig, folder, f"spectre_optimise_{material}_niveau{level}_pas5.png")
    fig, ax = curve_axes(title, "Position horizontale (m)", "Position verticale (m)")
    rows, cols = np.where(reference["domain"] == _env.NODE_ROBIN)
    present = mode["chi"][rows, cols].astype(bool)
    for mask, label, color in ((~present, "Réfléchissant", ".6"), (present, "Matériau poreux", "tab:blue")):
        ax.scatter(cols[mask]*reference["h"], rows[mask]*reference["h"], s=14, color=color, marker="s", label=label)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.legend()
    save_figure(fig, folder, f"repartition_{material}_niveau{level}_pas5.png")
    np.savetxt(Path(folder)/material/f"historique_niveau{level}_pas5.csv",
               np.column_stack((np.arange(len(mode["history"])), mode["history"])), delimiter=",",
               header="iteration_acceptee,J_moyenne_continue", comments="")
    np.savetxt(Path(folder)/material/f"spectre_optimise_niveau{level}_pas5.csv",
               np.column_stack((f, reference["initial"], reference["full"], mode["binary_energies"])), delimiter=",",
               header="frequence_hz,J_initial,J_entierement_garni,J_optimise_binaire", comments="")


def plot_material_comparisons(folder, materials, levels):
    """On rassemble les quatre matériaux avec quatre courbes au maximum par figure."""
    folder = Path(folder)
    materials_title = "Mélamine, laine de roche, laine de verre, ouate polyester"
    references = {name:{level:dict(np.load(folder/name/f"niveau{level}.npz")) for level in levels} for name in materials}
    fig, ax = curve_axes("Niveau 0 — "+materials_title+"\nMur entièrement garni — 50–3500 Hz — pas 5 Hz")
    for name, color, style in zip(materials, COLORS, STYLES):
        r = references[name][0]
        ax.plot(r["frequencies_hz"], r["full"], color=color, ls=style, lw=1.4, label=MATERIAL_LABELS[name])
        peaks = r["peaks"]
        ax.plot(r["frequencies_hz"][peaks], r["full"][peaks], "o", color=color, ms=2.5)
    ax.legend()
    save_figure(fig, folder, "comparaison_mur_plan.png")
    for name in materials:
        fig, ax = curve_axes(f"{MATERIAL_LABELS[name]} — niveaux 0, 1, 2 et 3\nMur entièrement garni — 50–3500 Hz — pas 5 Hz")
        for level, color, style in zip(levels, COLORS, STYLES):
            r = references[name][level]
            ax.plot(r["frequencies_hz"], r["full"], color=color, ls=style, lw=1.4, label=f"Niveau {level}")
        ax.legend()
        save_figure(fig, folder, f"geometrie_energie_{name}.png")
        fig, ax = curve_axes(f"{MATERIAL_LABELS[name]} — niveaux 0, 1, 2 et 3\nQuantité de matériau — 50–3500 Hz — pas 5 Hz",
                             "Part du mur garnie (%)", "Énergie J moyenne sur la bande")
        for level, color, style in zip(levels, COLORS, STYLES):
            q = np.load(folder/name/f"quantite_niveau{level}.npz")
            ax.plot(100*q["fractions"], q["energies"], "o", color=color, ls=style, lw=1.3, ms=3, label=f"Niveau {level}")
        ax.legend()
        save_figure(fig, folder, f"quantite_{name}.png")
    modes = {name:dict(np.load(folder/name/"descente_niveau3_pas5.npz")) for name in materials}
    title = "Niveau 3 — "+materials_title+"\nDescente de gradient — 50–3500 Hz — pas 5 Hz — 100 itérations maximum"
    fig, ax = curve_axes(title, "Itération acceptée", "Énergie J moyenne sur la bande")
    for name, color, style in zip(materials, COLORS, STYLES):
        history = modes[name]["history"]
        ax.plot(np.arange(len(history)), history, color=color, ls=style, lw=1.5, label=MATERIAL_LABELS[name])
    ax.legend()
    save_figure(fig, folder, "comparaison_descentes_niveau3_pas5.png")
    fig, ax = curve_axes(title)
    records = []
    for name, color, style in zip(materials, COLORS, STYLES):
        f = references[name][3]["frequencies_hz"]
        energy = modes[name]["binary_energies"]
        ax.plot(f, energy, color=color, ls=style, lw=1.4, label=MATERIAL_LABELS[name])
        records.append((name, modes[name]["accepted_steps"], modes[name]["binary_energy"],
                        np.trapezoid(energy, f), energy.max(), f[np.argmax(energy)], modes[name]["chi"].sum()))
    ax.legend()
    save_figure(fig, folder, "comparaison_spectres_niveau3_pas5.png")
    with (folder/"bilan_descentes.csv").open("w",newline="") as stream:
        writer=csv.writer(stream)
        writer.writerow(("materiau","iterations_acceptees","J_binaire_moyenne","J_binaire_integrale","J_max","frequence_max_hz","points_garnis"))
        writer.writerows(records)
    for level in levels:
        reference=references[materials[0]][level]
        fig, ax = curve_axes(f"Géométrie du mur — niveau {level}", "Position horizontale (m)", "Position verticale (m)")
        r,c=np.where(reference["domain"]==_env.NODE_ROBIN)
        ax.scatter(c*reference["h"],r*reference["h"],s=8,color="tab:blue")
        ax.set_aspect("equal")
        ax.invert_yaxis()
        save_figure(fig,folder,f"geometrie_niveau{level}.png")
