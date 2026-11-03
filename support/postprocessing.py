# -*- coding: utf-8 -*-


# Python packages
import matplotlib.pyplot
import numpy
import os


# MRG packages
import _env
import preprocessing


def myimshow(tab, **kwargs):
    """Customized plot."""

    if 'dpi' in kwargs and kwargs['dpi']:
        dpi = kwargs['dpi']
    else:
        dpi = 100

    # -- create figure
    fig = matplotlib.pyplot.figure(dpi=dpi)
    ax = matplotlib.pyplot.axes()

    if 'title' in kwargs and kwargs['title']:
        title = kwargs['title']
    if 'cmap' in kwargs and kwargs['cmap']:
        cmap = kwargs['cmap']
    else:
        cmap = 'jet'
    #if 'clim' in kwargs and kwargs['clim']:
    #    clim = kwargs['clim']
    if 'vmin' in kwargs and kwargs['vmin']:
        vmin = kwargs['vmin']
    if 'vmax' in kwargs and kwargs['vmax']:
        vmax = kwargs['vmax']

    # -- plot curves
    if 'cmap' in kwargs and kwargs['cmap']:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    else:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    if 'title' in kwargs and kwargs['title']:
        matplotlib.pyplot.title(title)
    else:
        matplotlib.pyplot.imshow(tab, cmap=cmap)
    if 'colorbar' in kwargs and kwargs['colorbar']:
        matplotlib.pyplot.colorbar()

#    if 'clim' in kwargs and kwargs['clim']:
#        matplotlib.pyplot.clim(clim)
    if 'vmin' in kwargs and kwargs['vmin']:
        matplotlib.pyplot.clim(vmin, vmax)

    if 'filename' in kwargs and kwargs['filename']:
        output_file = kwargs['filename']
        (root, ext) = os.path.splitext(output_file)
        matplotlib.pyplot.savefig(root + '_plot' + ext, format=ext[1:])
        matplotlib.pyplot.close()
    else:
        matplotlib.pyplot.show()
        matplotlib.pyplot.close()

    matplotlib.pyplot.close(fig)

    return


def _plot_uncontroled_solution(u, chi):
#def _plot_uncontroled_solution(x_plot, y_plot, x, y, u, chi):

    myimshow(numpy.real(u), title='$\operatorname{Re}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_re.jpg')
    myimshow(numpy.imag(u), title='$\operatorname{Im}(u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_u0_im.jpg')
    myimshow(chi, title='$\chi_{0}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chi0_re.jpg')
    # k_begin = 0
    # k_end = len(x) - 1
    # for k in range(k_begin, k_end):
    #     x_plot[k] = k
    #     y_plot[k] = chi[int(y[k]), int(x[k])]
    # matplotlib.pyplot.plot(x_plot, y_plot)
    # matplotlib.pyplot.title('$\chi_{0}$ in $\Omega$')
    # matplotlib.pyplot.show()

    return


def _plot_controled_solution(u, chi):
#def _plot_controled_solution(x_plot, y_plot, x, y, u, chi):

    myimshow(numpy.real(u), title='$\operatorname{Re}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_re.jpg')
    myimshow(numpy.imag(u), title='$\operatorname{Im}(u_{n})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_un_im.jpg')
    myimshow(chi, title='$\chi_{n}$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin=-1, vmax=1, filename='fig_chin_re.jpg')
    # k_begin = 0
    # k_end = len(x) - 1
    # for k in range(k_begin, k_end):
    #     x_plot[k] = k
    #     y_plot[k] = chi[int(y[k]), int(x[k])]
    # matplotlib.pyplot.plot(x_plot, y_plot)
    # matplotlib.pyplot.title('$\chi_{n}$ in $\Omega$')
    # matplotlib.pyplot.show()

    return


def _plot_error(err):

    myimshow(numpy.real(err), title='$\operatorname{Re}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err_real.jpg')
    myimshow(numpy.imag(err), title='$\operatorname{Im}(u_{n}-u_{0})$ in $\Omega$', colorbar='colorbar', cmap='jet', vmin = -1, vmax = 1, filename='fig_err.jpg')

    return

def _plot_energy_history(energy):
    """On trace le coût pendant la descente puis après le passage en binaire."""
    values = numpy.asarray(energy).ravel()
    matplotlib.pyplot.plot(values[:-1], label="Descente continue")
    last = len(values) - 2
    matplotlib.pyplot.plot([last, last], [values[-2], values[-1]], ":", color="tab:orange")
    matplotlib.pyplot.scatter(last, values[-1], marker="s", color="tab:orange",
                              label="Répartition finale binaire", zorder=3)
    matplotlib.pyplot.title("Descente et répartition finale du matériau")
    matplotlib.pyplot.xlabel("Étape acceptée de la descente")
    matplotlib.pyplot.ylabel("Critère d'énergie")
    matplotlib.pyplot.legend()
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig_energy_real.jpg')
    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close()
    return


def plot_rer_b_frequency_sweep(results, source, output_dir=None):
    """On trace la source choisie et le coût du champ en fonction de la fréquence."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # On crée le dossier demandé avant d’enregistrer les figures.
    os.makedirs(output_dir, exist_ok=True)
    frequencies = results["frequencies_hz"]

    # On trace le spectre au-delà des fréquences simulées sans résoudre Helmholtz.
    spectrum_frequencies = numpy.linspace(0.0, 3500.0, 701)
    spectrum_amplitudes = numpy.array([
        source(0.0, 2.0 * numpy.pi * frequency) for frequency in spectrum_frequencies
    ])
    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(spectrum_frequencies, spectrum_amplitudes)
    ax.axvspan(frequencies[0], frequencies[-1], color="gray", alpha=0.15,
               label="Fréquences calculées")
    ax.set_xlim(0.0, 3500.0)
    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Amplitude relative")
    ax.set_title("Amplitude de la source choisie")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig_rer_b_spectre.png"), dpi=150)
    matplotlib.pyplot.close(fig)

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(frequencies, results["energies"], marker="o", markersize=3)
    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Énergie acoustique numérique")
    ax.set_title("Énergie du domaine selon la fréquence")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig_rer_b_energie.png"), dpi=150)
    matplotlib.pyplot.close(fig)
    return
