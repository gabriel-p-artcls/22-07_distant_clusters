
"""
Plot the clusters in all four databases in the context of the Milky Way
"""


from astropy import units as u
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord
from astropy.io import ascii
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
from plot_pars import dpi, grid_x, grid_y, sc_sz, sc_ec, sc_lw
from plot_XYmap_v1 import momany

# Shorlin1     166.44 -61.23 .8  nan   nan   nan   nan  nan   12600 6.5   5594
# FSR0338      327.93 55.33  2.7 8.1   14655 nan   nan  nan   nan    8.1  14655
lit_data = """
Cluster      RA  DEC       Dm  A_OC02  D_OC02  A_CG20 D_CG20  A_WEBDA  D_WEBDA  A_MWSC  D_MWSC
Ber73        95.50  -6.35  2   9.18  9800  9.15 6158  9.36  6850  9.15  7881
Ber25        100.25 -16.52 5   9.7   11400 9.39 6780  9.6   11300 9.7   11400
Ber75        102.25 -24.00 4   9.6   9100  9.23 8304  9.48  9800  9.3   6273
Ber26        102.58 5.75   4   9.6   12589 nan   nan  9.6   4300  8.71  2724
Ber29        103.27 16.93  6   9.025 14871 9.49 12604 9.025 14871 9.1   10797
Tombaugh2    105.77 -20.82 3   9.01  6080  9.21 9316  9.01  13260 9.01  6565
Ber76        106.67 -11.73 5   9.18  12600 9.22 4746  9.18  12600 8.87  2360
FSR1212      106.94 -14.15 nan nan   nan   9.14 9682  nan   nan   8.65  1780
Saurer1      110.23 1.81   4   9.7   13200 nan   nan  9.85  13200 9.6   13719
Czernik30    112.83 -9.97  3   9.4   9120  9.46 6647  9.4   6200  9.2   6812
arpm2        114.69 -33.84 2   9.335 13341 9.48 11751 9.335 13341 9.335 13338
vdBH4        114.43 -36.07 2   nan   nan   nan  nan   8.3   19300 nan   nan
FSR1419      124.71 -47.79 nan nan   nan   9.21 11165 nan   nan   8.375 7746
vdBH37       128.95 -43.62 3   8.84  11220 8.24 4038  8.85  2500  7.5   5202
ESO09205     150.81 -64.75 5   9.3   5168  9.65 12444 9.78  10900 9.3   5168
ESO09218     153.74 -64.61 5   9.024 10607 9.46 9910  9.024 607   9.15  9548
Saurer3      160.35 -55.31 4   9.3   9550  nan   nan  9.45  8830  9.3   7075
Kronberger39 163.56 -61.74 .8  nan   11100 nan   nan  nan   nan   6.    4372
ESO09308     169.92 -65.22 1   9.74  14000 nan   nan  9.65  3700   9.8  13797
vdBH144      198.78 -65.92 1.5 8.9   12000 9.17 9649  8.9   12000  9    7241
vdBH176      234.85 -50.05 3   nan   nan   nan   nan  nan   13400  9.8  18887
Kronberger31 295.05 26.26  1.3 nan   11900 nan   nan  nan   nan    8.5  12617
Saurer6      297.76 32.24  1.8 9.29  9330  nan   nan  9.29  9330   9.2  7329
Ber56        319.43 41.83  3   9.6   12100 9.47 9516  9.6   12100  9.4  13180
Ber102       354.66 56.64  5   9.5   9638  9.59 10519 8.78  2600   9.14 4900
"""

out_folder = '../2_pipeline/plots/'


def main(dpi=dpi):
    """
    Gridspec idea: http://www.sc.eso.org/~bdias/pycoffee/codes/20160407/
                   gridspec_demo.html
    """
    data = ascii.read(lit_data)
    DBs_list = ('D_MWSC', 'D_WEBDA', 'D_OC02', 'D_CG20')

    # # Use this block to plot the ASteCA results instead
    # # ASteCA output data
    # if plot_ASteCA:
    #     asteca_data = ascii.read(
    #         '../2_pipeline/5_ASteCA/out/asteca_output.dat')
    #     asteca_names = list([_[3:].upper() for _ in asteca_data['NAME']])
    #     asteca_dists = []
    #     for cl in data['Cluster']:
    #         try:
    #             idx = asteca_names.index(cl.upper())
    #             d_pc = 10**(.2 * (asteca_data[idx]['d_mean'] + 5))
    #         except ValueError:
    #             d_pc = np.nan
    #         asteca_dists.append(round(d_pc, 0))
    #     data['D_AS'] = asteca_dists
    #     DBs_list = ('D_AS',)

    # Default Galactic Center is 8.3 kpc (Gillessen et al. 2009)
    gc_frame = coord.Galactocentric()

    # Obtain latitude, longitude
    eq = SkyCoord(
        ra=data['RA'] * u.degree, dec=data['DEC'] * u.degree,
        frame='icrs')
    lb = eq.transform_to('galactic')
    lon = lb.l.wrap_at(180 * u.deg).radian * u.radian
    lat = lb.b.radian * u.radian

    xyz_kpc = {}
    for cat in DBs_list:
        xyz_kpc[cat] = xyzCoords(data, cat, lon, lat, gc_frame)

    max_RGC = []
    for i, cl in enumerate(data['Cluster']):
        x_dist, y_dist, z_dist, R_GC = "", "", "", ""
        R_GC_old = 0.
        for cat in DBs_list:
            x_dist += " {:>6.2f}".format(xyz_kpc[cat][0][i].value)
            y_dist += " {:>6.2f}".format(xyz_kpc[cat][1][i].value)
            z_dist += " {:>6.2f}".format(xyz_kpc[cat][2][i].value)
            RGC = np.sqrt(
                xyz_kpc[cat][0][i]**2 + xyz_kpc[cat][1][i]**2
                + xyz_kpc[cat][2][i]**2)
            R_GC += " {:>6.2f}".format(RGC.value)
            if RGC.value > R_GC_old:
                R_GC_lst = [xyz_kpc[cat][0][i].value, xyz_kpc[cat][1][i].value,
                            xyz_kpc[cat][2][i].value]
                R_GC_old = RGC.value
        max_RGC.append(R_GC_lst)
        # print("{:<15}".format(cl), x_dist, y_dist, z_dist)
        print("{:<15}".format(cl), R_GC)

    # Sun's coords according to the Galactocentric frame.
    x_sun, z_sun = gc_frame.galcen_distance, gc_frame.z_sun
    s_xys = SkyCoord(
        -x_sun, 0., z_sun, unit='kpc', representation_type='cartesian')

    # colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colors = sns.color_palette("Spectral", 13)[2::3]
    # colors = sns.color_palette("Set2")
    # colors = sns.color_palette("Paired")[::2]
    # colors = sns.color_palette("cubehelix", 10)[::2]

    markers = ('o', '*', 'v', '^')
    Xmin, Xmax, Ymin, Ymax, Zmin, Zmax = -24, 11, -19, 16, -2.6, 2.6

    fig = plt.figure(figsize=(17, 17))
    gs = gridspec.GridSpec(grid_y, grid_x)

    plt.subplot(gs[0:4, 0:4])
    # plt.grid(ls=':', c='grey', lw=.5, zorder=.5)
    plt.axhline(0, ls=':', c='grey', zorder=-1)
    plt.axvline(0, ls=':', c='grey', zorder=-1)

    cl_plots1 = [[], []]
    for ic, cat in enumerate(DBs_list):
        x_kpc, y_kpc, z_kpc = xyz_kpc[cat]
        pl = plt.scatter(
            x_kpc, y_kpc, alpha=.8, marker=markers[ic], s=sc_sz * 2,
            lw=sc_lw, edgecolor=sc_ec, zorder=2.5, color=colors[ic])
        cl_plots1[0].append(pl)
        cl_plots1[1].append(cat.replace('D_', ''))

    # Plot Sun and center of Milky Way
    plt.scatter(s_xys.x, s_xys.y, c='yellow', s=50, edgecolor='k', zorder=2.5)
    plt.scatter(0., 0., c='k', marker='o', s=150, zorder=2.5)
    # Plot spiral arms
    cl_plots2 = plotSpiral()
    for cl in max_RGC:
        plt.plot((s_xys.x.value, cl[0]), (s_xys.y.value, cl[1]), zorder=-2,
                 c='grey', lw=.5)
    l1 = plt.legend(cl_plots1[0], cl_plots1[1], loc=1, fontsize=12)
    plt.legend(cl_plots2[0], cl_plots2[1], loc=4, fontsize=12)
    plt.gca().add_artist(l1)
    plt.xlim(Xmin, Xmax)
    plt.ylim(Ymin, Ymax)
    plt.xlabel(r"$x_{GC}$ [Kpc]", fontsize=15)
    plt.ylabel(r"$y_{GC}$ [Kpc]", fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    #
    # X_GC vs Z_GC
    # plt.subplot(gs[4:6, 0:4])
    plt.subplot(gs[0:2, 4:8])
    for ic, cat in enumerate(DBs_list):
        x_kpc, y_kpc, z_kpc = xyz_kpc[cat]
        plt.scatter(
            x_kpc, z_kpc, alpha=.8, color=colors[ic], marker=markers[ic],
            s=100, lw=.5, edgecolor='k', zorder=2.5)
    plt.axvline(0, ls=':', c='grey', zorder=-1)
    plt.axhline(0, ls=':', c='grey', zorder=-1)
    plt.scatter(s_xys.x, s_xys.z, c='yellow', s=50, edgecolor='k', zorder=5)
    plt.scatter(0., 0., c='k', marker='o', s=150, zorder=5)
    for cl in max_RGC:
        plt.plot((s_xys.x.value, cl[0]), (s_xys.z.value, cl[2]), zorder=-2,
                 c='grey', lw=.5)
    plt.xlabel(r"$x_{GC}\, [Kpc]$", fontsize=15)
    plt.ylabel(r"$z_{GC}\, [Kpc]$", fontsize=15)
    plt.xlim(Xmin, Xmax)
    plt.ylim(Zmin, Zmax)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    #
    # Y_GC vs Z_GC
    # plt.subplot(gs[6:8, 0:4])
    plt.subplot(gs[2:4, 4:8])
    for ic, cat in enumerate(DBs_list):
        x_kpc, y_kpc, z_kpc = xyz_kpc[cat]
        plt.scatter(
            y_kpc, z_kpc, alpha=.8, color=colors[ic], marker=markers[ic],
            s=100, lw=.5, edgecolor='k', zorder=2.5)
    plt.axvline(0, ls=':', c='grey', zorder=-1)
    plt.axhline(0, ls=':', c='grey', zorder=-1)
    plt.scatter(0., 0., c='k', marker='o', s=150, zorder=4)
    plt.scatter(s_xys.y, s_xys.z, c='yellow', s=50, edgecolor='k', zorder=5)
    for cl in max_RGC:
        plt.plot((s_xys.y.value, cl[1]), (s_xys.z.value, cl[2]), zorder=-2,
                 c='grey', lw=.5)
    plt.xlabel(r"$y_{GC}\, [Kpc]$", fontsize=15)
    plt.ylabel(r"$z_{GC}\, [Kpc]$", fontsize=15)
    plt.xlim(Ymin, Ymax)
    plt.ylim(Zmin, Zmax)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    fig.tight_layout()
    plt.savefig(out_folder + 'MWmap.png', bbox_inches='tight', dpi=dpi)


def xyzCoords(data, cat, lon, lat, gc_frame):
    """
    """
    try:
        dist_pc = data[cat].filled(np.nan)
    except AttributeError:
        dist_pc = data[cat]
    dist_pc = dist_pc / 1000.

    # Galactic coordinates.
    coords = SkyCoord(l=lon, b=lat, distance=dist_pc * u.kpc, frame='galactic')

    # Galactocentric coordinates.
    c_glct = coords.transform_to(gc_frame)

    # Rectangular coordinates
    x_kpc, y_kpc, z_kpc = c_glct.x, c_glct.y, c_glct.z

    return x_kpc, y_kpc, z_kpc


def plotSpiral():
    """
    """
    spiral_arms = momany()

    cl_plots = [[], []]
    for sp_name, vals in spiral_arms.items():
        xy_arm = np.array(list(zip(*vals)))
        if sp_name == 'Outer':
            pl, = plt.plot(
                xy_arm[0], xy_arm[1], c="#0B5CA4", ls='-.', lw=2, zorder=-1)
        if sp_name == 'Perseus':
            pl, = plt.plot(
                xy_arm[0], xy_arm[1], c='orange', ls='--', lw=2, zorder=-1)
        if sp_name == 'Orion-Cygnus':
            pl, = plt.plot(
                xy_arm[0], xy_arm[1], c='k', ls="-", lw=2, zorder=-1)
        elif sp_name == 'Carina-Sagittarius':
            pl, = plt.plot(
                xy_arm[0], xy_arm[1], c='b', ls=':', lw=2, zorder=-1)
        elif sp_name == 'Crux-Scutum':
            pl, = plt.plot(
                xy_arm[0], xy_arm[1], c='purple', ls='-.', lw=2, zorder=-1)
        elif sp_name == 'Norma':
            pl, = plt.plot(
                xy_arm[0], xy_arm[1], c='green', ls=':', lw=2, zorder=-1)
        cl_plots[0].append(pl)
        cl_plots[1].append(sp_name)

    return cl_plots


if __name__ == '__main__':
    plt.style.use('science')
    main()
