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
             "B5" : (0.20, 1.22, 2124000.0)}

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

Alpha0 = [50, -50]  # l'algorithme étant robuste, l'alpha0 n'est pas important et j'en ai donc mis un ici simplement
                    # pour ne pas réécrire un couple de départ à chaque test

def passage_CetR(alpha_reel, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1):

    """La fonction minimize prend en compte des vecteurs réels or on a écrit alpha sous forme complexe jusqu'ici.
    Cette fonction permet donc de passer d'alpha sous forme de couple [Reel, Imaginaire] à sa forme complexe pour calculer l'erreur.
    l'erreur est censé être réelle mais l'ordinateur pourrait afficher une partie réelle extremement faible par erreur. On prend la
    partie réelle pour éviter cela."""
    
    alpha = alpha_reel[0]+alpha_reel[1]*1j
    e = erreur(alpha, omega, mat, tab_k, tab_fourier, tab_l0, tab_l1)
    return np.real(e)

def alpha_opt(omega, g, car_mat, alpha0):
    
    """ On détermine ici le paramètre alpha optimal en fonction de la pulsation (qui n'a pas forcément d'impact), de la fonction g et du materiau.
    Il faut donner un point de départ alpha0 mais l'algorithme est assez robuste pour trouver le bon alpha qu'import le point de départ."""
    
    mat = materiau(car_mat)
    tab_k, tab_fourier, tab_l0, tab_l1 = coefficients(omega, g, mat)   # Les coefficients de fourier, les lambda0 et les lambda1 étant indépendants de alpha, on les calcule avant de rentrer dans l'optimisation.
    res = opt.minimize(passage_CetR, alpha0, args= (omega, mat, tab_k, tab_fourier, tab_l0, tab_l1), method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-10})
    return res.x, res.success, res.message              

# alpha_opt renvoie le alpha optimal determiner par l'algorithme mais celui-ci n'est pas forcément fiable
# c'est pourquoi on renvoie success (booléen) indiquant si l'algorithme considère le alpha comme fiable.
# Si ce n'est pas le cas, message donne la raison de cette erreur (ex: trop d'itérations).

### Alpha comme fonction de la fréquence (Q3) ###

def courbe(milieu, alpha0): 
    """On trace ici les parties réelle et imaginaire de alpha selon la fréquence pour les trois fonctions g."""

    car_mat = MATERIAUX[milieu]                 # on extrait le triplet des caractéristiques du milieu poreux
    mat = materiau(car_mat)                     # on calcule les paramètres correspondant pour déterminer les solutions théoriques indépendamment de l'algorithme sur α         
    Frequences = np.arange(100, 4001, 10, dtype=float)
    distance = np.abs(Frequences - fc*np.round(Frequences/fc))
    filtre = distance > ecart
    Frequences = Frequences[filtre]             # les lignes 156 à 158 servent à éviter les fréquences multiples de fc (ligne 24) pouvant amener à des divisions par 0
    depart1 = alpha0                            # pour chaque nouvelle pulsation on prend le alpha de la pulsation précédente pour avoir un algorithme plus rapide
    depart2 = alpha0                            # c'est vrai pour g1 et g2, mais pas g3 comme g3 dépend de omega, on garde donc le même départ pour g3
    tab_alpha1 = []
    tab_alpha2 = []
    tab_alpha3 = []
    tab_m = []
    #Relambda1eta10 = []                         # le alpha optimal théorique est lambda1(0, omega, mat)*eta1(mat)
    #Imlambda1eta10 = []                         # on trace donc aussi ces valeurs pour tester la validité et la précision du modèle
    #Relambda1eta1m = []                         # le alpha optimal théorique est lambda1(m(omega), omega, mat)*eta1(mat)
    #Imlambda1eta1m = []                         # on trace donc aussi ces valeurs pour tester la validité et la précision du modèle

    for freq in Frequences:
        omega = 2*np.pi*freq

        # determination de alpha pour g1 et comparaison à la valeur théorique
        # l1eta10 = lambda1(0,omega, mat)*mat[0]
        # Relambda1eta10.append(np.real(l1eta10))
        # Imlambda1eta10.append(np.imag(l1eta10))
        res1 = alpha_opt(omega, g1, car_mat, depart1)  
        if res1[1]==True:                       # on vérifie l'intéret du α (optimal ou non)
            tab_alpha1.append(res1[0])
            depart1 = res1[0]
        else:
            tab_alpha1.append([np.nan, np.nan])
            print(freq,res1[2])
        
        # détermination pour g2    
        res2 = alpha_opt(omega, g2, car_mat, depart2)
        if res2[1]==True:
            tab_alpha2.append(res2[0])
            depart2 = res2[0]
        else:
            tab_alpha2.append([np.nan, np.nan])
            print(freq,res2[2])
        
        # determination de alpha pour g3 et comparaison à la valeur théorique
        m = int(omega*l/(np.pi*c0))
        tab_m.append(m)
        #l1eta1m = lambda1(m*np.pi/l,omega,mat)*mat[0] 
        #Relambda1eta1m.append(np.real(l1eta1m))       
        #Imlambda1eta1m.append(np.imag(l1eta1m))       
        res3 = alpha_opt(omega, g3, car_mat, alpha0)
        if res3[1]==True:
            tab_alpha3.append(res3[0])
        else:
            tab_alpha3.append([np.nan, np.nan])
            print(freq,res3[2])
        

    tab_alpha1 = np.array(tab_alpha1)
    tab_alpha2 = np.array(tab_alpha2)
    tab_alpha3 = np.array(tab_alpha3)
    tab_m = np.array(tab_m)
    indices = np.where(np.diff(tab_m) != 0)[0]         # alpha(g3) présente des discontinuitées lorsque m(omega) change de valeurs.
    freq3 = np.insert(Frequences, indices+1, np.nan)   # On empeche donc de relier dans ces cas là avec des NAN
    tab_alpha3 = np.insert(tab_alpha3, indices+1, np.nan, axis=0)
    #Relambda1eta1m = np.insert(np.array(Relambda1eta1m), indices+1, np.nan)
    #Imlambda1eta1m = np.insert(np.array(Imlambda1eta1m), indices+1, np.nan)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(Frequences, tab_alpha1[:,0], label='g1')
    ax1.plot(Frequences, tab_alpha2[:,0], label='g2')
    ax1.plot(freq3, tab_alpha3[:,0], label='g3')
    #ax1.plot(Frequences, Relambda1eta10, label='Re(lambda1(0,omega)*eta1)')
    #ax1.plot(freq3, Relambda1eta1m, label='Re(lambda1(m(omega),omega)*eta1)')
    ax1.set_xlabel("frequence (en Hz)", fontsize=10)
    ax1.set_ylabel("Re(α) (en m**(-1))", fontsize=10)
    ax1.xaxis.set_minor_locator(MultipleLocator(100))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.grid(True, which='minor', alpha=0.3)
    ax1.grid(True, which='major', alpha=0.3)
    ax1.legend(fontsize=10)
    
    ax2.plot(Frequences, tab_alpha1[:,1], label='g1')
    ax2.plot(Frequences, tab_alpha2[:,1], label='g2')
    ax2.plot(freq3, tab_alpha3[:,1], label='g3')
    #ax2.plot(Frequences, Imlambda1eta10, label='Im(lambda1(0,omega)*eta1)')
    #ax2.plot(freq3, Imlambda1eta1m, label='Im(lambda1(m(omega),omega)*eta1)')
    ax2.set_xlabel("frequence (en Hz)", fontsize=10)
    ax2.set_ylabel("Im(α) (en m**(-1))", fontsize=10)
    ax2.xaxis.set_minor_locator(MultipleLocator(100))
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.grid(True, which='minor', alpha=0.3)
    ax2.grid(True, which='major', alpha=0.3)
    fig.suptitle(f"α en fonction de la fréquence dans les trois situations avec {milieu}", fontsize=16)
    plt.show()

# Pour apeller cette fonction, on utilisera un milieu inscrit dans le dictionnaire MATERIAUX
# car "courbe" cherche le triplet de caractéristiques (phi, alpha_h, sigma) de milieu dans le dictionnaire.
# Pour tester un nouveau milieu, il suffit donc de l'ajouter au dictionnaire.

### Comparaison pour différents matériaux (Q4) ###

def courbe_g_diff_mat(materiaux, alpha0, g):
    """ Cette fonction sert à comparer α(freq) pour différents matériaux présents dans le coursebook p.38 pour g1 ou g2.
    La situation de discontinuité avec g3 n'étant pas pratique à gérer dans ce cas (avec g en argument), une fonction 
    presque similaire spécifique à g3 suit celle-ci."""
    Frequences = np.arange(100, 4001, 10)
    distance = np.abs(Frequences - fc*np.round(Frequences/fc))
    filtre = distance > ecart
    Frequences = Frequences[filtre]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
     
    for nom, car_mat in materiaux.items():
        depart = alpha0                                # on recommence au même point de départ pour chaque matériau
        tab_alpha = []
        for freq in Frequences: 
            omega = 2*np.pi*freq
            k = omega/c0
            res = alpha_opt(omega, g, car_mat, depart)
            if res[1]==True:
                tab_alpha.append(res[0])
                depart = res[0]
            else:
                tab_alpha.append([np.nan, np.nan])
                print(freq,res[2])
        tab_alpha = np.array(tab_alpha)
        ax1.plot(Frequences, tab_alpha[:,0], label= nom)
        ax2.plot(Frequences, tab_alpha[:,1], label= nom)
    
    ax1.set_xlabel("frequence (en Hz)", fontsize=10)
    ax1.set_ylabel("Re(α) (en m**(-1))", fontsize=10)
    ax1.xaxis.set_minor_locator(MultipleLocator(100))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.grid(True, which='minor', alpha=0.3)
    ax1.grid(True, which='major', alpha=0.3)
    ax1.legend(fontsize=10)
    
    ax2.set_xlabel("frequence (en Hz)", fontsize=10)
    ax2.set_ylabel("Im(α) (en m**(-1))", fontsize=10)
    ax2.xaxis.set_minor_locator(MultipleLocator(100))
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.grid(True, which='minor', alpha=0.3)
    ax2.grid(True, which='major', alpha=0.3)
    fig.suptitle(f"α en fonction de la fréquence pour différents matériaux avec {g.__name__}", fontsize=16)
    plt.show()

def courbe_g3_diff_mat(materiaux, alpha0): 
    """ Même fonction adaptant le cas spécifique de g3"""
    
    Frequences = np.arange(100, 4001, 10, dtype= float)
    distance = np.abs(Frequences - fc*np.round(Frequences/fc))
    filtre = distance > ecart
    Frequences = Frequences[filtre]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    tab_m = (2*Frequences*l/c0).astype(int)
    tab_m = np.array(tab_m)
    indices = np.where(np.diff(tab_m) != 0)[0]         
    Freq_plot = np.insert(Frequences, indices+1, np.nan)   
    for nom, car_mat in materiaux.items():
        depart = alpha0
        tab_alpha = []
        for freq in Frequences: 
            omega = 2*np.pi*freq
            res = alpha_opt(omega, g3, car_mat, depart)
            if res[1]==True:
                tab_alpha.append(res[0])
            else:
                tab_alpha.append([np.nan, np.nan])
                print(freq,res[2])
        tab_alpha = np.array(tab_alpha)
        tab_alpha = np.insert(tab_alpha, indices+1, np.nan, axis=0)
        ax1.plot(Freq_plot, tab_alpha[:,0], label= nom)
        ax2.plot(Freq_plot, tab_alpha[:,1], label= nom)
    
    ax1.set_xlabel("frequence (en Hz)", fontsize=10)
    ax1.set_ylabel("Re(α) (en m**(-1))", fontsize=10)
    ax1.xaxis.set_minor_locator(MultipleLocator(100))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.grid(True, which='minor', alpha=0.3)
    ax1.grid(True, which='major', alpha=0.3)
    ax1.legend(fontsize=10)
    
    ax2.set_xlabel("frequence (en Hz)", fontsize=10)
    ax2.set_ylabel("Im(α) (en m**(-1))", fontsize=10)
    ax2.xaxis.set_minor_locator(MultipleLocator(100))
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.grid(True, which='minor', alpha=0.3)
    ax2.grid(True, which='major', alpha=0.3)
    fig.suptitle("α en fonction de la fréquence pour différents matériaux avec g3", fontsize=16)
    plt.show()

# Ces deux fonctions utilisent ici le dictionnaire comme argument. Plutôt que l'appeler automatiquement
# le dictionnaire est en argument si le lecteur souhaite utiliser un autre dictionnaire qu'il peut ajouter


# Tracé des coefficients d'absorption #

def absorption(materiaux, alpha0, g):
    """Fonction similaire aux précédentes mais on y trace les coefficients d'absorption pour la comparaison"""
    Frequences = np.arange(100, 4001, 10)
    distance = np.abs(Frequences - fc*np.round(Frequences/fc))
    filtre = distance > ecart
    Frequences = Frequences[filtre]
     
    for nom, car_mat in materiaux.items():
        depart = alpha0                                
        tab_absorption = []
        for freq in Frequences: 
            omega = 2*np.pi*freq
            K = omega/c0
            res = alpha_opt(omega, g, car_mat, depart)
            if res[1]==True:
                re_alpha_abs = np.abs(res[0][0])
                im_alpha_abs = np.abs(res[0][1])
                ab = 4*K*im_alpha_abs/(re_alpha_abs**2+(K+im_alpha_abs)**2)
                tab_absorption.append(ab)
            else:
                print(freq,res[2])
        tab_absorption = np.array(tab_absorption)
        plt.plot(Frequences, tab_absorption, label=nom) 
        ax = plt.gca()  
    
    plt.xlabel("frequence (en Hz)", fontsize=10)
    plt.ylabel("coefficient d'absorption", fontsize=10)
    ax.xaxis.set_minor_locator(MultipleLocator(100))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    plt.grid(True, which='minor', alpha=0.3)
    plt.grid(True, which='major', alpha=0.3)
    plt.legend(fontsize=10)
    plt.title(f"coefficient d'absorption en fonction de la fréquence pour différents matériaux avec {g.__name__}", fontsize=16)
    plt.show()

def absorption_g3(materiaux, alpha0): 
    """ Même fonction adaptant le cas spécifique de g3"""
    
    Frequences = np.arange(100, 4001, 10, dtype= float)
    distance = np.abs(Frequences - fc*np.round(Frequences/fc))
    filtre = distance > ecart
    Frequences = Frequences[filtre]
    tab_m = (2*Frequences*l/c0).astype(int)
    tab_m = np.array(tab_m)
    indices = np.where(np.diff(tab_m) != 0)[0]         
    Freq_plot = np.insert(Frequences, indices+1, np.nan)   
    for nom, car_mat in materiaux.items():
        depart = alpha0
        tab_absorption = []
        for freq in Frequences: 
            omega = 2*np.pi*freq
            K = ((omega/c0)**2 - ((2*freq*l/c0).astype(int)*np.pi/l)**2)**(1/2)
            res = alpha_opt(omega, g3, car_mat, depart)
            if res[1]==True:
                re_alpha_abs = np.abs(res[0][0])
                im_alpha_abs = np.abs(res[0][1])
                ab = 4*K*im_alpha_abs/(re_alpha_abs**2+(K+im_alpha_abs)**2)
                tab_absorption.append(ab)
            else:
                print(freq,res[2])
            tab_absorption = np.array(tab_absorption)
            plt.plot(Freq_plot, tab_absorption, label=nom)
            ax = plt.gca()

    plt.xlabel("frequence (en Hz)", fontsize=10)
    plt.ylabel("Re(α) (en m**(-1))", fontsize=10)
    ax.xaxis.set_minor_locator(MultipleLocator(100))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    plt.grid(True, which='minor', alpha=0.3)
    plt.grid(True, which='major', alpha=0.3)
    plt.legend(fontsize=10)
    plt.show()
    
print(absorption(MATERIAUX, Alpha0, g1))