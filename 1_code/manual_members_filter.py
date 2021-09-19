
from os import listdir
import numpy as np
from astropy.table import Table
from astropy.io import ascii
import matplotlib.pyplot as plt

# THESE PARAMETERS ARE VERY IMPORTANT AND RATHER ARBITRARY
#
# Filter pyUPMASK members
min_prob = .99

# # Set the PMs and/or Plx center, or estimate from the members
# pmCent = None  # (-4.8035, 11.1835)
# plxCent = None  # 2.4297

# # Filter coordinates by maximum radius (in deg)
# xyRad = 1.5

# # Filter by PM & Plx standard deviations, or by fixed values
# pmStd = (.75, .75)  # None
# plxStd = .1  # None

in_folder = '../2_pipeline/2_pyUPMASK/GMM_2dim/'
out_folder = '../2_pipeline/xx_manual_members/out/'
out_fig_folder = '../2_pipeline/xx_manual_members/tmp/'


def main():
    """
    """
    print("Reading data")

    files = listdir(in_folder)

    for file in files:
        print("\n", file)

        data = Table.read(in_folder + file, format='ascii')
        print("Total number of stars: {}".format(len(data)))

        msk = (data['Plx'].mask) | (data['BP-RP'].mask) |\
            (data['pmRA'].mask) | (data['pmDE'].mask)
        data = data[~msk]
        print("Stars without nans: {}".format(len(data)))

        print("Apply probability filter: P>{}".format(min_prob))
        msk = data["probs_final"] >= min_prob
        memb_d, field_d = data[msk], data[~msk]
        print("N_members={}, N_field={}".format(len(memb_d), len(field_d)))

        # Store cleaned members
        fout = out_folder + file
        ascii.write(memb_d, fout, format='csv', overwrite=True, comment='#')
        print("Clean members saved to file")

        # Plot
        gs_unit = 5
        gs_x, gs_y = 4, 2
        fig, axs = plt.subplots(gs_y, gs_x, figsize=(
            gs_unit * gs_x, gs_unit * gs_y))
        xyrange = fullFrame(axs, data)
        pyUPMASKMembs(axs, memb_d, min_prob, xyrange)
        fig.tight_layout()
        fout = out_fig_folder + file.replace('.dat', '.png')
        plt.savefig(fout, dpi=150, bbox_inches='tight')

        print("Finished")


def fullFrame(axs, data):
    """
    Full (zoomed) frame
    """
    ax = axs[0, 0]
    ax.set_title("N={} | Full frame".format(len(data)))
    xmin, xmax, ymin, ymax = data['_x'].max(), data['_y'].min(),\
        data['_x'].min(), data['_y'].max()
    ax.scatter(data['_x'], data['_y'], alpha=.5, marker='.', s=5, color='grey')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    #

    ax = axs[0, 1]
    pmra_max, pmra_min = np.percentile(data['pmRA'], (2.5, 97.5))
    pmde_min, pmde_max = np.percentile(data['pmDE'], (2.5, 97.5))
    ax.scatter(
        data['pmRA'], data['pmDE'], c='grey', alpha=.5, marker='.',
        s=5)
    ax.set_xlim(pmra_min, pmra_max)
    ax.set_ylim(pmde_min, pmde_max)
    #
    # axs[0, 2].set_title("(zoomed)")
    plx_min, plx_max = np.percentile(data['Plx'], (1, 99))
    msk = (data['Plx'] > plx_min) & (data['Plx'] < plx_max)
    axs[0, 2].hist(data['Plx'][msk], 50, color='grey')
    # axs[0, 2].set_xlim(plx_min, plx_max)
    #
    axs[0, 3].scatter(
        data['BP-RP'], data['Gmag'], c='grey', alpha=.5, marker='.',
        s=5)
    axs[0, 3].grid(ls=':', lw=.7, zorder=-1)
    # axs[0, 3].set_xlim(-.2, 3.)
    # axs[0, 3].set_ylim(18.5, 4)
    axs[0, 3].invert_yaxis()

    return (xmin, xmax, ymin, ymax)


def pyUPMASKMembs(axs, memb_d, min_prob, xyrange):
    """
    """
    ax = axs[1, 0]
    ax.set_title("N={} | P>{:.2f}".format(len(memb_d), min_prob))
    ax.scatter(memb_d['_x'], memb_d['_y'], alpha=.25)
    ax.set_xlim(xyrange[0], xyrange[1])
    ax.set_ylim(xyrange[2], xyrange[3])
    #
    axs[1, 1].scatter(memb_d['pmRA'], memb_d['pmDE'], alpha=.25)
    #
    axs[1, 2].hist(memb_d['Plx'], 50)
    #
    axs[1, 3].scatter(memb_d['BP-RP'], memb_d['Gmag'], alpha=.5,
                      edgecolor='C0', facecolor='none')
    axs[1, 3].grid(ls=':', lw=.7, zorder=-1)
    # axs[1, 3].set_xlim(-.2, 3.)
    # axs[1, 3].set_ylim(18, 4)
    axs[1, 3].invert_yaxis()


if __name__ == '__main__':
    main()
