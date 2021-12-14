
"""
Generate the age versus FeH plot
"""

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import ascii
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from plot_pars import dpi, grid_x, grid_y, ft_sz, sc_sz, sc_ec, sc_lw
from plot_Fe_vs_R import xyzCoords, ZtoFeH

radec_data = """
Cluster      RA  DEC
Ber73        95.50  -6.35
Ber25        100.25 -16.52
Ber75        102.25 -24.00
Ber26        102.58 5.75
Ber29        103.27 16.93
Tombaugh2    105.77 -20.82
Ber76        106.67 -11.73
FSR1212      106.94 -14.15
Saurer1      110.23 1.81
Czernik30    112.83 -9.97
arpm2        114.69 -33.84
vdBH4        114.43 -36.07
FSR1419      124.71 -47.79
vdBH37       128.95 -43.62
ESO09205     150.81 -64.75
ESO09218     153.74 -64.61
Saurer3      160.35 -55.31
Kronberger39 163.56 -61.74
ESO09308     169.92 -65.22
vdBH144      198.78 -65.92
vdBH176      234.85 -50.05
Kronberger31 295.05 26.26
Saurer6      297.76 32.24
Ber56        319.43 41.83
Ber102       354.66 56.64
"""
radec_data = ascii.read(radec_data)

# The 10 verified clusters from the original set of 16
_16_clusts = """
Cluster,z,ez,age,ea,E_BV,eE,Mass,eM,dist,ed,lon,lat
vdBH73,0.019,0.004,0.78,0.09,1.06,0.04,2.6,0.9,5.01,0.61,273.634,0.951
RUP85,0.021,0.003,0.18,0.03,1.06,0.03,2.6,0.5,4.80,0.26,280.15,0.160
vdBH85,0.014,0.002,7.50,0.80,0.30,0.03,2.2,0.5,4.61,0.26,276.914,4.544
vdBH87,0.025,0.002,0.25,0.08,0.55,0.04,1.4,0.2,2.08,0.09,280.719,0.059
TR12,0.009,0.002,0.70,0.10,0.31,0.03,0.7,0.1,3.50,0.15,283.828,-3.698
vdBH92,0.009,0.004,0.02,0.01,0.65,0.03,0.4,0.1,2.59,0.11,282.984,0.438
TR13,0.007,0.004,0.11,0.02,0.56,0.02,0.7,0.2,4.81,0.33,285.515,-2.353
vdBH106,0.012,0.003,3.00,0.80,0.30,0.04,0.5,0.2,4.87,0.81,286.048,4.700
RUP162,0.009,0.002,0.80,0.20,0.54,0.03,1.2,0.2,4.43,0.20,289.638,-2.545
NGC4349,0.011,0.004,0.29,0.09,0.41,0.05,2.0,0.1,1.88,0.05,299.719,0.830
"""
_16_clusts = ascii.read(_16_clusts)

in_folder = '../2_pipeline/5_ASteCA/out/'
out_folder = '../2_pipeline/plots/'


def main(dpi=dpi):
    """
    """
    asteca_data = ascii.read(in_folder + 'asteca_output.dat')

    radec_names = list([_.upper() for _ in radec_data['Cluster']])
    radec = []
    for cl in asteca_data:
        idx = radec_names.index(cl['NAME'][3:].upper())
        radec.append((radec_data['RA'][idx], radec_data['DEC'][idx]))
    radec = np.array(radec).T

    # Obtain latitude, longitude
    eq = SkyCoord(
        ra=radec[0] * u.degree, dec=radec[1] * u.degree, frame='icrs')
    lb = eq.transform_to('galactic')
    lon = lb.l.wrap_at(180 * u.deg).radian * u.radian
    lat = lb.b.radian * u.radian

    dist_pc = 10**(.2 * (np.array(
        [asteca_data['d_16th'], asteca_data['d_median'],
         asteca_data['d_84th']]) + 5))
    R_GC = xyzCoords(dist_pc, lon, lat)

    Age = (10**asteca_data['a_median']) / 1e9
    Age_16 = (10**asteca_data['a_16th']) / 1e9
    Age_84 = (10**asteca_data['a_84th']) / 1e9
    FeH = ZtoFeH(asteca_data['z_median'])
    FeH_16 = ZtoFeH(asteca_data['z_16th'])
    FeH_84 = ZtoFeH(asteca_data['z_84th'])

    dist_pc, lon, lat = _16_clusts['dist'] * 1000., _16_clusts['lon'],\
        _16_clusts['lat']
    lon, lat = lon * u.deg, lat * u.deg
    _16_R_GC = xyzCoords(dist_pc, lon, lat)
    _16_Age = _16_clusts['age']  # np.log10(_16_clusts['age'] * 1e9)
    _16_Age_std = _16_clusts['ea']
    _16_FeH = ZtoFeH(_16_clusts['z'])
    _16_FeH_std = _16_clusts['ez'] / (_16_clusts['z'] * np.log(10))

    #
    fig = plt.figure(figsize=(20, 20))
    gs = gridspec.GridSpec(grid_y, grid_x)

    ax = plt.subplot(gs[0:2, 0:2])

    x, y = _16_FeH.value, _16_Age
    plt.errorbar(
        x, y, xerr=_16_FeH_std, yerr=_16_Age_std, fmt='none', c='grey',
        ls='none', zorder=0)
    plt.scatter(
        x, y, marker='^', s=sc_sz, c=_16_R_GC, ec=sc_ec, lw=sc_lw)

    x, y = FeH.value, Age
    xerr = np.array([x - FeH_16, FeH_84 - x])
    yerr = np.array([y - Age_16, Age_84 - y])
    plt.errorbar(
        x, y, xerr=xerr, yerr=yerr, fmt='none', c='grey', ls='none', zorder=0)
    plt.scatter(
        x, y, s=sc_sz, c=R_GC.T[1].value, ec=sc_ec, lw=sc_lw, zorder=5)

    # ax.annotate("SAU1", (txt['saurer1'][0] + .25, txt['saurer1'][1] + .025))

    # plt.xlim(7., 23)
    # plt.ylim(-0.75, 0.3)
    cbar = plt.colorbar()
    cbar.set_label(r"$R_{GC}$ [kpc]", fontsize=ft_sz)
    plt.ylabel("t (Gyr)", fontsize=ft_sz)
    plt.xlabel("[Fe/H]", fontsize=ft_sz)

    fig.tight_layout()
    plt.savefig(out_folder + "age_vs_Fe_H.png", dpi=dpi, bbox_inches='tight')


if __name__ == '__main__':
    plt.style.use('science')
    main()
