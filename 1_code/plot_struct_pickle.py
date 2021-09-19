
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
import pickle


"""
This file produces the structure images using as input the pickle file
generated with the 'plot_struct.py' code.
"""

output_subdir = '../2_pipeline/5_ASteCA/tmp/'
forder = (
    'BER73', 'BER25', 'BER75', 'BER26', 'TOMB2', 'BER76', 'F1212', 'SAU1',
    'CZER30', 'ARPM2', 'BH4', 'F1419', 'BH37', 'E9205', 'E9218', 'SAU3',
    'KRON39', 'E9308', 'BH144', 'BH176', 'KRON31', 'SAU6', 'BER56', 'BER102')
# This determines the size of the figure
fig_mult = 4


def main():
    """
    """
    data = []
    with open("struct.pickle", 'rb') as fr:
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
        fig, axes = plt.subplots(
            N, 3, figsize=(3 * fig_mult, N * fig_mult * .9))
        for j, name in enumerate(forder[i_old:i]):
            print(i_old, j, name)
            arglist = data[clidx[name]][name]
            ax1, ax2, ax3 = axes[j]
            mplot(name, arglist, ax1, ax2, ax3, fig, j)
        fig.tight_layout()
        plt.savefig(output_subdir + '{}_struct.png'.format(i_old), dpi=300)
        plt.clf()
        plt.close("all")
        i_old = i

    name, N = 'BER29', 1
    fig, axes = plt.subplots(N, 3, figsize=(3 * fig_mult, N * fig_mult))
    arglist = data[clidx[name]][name]
    ax1, ax2, ax3 = axes
    mplot(name, arglist, ax1, ax2, ax3, fig)
    fig.tight_layout()
    plt.savefig(output_subdir + 'BER29_struct.png', dpi=300)
    plt.clf()
    plt.close("all")


def mplot(name, arglist, ax1, ax2, ax3, fig, j=3):
    """
    """
    pl_full_frame(ax1, j, name, *arglist[0])
    pl_densmap(ax2, j, *arglist[1])
    pl_rad_dens(ax3, j, fig, *arglist[2])


def pl_full_frame(
    ax, j, name, x_min, x_max, y_min, y_max, kde_cent, x, y, st_sizes_arr,
        clust_rad, fs=15):
    """
    x,y finding chart of full frame
    """
    if name in ('KRON39', 'E9308', 'BH144', 'BH176', 'KRON31', 'SAU6'):
        st_sizes_arr = st_sizes_arr * .25
    ax.scatter(x, y, marker='o', c='black', s=st_sizes_arr)
    # Radius
    circle = plt.Circle(
        (kde_cent[0], kde_cent[1]), clust_rad, color='red', fill=False)
    ax.add_artist(circle)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.invert_xaxis()
    if j in (3, 7, 11, 15, 19, 23):
        ax.set_xlabel(r'$\alpha^{*}$', fontsize=fs)
    ax.set_ylabel(r'$\delta^{*}$', fontsize=fs)


def pl_densmap(ax, j, kde_cent, frame_kde_cent, clust_rad, fs=15):
    """
    Coordinates 2D KDE.
    """
    # Radius
    circle = plt.Circle(
        (kde_cent[0], kde_cent[1]), clust_rad, color='r', fill=False)
    ax.add_artist(circle)

    ext_range, x_grid, y_grid, k_pos = frame_kde_cent
    kde = np.reshape(k_pos.T, x_grid.shape)
    ax.imshow(
        np.rot90(kde), cmap=plt.get_cmap('RdYlBu_r'), extent=ext_range)
    ax.contour(x_grid, y_grid, kde, colors='#551a8b', linewidths=0.5)
    ax.invert_xaxis()
    if j in (3, 7, 11, 15, 19, 23):
        ax.set_xlabel(r'$\alpha^{*}$', fontsize=fs)
    ax.set_ylabel(r'$\delta^{*}$', fontsize=fs)
    ax.set_aspect(aspect="auto")


def pl_rad_dens(
    ax, j, fig, rdp_radii, rdp_points, rdp_stddev, rad_max,
    field_dens, e_fdens, clust_rad, kp_ndim, KP_Bys_rc, KP_Bys_rt,
        KP_plot, name, fs=15):
    """
    Radial density plot.
    """

    KP_cent_dens, _16_84_rang, _84_kp, _16_kp = 0., 0., 0., 0.
    if kp_ndim in (2, 4):
        KP_cent_dens, _16_84_rang, _84_kp, _16_kp = KP_plot['KP_cent_dens'],\
            KP_plot['_16_84_rang'], KP_plot['_84_kp'], KP_plot['_16_kp']

    # Convert from deg to arcmin
    rdp_radii = np.array(rdp_radii) * 60.
    clust_rad, rad_max = clust_rad * 60., rad_max * 60.
    KP_Bys_rc, KP_Bys_rt = KP_Bys_rc * 60., KP_Bys_rt * 60.
    field_dens, e_fdens, KP_cent_dens = field_dens / 3600.,\
        e_fdens / 3600., KP_cent_dens / 3600.
    _16_84_rang, _84_kp, _16_kp = _16_84_rang * 60.,\
        _84_kp / 3600., _16_kp / 3600.
    rdp_points = np.array(rdp_points) / 3600.
    rdp_stddev = np.array(rdp_stddev) / 3600.
    coord2 = 'arcmin'

    if j in (3, 7, 11, 15, 19, 23):
        ax.set_xlabel(r'radius [{}]'.format(coord2), fontsize=fs)
    ax.set_ylabel(r"$\rho$ [st/{}$^{{2}}$]".format(coord2), fontsize=fs)

    Nmax = int(len(rdp_points) * .9)
    rdp_radii, rdp_points, rdp_stddev = rdp_radii[:Nmax], rdp_points[:Nmax],\
        rdp_stddev[:Nmax]
    rad_max = rdp_radii[-1]

    # Plot density profile
    ax.plot(rdp_radii, rdp_points, marker='o', ms=5, lw=0., zorder=3,
            label="RDP")
    # Plot error bars
    ax.errorbar(
        rdp_radii, rdp_points, yerr=rdp_stddev, fmt='none', ecolor='grey',
        lw=1., zorder=1)

    # Plot background level.
    ax.hlines(y=field_dens, xmin=0, xmax=max(rdp_radii), color='k', ls='--',
              zorder=5)
    if not np.isnan(e_fdens):
        ax.hlines(
            y=field_dens - e_fdens, xmin=0, xmax=max(rdp_radii),
            color='k', ls=':', zorder=5)
        ax.hlines(
            y=field_dens + e_fdens, xmin=0, xmax=max(rdp_radii),
            color='k', ls=':', zorder=5)

    # Set plot limits
    delta_backg = 0.15 * (max(rdp_points) - field_dens)
    N_half = int(len(rdp_points) * .5)
    y_max = min(ax.get_ylim()[1], max(rdp_points[:N_half]) + delta_backg)
    y_min = field_dens - (e_fdens + e_fdens * .8)
    if y_min <= 0.:
        y_min = 1.
    y_mid_point = max((y_min + y_max) * .25, field_dens + e_fdens * 2)

    # Plot radius.
    ax.vlines(x=clust_rad, ymin=field_dens, ymax=y_mid_point, lw=1.5,
              color='r', zorder=5)

    #
    ob = offsetbox.AnchoredText(name, pad=0.2, loc=1, prop={'fontsize': 20})
    ax.add_artist(ob)

    # Plot King profile. Use median values
    if kp_ndim in (2, 4):
        # Plot curve. Values outside of rt contribute 'fd'.
        kpf_xvals = np.linspace(rdp_radii[0], KP_Bys_rt[1], 100)
        kpf_yvals = KP_cent_dens * KingProf(
            kpf_xvals, KP_Bys_rc[1], KP_Bys_rt[1]) + field_dens
        ax.plot(kpf_xvals, kpf_yvals, 'g--', lw=2., zorder=3)
        # 16-84th range
        idx = (np.abs(_16_84_rang - kpf_xvals[-1])).argmin()
        # 16-84 region
        ax.fill_between(
            _16_84_rang[:idx], _84_kp[:idx], _16_kp[:idx], facecolor='green',
            alpha=0.1)

        # Core radius
        rc_ymax = KP_cent_dens * KingProf(
            KP_Bys_rc[1], KP_Bys_rc[1], KP_Bys_rt[1]) + field_dens
        ax.vlines(
            x=KP_Bys_rc[1], ymin=field_dens, ymax=rc_ymax,
            color='g', linestyles=':', lw=2., zorder=5)
        # Tidal radius
        ax.vlines(x=KP_Bys_rt[1], ymin=field_dens, ymax=y_mid_point,
                  color='g', zorder=5)

    ax.set_xlim(rdp_radii[0] - rdp_radii[0] * .15, rad_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xscale('log')
    ax.set_yscale('log')

    fig.canvas.draw()
    xminf = (2, 3, 4, 5, 6, 7, 8)
    ax.xaxis.set_minor_formatter(
        lambda x, t: f'{x:.0f}' if x in xminf else None)
    ax.xaxis.set_major_formatter(
        lambda x, t: f'{x:.0f}' if x == 1 else None)
    ax.yaxis.set_minor_formatter(
        lambda x, t: f'{x:.0f}' if x >= field_dens else None)
    ax.yaxis.set_major_formatter(
        lambda x, t: f'{x:.0f}' if x >= field_dens else None)


def KingProf(r_in, rc, rt):
    """
    King (1962) profile.
    """
    return ((1. / np.sqrt(1. + (r_in / rc) ** 2))
            - (1. / np.sqrt(1. + (rt / rc) ** 2))) ** 2


if __name__ == '__main__':
    plt.style.use('science')
    main()
