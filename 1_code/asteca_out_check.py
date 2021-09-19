
from astropy.io import ascii
import numpy as np
from numpy.random import MT19937, RandomState, SeedSequence
import matplotlib.pyplot as plt

# Set random seed
seed = np.random.randint(100000000)
print("Random seed: {}".format(seed))
RandomState(MT19937(SeedSequence(seed)))

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
root_f = '../2_pipeline/5_ASteCA/'
out_folder = 'tmp/'


def main():
    """
    """
    DBvsASteCA()

    # ASteCAvsASteCA()


def DBvsASteCA():
    """
    """
    in_folder = root_f + 'out/'

    data = ascii.read(in_folder + 'asteca_output.dat')

    lit_names = [_.lower() for _ in lit_data['Cluster']]
    age_dct, dist_dct = {}, {}
    for cl in data:
        cl_name = cl['NAME'][3:]
        cl_i = lit_names.index(cl_name)
        age_dct[cl_name] = (
            cl['a_median'], cl['a_16th'], cl['a_84th'], lit_data[cl_i]['A_OC'],
            lit_data[cl_i]['A_CG'], lit_data[cl_i]['A_WB'],
            lit_data[cl_i]['A_MW'])
        dist_dct[cl_name] = (
            cl['d_median'], cl['d_16th'], cl['d_84th'], lit_data[cl_i]['D_OC'],
            lit_data[cl_i]['D_CG'], lit_data[cl_i]['D_WB'],
            lit_data[cl_i]['D_MW'])

    xlab = ('OPENCLUST', 'C-G', 'WEBDA', 'MWSC')

    fig, axes = plt.subplots(1, 4, figsize=(24, 6))
    for i, ax in enumerate(axes):
        xymin, xymax = 20, 0
        for cl, vals in age_dct.items():
            x, y, y_16, y_84 = list(map(
                float, (vals[i + 3], vals[0], vals[1], vals[2])))
            yerr = np.array([[y - y_16, y_84 - y]]).T
            col = dist_dct[cl][0]
            ax.errorbar(x, y, yerr=yerr, fmt='', c='grey', alpha=.5, zorder=1)
            ax.scatter(x, y, c=col, vmin=12, vmax=16, zorder=4)
            xymin, xymax = min(xymin, x, y), max(xymax, x, y)
            ax.annotate(cl, (x + .02, y))
        xymin, xymax = xymin - .2, xymax + .2
        ax.plot((xymin, xymax), (xymin, xymax), ls='--', marker='', lw=.8)
        ax.set_xlim(xymin, xymax)
        ax.set_ylim(xymin, xymax)
        ax.set_xlabel("log(age) [{}]".format(xlab[i]))
        ax.set_ylabel("log(age) [ASteCA]")

    fig.tight_layout()
    plt.savefig(
        root_f + out_folder + "ages.png", dpi=150, bbox_inches='tight')

    #
    #
    xymin, xymax = (1900, 1900, 1900, 1000), (16500, 16500, 20500, 21500)
    fig, axes = plt.subplots(2, 4, figsize=(24, 12))

    for i, yax in enumerate(axes):
        for j, ax in enumerate(yax):
            for cl, vals in dist_dct.items():
                x, y, y_16, y_84 = list(map(
                    float, (vals[j + 3], vals[0], vals[1], vals[2])))
                y, y_16, y_84 = 10**(.2 * (y + 5)), 10**(.2 * (y_16 + 5)),\
                    10**(.2 * (y_84 + 5))
                col = age_dct[cl][0]
                if i == 0:
                    yerr = np.array([[y - y_16, y_84 - y]]).T
                    ax.errorbar(x, y, yerr=yerr, fmt='', c='grey', alpha=.5,
                                zorder=1)
                    ax.scatter(x, y, c=col, vmin=8.8, vmax=10, zorder=4)
                    ax.annotate(cl, (x + 100, y))
                else:
                    yerr = np.array([[y - y_16, y_84 - y]]).T
                    ax.errorbar(x, x - y, yerr=yerr, fmt='', c='grey',
                                alpha=.5, zorder=1)
                    ax.scatter(x, x - y, c=col, vmin=8.8, vmax=10, zorder=4)
                    ax.annotate(cl, (x + 100, x - y))

            if i == 0:
                ax.plot((xymin[j], xymax[j]), (xymin[j], xymax[j]),
                        ls='--', marker='', lw=.8)
                ax.set_xlim(xymin[j], xymax[j])
                ax.set_ylim(xymin[j], xymax[j])
                ax.set_xlabel("dist [{}]".format(xlab[j]))
                ax.set_ylabel("dist [ASteCA]")
            if i == 1:
                ax.plot((xymin[j], xymax[j]), (0, 0),
                        ls='--', marker='', lw=.8)
                ax.set_xlim(xymin[j], xymax[j])
                ax.set_xlabel("dist [{}]".format(xlab[j]))
                ax.set_ylabel(r"$\Delta$ ({} - ASteCA)".format(xlab[j]))

    fig.tight_layout()
    plt.savefig(root_f + out_folder + "dist.png", dpi=150, bbox_inches='tight')


def ASteCAvsASteCA():
    """
    """
    run1, run2, run3 = '1st', '2nd', '3rd'
    in_folder = '../2_pipeline/xx_ASteCA/{}_run/'.format(run1)
    data1 = ascii.read(in_folder + 'asteca_output.dat')
    in_folder = '../2_pipeline/xx_ASteCA/{}_run/'.format(run2)
    data2 = ascii.read(in_folder + 'asteca_output.dat')
    in_folder = '../2_pipeline/xx_ASteCA/{}_run/'.format(run3)
    data3 = ascii.read(in_folder + 'asteca_output.dat')

    d2_names = list(data2['NAME'])
    d3_names = list(data3['NAME'])

    labels, dist1, dist2, dist3 = [], [], [], []
    dist_12, dist_13, dist_23 = [], [], []
    for cl in data1:
        labels.append(cl['NAME'][3:])
        i2 = d2_names.index(cl['NAME'])
        i3 = d3_names.index(cl['NAME'])
        d1, d2, d3 = cl['d_mean'], data2[i2]['d_mean'],\
            data3[i3]['d_mean']

        d1, d2, d3 = 10**(.2 * (d1 + 5)), 10**(.2 * (d2 + 5)),\
            10**(.2 * (d3 + 5))
        dist1.append(d1)
        dist2.append(d2)
        dist3.append(d3)
        print(cl['NAME'][3:], d1, d2, d3)

        # d1, d2, d3 = 10**(.2 * (d1 + 5)), 10**(.2 * (d2 + 5)),\
        #     10**(.2 * (d3 + 5))
        # dist1.append(d1)
        # dist_12.append(d1 - d2)
        # dist_13.append(d1 - d3)
        # dist_23.append(d2 - d3)

    x = np.arange(len(labels))  # the label locations
    width = 0.3  # the width of the bars
    fig, ax = plt.subplots()
    ax.bar(x - width, dist1, width, label='Men')
    ax.bar(x, dist2, width, label='Women')
    ax.bar(x + width, dist3, width, label='Women')
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=70)
    # ax.set_ylim(12, 16)
    ax.set_ylim(2000, 16000)
    plt.show()


    # fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # ax1.scatter(dist1 - np.array(dist_13), dist_12, label='R1-R2')
    # for i, lb in enumerate(labels):
    #     ax1.annotate(lb, (dist1[i] - dist_13[i], dist_12[i]))
    # ax1.axhline(0., ls=':', c='r')
    # ax1.set_xlabel('dist (R3)')
    # ax1.set_ylabel(r"$\Delta$ (R1-R2)")

    # ax2.scatter(dist1 - np.array(dist_12), dist_13, label='R1-R3')
    # for i, lb in enumerate(labels):
    #     ax2.annotate(lb, (dist1[i] - dist_12[i], dist_13[i]))
    # ax2.axhline(0., ls=':', c='r')
    # ax2.set_xlabel('dist (R2)')
    # ax2.set_ylabel(r"$\Delta$ (R1-R3)")

    # ax3.scatter(dist1, dist_23, label='R2-R3')
    # for i, lb in enumerate(labels):
    #     ax3.annotate(lb, (dist1[i], dist_23[i]))
    # ax3.axhline(0., ls=':', c='r')
    # ax3.set_xlabel('dist (R1)')
    # ax3.set_ylabel(r"$\Delta$ (R2-R3)")

    # ax1.legend()
    # ax2.legend()
    # ax3.legend()

    # fig.tight_layout()
    # plt.show()


if __name__ == '__main__':
    main()
