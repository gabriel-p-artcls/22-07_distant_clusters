
from astropy.io import ascii
import numpy as np
from numpy.random import MT19937, RandomState, SeedSequence
import matplotlib.pyplot as plt

# Set random seed
seed = np.random.randint(100000000)
print("Random seed: {}".format(seed))
RandomState(MT19937(SeedSequence(seed)))


def main():
    """
    Check different ASteCA runs
    """
    ASteCAvsASteCA()


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
