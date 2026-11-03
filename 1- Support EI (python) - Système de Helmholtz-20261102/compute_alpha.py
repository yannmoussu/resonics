# -*- coding: utf-8 -*-
# Fichier : compute_alpha.py

import numpy as np
import matplotlib.pyplot as plt

# Matériaux poreux (Paramètres du modèle équivalent fluide : phi, sigma, alpha_inf, Lambda, Lambda_prime, epaisseur d)
MATERIALS = {
    "melamine_foam": {
        "name": "Mousse de Mélamine",
        "phi": 0.99,           # Porosité [-]
        "sigma": 12000.0,      # Résistivité [N.s/m^4]
        "alpha_inf": 1.02,     # Tortuosité [-]
        "Lambda": 100e-6,      # Longueur visqueuse [m]
        "Lambda_p": 200e-6,    # Longueur thermique [m]
        "d": 0.05              # Épaisseur de la couche [m]
    },
    "rock_wool": {
        "name": "Laine de Roche (Haute densité)",
        "phi": 0.94,
        "sigma": 40000.0,
        "alpha_inf": 1.06,
        "Lambda": 50e-6,
        "Lambda_p": 110e-6,
        "d": 0.05
    },
    "hemp_fiber": {
        "name": "Fibre de Chanvre (Biosourcé)",
        "phi": 0.90,
        "sigma": 25000.0,
        "alpha_inf": 1.05,
        "Lambda": 70e-6,
        "Lambda_p": 150e-6,
        "d": 0.05
    }
}

def compute_alpha(wavenumber, material_key="rock_wool", c0=340.0):
    """
    Calcule le coefficient d'absorption complexe Alpha(omega) compatible avec 
    la convention de signe de processing.py (Re(Alpha) > 0, Im(Alpha) < 0).
    
    :param wavenumber: Nombre d'onde k = omega / c0 (float ou array)
    :param material_key: Clé du matériau choisi dans MATERIALS
    :param c0: Célérité du son dans l'air (m/s)
    :return: Alpha complexe
    """
    mat = MATERIALS[material_key]
    phi = mat["phi"]
    sigma = mat["sigma"]
    alpha_inf = mat["alpha_inf"]
    Lambda = mat["Lambda"]
    Lambda_p = mat["Lambda_p"]
    d = mat["d"]

    # Constantes de l'air
    rho0 = 1.213          # Masse volumique de l'air [kg/m^3]
    eta = 1.84e-5         # Viscosité dynamique [Pa.s]
    P0 = 101325.0         # Pression atmosphérique [Pa]
    gamma = 1.4           # Ratio des capacités thermiques [-]
    Pr = 0.71             # Nombre de Prandtl [-]

    omega = wavenumber * c0  # Pulsation [rad/s]

    # Modèle de Johnson-Champoux-Allard (JCA) avec convention temporelle exp(-i*omega*t)
    # 1. Densité effective complexe rho_eff(omega)
    visc_term = np.sqrt(1.0 - (4.0 * 1j * (alpha_inf**2) * eta * rho0 * omega) / ((sigma * Lambda * phi)**2))
    rho_eff = (rho0 * alpha_inf / phi) * (1.0 - (sigma * phi / (1j * omega * rho0 * alpha_inf)) * visc_term)

    # 2. Module de compressibilité effectif complexe K_eff(omega)
    therm_term = np.sqrt(1.0 - (1j * rho0 * omega * Pr * (Lambda_p**2)) / (16.0 * eta))
    denom_K = gamma - (gamma - 1.0) / (1.0 - (8.0 * eta / (1j * rho0 * omega * Pr * (Lambda_p**2))) * therm_term)
    K_eff = (gamma * P0 / phi) / denom_K

    # 3. Nombre d'onde et impédance caractéristique dans le poreux
    k_p = omega * np.sqrt(rho_eff / K_eff)
    Z_c = np.sqrt(rho_eff * K_eff)

    # 4. Admittance de surface réduite pour une couche d'épaisseur d sur fond rigide
    # Y_s = 1 / Z_s = i * tan(k_p * d) / Z_c
    # Coefficient de Robin physique : alpha_phys = -i * omega * rho0 / Z_s = omega * rho0 * tan(k_p * d) / Z_c
    alpha_phys = omega * rho0 * np.tan(k_p * d) / Z_c

    # Convention de processing.py : Re(Alpha) > 0 et Im(Alpha) < 0 pour dissiper l'énergie
    Alpha = np.abs(np.real(alpha_phys)) - 1j * np.abs(np.imag(alpha_phys))
    return Alpha

def compare_materials():
    """Compare les performances d'absorption des 3 matériaux sur [100 Hz, 2000 Hz]."""
    freqs = np.linspace(100, 2000, 200)
    c0 = 340.0
    rho0 = 1.213
    Z0 = rho0 * c0
    k_vals = 2.0 * np.pi * freqs / c0

    plt.figure(figsize=(10, 5), dpi=100)
    for key, mat in MATERIALS.items():
        Alpha = compute_alpha(k_vals, material_key=key, c0=c0)
        # Coefficient d'absorption acoustique sous incidence normale : a_abs = 1 - |R|^2
        # Sur fond rigide avec du/dn + Alpha * u = 0 et Im(Alpha) < 0 :
        # Z_norm = Z_s / Z0 = -i * k / Alpha (de partie réelle > 0) et R = (Z_norm - 1) / (Z_norm + 1)
        Z_norm = -1j * k_vals / Alpha
        R = (Z_norm - 1.0) / (Z_norm + 1.0)
        a_abs = 1.0 - np.abs(R)**2
        plt.plot(freqs, a_abs, lw=2, label=rf"{mat['name']} ($\sigma={mat['sigma']/1000:.0f}$ kN.s/m$^4$)")

    plt.title("Comparaison du coefficient d'absorption sous incidence normale ($d = 5$ cm)")
    plt.xlabel("Fréquence $f$ (Hz)")
    plt.ylabel("Coefficient d'absorption $\\alpha_{\\mathrm{abs}} = 1 - |R|^2$")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("fig_comparaison_materiaux.jpg")
    plt.close()

if __name__ == "__main__":
    compare_materials()
    for key in MATERIALS:
        val = compute_alpha(10.0, key)
        print(f"{MATERIALS[key]['name']} (k=10) -> Alpha = {val.real:.2f} {val.imag:+.2f}j")