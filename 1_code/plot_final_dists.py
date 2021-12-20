
"""
Plot the distances obtained with ASteCA versus those from the four databases
"""


from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from adjustText import adjust_text
from plot_pars import dpi, grid_x, grid_y, ft_sz, sc_sz, sc_ec, sc_lw


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

short_n = {
    'saurer1': 'SAU1', 'czernik30': 'CZER30', 'arpm2': 'ARPM2',
    'saurer3': 'SAU3', 'ber102': 'BER102', 'eso09205': 'E9205',
    'saurer6': 'SAU6', 'ber25': 'BER25', 'ber26': 'BER26',
    'eso09218': 'E9218', 'tombaugh2': 'TOMB2', 'eso09308': 'E9308',
    'vdbh144': 'BH144', 'fsr1212': 'F1212', 'ber56': 'BER56',
    'fsr1419': 'F1419', 'ber73': 'BER73', 'kronberger31': 'KRON31',
    'vdbh37': 'BH37', 'ber75': 'BER75', 'kronberger39': 'KRON39',
    'vdbh4': 'BH4', 'ber76': 'BER76', 'ber29': 'BER29', 'vdbh176': 'BH176'}

in_folder = '../2_pipeline/5_ASteCA/out/'
out_folder = '../2_pipeline/plots/'


def main(dpi=dpi):
    """
    """
    data = ascii.read(in_folder + 'asteca_output.dat')

    lit_names = [_.lower() for _ in lit_data['Cluster']]
    age_dct, dist_dct = {}, {}
    vmin, vmax = 1000, 0
    for cl in data:
        cl_name = cl['NAME'][3:]
        cl_i = lit_names.index(cl_name)
        age_dct[cl_name] = cl['a_median']
        vmin, vmax = min(vmin, cl['a_median']), max(vmax, cl['a_median'])
        dist_dct[cl_name] = (
            cl['d_median'], cl['d_16th'], cl['d_84th'], lit_data[cl_i]['D_MW'],
            lit_data[cl_i]['D_WB'], lit_data[cl_i]['D_OC'],
            lit_data[cl_i]['D_CG'])

    fig = plt.figure(figsize=(20, 20))
    gs = gridspec.GridSpec(grid_y, grid_x)
    # xlab = ('MWSC', 'WEBDA', 'OPENCLUST', 'Cantat-Gaudin')
    xylim = (100, 20800)

    # y0, y1, x0, x1
    gs_ij = ((0, 2, 0, 2), (0, 2, 2, 4), (2, 4, 0, 2), (2, 4, 2, 4))

    for db_id, xlab in enumerate(
            ('MWSC', 'WEBDA', 'OPENCLUST', 'Cantat-Gaudin')):

        dd = {}
        for cl, vals in dist_dct.items():
            x, y, y_16, y_84 = list(map(
                float, (vals[db_id + 3], vals[0], vals[1], vals[2])))
            # Skip missing clusters
            if np.isnan(x):
                continue
            y, y_16, y_84 = 10**(.2 * (y + 5)), 10**(.2 * (y_16 + 5)),\
                10**(.2 * (y_84 + 5))
            dd[cl] = (x, y, y_16, y_84, age_dct[cl])

        y0, y1, x0, x1 = gs_ij[db_id]
        ax1 = plt.subplot(gs[y0:y1, x0:x1])

        texts = []
        for cl, (x, y, y_16, y_84, col) in dd.items():
            yerr = np.array([[y - y_16, y_84 - y]]).T
            ax1.errorbar(x, y, yerr=yerr, fmt='', c='grey', zorder=1)
            ax1.scatter(
                x, y, c=col, s=sc_sz, ec=sc_ec, lw=sc_lw,
                zorder=4, vmin=vmin, vmax=vmax)
            texts.append(ax1.text(x, y, short_n[cl]))

        adjust_text(texts)
        ax1.plot(xylim, xylim, ls='--', c='k', lw=1.5, zorder=0)
        ax1.set_xlim(*xylim)
        ax1.set_ylim(*xylim)
        if db_id in (0, 1):
            ax1.set_xticklabels([])
        if db_id in (1, 3):
            ax1.set_yticklabels([])
        ax1.set_xlabel("{} [pc]".format(xlab), fontsize=ft_sz)
        if db_id in (0, 2):
            ax1.set_ylabel("ASteCA [pc]", fontsize=ft_sz)

        #
        ax2 = plt.subplot(gs[db_id:db_id + 1, 4:6])
        for cl, (x, y, y_16, y_84, col) in dd.items():
            yerr = np.array([[y - y_16, y_84 - y]]).T
            ax2.errorbar(
                x, x - y, yerr=yerr, fmt='', c='grey', zorder=1)
            im = ax2.scatter(
                x, x - y, c=col, s=sc_sz, ec=sc_ec, lw=sc_lw,
                vmin=vmin, vmax=vmax, zorder=4)

        ax2.plot(xylim, (0, 0), ls='--', c='k', lw=1.5, zorder=0)
        ax2.set_xlim(*xylim)
        ax2.set_xlabel("{} [pc]".format(xlab), fontsize=ft_sz)
        # if db_id in (0, 2):
        # ax2.set_ylabel(r"$\Delta$ [pc]", fontsize=ft_sz)

        # if db_id in (1, 3):
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.set_ylabel(r"$\log$ age", fontsize=ft_sz)

    fig.tight_layout()
    plt.savefig(out_folder + "dist.png", dpi=dpi, bbox_inches='tight')


if __name__ == '__main__':
    plt.style.use('science')
    main()

    # for i in (0, 2):
    #     for j in (0, 1, 2, 3):
    #         yf = i + 2 if i == 0 else i + 1
    #         ax = plt.subplot(gs[i:yf, 2 * j:2 * j + 2])
    #         texts = []
    #         for cl, vals in dist_dct.items():
    #             x, y, y_16, y_84 = list(map(
    #                 float, (vals[j + 3], vals[0], vals[1], vals[2])))
    #             # Skip missing clusters
    #             if np.isnan(x):
    #                 continue

    #             y, y_16, y_84 = 10**(.2 * (y + 5)), 10**(.2 * (y_16 + 5)),\
    #                 10**(.2 * (y_84 + 5))
    #             col = age_dct[cl]
    #             if i == 0:
    #                 yerr = np.array([[y - y_16, y_84 - y]]).T
    #                 ax.errorbar(x, y, yerr=yerr, fmt='', c='grey', zorder=1)
    #                 im = ax.scatter(
    #                     x, y, c=col, s=sc_sz, ec=sc_ec, lw=sc_lw,
    #                     zorder=4, vmin=vmin, vmax=vmax)
    #                 # xo = np.random.choice((-3000, 200))
    #                 # yo = np.random.choice((-1000, 500))
    #                 # ax.annotate(short_n[cl], (x + xo, y + yo), zorder=5)
    #             else:
    #                 yerr = np.array([[y - y_16, y_84 - y]]).T
    #                 ax.errorbar(
    #                     x, x - y, yerr=yerr, fmt='', c='grey', zorder=1)
    #                 im = ax.scatter(
    #                     x, x - y, c=col, s=sc_sz, ec=sc_ec, lw=sc_lw,
    #                     vmin=vmin, vmax=vmax, zorder=4)
    #             if i == 0:
    #                 texts.append(ax.text(x, y, short_n[cl]))

    #         if i == 0:
    #             adjust_text(texts)
    #             ax.plot(xylim, xylim, ls='--', c='k', lw=1.5, zorder=0)
    #             ax.set_xlim(*xylim)
    #             ax.set_ylim(*xylim)
    #             ax.set_xticklabels([])
    #             # ax.set_xlabel("{} [pc]".format(xlab[j]), fontsize=14)
    #             if j == 0:
    #                 ax.set_ylabel("ASteCA [pc]")
    #         if i == 2:
    #             ax.plot(xylim, (0, 0), ls='--', c='k', lw=1.5, zorder=0)
    #             ax.set_xlim(*xylim)
    #             ax.set_xlabel("{} [pc]".format(xlab[j]))
    #             if j == 0:
    #                 ax.set_ylabel(r"(DB - ASteCA) [pc]")
    #         # if j != 0:
    #         #     ax.set_yticklabels([])
    #         if j == 3:
    #             divider = make_axes_locatable(ax)
    #             cax = divider.append_axes('right', size='5%', pad=0.05)
    #             cbar = fig.colorbar(im, cax=cax, orientation='vertical')
    #             cbar.ax.set_ylabel(r"$\log$ age")
