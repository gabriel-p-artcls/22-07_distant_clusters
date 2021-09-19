
from os import listdir
from astropy.io import ascii
import numpy as np
from scipy.stats import median_abs_deviation as MAD
import matplotlib.pyplot as plt

"""
A simple way to estimate the number of members. Starting from fixed center
values in xy+PMs+Plx, we count how many stars are simultaneously included
in growing 5D spheres.

Did not obtain good results. Abandoned
"""


in_folder = '../2_pipeline/2_pyUPMASK/GMM_2dim/'
out_fig_folder = '../2_pipeline/xx_ring_members_estim/tmp/'

cl_rads = {
    'arpm2': 0.05, 'ber26': 0.027, 'ber29': 0.033, 'ber56': 0.075,
    'ber76': 0.067, 'eso09308': 0.025, 'fsr0338': 0.033, 'saurer1': 0.033,
    'shorlin1': 0.033, 'tombaugh2': 0.058, 'vdbh4': 0.033, 'vdbh76': 0.033,
    'vdbh144': 0.025}


def main(rad_step=50, NMAD=1):
    """
    rad_step  :
    NMAD      :
    """
    files = listdir(in_folder)
    files.sort()

    for file in files:
        print("\n", file)

        print("Reading data")
        data = ascii.read(in_folder + file)
        print("Total number of stars:", len(data))

        # The centers are estimated using a high probability subset
        RA_m, DE_m, Plx_m, pmRA_m, pmDE_m = centers(data)
        # print(RA_m, DE_m)

        rad_xy = cl_rads[file.replace('.dat', '')]
        msk_xy = np.sqrt(
            (data['_x'] - RA_m)**2 + (data['_y'] - DE_m)**2) < rad_xy
        print("Stars within radius:", msk_xy.sum())

        # max_PM = np.median(np.sqrt(
        #     data['pmRA'][msk_xy]**2 + data['pmDE'][msk_xy]**2))
        # max_Plx = np.ptp(data['Plx'][msk_xy])
        max_PM = 3 * min(MAD(data['pmRA'][msk_xy]), MAD(data['pmDE'][msk_xy]))
        max_Plx = 3 * MAD(data['Plx'][msk_xy])

        N_membs_rad = []
        for rad_PM in np.linspace(.1, max_PM, 20):

            msk_PM = np.sqrt((data['pmRA'][msk_xy] - pmRA_m)**2
                             + (data['pmDE'][msk_xy] - pmDE_m)**2) < rad_PM
            # msk_PM_fl = np.sqrt((data['pmRA'][~msk_xy] - pmRA_m)**2
            #                     + (data['pmDE'][~msk_xy] - pmDE_m)**2) < rad_PM

            for rad_Plx in np.linspace(.01, max_Plx, 20):
                msk_Plx = abs(data['Plx'][msk_xy][msk_PM] - Plx_m) < rad_Plx
                # msk_Plx_fl = abs(
                #     data['Plx'][~msk_xy][msk_PM_fl] - Plx_m) < rad_Plx

                # Apply filters
                # msk = msk_Plx
                # msk_fl = msk_Plx_fl
                dens = msk_Plx.sum() / (rad_PM * rad_Plx)
                N_membs_rad.append([msk_Plx.sum(), dens])
                print("{:.2f} {:.2f}, {:.2f} --> {:.0f}".format(
                    rad_PM, rad_Plx, msk_Plx.sum(), dens))


        N_membs_rad = np.array(N_membs_rad).T
        import pdb; pdb.set_trace()  # breakpoint 8b36262f //
        

        fig = plt.figure(figsize=(10, 5))
        plt.title("Nmemb={}".format(N_membs_rad[1][-1]))
        plt.plot(*N_membs_rad)
        plt.xlabel("Rad xy [arcmin]")
        plt.ylabel("N_membs")
        plt.grid(ls=':', c='grey')
        fig.tight_layout()
        fout = out_fig_folder + file.replace('.dat', '.png')
        plt.savefig(fout, dpi=150, bbox_inches='tight')


def centers(data, pmin=.99, pstep=.01, Nmin_p=0.01, Nstd=5):
    """
    Estimate the center of the cluster in parallax and proper motions, using
    a subset of stars with the largest assigned probabilities.

    pmin: starting probability cut value
    pstep: step used to diminish the probability cut
    Nmin_p: minimum percentage of stars required to estimate the centers
    Nstd: number of STDDEVS used to remove outliers
    """
    def rmOutliers(dd):
        """
        Remove obvious outliers from Plx+PMs, before estimating the centers
        """
        d_plx, d_pmra, d_pmde = MAD(dd['Plx']), MAD(dd['pmRA']),\
            MAD(dd['pmDE'])
        msk = (abs(dd['Plx'] - np.median(dd['Plx'])) < Nstd * d_plx) &\
            (abs(dd['pmRA'] - np.median(dd['pmRA'])) < Nstd * d_pmra) &\
            (abs(dd['pmDE'] - np.median(dd['pmDE'])) < Nstd * d_pmde)
        return dd[msk]

    Nmin = max(10, min(100, int(len(data) * Nmin_p)))

    check_flag = True
    while check_flag:
        msk = data['probs_final'] > pmin
        data_clean = rmOutliers(data[msk])
        if len(data_clean) < Nmin:
            pmin -= pstep
            continue
        cx_c = np.nanmedian(data_clean['_x'])
        cy_c = np.nanmedian(data_clean['_y'])
        pmRA_c = np.nanmedian(data_clean['pmRA'])
        pmDE_c = np.nanmedian(data_clean['pmDE'])
        Plx_c = np.nanmedian(data_clean['Plx'])

        # cx_std = np.std(data_clean['_x'])
        # cy_std = np.std(data_clean['_y'])
        # pmRA_std = np.std(data_clean['pmRA'])
        # pmDE_std = np.std(data_clean['pmDE'])
        # Plx_std = np.std(data_clean['Plx'])

        check_flag = False
        break

    if check_flag:
        raise ValueError("Could not estimate the ra, dec, Plx & PMs center")

    return cx_c, cy_c, Plx_c, pmRA_c, pmDE_c


if __name__ == '__main__':
    main()
