# -*- coding: utf-8 -*-
# Fichier : compute_alpha.py (modèle coursebook / dossier support avec OUATE_POLYESTER)

from math import sqrt
import numpy as np
import scipy.integrate as integr
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

#### Paramètres du modèle du coursebook (support) ###

A = 1
B = 1
gamma_p = 7 / 5
l = 2.5        # m
L = 10         # m
delta_x = 0.5  # m
N = int(L / delta_x)
ecart = 1      # Hz

# Air #
rho0 = 1.2     # kg*m**(-3)
c0 = 343       # m*s**(-1)
xi0 = c0**(-2) # s**2*m**(-2)
eta0 = 1       # sans dimension selon la convention du coursebook
fc = c0 / (2 * l)

# Matériaux du dossier support : (phi, alpha_h, sigma) #
MATERIAUX = {
    "MELAMINE": (0.99, 1.02, 14000.0),
    "ISOREL": (0.70, 1.15, 142300.0),
    "ITFH": (0.94, 1.0, 9067.0),
    "B5": (0.20, 1.22, 2124000.0),
    "LAINE_ROCHE": (0.97, 1.1, 30000),
    "LAINE_VERRE": (0.99, 1.1, 20000),
    "OUATE_POLYESTER": (0.9, 1.05, 15000),
}

# Alias de compatibilité avec les scripts des jours 1 à 4
MATERIAL_ALIASES = {
    "OUATE_POLYESTER": "OUATE_POLYESTER",
    "ouate_polyester": "OUATE_POLYESTER",
    "hemp_fiber": "OUATE_POLYESTER",
    "LAINE_ROCHE": "LAINE_ROCHE",
    "rock_wool": "LAINE_ROCHE",
    "LAINE_VERRE": "LAINE_VERRE",
    "MELAMINE": "MELAMINE",
    "melamine_foam": "MELAMINE",
    "ISOREL": "ISOREL",
    "ITFH": "ITFH",
    "B5": "B5",
}


def materiau(car_mat):
    """Calcul des paramètres liés au matériau en fonction de la porosité, la tortuosité et la résistivité à l'air.
    Le matériau est représenté par le triplet car_mat = (phi, alpha_h, sigma) avant d'être transformé par cette fonction.
    Les formules sont tirées du coursebook p.38."""
    phi = car_mat[0]
    alpha_h = car_mat[1]
    sigma = car_mat[2]
    return (
        phi / alpha_h,
        sigma * (phi**2) * gamma_p / ((c0**2) * rho0 * alpha_h),
        phi * gamma_p / (c0**2),
    )  # dans l'ordre : eta1, a et xi1


### Fonctions et Fourier ###

def g1(y, omega):
    """g1 est indépendante de y et le S(omega) défini dans le rapport ne rentre pas
    en compte dans le calcul du alpha et ne nécessite donc pas d'être codé."""
    return 1


def g2(y, omega):
    s = l / 5
    return np.exp(-y**2 / (2 * s**2))


def g3(y, omega):
    """Dans cette modélisation, les variables ne sont pas séparables et le terme m(omega) a un impact sur alpha."""
    m = int(omega * l / (np.pi * c0))
    return np.cos(m * np.pi / l * y)


def g_k(g, k, omega):
    """Calcul des coefficients de Fourier via la fonction quad de scipy.integrate."""
    if g is g1:
        return 1.0 + 0.0j if abs(k) < 1e-14 else 0.0 + 0.0j
    Re = integr.quad(g, -l, l, args=(omega,), weight='cos', wvar=k)[0]
    Im = integr.quad(g, -l, l, args=(omega,), weight='sin', wvar=k)[0]
    return (Re - Im * 1j) / (2 * l)


def coefficients(omega, g, mat):
    """Cette fonction détermine les coefficients de Fourier de g selon y à la
    pulsation omega dans un milieu représenté par le triplet (eta1, a, xi1)."""
    tab_k = []
    tab_fourier = []
    tab_l0 = []
    tab_l1 = []
    for n in range(-N, N + 1):
        k = n * np.pi / l
        tab_k.append(k)
        tab_fourier.append(g_k(g, k, omega))
        tab_l0.append(lambda0(k, omega))
        tab_l1.append(lambda1(k, omega, mat))
    return tab_k, tab_fourier, tab_l0, tab_l1


### Coefficients du théorème ###

def lambda0(k, omega):
    if k**2 >= xi0 * omega**2 / eta0:
        return sqrt(k**2 - xi0 * omega**2 / eta0)
    else:
        return sqrt(xi0 * omega**2 / eta0 - k**2) * 1j


def lambda1(k, omega, mat):
    term = k**2 - mat[2] * omega**2 / mat[0]
    hypot = np.sqrt(term**2 + (mat[1] * omega / mat[0])**2)
    re = (1.0 / np.sqrt(2.0)) * np.sqrt(term + hypot)
    im = (1.0 / np.sqrt(2.0)) * np.sqrt(-term + hypot)
    return re - im * 1j


def f(x, l0):
    return (l0 * eta0 - x) * np.exp(-l0 * L) + (l0 * eta0 + x) * np.exp(l0 * L)


def chi(alpha, gk, mat, l0, l1):
    return gk * ((l0 * eta0 - l1 * mat[0]) / f(l1 * mat[0], l0) - (l0 * eta0 - alpha) / f(alpha, l0))


def gamma(alpha, gk, mat, l0, l1):
    return gk * ((l0 * eta0 + l1 * mat[0]) / f(l1 * mat[0], l0) - (l0 * eta0 + alpha) / f(alpha, l0))


def e_k(alpha, k, omega, gk, mat, l0, l1):
    if abs(gk) == 0.0:
        return 0.0
    c = chi(alpha, gk, mat, l0, l1)
    g = gamma(alpha, gk, mat, l0, l1)
    if k**2 >= xi0 * omega**2 / eta0:
        return (
            (A + B * np.abs(k)**2) * (1 / (2 * l0) * (np.abs(c)**2 * (1 - np.exp(-2 * l0 * L)) + np.abs(g)**2 * (np.exp(2 * l0 * L) - 1)) + 2 * L * np.real(c * np.conj(g)))
            + B * l0 / 2 * (np.abs(c)**2 * (1 - np.exp(-2 * l0 * L)) + np.abs(g)**2 * (np.exp(2 * l0 * L) - 1))
            - 2 * B * l0**2 * L * np.real(c * np.conj(g))
        )
    else:
        return (
            (A + B * np.abs(k)**2) * (L * (np.abs(c)**2 + np.abs(g)**2) + np.imag(c * np.conj(g) * (1 - np.exp(-2 * l0 * L))) / l0 * 1j)
            + B * L * np.abs(l0)**2 * (np.abs(c)**2 + np.abs(g)**2)
            + B * l0 * np.imag(c * np.conj(g) * (1 - np.exp(-2 * l0 * L))) * 1j
        )


### Définition du terme d'erreur à minimiser ###

def erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):
    e = 0
    for k, gk, l0, l1 in zip(tab_k, tab_fourier, tab_l0, tab_l1):
        if abs(gk) > 0.0:
            e += e_k(alpha, k, omega, gk, mat, l0, l1)
    return e


### Détermination du alpha optimal ###

Alpha0 = [50, -50]


def passage_CetR(alpha_reel, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):
    alpha = alpha_reel[0] + alpha_reel[1] * 1j
    e = erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1)
    return np.real(e)


def compute_alpha(omega_or_k, g=None, car_mat=None, alpha0=None, material_key="OUATE_POLYESTER", c0=343.0):
    """
    Compatible à la fois avec :
    1. La signature du dossier support :
       compute_alpha(omega, g1, MATERIAUX["OUATE_POLYESTER"], Alpha0) -> (res.x, res.success, res.message)
    2. L'appel vectorisé par nombre d'onde k = omega / c0 :
       compute_alpha(k_vals, material_key="OUATE_POLYESTER", c0=343.0) -> complexe ou tableau complexe Alpha
    """
    if callable(g) and car_mat is not None:
        if alpha0 is None:
            alpha0 = Alpha0
        mat = materiau(car_mat)
        tab_k, tab_fourier, tab_l0, tab_l1 = coefficients(omega_or_k, g, mat)
        res = opt.minimize(
            passage_CetR, alpha0,
            args=(omega_or_k, mat, tab_k, tab_fourier, tab_l0, tab_l1),
            method='Nelder-Mead',
            options={'xatol': 1e-6, 'fatol': 1e-10}
        )
        return res.x, res.success, res.message

    # Mode direct par nombre d'onde k (ou tableau de nombres d'onde) pour g = g1
    if isinstance(g, str):
        material_key = g
    mat_name = MATERIAL_ALIASES.get(material_key, "OUATE_POLYESTER")
    car = MATERIAUX[mat_name]
    mat = materiau(car)
    omega = np.asarray(omega_or_k, dtype=np.float64) * float(c0)
    # Pour g1(y) = 1, seul le mode de Fourier k = 0 est non nul et le minimum exact de e(alpha) = 0 est lambda1(0, omega, mat) * eta1
    alpha_val = lambda1(0.0, omega, mat) * mat[0]
    if np.ndim(omega_or_k) == 0:
        return complex(alpha_val)
    return alpha_val
