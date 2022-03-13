
"""
Helper script, compare GMM+DBSCAN+HDBSCAN for the SAURER 1 cluster.
DBSCAN used eps=0.05 (default parameter produced horrible results), the other
two methods used all the default parameters.
"""

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np


in_folder = '../2_pipeline/2_pyUPMASK/'


def main(vmin=.5):
    """
    """
    GMM_run = ascii.read(in_folder + 'saurer1_GMM.dat')
    msk = GMM_run['probs_final'] > vmin
    GMM_run = GMM_run[msk]

    DBSCAN_run = ascii.read(in_folder + 'saurer1_DBSCAN.dat')
    msk = DBSCAN_run['probs_final'] > vmin
    DBSCAN_run = DBSCAN_run[msk]

    HDBSCAN_run = ascii.read(in_folder + 'saurer1_HDBSCAN.dat')
    msk = HDBSCAN_run['probs_final'] > vmin
    HDBSCAN_run = HDBSCAN_run[msk]

    plt.subplot(231)
    plt.title("GMM (N={})".format(len(GMM_run)))
    msk1 = np.argsort(GMM_run['probs_final'])  # [::-1]
    plt.scatter(
        GMM_run['BP-RP'][msk1], GMM_run['Gmag'][msk1],
        c=GMM_run['probs_final'][msk1], alpha=.75, vmin=vmin, vmax=1,
        cmap="plasma_r")
    # plt.gca().invert_yaxis()
    plt.xlim(0, 3)
    plt.ylim(21, 12)
    plt.xlabel('BP-RP')
    plt.ylabel('G')
    plt.colorbar()

    plt.subplot(232)
    plt.title("DBSCAN (N={})".format(len(DBSCAN_run)))
    msk2 = np.argsort(DBSCAN_run['probs_final'])  # [::-1]
    plt.scatter(
        DBSCAN_run['BP-RP'][msk2], DBSCAN_run['Gmag'][msk2],
        c=DBSCAN_run['probs_final'][msk2], alpha=.75, vmin=vmin, vmax=1,
        cmap="plasma_r")
    plt.xlim(0, 3)
    plt.ylim(21, 12)
    plt.xlabel('BP-RP')
    plt.ylabel('G')
    plt.colorbar()

    plt.subplot(233)
    plt.title("HDBSCAN (N={})".format(len(HDBSCAN_run)))
    msk3 = np.argsort(HDBSCAN_run['probs_final'])  # [::-1]
    plt.scatter(
        HDBSCAN_run['BP-RP'][msk3], HDBSCAN_run['Gmag'][msk3],
        c=HDBSCAN_run['probs_final'][msk3], alpha=.75, vmin=vmin, vmax=1,
        cmap="plasma_r")
    plt.xlim(0, 3)
    plt.ylim(21, 12)
    plt.xlabel('BP-RP')
    plt.ylabel('G')
    plt.colorbar()

    plt.subplot(234)
    plt.scatter(
        GMM_run['pmRA'][msk1], GMM_run['pmDE'][msk1],
        c=GMM_run['probs_final'][msk1], alpha=.75, vmin=vmin, vmax=1,
        cmap="plasma_r")
    plt.colorbar()
    plt.xlabel('pmRA')
    plt.ylabel('pmDE')

    plt.subplot(235)
    plt.scatter(
        DBSCAN_run['pmRA'][msk2], DBSCAN_run['pmDE'][msk2],
        c=DBSCAN_run['probs_final'][msk2], alpha=.75, vmin=vmin, vmax=1,
        cmap="plasma_r")
    plt.colorbar()
    plt.xlabel('pmRA')
    plt.ylabel('pmDE')

    plt.subplot(236)
    plt.scatter(
        HDBSCAN_run['pmRA'][msk3], HDBSCAN_run['pmDE'][msk3],
        c=HDBSCAN_run['probs_final'][msk3], alpha=.75, vmin=vmin, vmax=1,
        cmap="plasma_r")
    plt.colorbar()
    plt.xlabel('pmRA')
    plt.ylabel('pmDE')

    plt.show()


if __name__ == '__main__':
    plt.style.use('science')
    main()
