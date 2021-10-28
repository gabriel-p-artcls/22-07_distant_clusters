
import os
import numpy as np
from scipy.stats import median_abs_deviation as MAD
from astropy.io import ascii


"""
Estimate the parallax median and MAD (in pc) for the Gaia EDR3 corrected
parallax values of the members list
"""

in_dir = '../2_pipeline/6_Plx_corr/'
for file in os.listdir(in_dir):
    if file.endswith('.md'):
        continue
    data = ascii.read(in_dir + file)

    try:
        data = data[~data['BP-RP'].mask]
    except:
        pass
    try:
        data = data[~data['e_BP-RP'].mask]
    except:
        pass
    try:
        data = data[~data['Gmag'].mask]
    except:
        pass
    try:
        data = data[~data['e_Gmag'].mask]
    except:
        pass
    try:
        data = data[~data['Plx_corr'].mask]
    except:
        pass

    plx, outlr_std = data['Plx_corr'], 3

    max_plx = np.nanmedian(plx) + outlr_std * np.nanstd(plx)
    min_plx = np.nanmedian(plx) - outlr_std * np.nanstd(plx)
    plx_2s_msk = (plx < max_plx) & (plx > min_plx)
    plx_clp = plx[plx_2s_msk]

    median = 1000. / np.median(plx_clp)
    std = MAD(1000 / plx_clp)
    print(file, "{:.0f}  {:.0f}".format(median, std))
