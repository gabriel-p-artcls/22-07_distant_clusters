from astropy import units as u
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord
from astropy.io import ascii
# import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import numpy as np
from plot_pars import dpi, grid_x, grid_y
from plot_XYmap import plotSpiral
from plot_Fe_vs_R import ZtoFeH


lit_data = """
Cluster      RA  DEC       Dm  A_OC  D_OC  A_CG D_CG  A_WB  D_WB  A_MW  D_MW   RV      pmRA   pmDE      pmRA_CG   pmDE_CG
Ber73        95.50  -6.35  2   9.18  9800  9.15 6158  9.36  6850  9.15  7881   112.41  0.23434  1.0619  0.227     1.110
Ber25        100.25 -16.52 5   9.7   11400 9.39 6780  9.6   11300 9.7   11400  108.07  -0.1264  0.8662  -0.114    0.845
Ber75        102.25 -24.00 4   9.6   9100  9.23 8304  9.48  9800  9.3   6273   122.41  -0.2216  1.1369  -0.264    1.088
Ber26        102.58 5.75   4   9.6   12589 nan   nan  9.6   4300  8.71  2724   68.00   0.1589   0.3849   nan      nan
Ber29        103.27 16.93  6   9.025 14871 9.49 12604 9.025 14871 9.1   10797  25.72   0.1491   -1.0549  0.151    -1.010
Tombaugh2    105.77 -20.82 3   9.01  6080  9.21 9316  9.01  13260 9.01  6565   122.47  -0.4871  1.3870   -0.464   1.349
Ber76        106.67 -11.73 5   9.18  12600 9.22 4746  9.18  12600 8.87  2360   73.02   -0.5982  1.4057   -0.580   1.400
FSR1212      106.94 -14.15 nan nan   nan   9.14 9682  nan   nan   8.65  1780   71.82   -0.3401  0.522   -0.246   0.314
Saurer1      110.23 1.81   4   9.7   13200 nan   nan  9.85  13200 9.6   13719  98.00   -0.2881  -0.2546  nan      nan
Czernik30    112.83 -9.97  3   9.4   9120  9.46 6647  9.4   6200  9.2   6812   82.07   -0.6182  -0.0701  -0.587   -0.097
arpm2        114.69 -33.84 2   9.335 13341 9.48 11751 9.335 13341 9.335 13338  58.25   -0.4895  1.2485   -0.513   1.225
vdBH4        114.43 -36.07 2   nan   nan   nan  nan   8.3   19300 nan   nan    0.00    -0.8201  2.1237   nan      nan
FSR1419      124.71 -47.79 nan nan   nan   9.21 11165 nan   nan   8.375 7746   0.00    -2.4768  2.8472   -2.529   2.860
vdBH37       128.95 -43.62 3   8.84  11220 8.24 4038  8.85  2500  7.5   5202   51.90   -3.5002  3.9929   -3.484   3.953
ESO09205     150.81 -64.75 5   9.3   5168  9.65 12444 9.78  10900 9.3   5168   57.40   -3.0043  2.4768   -2.919   2.397
ESO09218     153.74 -64.61 5   9.024 10607 9.46 9910  9.024 607   9.15  9548   65.47   -3.5909  2.7215   -3.551   2.761
Saurer3      160.35 -55.31 4   9.3   9550  nan   nan  9.45  8830  9.3   7075   0.00    -6.6955  3.2950   nan      nan
Kronberger39 163.56 -61.74 .8  nan   11100 nan   nan  nan   nan   6.    4372   0.00    -4.4255  1.8950   nan      nan
ESO09308     169.92 -65.22 1   9.74  14000 nan   nan  9.65  3700   9.8  13797  86.00   -4.0370  1.3845   nan      nan
vdBH144      198.78 -65.92 1.5 8.9   12000 9.17 9649  8.9   12000  9    7241   40.00   -5.1392  -0.4709  -5.11    -0.375
vdBH176      234.85 -50.05 3   nan   nan   nan   nan  nan   13400  9.8  18887  11.20   -3.9673  -3.0758  nan      nan
Kronberger31 295.05 26.26  1.3 nan   11900 nan   nan  nan   nan    8.5  12617  32.1    -2.3605  -4.6224  nan      nan
Saurer6      297.76 32.24  1.8 9.29  9330  nan   nan  9.29  9330   9.2  7329   0.00    -2.6032  -4.1481  nan      nan
Ber56        319.43 41.83  3   9.6   12100 9.47 9516  9.6   12100  9.4  13180  -54.95  -1.9199  -1.8125  -1.901  -1.831
Ber102       354.66 56.64  5   9.5   9638  9.59 10519 8.78  2600   9.14 4900   0.00    -1.556  -0.3574   -1.559  -0.340
"""
lit_data = ascii.read(lit_data)

out_folder = '../2_pipeline/plots/'


def main(dpi=dpi):
    """
    """

    # Use this block to plot the ASteCA results instead ASteCA output data
    asteca_data = ascii.read('../2_pipeline/5_ASteCA/out/asteca_output.dat')
    asteca_names = list([_[3:].upper() for _ in asteca_data['NAME']])
    asteca_pars = []
    # d_84, d_16 = [], []
    for cl in lit_data['Cluster']:
        try:
            idx = asteca_names.index(cl.upper())
            d_pc = 10**(.2 * (asteca_data[idx]['d_median'] + 5))
            # dis_84 = 10**(.2 * (asteca_data[idx]['d_84th'] + 5))/1000
            # dis_16 = 10**(.2 * (asteca_data[idx]['d_16th'] + 5))/1000
            feh = ZtoFeH(asteca_data[idx]['z_median'])
            age = asteca_data[idx]['a_median']
            mass = asteca_data[idx]['M_median']
            bfr = asteca_data[idx]['b_median']
        except ValueError:
            feh, age, d_pc, mass, bfr = [np.nan] * 5
        # asteca_dists.append(round(d_pc, 2))
        asteca_pars.append([feh, age, d_pc, mass, bfr])
        # d_16.append(round(dis_16, 2))
        # d_84.append(round(dis_84, 2))
    asteca_pars = np.array(asteca_pars).T

    plot(lit_data, asteca_pars)


def plot(lit_data, asteca_pars):
    """
    Gridspec idea: http://www.sc.eso.org/~bdias/pycoffee/codes/20160407/
                   gridspec_demo.html
    """
    # Default Galactic Center is 8.3 kpc (Gillessen et al. 2009)
    gc_frame = coord.Galactocentric()

    # Obtain latitude, longitude
    eq = SkyCoord(
        ra=lit_data['RA'] * u.degree, dec=lit_data['DEC'] * u.degree,
        frame='icrs')
    lb = eq.transform_to('galactic')
    lon = lb.l.wrap_at(180 * u.deg).radian * u.radian
    lat = lb.b.radian * u.radian

    xyz_kpc = xyzCoords(lit_data, asteca_pars[2], lon, lat, gc_frame)
    x_kpc, y_kpc, z_kpc, vx, vy, vz = xyz_kpc

    # Sun's coords according to the Galactocentric frame.
    x_sun, z_sun = gc_frame.galcen_distance, gc_frame.z_sun
    s_xys = SkyCoord(
        -x_sun, 0., z_sun, unit='kpc', representation_type='cartesian')

    Xmin, Xmax, Ymin, Ymax, Zmin, Zmax = -24, 11, -19, 16, -2.6, 2.6

    fig = plt.figure(figsize=(19, 17))
    gs = gridspec.GridSpec(grid_y, grid_x)

    ax = plt.subplot(gs[0:4, 0:4])
    plt.axhline(0, ls=':', c='grey', zorder=-1)
    plt.axvline(0, ls=':', c='grey', zorder=-1)

    im = plt.scatter(
        x_kpc, y_kpc, alpha=.75, s=asteca_pars[3] / 100, lw=.5,
        c=asteca_pars[1], edgecolor='k', zorder=2.5)
        #, vmin=8.9, vmax=9.9)
        # cmap="plasma")

    plotVectors(lit_data, x_kpc, y_kpc, vx, vy)

    # Plot Sun and center of Milky Way
    plt.scatter(s_xys.x, s_xys.y, c='yellow', s=50, edgecolor='k', zorder=2.5)
    plt.scatter(0., 0., c='k', marker='o', s=150, zorder=2.5)
    # Plot spiral arms
    cl_plots = plotSpiral()

    plt.legend(cl_plots[0], cl_plots[1], loc=4, fontsize=12)
    plt.xlim(Xmin, Xmax)
    plt.ylim(Ymin, Ymax)
    plt.xlabel(r"$x_{GC}$ [Kpc]", fontsize=15)
    plt.ylabel(r"$y_{GC}$ [Kpc]", fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='2%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.set_label(r"$\log(age)$", fontsize=15)

    #
    # X_GC vs Z_GC
    ax = plt.subplot(gs[0:2, 4:8])
    im = plt.scatter(
        x_kpc, z_kpc, alpha=.75, s=asteca_pars[3] / 100, lw=.5,
        c=asteca_pars[0], edgecolor='k', zorder=2.5, cmap='plasma')
    plt.axvline(0, ls=':', c='grey', zorder=-1)
    plt.axhline(0, ls=':', c='grey', zorder=-1)
    plt.scatter(s_xys.x, s_xys.z, c='yellow', s=50, edgecolor='k', zorder=5)
    plt.scatter(0., 0., c='k', marker='o', s=150, zorder=5)
    plt.xlabel(r"$x_{GC}\, [Kpc]$", fontsize=15)
    plt.ylabel(r"$z_{GC}\, [Kpc]$", fontsize=15)
    plt.xlim(Xmin, Xmax)
    plt.ylim(Zmin, Zmax)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plotVectors(lit_data, x_kpc, z_kpc, vx, vz)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='2%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.set_label("[Fe/H]", fontsize=15)

    #
    # Y_GC vs Z_GC
    ax = plt.subplot(gs[2:4, 4:8])
    im = plt.scatter(
        y_kpc, z_kpc, alpha=.75, s=asteca_pars[3] / 100, lw=.5,
        c=asteca_pars[4], edgecolor='k', zorder=2.5, cmap='cividis')
    plt.axvline(0, ls=':', c='grey', zorder=-1)
    plt.axhline(0, ls=':', c='grey', zorder=-1)
    plt.scatter(0., 0., c='k', marker='o', s=150, zorder=4)
    plt.scatter(s_xys.y, s_xys.z, c='yellow', s=50, edgecolor='k', zorder=5)
    plt.xlabel(r"$y_{GC}\, [Kpc]$", fontsize=15)
    plt.ylabel(r"$z_{GC}\, [Kpc]$", fontsize=15)
    plt.xlim(Ymin, Ymax)
    plt.ylim(Zmin, Zmax)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plotVectors(lit_data, y_kpc, z_kpc, vy, vz)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='2%', pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    cbar.set_label(r"$b_{fr}$", fontsize=15)

    fig.tight_layout()
    fig.savefig(out_folder + 'MWmap_AS.png', dpi=dpi, bbox_inches='tight')

    # R_GC = np.sqrt(x_kpc**2 + y_kpc**2 + z_kpc**2)
    # ascii.write([
    #     lit_data['Cluster'], lit_data['D_AS'], d_16, d_84, R_GC, x_kpc,
    #     y_kpc, z_kpc, lit_data['pmRA'], lit_data['pmDE'], lit_data['RV']],
    #     'table_CL.dat', names=[
    #         'Cl', 'Dist', 'd_16', 'd_84', 'R_GC', 'X', 'Y', 'Z', 'pmRA',
    #         'pmDE', 'RV'], overwrite=True)


def plotVectors(lit_data, x, y, vx, vy):
    """
    """
    vxy = np.sqrt(vx**2 + vy**2)
    xyf = x + vx / (vxy.max()) * 6
    yxf = y + vy / (vxy.max()) * 6
    for i, xi in enumerate(x):
        if lit_data['RV'][i] != 0.00:
            # plt.arrow(
            #     x=xi, y=y[i], dx=xyf[i] - xi,
            #     dy=yxf[i] - y[i], color='slateblue', overhang=10,
            #     width=wd, head_width=hw, head_length=hl)
            #
            # The above made the arrow heads look weird
            # Source: https://stackoverflow.com/a/52613154/1391441
            txt = "-|>,head_width={},head_length={}".format(0.3, 0.5)
            # color='slateblue'
            prop = dict(
                arrowstyle=txt, color='k', shrinkA=0, shrinkB=0)
            plt.annotate(
                "", xy=(xyf[i], yxf[i]), xytext=(xi, y[i]), arrowprops=prop,
                zorder=0)


def xyzCoords(data, dist_pc, lon, lat, gc_frame):
    """
    """
    # Galactic coordinates.
    coords = coord.SkyCoord(
        ra=data['RA'] * u.degree, dec=data['DEC'] * u.degree,
        distance=dist_pc * u.pc,
        pm_ra_cosdec=data['pmRA'] * u.mas / u.yr,
        pm_dec=data['pmDE'] * u.mas / u.yr,
        radial_velocity=data['RV'] * u.km / u.s, frame='icrs')

    # Galactocentric coordinates.
    c_glct = coords.transform_to(gc_frame)

    # Rectangular coordinates
    x_kpc, y_kpc, z_kpc = np.array(c_glct.x.to(u.kpc)), np.array(
        c_glct.y.to(u.kpc)), np.array(c_glct.z.to(u.kpc))

    # Velocities
    vx, vy, vz = np.array(c_glct.v_x), np.array(c_glct.v_y), np.array(
        c_glct.v_z)

    return x_kpc, y_kpc, z_kpc, vx, vy, vz


if __name__ == '__main__':
    # plt.style.use(['science', 'no-latex'])
    plt.style.use('science')
    main()
