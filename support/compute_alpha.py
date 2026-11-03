from math import sqrt
import numpy as np
import scipy.integrate as integr
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

#### Paramètres ###

A = 1
B = 1
gamma_p = 7/5
l = 2.5        # m
L = 10        # m
delta_x = 0.5  # m
N = int(L/delta_x)
ecart = 1      # Hz
# air #
rho0 = 1.2     # kg*m**(-3)
c0 = 343       # m*s**(-1)
xi0 = c0**(-2) # s**2*m**(-2)
eta0 = 1       # sans dimension selon la convention du coursebook
fc = c0/(2*l)

# materiaux #

MATERIAUX = {"MELAMINE" : (0.99, 1.02, 14000.0),
             "ISOREL" : (0.70, 1.15, 142300.0),
             "ITFH" : (0.94, 1.0, 9067.0),
             "B5" : (0.20, 1.22, 2124000.0),
             "LAINE_ROCHE" : (0.97, 1.1, 30000),
             "LAINE_VERRE" : (0.99, 1.1 ,20000),
             "OUATE_POLYESTER" :(0.9, 1.05, 15000)}

def materiau(car_mat):
    """Calcul des paramètres liés au matériau en fonction de la porosité, la tortuosité et la résistivité à l'air.
    Le materiau est représenta par le triplet car_mat = (phi, alpha_h, sigma) avant d'être transformé par cette fonction.
    Les formules sont tirés du coursebook p.38"""
    
    phi = car_mat[0]
    alpha_h = car_mat[1]
    sigma = car_mat[2]
    return (phi/alpha_h, sigma*(phi**2)*gamma_p/((c0**2)*rho0*alpha_h), phi*gamma_p/(c0**2))  # dans l'ordre : eta1, a et xi1


### Fonctions et Fourier ###

def g1(y, omega):
    """g1 est indépendante de y et le S(omega) défini dans le raport ne rentre pas 
    en compte dans le calcul du alpha et ne nécessite donc pas d'être codé."""
    return 1

def g2(y, omega):   # même chose concernant S(omega).
    s = l/5
    return np.exp(-y**2/(2*s**2))

def g3(y, omega): 
    """Dans cette modélisation, les variables ne sont pas séparables et le terme m(omega) a un impact sur alpha."""
    
    m = int(omega*l/(np.pi*c0))
    return np.cos(m*np.pi/l*y)

def g_k(g,k,omega):
    """Calcul des coefficients de Fourier via la fonction quad de scipy.integrate.
    La fonction quad prend en argument des fonctions réelles. On décompose donc l'exponentielle complexe."""
    
    Re = integr.quad(g, -l, l, args= (omega,), weight='cos', wvar= k)[0]
    Im = integr.quad(g, -l, l, args= (omega,), weight='sin', wvar= k)[0]
    return (Re-Im*1j)/(2*l)

def coefficients(omega, g, mat):
    """Cette fonction détermine les coefficients de Fourier de g selon y à la 
    pulsation omega dans un milieu représenté par le triplet (eta1, a, xi1)."""
    
    tab_k = []
    tab_fourier = []
    tab_l0 = []
    tab_l1 = []
    for n in range(-N, N+1):
        k = n*np.pi/l
        tab_k.append(k)
        tab_fourier.append(g_k(g, k, omega))
        tab_l0.append(lambda0(k, omega))
        tab_l1.append(lambda1(k, omega, mat))
    return tab_k, tab_fourier, tab_l0, tab_l1

### Coefficients du théorème ###

def lambda0(k, omega):
    if k**2 >= xi0*omega**2/eta0:
        return sqrt(k**2-xi0*omega**2/eta0)
    else:
        return sqrt(xi0*omega**2/eta0-k**2)*1j

def lambda1(k, omega, mat):
    return 1/sqrt(2)*sqrt(k**2 - mat[2]*omega**2/mat[0] + sqrt((k**2 - mat[2]*omega**2/mat[0])**2 + (mat[1]*omega/mat[0])**2)) - 1/sqrt(2)*sqrt(mat[2]*omega**2/mat[0] - k**2 + sqrt((k**2 - mat[2]*omega**2/mat[0])**2 + (mat[1]*omega/mat[0])**2))*1j

def f(x, l0):
    return (l0*eta0 - x)*np.exp(-l0*L) + (l0*eta0 + x)*np.exp(l0*L)

def chi(alpha, gk, mat, l0, l1):
    return gk*((l0*eta0-l1*mat[0])/f(l1*mat[0], l0) - (l0*eta0-alpha)/f(alpha, l0))

def gamma(alpha, gk, mat, l0, l1):
    return gk*((l0*eta0+l1*mat[0])/f(l1*mat[0], l0) - (l0*eta0+alpha)/f(alpha, l0))

def e_k(alpha, k, omega, gk, mat, l0, l1):
    c = chi(alpha, gk, mat, l0, l1)
    g = gamma(alpha, gk, mat, l0, l1)    
    if k**2 >= xi0*omega**2/eta0:
        return (A+B*np.abs(k)**2) * (1/(2*l0) * (np.abs(c)**2*(1-np.exp(-2*l0*L)) + np.abs(g)**2*(np.exp(2*l0*L)-1)) + 2*L*np.real(c*np.conj(g))) + B*l0/2 * (np.abs(c)**2*(1-np.exp(-2*l0*L)) + np.abs(g)**2*(np.exp(2*l0*L)-1)) - 2*B*l0**2*L*np.real(c*np.conj(g)) 
    else :
        return (A+B*np.abs(k)**2) * (L*(np.abs(c)**2+np.abs(g)**2) + np.imag(c*np.conj(g)*(1-np.exp(-2*l0*L)))/l0*1j) + B*L*np.abs(l0)**2*(np.abs(c)**2+np.abs(g)**2) + B*l0*np.imag(c*np.conj(g)*(1-np.exp(-2*l0*L)))*1j


### Définition du terme d'erreur à minimiser ###

def erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):
    e = 0
    for k, gk, l0, l1 in zip(tab_k, tab_fourier, tab_l0, tab_l1):
        e += e_k(alpha, k, omega, gk, mat, l0, l1)
    return e


### Determination du alpha optimal ###

Alpha0 = [50, -50]  # On choisit le point de départ dans la convention du polycopié.

def passage_CetR(alpha_reel, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):

    """La fonction minimize prend en compte des vecteurs réels or on a écrit alpha sous forme complexe jusqu'ici.
    Cette fonction permet donc de passer d'alpha sous forme de couple [Reel, Imaginaire] à sa forme complexe pour calculer l'erreur.
    l'erreur est censé être réelle mais l'ordinateur pourrait afficher une partie réelle extremement faible par erreur. On prend la
    partie réelle pour éviter cela."""
    
    alpha = alpha_reel[0]+alpha_reel[1]*1j
    e = erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1)
    return np.real(e)

def compute_alpha(omega, g, car_mat, alpha0):
    
    """ On détermine ici le paramètre alpha optimal en fonction de la pulsation (qui n'a pas forcément d'impact), de la fonction g et du materiau.
    On utilise le signe du polycopié pour le point de départ et le coefficient renvoyé.
    Le résultat contient les parties réelle et imaginaire, le succès et le message de la minimisation."""
    
    mat = materiau(car_mat)
    tab_k, tab_fourier, tab_l0, tab_l1 = coefficients(omega, g, mat)   # Les coefficients de fourier, les lambda0 et les lambda1 étant indépendants de alpha, on les calcule avant de rentrer dans l'optimisation.
    res = opt.minimize(passage_CetR, alpha0, args= (omega, mat, tab_k, tab_fourier, tab_l0, tab_l1), method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-10})
    return res.x, res.success, res.message              

# On vérifie le succès de la minimisation avant d’utiliser le coefficient.

### Alpha comme fonction de la fréquence (Q3) ###
