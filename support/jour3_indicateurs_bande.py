# -*- coding: utf-8 -*-
"""On résume chaque placement du jour 3 par des indicateurs sur toute la bande de fréquences.

Aucun calcul de Helmholtz n'est relancé : on relit les spectres enregistrés
dans resultats_jour3/data_jour3.npz par jour3_multifrequence_et_volume.py.
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "resultats_jour3")
DATA_FILE = os.path.join(OUTPUT_DIR, "data_jour3.npz")


def band_mean(frequencies, costs):
    """On calcule la moyenne du coût sur la bande par la méthode des trapèzes."""
    frequencies = np.asarray(frequencies, dtype=float)
    costs = np.asarray(costs, dtype=float)
    if len(frequencies) == 1:
        return float(costs[0])
    # Chaque trapèze a pour aire (largeur de l'intervalle) x (moyenne des deux coûts).
    area = np.sum((frequencies[1:] - frequencies[:-1]) * (costs[1:] + costs[:-1]) / 2.0)
    return float(area / (frequencies[-1] - frequencies[0]))


def placements_of_level(data, level):
    """On rassemble les spectres disponibles pour un niveau, du plus simple au plus garni."""
    placements = [("Initiale", data[f"E_init_spec_l{level}"])]
    number = 1
    # Le nombre de placements à une fréquence dépend des pics trouvés au jour 3.
    while f"E_mono_spec_l{level}_peak{number}" in data:
        frequency = float(data[f"mono_frequency_l{level}_peak{number}"])
        placements.append((f"Une fréquence ({frequency:.0f} Hz)",
                           data[f"E_mono_spec_l{level}_peak{number}"]))
        number += 1
    targets = ", ".join(f"{f:.0f}" for f in data[f"multi_frequencies_l{level}"])
    placements.append((f"Plusieurs fréquences ({targets} Hz)", data[f"E_multi_spec_l{level}"]))
    placements.append(("Entièrement garni", data[f"E_full_spec_l{level}"]))
    return placements


def compute_indicators(frequencies, placements):
    """On calcule pour chaque placement le coût moyen, le pire cas, la réduction et la part du gain."""
    initial_mean = band_mean(frequencies, placements[0][1])
    full_mean = band_mean(frequencies, placements[-1][1])
    reference_gain = initial_mean - full_mean
    rows = []
    for name, spectrum in placements:
        spectrum = np.asarray(spectrum, dtype=float)
        mean = band_mean(frequencies, spectrum)
        worst = int(np.argmax(spectrum))
        rows.append({
            "placement": name,
            "J_bande": mean,
            "J_max": float(spectrum[worst]),
            "f_J_max_hz": float(frequencies[worst]),
            # Le coût est une énergie, on exprime donc le rapport en 10 log10.
            "reduction_dB": float(10.0 * np.log10(initial_mean / mean)),
            # On mesure la part du gain du mur entièrement garni obtenue avec 30 % de matériau.
            "part_du_gain_pct": float(100.0 * (initial_mean - mean) / reference_gain)
            if abs(reference_gain) > 1e-14 else np.nan,
        })
    return rows


def run_band_indicators():
    """On produit le tableau et la figure des indicateurs pour les trois niveaux."""
    if not os.path.exists(DATA_FILE):
        print("Fichier introuvable :", DATA_FILE)
        print("Il faut d'abord lancer jour3_multifrequence_et_volume.py.")
        return None
    data = dict(np.load(DATA_FILE))
    frequencies = data["freqs"]
    volume = float(data["volume_fraction"])
    levels = [level for level in (0, 1, 2) if f"E_init_spec_l{level}" in data]

    all_rows = {}
    for level in levels:
        all_rows[level] = compute_indicators(frequencies, placements_of_level(data, level))
        print(f"\nNiveau {level} (bande {frequencies[0]:.0f}-{frequencies[-1]:.0f} Hz, {volume:.0%} de matériau)")
        for row in all_rows[level]:
            print(f"  {row['placement']:<40s} J_bande = {row['J_bande']:.4e}  "
                  f"réduction = {row['reduction_dB']:5.2f} dB  part du gain = {row['part_du_gain_pct']:6.1f} %  "
                  f"pire cas à {row['f_J_max_hz']:.0f} Hz")

    # On enregistre toutes les valeurs dans un seul tableau.
    with open(os.path.join(OUTPUT_DIR, "indicateurs_bande.csv"), "w", newline="", encoding="utf-8") as stream:
        fields = ["niveau"] + list(all_rows[levels[0]][0])
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for level in levels:
            for row in all_rows[level]:
                writer.writerow({"niveau": level, **row})

    # Première ligne : réduction en dB. Seconde ligne : part du gain du mur entièrement garni.
    fig, axes = plt.subplots(2, len(levels), figsize=(4.5 * len(levels), 7.5), squeeze=False)
    for column, level in enumerate(levels):
        rows = all_rows[level]
        labels = [row["placement"] for row in rows]
        positions = np.arange(len(rows))
        colors = ["tab:gray"] + ["tab:blue"] * (len(rows) - 3) + ["tab:green", "black"]
        ax = axes[0, column]
        ax.bar(positions, [row["reduction_dB"] for row in rows], color=colors)
        ax.set(title=f"Niveau {level}", ylabel="Réduction par rapport à l'initiale (dB)")
        ax = axes[1, column]
        ax.bar(positions, [row["part_du_gain_pct"] for row in rows], color=colors)
        ax.axhline(100.0, color="black", ls="--", lw=1)
        ax.set(ylabel="Part du gain du mur entièrement garni (%)")
        for ax in axes[:, column]:
            ax.set_xticks(positions, labels, rotation=40, ha="right", fontsize=7)
            ax.grid(axis="y", alpha=0.3)
    fig.suptitle(f"Performances sur toute la bande {frequencies[0]:.0f}-{frequencies[-1]:.0f} Hz "
                 f"avec {volume:.0%} de matériau (sauf mur entièrement garni)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_j3_4_indicateurs_bande.jpg"), dpi=160)
    plt.close(fig)
    return all_rows


if __name__ == "__main__":
    run_band_indicators()