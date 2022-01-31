
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, ListedColormap
import matplotlib.offsetbox as offsetbox

"""
This script generates the VPD + CMDs for all the clusters from the
"fundpars.pickle" file.
"""

output_subdir = '../2_pipeline/plots/'
forder = (
    'BER73', 'BER25', 'BER75', 'BER26', 'TOMB2', 'BER76', 'F1212', 'SAU1',
    'CZER30', 'ARPM2', 'BH4', 'F1419', 'BH37', 'E9205', 'E9218', 'SAU3',
    'KRON39', 'E9308', 'BH144', 'BH176', 'KRON31', 'SAU6', 'BER56', 'BER102')

# Size of scatter points
pt_sz = 40
# This determines the size of the figure
fig_mult = 4


def main():
    """
    """

    data = []
    with open("fundpars.pickle", 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass
    clidx = {}
    for i, cl in enumerate(data):
        clidx[list(cl.keys())[0]] = i

    i_old, N = 0, 4
    for i in range(N, len(forder) + 1, N):
        fig, axes = plt.subplots(N, 3, figsize=(3 * fig_mult, N * fig_mult))
        for j, name in enumerate(forder[i_old:i]):
            print(i_old, j, name)
            arglist = data[clidx[name]][name]
            ax1, ax2, ax3 = axes[j]
            mplot(arglist, ax1, ax2, ax3, j)
        fig.tight_layout()
        fname = output_subdir + '{}_fpars.png'.format(i_old)
        plt.savefig(fname, dpi=300)
        plt.clf()
        plt.close("all")
        i_old = i

    name, N = 'BER29', 1
    fig, axes = plt.subplots(N, 3, figsize=(3 * fig_mult, N * fig_mult))
    arglist = data[clidx[name]][name]
    ax1, ax2, ax3 = axes
    mplot(arglist, ax1, ax2, ax3)
    fig.tight_layout()
    plt.savefig(output_subdir + 'BER29_fpars.png', dpi=300)
    plt.clf()
    plt.close("all")


def mplot(arglist, ax1, ax2, ax3, j=3):
    """
    """
    pl_PMs(ax1, j, *arglist[0])
    pl_mps_phot_diag(ax2, j, *arglist[1])
    pl_bf_synth_cl(ax3, j, *arglist[2])


def pl_PMs(ax, j, data_all, data, sz_pt):
    """
    """
    if j in (3, 7, 11, 15, 19, 23):
        ax.set_xlabel('pmRA')

    ax.scatter(
        data_all['pmRA'], data_all['pmDE'], marker='.', c='grey', alpha=.35,
        zorder=0)
    ax.scatter(
        data['pmRA'], data['pmDE'], c='green', lw=0.3, edgecolor='w', zorder=3)
    medra, medde = np.nanmedian(np.array(data_all['pmRA'])),\
        np.nanmedian(np.array(data_all['pmDE']))
    stdra, stdde = np.nanstd(np.array(data_all['pmRA'])),\
        np.nanstd(np.array(data_all['pmDE']))
    ax.set_xlim(medra - 2 * stdra, medra + 2 * stdra)
    ax.set_ylim(medde - 2 * stdde, medde + 2 * stdde)
    ax.set_ylabel('pmDE')


def pl_mps_phot_diag(
    ax, j, gs_y1, gs_y2, x_min_cmd, x_max_cmd, y_min_cmd, y_max_cmd, x_ax,
    y_ax, obs_x, obs_y, err_bar, cl_sz_pt, hess_xedges, hess_yedges, x_isoch,
        y_isoch, phot_Nsigma):
    """
    Star's membership probabilities on cluster's photometric diagram.
    """
    if j in (3, 7, 11, 15, 19, 23):
        ax.set_xlabel('(G' + r'$_{BP}$' + '-G' + r'$_{RP}$)')
    ax.set_ylabel('G')

    # Plot grid.
    gls, gc = plt.rcParams['grid.linestyle'], plt.rcParams['grid.color']
    for x_ed in hess_xedges:
        # vertical lines
        ax.axvline(x_ed, linestyle=gls, lw=.3, color=gc, zorder=1)
    for y_ed in hess_yedges:
        # horizontal lines
        ax.axhline(y_ed, linestyle=gls, lw=.3, color=gc, zorder=1)

    # Plot stars used in the best fit process.
    ax.scatter(obs_x, obs_y, c='green', lw=0.3, edgecolor='w', zorder=4)

    # Plot sigma region
    if phot_Nsigma:
        cGreys = plt.cm.get_cmap('Greys', 100)
        cmap = ListedColormap(cGreys(range(65)))
        # Extend one bin upwards and to the left
        ybin = abs(hess_yedges[1] - hess_yedges[0])
        hess_yedges = [hess_yedges[0] - ybin] + list(hess_yedges)
        xbin = abs(hess_xedges[1] - hess_xedges[0])
        hess_xedges = [hess_xedges[0] - xbin] + list(hess_xedges)
        ax.hist2d(*phot_Nsigma, bins=(
            hess_xedges, hess_yedges), cmap=cmap, norm=LogNorm())
    # Plot isochrone.
    ax.plot(x_isoch, y_isoch, 'r', lw=1., zorder=6)

    ax.set_xlim(x_min_cmd, x_max_cmd)
    ax.set_ylim(20.8, y_max_cmd)

    # If list is not empty, plot error bars at several values. The
    # prep_plots.error_bars() is not able to handle the color-color diagram.
    x_val, mag_y, xy_err = err_bar
    if x_val:
        xye_i = {
            '0': (mag_y, 0, 1), '2': (mag_y, 0, 2),
            '4': (np.linspace(min(obs_y), max(obs_y), len(x_val)), 1, 2)}
        ax.errorbar(
            x_val, xye_i[str(gs_y1)][0], yerr=xy_err[xye_i[str(gs_y1)][1]],
            xerr=xy_err[xye_i[str(gs_y1)][2]],
            fmt='k.', lw=0.8, ms=0., zorder=4)


def pl_bf_synth_cl(
    ax, j, x_min_cmd, x_max_cmd, y_min_cmd, y_max_cmd, x_ax, y_ax,
    hess_xedges, hess_yedges, x_synth, y_synth, sy_sz_pt, binar_idx, x_isoch,
        y_isoch, name):
    """
    Best fit synthetic cluster obtained.
    """
    if j in (3, 7, 11, 15, 19, 23):
        ax.set_xlabel('(G' + r'$_{BP}$' + '-G' + r'$_{RP}$)')

    ax.set_xlim(x_min_cmd, x_max_cmd)
    ax.set_ylim(20.8, y_max_cmd)
    ax.set_ylabel('G')

    gls, gc = plt.rcParams['grid.linestyle'], plt.rcParams['grid.color']
    for x_ed in hess_xedges:
        # vertical lines
        ax.axvline(x_ed, linestyle=gls, lw=.3, color=gc, zorder=1)
    for y_ed in hess_yedges:
        # horizontal lines
        ax.axhline(y_ed, linestyle=gls, lw=.3, color=gc, zorder=1)

    # Single systems
    ax.scatter(
        x_synth[~binar_idx], y_synth[~binar_idx], c='blue', lw=0.3,
        edgecolor='k', zorder=2)
    # Binary systems
    ax.scatter(
        x_synth[binar_idx], y_synth[binar_idx], c='red', lw=0.3,
        edgecolor='k', zorder=3)
    # Plot isochrone.
    ax.plot(x_isoch, y_isoch, '#21B001', lw=1., zorder=6)

    ob = offsetbox.AnchoredText(name, pad=0.2, loc=2, prop={'fontsize': 20})
    ax.add_artist(ob)


if __name__ == '__main__':
    plt.style.use('science')
    main()
