
from astropy import units as u
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord
from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np

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


def main():
    """
    Plot [Fe/H] vs R_GC distribution for the ASteCA results
    """
    asteca_data = ascii.read('../2_pipeline/5_ASteCA/out/asteca_output.dat')

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

    dist_pc = 10**(.2 * (asteca_data['d_median'] + 5))
    R_GC = xyzCoords(dist_pc, lon, lat)
    Fe = np.log(asteca_data['z_median'] / 0.0152)
    Fe_std = asteca_data['z_std'] / asteca_data['z_median'] * (1 / np.log(10))
    for i, _ in enumerate(asteca_data['NAME']):
        print("{}, Fe={:.2f}, R_GC={:.1f}".format(_[3:], Fe[i], R_GC[i]))

    plt.errorbar(
        R_GC.value, Fe.value, yerr=Fe_std, fmt='o', c='grey', ls='none')
    # plt.scatter(R_GC, Fe)
    plt.show()


def xyzCoords(dist_pc, lon, lat):
    """
    """
    gc_frame = coord.Galactocentric()
    dist_pc = dist_pc / 1000.

    # Galactic coordinates.
    coords = SkyCoord(l=lon, b=lat, distance=dist_pc * u.kpc, frame='galactic')

    # Galactocentric coordinates.
    c_glct = coords.transform_to(gc_frame)

    # Rectangular coordinates
    x_kpc, y_kpc, z_kpc = c_glct.x, c_glct.y, c_glct.z

    return np.sqrt(x_kpc**2 + y_kpc**2 + z_kpc**2)


if __name__ == '__main__':
    main()
