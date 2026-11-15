"""On trace les parties réelle et imaginaire du coefficient de l'ouate."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_alpha_ouate():
    """On lit les coefficients enregistrés et on trace les deux courbes."""
    folder = Path(__file__).resolve().parent
    data = np.genfromtxt(folder / "data/alpha_ouate.csv", delimiter=",", names=True)
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.plot(data["frequence_hz"], data["alpha_reel"], lw=1.7, label="Re α")
    ax.plot(data["frequence_hz"], data["alpha_imaginaire"], lw=1.7, label="Im α")
    ax.set(xlabel="Fréquence (Hz)", ylabel="Coefficient de paroi (m⁻¹)",
           title="Ouate de polyester", xlim=(50, 2000))
    ax.axhline(0, color="0.5", linewidth=0.7)
    ax.grid(alpha=0.2)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(folder / "figures/alpha_ouate.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    plot_alpha_ouate()
