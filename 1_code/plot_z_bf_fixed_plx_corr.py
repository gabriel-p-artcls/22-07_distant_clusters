

"""
Generates two plots:

1. Difference between the distances estimated with the ASteCA run
setting all the fundamental parameters free, and several runs with either
the metallicity, the binary fraction, or both fixed.

Runs in 'asteca_zfixed.dat':

01/02: z=0.0152, b_fr=0.0
03/04: z=0.0152, b_fr=free
05   : z=free  , b_fr=0.0
06   : z=0.0152, b_fr=0.3


2. Distances estimated by ASteCA vs other distance estimates.

The median is obtained as 1000/median(plx_i) (for all members), the MAD is
obtained as MAD(1000 / plx). The 'plx_median_MAD.py' script obtains these
values

The 'ASteCA _16 _84' columns are obtained through Bayesian inference of the
parallaxes with a uniform prior, using ASteCA (the first column is the median).

The 'Kalkayotl _16K  _84K' columns are obtained with the Kalkayotl code
using a uniform prior.
"""

import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from plot_pars import dpi, grid_x, grid_y, sc_sz, sc_ec, sc_lw


# Distances obtained with the corrected parallaxes
plx_corr_data = """
Cluster      plx_median plx_MAD ASteCA _16   _84   Kalkayotl _16K  _84K
arpm2        9734       5256    8038   7718  8401  8251      7380  9350
ber102       9840       5754    8029   7665  8438  8245      7346  9449
ber25        7447       3034    7147   6954  7357  7276      6619  8027
ber26        5412       2404    4940   4688  5217  5001      4562  5522
ber29        11315      5603    7930   7648  8234  8224      7332  9256
ber56        10068      4972    9318   9077  9589  9541      8524  10814
ber73        7577       3224    6881   6594  7196  6999      6326  7843
ber75        6586       2907    6894   6628  7189  6997      6351  7830
ber76        5242       1887    4559   4465  4657  4580      4320  4884
czernik30    5958       1588    5958   5813  6112  6035      5593  6558
eso09205     11355      6467    11514  10987 12108 11836     10191 13924
eso09218     9779       5548    7219   7094  7350  4510      4321  4709
eso09308     10011      5698    9807   9109  10660 10336     8856  12528
fsr1212      6504       2477    5297   5096  5507  5326      4924  5814
fsr1419      8732       4333    8611   8211  9057  8946      7953  10314
kronberger31 8468       5222    6871   6638  7115  6959      6336  7725
kronberger39 7941       4999    6337   5899  6825  6227      5566  7065
saurer1      7169       3193    6566   6057  7175  6692      5856  7821
saurer3      7117       3965    4528   4398  4668  4573      4274  4920
saurer6      9483       5683    9346   8762  9981  7841      7003  8872
tombaugh2    7342       3015    5513   5452  5574  4442      4254  4635
vdbh144      10495      5156    8330   8060  8621  8806      7881  9962
vdbh176      10660      4587    5211   5078  5352  4141      3968  4329
vdbh37       3459       408     3496   3461  3529  3509      3357  3675
vdbh4        7579       2916    7670   7238  8147  7989      7071  9158
"""

short_n = {
    'saurer1': 'SAU1', 'czernik30': 'CZER30', 'arpm2': 'ARPM2',
    'saurer3': 'SAUR3', 'ber102': 'BER102', 'eso09205': 'E9205',
    'saurer6': 'SAU6', 'ber25': 'BER25', 'ber26': 'BER26',
    'eso09218': 'E9218', 'tombaugh2': 'TOMB2', 'eso09308': 'E9308',
    'vdbh144': 'BH144', 'fsr1212': 'F1212', 'ber56': 'BER56',
    'fsr1419': 'F1419', 'ber73': 'BER73', 'kronberger31': 'KRON31',
    'vdbh37': 'BH37', 'ber75': 'BER75', 'kronberger39': 'KRON39',
    'vdbh4': 'BH4', 'ber76': 'BER76', 'ber29': 'BER29', 'vdbh176': 'BH176'}

root_f = '../2_pipeline/5_ASteCA/'
out_folder = '../2_pipeline/plots/'


def main(dpi=dpi):
    """
    """
    # ASteCA output data
    asteca_data = ascii.read('../2_pipeline/5_ASteCA/out/asteca_output.dat')
    d_asteca = {}
    for cl in asteca_data:
        d_asteca[cl['NAME'][3:]] = ditsMod2pc([cl['d_median']])[0]

    # ASteCA z fixed data
    asteca_zfixed = ascii.read('../2_pipeline/5_ASteCA/out/asteca_zfixed.dat')
    z_bf_fixed, z_fixed, b_fixed, z_bf_fixed2 = {}, {}, {}, {}
    for cl in asteca_zfixed:
        d_pc = ditsMod2pc([cl['d_median']])[0]
        if cl['NAME'].startswith('01') or cl['NAME'].startswith('02'):
            z_bf_fixed[cl['NAME'][3:]] = d_pc
        elif cl['NAME'].startswith('03') or cl['NAME'].startswith('04'):
            z_fixed[cl['NAME'][3:]] = d_pc
        elif cl['NAME'].startswith('05'):
            b_fixed[cl['NAME'][3:]] = d_pc
        elif cl['NAME'].startswith('06'):
            z_bf_fixed2[cl['NAME'][3:]] = d_pc

    # Plx distances
    plx_data = ascii.read(plx_corr_data)
    plx_median, plx_asteca, plx_kalkayotl = {}, {}, {}
    for cl in plx_data:
        plx_median[cl['Cluster']] = cl['plx_median']
        plx_asteca[cl['Cluster']] = cl['ASteCA']
        plx_kalkayotl[cl['Cluster']] = cl['Kalkayotl']

    #
    fig = plt.figure(figsize=(20, 20))
    gs = gridspec.GridSpec(grid_y, grid_x)

    ax = plt.subplot(gs[0:2, 0:2])
    sols = {
        'z_bf_fixed': (z_bf_fixed, r'$Z=Z_{\odot},b_{fr}=0.0$'),
        'z_fixed': (z_fixed, r'$Z=Z_{\odot}$'),
        'b_fixed': (b_fixed, r'$b_{fr}=0.0$'),
        'z_bf_fixed2': (z_bf_fixed2, r"$Z=Z_{\odot},b_{fr}=0.3$")
    }
    plotDistDelta(ax, d_asteca, sols)

    ax = plt.subplot(gs[2:4, 0:2])
    sols = {
        'plx_median': (plx_median, r'median(Plx)$^{-1}$'),
        'plx_asteca': (plx_asteca, 'ASteCA'),
        'plx_kalkayotl': (plx_kalkayotl, 'Kalkayotl')
    }
    plotDistDelta(ax, d_asteca, sols, True)

    fig.tight_layout()
    plt.savefig(
        out_folder + "d_zb_fixed_plx.png", dpi=dpi, bbox_inches='tight')


def plotDistDelta(ax, d_asteca, sols, xlabel=False):
    """
    """
    cols = sns.color_palette()
    marker = ('o', '*', '^', 'v')

    for i, (k, sol) in enumerate(sols.items()):
        # print(sol)
        x, y = [], []
        for cl, d_a in d_asteca.items():
            x.append(d_a)
            y.append(d_a - sol[0][cl])
        ax.scatter(
            x, y, alpha=.6, color=cols[i], marker=marker[i], label=sol[1],
            s=sc_sz, lw=sc_lw, ec=sc_ec)
        ax.axhline(np.median(y), ls=':', c=cols[i], lw=1.5)

        # # Tested linear fit, There is no appreciable slope in the fit
        # from sklearn.linear_model import LinearRegression
        # X = np.array(x).reshape(-1, 1)
        # reg = LinearRegression().fit(X, y)
        # xx = np.arange(min(x), max(x), 10)
        # yy = reg.predict(xx.reshape(-1, 1))
        # plt.plot(xx, yy, ls=':', c=cols[i], lw=2)

    ax.axhline(0, ls='--', c='k', lw=2)
    if xlabel is True:
        ax.set_xlabel("ASteCA [pc]", fontsize=14)
        leg_pos = 'upper left'
        ax.set_ylabel(r"(ASteCA - Plx dist$^{*}$) [pc]", fontsize=14)
    else:
        leg_pos = 'lower right'
        ax.set_ylabel(r"(ASteCA - ASteCA$^{*}$) [pc]", fontsize=14)
    ax.legend(loc=leg_pos, frameon=True, framealpha=0.5)
    # plt.xlim(2100, 16400)


def ditsMod2pc(dms):
    """
    Distance modulus to distance in parsec
    """
    d_pc = []
    for dm in dms:
        d_pc.append(10**(.2 * (dm + 5)))

    return d_pc


if __name__ == '__main__':
    plt.style.use('science')
    main()
