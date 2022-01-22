
"""
Plot the distances obtained with ASteCA versus those from the four databases
"""


from astropy.io import ascii
# import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.gridspec as gridspec
from plot_pars import dpi, grid_x, grid_y, sc_sz, sc_ec, sc_lw, ft_sz


lit_data = """
Cluster      RA  DEC       Dm  A_OC  D_OC  A_CG D_CG  A_WB  D_WB  A_MW  D_MW
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
Shorlin1     166.44 -61.23 .8  nan   nan   nan   nan  nan   12600 6.5   5594
ESO09308     169.92 -65.22 1   9.74  14000 nan   nan  9.65  3700   9.8  13797
vdBH144      198.78 -65.92 1.5 8.9   12000 9.17 9649  8.9   12000  9    7241
vdBH176      234.85 -50.05 3   nan   nan   nan   nan  nan   13400  9.8  18887
Kronberger31 295.05 26.26  1.3 nan   11900 nan   nan  nan   nan    8.5  12617
Saurer6      297.76 32.24  1.8 9.29  9330  nan   nan  9.29  9330   9.2  7329
Ber56        319.43 41.83  3   9.6   12100 9.47 9516  9.6   12100  9.4  13180
FSR0338      327.93 55.33  2.7 8.1   14655 nan   nan  nan   nan    8.1  14655
Ber102       354.66 56.64  5   9.5   9638  9.59 10519 8.78  2600   9.14 4900
"""
lit_data = ascii.read(lit_data)

in_folder = '../2_pipeline/5_ASteCA/out/'
out_folder = '../2_pipeline/plots/'


def main(dpi=dpi):
    """
    """
    data = ascii.read(in_folder + 'asteca_output.dat')

    lit_names = [_.lower() for _ in lit_data['Cluster']]
    age_dct = {'x': [], 'A_MW': [], 'A_WB': [], 'A_OC': [], 'A_CG': []}
    for cl in data:
        cl_name = cl['NAME'][3:]
        cl_i = lit_names.index(cl_name)
        age_asteca = (10**cl['a_median']) / 1e9
        age_dct['x'].append(age_asteca)
        age_dct['A_MW'].append(age_asteca - (10**lit_data[cl_i]['A_MW']) / 1e9)
        age_dct['A_WB'].append(age_asteca - (10**lit_data[cl_i]['A_WB']) / 1e9)
        age_dct['A_OC'].append(age_asteca - (10**lit_data[cl_i]['A_OC']) / 1e9)
        age_dct['A_CG'].append(age_asteca - (10**lit_data[cl_i]['A_CG']) / 1e9)
        print("{:<17}: {:.2f} {:.2f} {:.2f} {:.2f}".format(
            cl_name, cl['a_median'] - lit_data[cl_i]['A_MW'],
            cl['a_median'] - lit_data[cl_i]['A_WB'],
            cl['a_median'] - lit_data[cl_i]['A_OC'],
            cl['a_median'] - lit_data[cl_i]['A_CG']))

    #
    fig = plt.figure(figsize=(25, 25))
    gs = gridspec.GridSpec(grid_y, grid_x)
    ax = plt.subplot(gs[0:1, 0:2])

    ax.scatter(age_dct['x'], age_dct['A_MW'], label="MWSC",
               s=sc_sz, ec=sc_ec, lw=sc_lw, alpha=.5, marker='o')
    ax.scatter(age_dct['x'], age_dct['A_WB'], label="WEBDA",
               s=sc_sz, ec=sc_ec, lw=sc_lw, alpha=.5, marker='s')
    ax.scatter(age_dct['x'], age_dct['A_OC'], label="OC02",
               s=sc_sz, ec=sc_ec, lw=sc_lw, alpha=.5, marker='^')
    ax.scatter(age_dct['x'], age_dct['A_CG'], label="CG20",
               s=sc_sz, ec=sc_ec, lw=sc_lw, alpha=.5, marker='v')

    ax.axhline(0, ls=':', c='k')
    ax.set_xlabel("ASteCA [Gyr]", fontsize=ft_sz)
    ax.set_ylabel("(ASteCA - DB) [Gyr]", fontsize=ft_sz)
    plt.legend()

    fig.tight_layout()
    plt.savefig(out_folder + "ages.png", dpi=dpi, bbox_inches='tight')


if __name__ == '__main__':
    plt.style.use('science')
    main()
