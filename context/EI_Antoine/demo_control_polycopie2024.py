# -*- coding: utf-8 -*-
"""On étudie les murs et les matériaux avec le programme d'Antoine."""
from pathlib import Path
import hashlib
import json
import numpy
import _env
import preprocessing
import processing
import postprocessing
import compute_alpha

N_POINTS = 128
LEVELS = (0, 1, 2, 3)
LEVEL = 3
MATERIALS = ("MELAMINE", "LAINE_ROCHE", "LAINE_VERRE", "OUATE_POLYESTER")
SOURCE = preprocessing.source_rer_b
G_SOURCE = compute_alpha.g1
C = 343.0
FREQUENCIES = numpy.arange(50.0, 2001.0, 5.0)
MODES = ("mono", "resonances", "bande50", "bande5")
N_ITERATIONS = 100
MU_INITIAL = 5.0
DELTA = 1e-5
MU_MIN = 1e-10
VOLUMES = (.1, .3, .5, .7, 1.0)
RESULTS = Path(__file__).resolve().parent / "resultats"


def your_compute_objective_function(domain_omega, u, spacestep):
    """On conserve la somme utilisée par Antoine sur les points du domaine."""
    mask = domain_omega != _env.NODE_COMPLEMENTARY
    return float(numpy.sum(numpy.abs(u[mask]) ** 2) * spacestep ** 2)


def frequency_weights(frequencies):
    """On reprend les poids des trapèzes normalisés utilisés par Antoine."""
    frequencies = numpy.asarray(frequencies, dtype=float)
    weights = numpy.ones(len(frequencies))
    if len(frequencies) > 1:
        weights[:] = 0
        for j in range(len(frequencies) - 1):
            weights[j] += (frequencies[j + 1] - frequencies[j]) / 2
            weights[j + 1] += (frequencies[j + 1] - frequencies[j]) / 2
        weights /= frequencies[-1] - frequencies[0]
    return weights


def prepare_frequencies(domain, spacestep, frequencies, c, material, g_source,
                        source=None, coefficient_cache=None):
    """On calcule les coefficients et les données de Dirichlet avant la descente."""
    source = SOURCE if source is None else source
    cache = {} if coefficient_cache is None else coefficient_cache
    frequencies = numpy.asarray(frequencies, dtype=float)
    alpha0 = compute_alpha.Alpha0
    alphas, f_dirs = [], []
    y = (numpy.arange(domain.shape[1]) - (domain.shape[1] - 1) / 2) * spacestep
    for frequency in frequencies:
        omega = 2 * numpy.pi * frequency
        if float(frequency) not in cache:
            pair, success, message = compute_alpha.compute_alpha(omega, g_source, material, alpha0)
            alpha = complex(*pair)
            if not success or not numpy.isfinite(alpha) or alpha.real <= 0 or alpha.imag >= 0:
                print("Coefficient non validé à", frequency, "Hz :", message, flush=True)
                return None
            cache[float(frequency)] = alpha
        alpha = cache[float(frequency)]
        alpha0 = [alpha.real, alpha.imag]
        alphas.append(alpha)
        f_dir = numpy.zeros(domain.shape, dtype=complex)
        f_dir[0, :] = source(y, omega)
        f_dirs.append(f_dir)
    return {"frequencies_hz": frequencies, "wavenumbers": 2 * numpy.pi * frequencies / c,
            "alphas": numpy.asarray(alphas), "f_dirs": f_dirs}


def subset_frequencies(data, indices):
    """On sélectionne les fréquences utiles sans recalculer les coefficients."""
    indices = numpy.asarray(indices, dtype=int)
    return {"frequencies_hz": data["frequencies_hz"][indices],
            "wavenumbers": data["wavenumbers"][indices], "alphas": data["alphas"][indices],
            "f_dirs": [data["f_dirs"][j] for j in indices]}


def compute_boundary_gradient(domain, spacestep, Alpha, chi, u, p, prepared, f_rob=None):
    """On additionne les contributions de chaque voisin intérieur au gradient de bord."""
    rows, nodes = prepared["robin_rows"], prepared["robin_nodes"]
    beta = prepared["robin_beta"]
    denominator = beta + spacestep * Alpha * chi.ravel()[nodes]
    load = 0 if f_rob is None else spacestep * f_rob.ravel()[nodes]
    values = -numpy.real(prepared["robin_coefficients"] * Alpha * p.ravel()[rows]
                         * (beta * u.ravel()[rows] + load) / denominator ** 2)
    gradient = numpy.zeros(domain.shape)
    numpy.add.at(gradient.ravel(), nodes, values)
    return gradient


def evaluate_frequencies(domain, spacestep, data, chi, f, f_neu, f_rob,
                         beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                         prepared, weights=None):
    """On calcule les énergies et, si demandé, leur gradient de bord pondéré."""
    energies = numpy.zeros(len(data["frequencies_hz"]))
    gradient = numpy.zeros(domain.shape) if weights is not None else None
    for j, (wave, Alpha, f_dir) in enumerate(zip(data["wavenumbers"], data["alphas"], data["f_dirs"])):
        u, matrix, factor = processing.solve_helmholtz(
            domain, spacestep, wave, f, f_dir, f_neu, f_rob,
            beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi,
            prepared=prepared, return_system=True,
        )
        energies[j] = your_compute_objective_function(domain, u, spacestep)
        if weights is not None:
            # On résout le même problème adjoint qu'Antoine avec la factorisation du champ.
            rhs = -2 * spacestep ** 2 * numpy.conj(u).ravel()
            p = factor.solve(rhs).reshape(domain.shape)
            p[domain != _env.NODE_INTERIOR] = 0
            gradient += weights[j] * compute_boundary_gradient(
                domain, spacestep, Alpha, chi, u, p, prepared, f_rob,
            )
    return energies, gradient, u


def compute_chi_1(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                  beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob, Alpha, chi):
    """On calcule l'énergie pour la répartition fournie, à une fréquence."""
    u = processing.solve_helmholtz(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                   beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, Alpha * chi)
    return your_compute_objective_function(domain_omega, u, spacestep)


def project_distribution(chi_tilde, domain, V_obj):
    """On reprend la projection par écrêtage et dichotomie d'Antoine."""
    robin = domain == _env.NODE_ROBIN
    S = numpy.sum(robin)
    l_min, l_max = -1 - numpy.max(numpy.abs(chi_tilde)), 1 + numpy.max(numpy.abs(chi_tilde))
    for _ in range(60):
        l = (l_min + l_max) / 2
        chi = preprocessing.set2zero(numpy.maximum(0, numpy.minimum(chi_tilde + l, 1)), domain)
        if numpy.sum(chi) / S > V_obj:
            l_max = l
        else:
            l_min = l
    return chi


def binarize_distribution(chi, domain, V_obj):
    """On garde les plus grandes densités avec le nombre de points garnis imposé."""
    robin = domain == _env.NODE_ROBIN
    nodes = numpy.argwhere(robin)[numpy.argsort(-chi[robin], kind="stable")]
    binary = numpy.zeros(domain.shape)
    for i, j in nodes[:int(round(V_obj * numpy.sum(robin)))]:
        binary[i, j] = 1
    return binary


def your_multifrequency_optimization(domain_omega, spacestep, frequencies, c, f, f_neu, f_rob,
                                     beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                                     material, g_source, mu, chi, V_obj, *,
                                     prepared=None, frequency_data=None, iterations=None,
                                     return_details=False, checkpoint=None, verbose=False, step_rule="increment"):
    """On reprend la descente multifréquentielle projetée d'Antoine."""
    frequencies = numpy.asarray(frequencies, dtype=float)
    if len(frequencies) == 0 or not numpy.all(numpy.isfinite(frequencies)) or numpy.any(numpy.diff(frequencies) <= 0):
        print("On fournit des fréquences distinctes dans l'ordre croissant.")
        return None
    k_max = N_ITERATIONS if iterations is None else int(iterations)
    weights = frequency_weights(frequencies)
    data = frequency_data
    if data is None:
        data = prepare_frequencies(domain_omega, spacestep, frequencies, c, material, g_source)
    if data is None:
        return None
    if prepared is None:
        prepared = processing.prepare_helmholtz_system(
            domain_omega, spacestep, beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
        )
    arguments = (domain_omega, spacestep, data)
    loads = (f, f_neu, f_rob, beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, prepared)
    chi = project_distribution(chi, domain_omega, V_obj)
    history = []
    variation = 1.0
    path = None if checkpoint is None else Path(checkpoint)
    if path is not None and path.exists():
        saved = dict(numpy.load(path))
        chi, history, mu = saved["chi"], saved["history"].tolist(), float(saved["mu"])
        variation = float(saved.get("variation", 1.0))
    energies, grad, u = evaluate_frequencies(*arguments, chi, *loads, weights)
    if not numpy.all(numpy.isfinite(energies)) or not numpy.all(numpy.isfinite(grad)):
        print("Les énergies ou le gradient ne sont pas finis.")
        return None
    current = float(weights @ energies)
    if history:
        if not numpy.isclose(history[-1], current, rtol=1e-9, atol=1e-12):
            print("Le calcul de reprise ne correspond pas à l'énergie enregistrée.")
            return None
    else:
        history = [current]
    n = len(history) - 1
    while variation >= DELTA and n < k_max and mu > MU_MIN:
        if verbose:
            print('---- iteration number = ', n)
            print('1. computing solution of Helmholtz problem, i.e., u')
            print('2. computing solution of adjoint problem, i.e., p')
            print('3. computing objective function, i.e., energy')
            print('4. computing parametric gradient')
        accepted = False
        while mu > MU_MIN:
            if verbose:
                print('    a. computing gradient descent')
            chi_tilde = chi - mu * grad
            if verbose:
                print('    b. computing projected gradient')
            chi_new = project_distribution(chi_tilde, domain_omega, V_obj)
            if numpy.array_equal(chi_new, chi):
                break
            if verbose:
                print('    c. computing solution of Helmholtz problem, i.e., u')
                print('    d. computing objective function, i.e., energy (E)')
            values, grad_new, u_new = evaluate_frequencies(*arguments, chi_new, *loads, weights)
            energy_new = float(weights @ values)
            if numpy.isfinite(energy_new) and energy_new < history[-1]:
                variation = float(numpy.max(numpy.abs(chi_new - chi)))
                if step_rule == "bb":
                    # On conserve le réglage du pas utilisé par Antoine pour la bande.
                    robin = domain_omega == _env.NODE_ROBIN
                    step = (chi_new - chi)[robin]
                    change = (grad_new - grad)[robin]
                    denominator = numpy.dot(change, change)
                    new_mu = abs(numpy.dot(step, change)) / denominator if denominator > 0 else mu
                    mu = new_mu if new_mu > 0 else mu
                else:
                    mu = mu + 0.001
                chi, energies, grad, u = chi_new, values, grad_new, u_new
                history.append(energy_new)
                n += 1
                accepted = True
                if path is not None:
                    numpy.savez_compressed(path, chi=chi, history=numpy.asarray(history), mu=mu, variation=variation)
                print("Étape", n, "sur", k_max, ": Énergie J =", energy_new, flush=True)
                break
            mu = mu / 2
        if not accepted:
            break
    chi_relaxed = chi.copy()
    chi = binarize_distribution(chi_relaxed, domain_omega, V_obj)
    if verbose:
        print('end. computing solution of Helmholtz problem, i.e., u')
    binary_energies, grad, u = evaluate_frequencies(*arguments, chi, *loads, weights)
    result = {"frequencies_hz": frequencies, "weights": weights, "alphas": data["alphas"],
              "history": numpy.asarray(history), "chi_relaxed": chi_relaxed, "chi": chi,
              "binary_energy": float(weights @ binary_energies),
              "objective_binary_energies": binary_energies, "accepted_steps": n,
              "max_iterations": k_max, "mu_final": mu, "V_obj": V_obj, "u": u, "grad": grad}
    if return_details:
        return result
    return chi, result["history"].reshape(-1, 1)


def your_optimization_procedure(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
                                 beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                                 Alpha, mu, chi, V_obj, *, prepared=None, iterations=None,
                                 return_details=False, checkpoint=None):
    """On utilise la même descente pour la fréquence et la source fournies."""
    frequency = C * omega / (2 * numpy.pi)
    data = {"frequencies_hz": numpy.array([frequency]), "wavenumbers": numpy.array([omega]),
            "alphas": numpy.array([Alpha]), "f_dirs": [f_dir]}
    result = your_multifrequency_optimization(
        domain_omega, spacestep, [frequency], C, f, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
        None, G_SOURCE, mu, chi, V_obj,
        prepared=prepared, frequency_data=data, iterations=iterations,
        return_details=True, checkpoint=checkpoint, verbose=True,
    )
    if result is None or return_details:
        return result
    return result["chi"], result["history"].reshape(-1, 1), result["u"], result["grad"]


def your_band_optimization(domain_omega, spacestep, frequencies, c, f, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
                           material, g_source, mu, chi, V_obj, **options):
    """On reprend le moteur multifréquentiel pour la grille régulière de la bande."""
    return your_multifrequency_optimization(
        domain_omega, spacestep, frequencies, c, f, f_neu, f_rob,
        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
        material, g_source, mu, chi, V_obj, step_rule="bb", **options,
    )


def make_problem(N=N_POINTS, level=LEVEL):
    """On prépare la géométrie et les coefficients fournis dans le programme d'Antoine."""
    M = 2 * N
    spacestep = 1.0 / N
    beta_pde, alpha_pde, alpha_dir, beta_neu, alpha_rob, beta_rob = preprocessing._set_coefficients_of_pde(M, N)
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)
    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level)
    chi = preprocessing.set2zero(preprocessing._set_chi(M, N, x, y), domain_omega)
    prepared = processing.prepare_helmholtz_system(
        domain_omega, spacestep, beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob,
    )
    return {"domain": domain_omega, "h": spacestep, "N": N, "level": level, "x": x, "y": y,
            "chi_initial": chi, "V_obj": float(chi.sum()/numpy.sum(domain_omega == _env.NODE_ROBIN)),
            "prepared": prepared, "f": f, "f_neu": f_neu, "f_rob": f_rob,
            "beta_pde": beta_pde, "alpha_pde": alpha_pde, "alpha_dir": alpha_dir,
            "beta_neu": beta_neu, "beta_rob": beta_rob}


def evaluate_problem(problem, chi, data, weights=None):
    """On transmet les données du domaine à la boucle de résolution d'Antoine."""
    return evaluate_frequencies(
        problem["domain"], problem["h"], data, chi, problem["f"], problem["f_neu"], problem["f_rob"],
        problem["beta_pde"], problem["alpha_pde"], problem["alpha_dir"], problem["beta_neu"],
        problem["beta_rob"], problem["prepared"], weights,
    )


def local_maxima(energies):
    """On garde les points dont l'énergie dépasse celle des deux voisins."""
    return numpy.flatnonzero((energies[1:-1] > energies[:-2]) & (energies[1:-1] > energies[2:])) + 1


def quantity_comparison(problem, data):
    """On agrandit la portion garnie autour de sa position initiale sur le contour."""
    nodes = []
    for y, x in zip(problem["y"][:-1], problem["x"][:-1]):
        node = (int(y), int(x))
        if not nodes or node != nodes[-1]:
            nodes.append(node)
    fractions, energies = [], []
    weights = frequency_weights(data["frequencies_hz"])
    for fraction in VOLUMES:
        count = int(round(fraction * len(nodes)))
        start = max(0, min(len(nodes)-count, int(round(.4*len(nodes)-count/2))))
        chi = numpy.zeros(problem["domain"].shape)
        for i, j in nodes[start:start+count]:
            chi[i, j] = 1
        values, _, _ = evaluate_problem(problem, chi, data)
        fractions.append(float(chi.sum()/len(nodes)))
        energies.append(float(weights @ values))
    return numpy.array(fractions), numpy.array(energies)


def code_hashes():
    """On identifie les fichiers de calcul qui ont produit les résultats."""
    folder = Path(__file__).resolve().parent
    return {name: hashlib.sha256((folder/name).read_bytes()).hexdigest()
            for name in ("demo_control_polycopie2024.py", "processing.py", "preprocessing.py", "compute_alpha.py")}


def study_material(name, output_dir=None):
    """On calcule les références puis les quatre descentes du matériau au niveau choisi."""
    root = RESULTS if output_dir is None else Path(output_dir)
    folder = root/name
    folder.mkdir(parents=True, exist_ok=True)
    parameters = {"source_directory": "context/EI_Antoine", "code_hashes": code_hashes(),
                  "material": name, "material_parameters": list(compute_alpha.MATERIAUX[name]),
                  "N_points": N_POINTS, "levels": list(LEVELS), "optimization_level": LEVEL,
                  "max_iterations": N_ITERATIONS, "frequencies_hz": FREQUENCIES.tolist(),
                  "mu_initial": MU_INITIAL, "mu_increment": .001, "mu_min": MU_MIN,
                  "band_step_rule": "bb", "projection": "clip_dichotomy",
                  "delta": DELTA, "gradient": "gradient_de_bord", "source": SOURCE.__name__,
                  "identification_profile": G_SOURCE.__name__, "robin_sign": "+", "c": C,
                  "alpha0": compute_alpha.Alpha0,
                  "material_fit": {key: getattr(compute_alpha,key) for key in ("l","L","N","A","B","gamma_p","rho0","c0")},
                  "modes": list(MODES), "quantity_fractions": list(VOLUMES)}
    filename = folder/"parametres.json"
    if filename.exists() and json.loads(filename.read_text()) != parameters:
        print("Les paramètres ont changé. On choisit un autre dossier pour les nouveaux résultats.")
        return None
    filename.write_text(json.dumps(parameters, ensure_ascii=False, indent=2)+"\n")
    cache = {}
    coefficient_file = folder/"coefficients.npz"
    if coefficient_file.exists():
        saved = numpy.load(coefficient_file)
        cache.update(zip(saved["frequencies_hz"].tolist(), saved["alphas"].tolist()))
    data = None
    for level in LEVELS:
        problem = make_problem(N_POINTS, level)
        if data is None:
            data = prepare_frequencies(problem["domain"], problem["h"], FREQUENCIES, C,
                                       compute_alpha.MATERIAUX[name], G_SOURCE, coefficient_cache=cache)
            if data is None:
                return None
            numpy.savez_compressed(coefficient_file, frequencies_hz=FREQUENCIES, alphas=data["alphas"])
        reference_file = folder/f"niveau{level}.npz"
        if reference_file.exists():
            reference = dict(numpy.load(reference_file))
        else:
            full = (problem["domain"] == _env.NODE_ROBIN).astype(float)
            full_values, _, _ = evaluate_problem(problem, full, data)
            initial_values, _, _ = evaluate_problem(problem, problem["chi_initial"], data)
            reference = {"frequencies_hz": FREQUENCIES, "full": full_values, "initial": initial_values,
                         "domain": problem["domain"], "chi_initial": problem["chi_initial"],
                         "h": problem["h"], "peaks": local_maxima(full_values)}
            numpy.savez_compressed(reference_file, **reference)
        quantity_file = folder/f"quantite_niveau{level}.npz"
        if not quantity_file.exists():
            fractions, values = quantity_comparison(problem, data)
            numpy.savez_compressed(quantity_file, fractions=fractions, energies=values)
        print(name, "niveau", level, ": références et quantités terminées", flush=True)
    # On conserve ce domaine de niveau trois pour les quatre comparaisons de descente.
    if problem["level"] != LEVEL:
        problem = make_problem(N_POINTS, LEVEL)
        reference = dict(numpy.load(folder/f"niveau{LEVEL}.npz"))
    peak_indices = reference["peaks"]
    if not len(peak_indices):
        peak_indices = numpy.array([reference["full"].argmax()])
    mono_index = peak_indices[numpy.argmax(reference["full"][peak_indices])]
    selections = {"mono": numpy.array([mono_index]), "resonances": peak_indices,
                  "bande50": numpy.flatnonzero((FREQUENCIES-50) % 50 == 0),
                  "bande5": numpy.arange(len(FREQUENCIES))}
    validation = None
    for mode_name in MODES:
        mode_file = folder/f"descente_{mode_name}.npz"
        selected = subset_frequencies(data, selections[mode_name])
        checkpoint = folder/f"reprise_{mode_name}.npz"
        if mode_file.exists():
            result = dict(numpy.load(mode_file))
        else:
            print(name, "niveau", LEVEL, ": descente", mode_name, flush=True)
            common = (problem["domain"], problem["h"], selected["frequencies_hz"], C,
                      problem["f"], problem["f_neu"], problem["f_rob"],
                      problem["beta_pde"], problem["alpha_pde"], problem["alpha_dir"],
                      problem["beta_neu"], problem["beta_rob"], compute_alpha.MATERIAUX[name],
                      G_SOURCE, MU_INITIAL, problem["chi_initial"].copy(), problem["V_obj"])
            options = {"prepared": problem["prepared"], "frequency_data": selected,
                       "return_details": True, "checkpoint": checkpoint}
            if mode_name == "mono":
                j = selections[mode_name][0]
                result = your_optimization_procedure(
                    problem["domain"], problem["h"], data["wavenumbers"][j],
                    problem["f"], data["f_dirs"][j], problem["f_neu"], problem["f_rob"],
                    problem["beta_pde"], problem["alpha_pde"], problem["alpha_dir"],
                    problem["beta_neu"], problem["beta_rob"], data["alphas"][j]*problem["chi_initial"],
                    data["alphas"][j], MU_INITIAL, problem["chi_initial"].copy(), problem["V_obj"],
                    prepared=problem["prepared"], return_details=True, checkpoint=checkpoint,
                )
            else:
                function = your_multifrequency_optimization if mode_name == "resonances" else your_band_optimization
                result = function(*common, **options)
            if result is None:
                return None
            # On garde le résultat de calcul et on sépare les champs temporaires volumineux.
            result.pop("u", None)
            result.pop("grad", None)
            numpy.savez_compressed(mode_file, **result)
            if checkpoint.exists():
                checkpoint.unlink()
        spectrum_file = folder/f"spectre_{mode_name}.npz"
        if not spectrum_file.exists():
            binary_values, _, _ = evaluate_problem(problem, result["chi"], data)
            numpy.savez_compressed(spectrum_file, frequencies_hz=FREQUENCIES,
                                   initial=reference["initial"], full=reference["full"], binary=binary_values)
        validation_file = folder/f"validation_{mode_name}.npz"
        if not validation_file.exists():
            if validation is None:
                fine = numpy.sort(numpy.r_[FREQUENCIES, (FREQUENCIES[:-1]+FREQUENCIES[1:])/2])
                validation = prepare_frequencies(problem["domain"], problem["h"], fine, C,
                                                compute_alpha.MATERIAUX[name], G_SOURCE, coefficient_cache=cache)
                initial_fine, _, _ = evaluate_problem(problem, problem["chi_initial"], validation)
                full_fine, _, _ = evaluate_problem(problem, (problem["domain"] == _env.NODE_ROBIN).astype(float), validation)
            binary_fine, _, _ = evaluate_problem(problem, result["chi"], validation)
            numpy.savez_compressed(validation_file, frequencies_hz=validation["frequencies_hz"],
                                   initial=initial_fine, full=full_fine, binary=binary_fine)
        print(name, mode_name, ": résultats et contrôle fréquentiel enregistrés", flush=True)
    return str(folder)


def run_all_studies(output_dir=None):
    """On calcule les quatre matériaux puis on rassemble les figures."""
    folder = RESULTS if output_dir is None else Path(output_dir)
    for name in MATERIALS:
        if study_material(name, folder) is None:
            return None
    postprocessing.plot_all_results(folder, MATERIALS, LEVELS, MODES)
    return folder


if __name__ == "__main__":
    run_all_studies()
