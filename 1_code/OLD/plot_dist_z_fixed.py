

"""
Plot the difference between the distances estimated with the ASteCA run
setting all the fundamental parameters free, and several runs with either
the metallicity, the binary fraction, or both fixed.

Runs in 'asteca_zfixed.dat':

01/02: z=0.0152, b_fr=0.0
03/04: z=0.0152, b_fr=free
05   : z=free  , b_fr=0.0
06   : z=0.0152, b_fr=0.3
"""

import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
import seaborn as sns


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


def main(dpi=300):
    """
    """
    # ASteCA output data
    asteca_data = ascii.read('../2_pipeline/5_ASteCA/out/asteca_output.dat')
    dists_ages = {}
    for cl in asteca_data:
        d_pc = 10**(.2 * (cl['d_median'] + 5))
        d_16th = 10**(.2 * (cl['d_16th'] + 5))
        d_84th = 10**(.2 * (cl['d_84th'] + 5))
        age = cl['a_median']
        dists_ages[cl['NAME'][3:]] = (d_pc, d_16th, d_84th, age)

    # ASteCA z fixed data
    asteca_zfixed = ascii.read('../2_pipeline/5_ASteCA/out/asteca_zfixed.dat')

    z_bf_fixed, z_fixed, b_fixed, z_bf_fixed2 = {}, {}, {}, {}
    for cl in asteca_zfixed:
        if cl['NAME'].startswith('01') or cl['NAME'].startswith('02'):
            d_pc = 10**(.2 * (cl['d_median'] + 5))
            d_16th = 10**(.2 * (cl['d_16th'] + 5))
            d_84th = 10**(.2 * (cl['d_84th'] + 5))
            age = cl['a_median']
            z_bf_fixed[cl['NAME'][3:]] = (d_pc, d_16th, d_84th, age)
        elif cl['NAME'].startswith('03') or cl['NAME'].startswith('04'):
            d_pc = 10**(.2 * (cl['d_median'] + 5))
            d_16th = 10**(.2 * (cl['d_16th'] + 5))
            d_84th = 10**(.2 * (cl['d_84th'] + 5))
            age = cl['a_median']
            z_fixed[cl['NAME'][3:]] = (d_pc, d_16th, d_84th, age)
        elif cl['NAME'].startswith('05'):
            d_pc = 10**(.2 * (cl['d_median'] + 5))
            d_16th = 10**(.2 * (cl['d_16th'] + 5))
            d_84th = 10**(.2 * (cl['d_84th'] + 5))
            age = cl['a_median']
            b_fixed[cl['NAME'][3:]] = (d_pc, d_16th, d_84th, age)
        elif cl['NAME'].startswith('06'):
            d_pc = 10**(.2 * (cl['d_median'] + 5))
            d_16th = 10**(.2 * (cl['d_16th'] + 5))
            d_84th = 10**(.2 * (cl['d_84th'] + 5))
            age = cl['a_median']
            z_bf_fixed2[cl['NAME'][3:]] = (d_pc, d_16th, d_84th, age)

    fig, ax = plt.subplots(figsize=(5, 5))

    z_sols = {
        'z_bf_fixed': z_bf_fixed, 'z_fixed': z_fixed, 'b_fixed': b_fixed,
        'z_bf_fixed2': z_bf_fixed2}
    cols = sns.color_palette()
    marker = ('o', '*', '^', 'v')
    labels = (
        r'$Z=Z_{\odot},b_{fr}=0.0$', r'$Z=Z_{\odot}$', r'$b_{fr}=0.0$',
        r"$Z=Z_{\odot},b_{fr}=0.3$")

    for i, sol in enumerate((
            'z_bf_fixed', 'z_fixed', 'b_fixed', 'z_bf_fixed2')):
        print(sol)
        x, y = [], []
        for cl, d_a in dists_ages.items():
            x.append(d_a[0])
            y.append(d_a[0] - z_sols[sol][cl][0])
        ax.scatter(
            x, y, alpha=.6, color=cols[i], marker=marker[i],
            label=labels[i])
        ax.axhline(np.median(y), ls=':', c=cols[i], lw=2)

        # # Tested linear fit, There is no appreciable slope in the fit
        # from sklearn.linear_model import LinearRegression
        # X = np.array(x).reshape(-1, 1)
        # reg = LinearRegression().fit(X, y)
        # xx = np.arange(min(x), max(x), 10)
        # yy = reg.predict(xx.reshape(-1, 1))
        # plt.plot(xx, yy, ls=':', c=cols[i], lw=2)

    ax.axhline(0, ls='--', c='k', lw=.8)
    ax.set_xlabel("ASteCA [pc]", fontsize=14)
    ax.set_ylabel(r"ASteCA - ASteCA$^{*}$ [pc]", fontsize=14)
    ax.legend(loc='lower right', frameon=True)

    fig.tight_layout()
    plt.savefig(out_folder + "d_zb_fixed.png", dpi=dpi, bbox_inches='tight')


if __name__ == '__main__':
    plt.style.use('science')
    main()
