from math import sqrt
import numpy as np
import scipy.integrate as integr
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# On fixe les poids de l'écart sur le champ et sur ses variations spatiales.
A = 1
B = 1
# On fixe le rapport des capacités thermiques du gaz.
gamma_p = 7/5
# On fixe la demi-largeur du modèle d'identification en mètres.
l = 2.5
# On fixe la longueur du modèle d'identification en mètres.
L = 10
# On choisit le pas utilisé pour définir le nombre de modes conservés.
delta_x = 0.5
N = int(L/delta_x)
# On conserve le pas fréquentiel de référence en hertz.
ecart = 1

# On fixe la masse volumique de l'air en kilogrammes par mètre cube.
rho0 = 1.2
# On fixe la célérité de l'air en mètres par seconde.
c0 = 343
# On calcule le coefficient temporel à partir de la célérité de l'air.
xi0 = c0**(-2)
# On choisit le coefficient spatial de référence dans l'air.
eta0 = 1
# On calcule la première fréquence de coupure du modèle d'identification.
fc = c0/(2*l)


# Chaque matériau est décrit par sa porosité, sa tortuosité et sa résistivité dans cet ordre.
MATERIAUX = {"MELAMINE" : (0.99, 1.02, 14000.0),
             "ISOREL" : (0.70, 1.15, 142300.0),
             "ITFH" : (0.94, 1.0, 9067.0),
             "B5" : (0.20, 1.22, 2124000.0),
             "LAINE_ROCHE" : (0.97, 1.1, 30000),
             "LAINE_VERRE" : (0.99, 1.1 ,20000),
             "OUATE_POLYESTER" :(0.9, 1.05, 15000)}

def materiau(car_mat):
    """On transforme les caractéristiques du matériau en coefficients du modèle poreux."""

    # On lit la porosité, la tortuosité et la résistivité dans cet ordre.
    phi = car_mat[0]
    alpha_h = car_mat[1]
    sigma = car_mat[2]
    return (phi/alpha_h, sigma*(phi**2)*gamma_p/((c0**2)*rho0*alpha_h), phi*gamma_p/(c0**2))


def g1(y, omega):
    """On renvoie un profil de source uniforme."""
    return 1

def g2(y, omega):
    """On renvoie un profil de source gaussien centré sur le bord."""
    # On choisit la largeur du profil à partir de la largeur du bord.
    s = l/5
    return np.exp(-y**2/(2*s**2))

def g3(y, omega):
    """On renvoie un profil oscillant dont le mode dépend de la pulsation."""

    # On choisit le nombre d'oscillations spatiales à la pulsation fournie.
    m = int(omega*l/(np.pi*c0))
    return np.cos(m*np.pi/l*y)

def g_k(g,k,omega):
    """On calcule un coefficient de Fourier en séparant ses parties réelle et imaginaire."""

    # On effectue les deux intégrations réelles nécessaires au coefficient complexe.
    Re = integr.quad(g, -l, l, args= (omega,), weight='cos', wvar= k)[0]
    Im = integr.quad(g, -l, l, args= (omega,), weight='sin', wvar= k)[0]
    return (Re-Im*1j)/(2*l)

def coefficients(omega, g, mat):
    """On prépare les coefficients de source et de propagation pour chaque mode."""

    tab_k = []
    tab_fourier = []
    tab_l0 = []
    tab_l1 = []
    # On parcourt les modes dans les deux sens du développement de Fourier.
    for n in range(-N, N+1):
        k = n*np.pi/l
        tab_k.append(k)
        tab_fourier.append(g_k(g, k, omega))
        tab_l0.append(lambda0(k, omega))
        tab_l1.append(lambda1(k, omega, mat))
    return tab_k, tab_fourier, tab_l0, tab_l1


def lambda0(k, omega):
    """On calcule la propagation ou la décroissance d'un mode dans l'air."""
    # On distingue la décroissance spatiale d'une propagation oscillante.
    if k**2 >= xi0*omega**2/eta0:
        return sqrt(k**2-xi0*omega**2/eta0)
    else:
        return sqrt(xi0*omega**2/eta0-k**2)*1j

def lambda1(k, omega, mat):
    """On calcule le coefficient complexe de propagation dans le matériau poreux."""
    return 1/sqrt(2)*sqrt(k**2 - mat[2]*omega**2/mat[0] + sqrt((k**2 - mat[2]*omega**2/mat[0])**2 + (mat[1]*omega/mat[0])**2)) - 1/sqrt(2)*sqrt(mat[2]*omega**2/mat[0] - k**2 + sqrt((k**2 - mat[2]*omega**2/mat[0])**2 + (mat[1]*omega/mat[0])**2))*1j

def f(x, l0):
    """On calcule le dénominateur associé à la propagation d'un mode."""
    return (l0*eta0 - x)*np.exp(-l0*L) + (l0*eta0 + x)*np.exp(l0*L)

def chi(alpha, gk, mat, l0, l1):
    """On calcule la première composante de l'écart entre les deux champs."""
    return gk*((l0*eta0-l1*mat[0])/f(l1*mat[0], l0) - (l0*eta0-alpha)/f(alpha, l0))

def gamma(alpha, gk, mat, l0, l1):
    """On calcule la seconde composante de l'écart entre les deux champs."""
    return gk*((l0*eta0+l1*mat[0])/f(l1*mat[0], l0) - (l0*eta0+alpha)/f(alpha, l0))

def e_k(alpha, k, omega, gk, mat, l0, l1):
    """On calcule la contribution d'un mode à l'écart énergétique entre les deux modèles."""
    # On calcule les deux composantes de l'écart de champ pour ce mode.
    c = chi(alpha, gk, mat, l0, l1)
    g = gamma(alpha, gk, mat, l0, l1)
    # On utilise l'expression adaptée au comportement du mode dans l'air.
    if k**2 >= xi0*omega**2/eta0:
        return (A+B*np.abs(k)**2) * (1/(2*l0) * (np.abs(c)**2*(1-np.exp(-2*l0*L)) + np.abs(g)**2*(np.exp(2*l0*L)-1)) + 2*L*np.real(c*np.conj(g))) + B*l0/2 * (np.abs(c)**2*(1-np.exp(-2*l0*L)) + np.abs(g)**2*(np.exp(2*l0*L)-1)) - 2*B*l0**2*L*np.real(c*np.conj(g))
    else :
        return (A+B*np.abs(k)**2) * (L*(np.abs(c)**2+np.abs(g)**2) + np.imag(c*np.conj(g)*(1-np.exp(-2*l0*L)))/l0*1j) + B*L*np.abs(l0)**2*(np.abs(c)**2+np.abs(g)**2) + B*l0*np.imag(c*np.conj(g)*(1-np.exp(-2*l0*L)))*1j


def erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):
    """On additionne les écarts énergétiques de tous les modes."""
    e = 0
    # On associe à chaque mode ses coefficients déjà préparés.
    for k, gk, l0, l1 in zip(tab_k, tab_fourier, tab_l0, tab_l1):
        e += e_k(alpha, k, omega, gk, mat, l0, l1)
    return e


# On fixe le point de départ de la recherche du coefficient complexe.
Alpha0 = [50, -50]


def passage_CetR(alpha_reel, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):
    """On reconstruit un coefficient complexe à partir de ses deux parties réelles."""

    # On utilise deux inconnues réelles pour permettre la minimisation numérique.
    alpha = alpha_reel[0]+alpha_reel[1]*1j
    e = erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1)
    # On garde la partie réelle de l'écart évalué.
    return np.real(e)

def compute_alpha(omega, g, car_mat, alpha0):
    """On recherche le coefficient de paroi qui minimise l'écart avec le modèle poreux."""

    # On transforme les caractéristiques du matériau avant la recherche.
    mat = materiau(car_mat)
    # On prépare une seule fois les quantités indépendantes du coefficient recherché.
    tab_k, tab_fourier, tab_l0, tab_l1 = coefficients(omega, g, mat)
    # On cherche les deux parties du coefficient avec la méthode de Nelder et Mead.
    res = opt.minimize(passage_CetR, alpha0, args= (omega, mat, tab_k, tab_fourier, tab_l0, tab_l1), method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-10})
    # On renvoie le coefficient trouvé et les informations de fin de recherche.
    return res.x, res.success, res.message
