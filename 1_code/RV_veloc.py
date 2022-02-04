
import os
from astropy.io import ascii

"""
See if any of the members for the clusters with no radial velocities in the
literature (BH4, F1419, E9218, SAU3, KRON39, KRON31, SAU6, BER102) has a value
assigned by the Gaia eDR3 data.
"""

membs_path = "../2_pipeline/3_members_select/out"
all_path = "../0_data/"

clusters = ("vdbh4", "fsr1419", "eso09218", "saurer3", "kronberger39",
            "kronberger31", "saurer6", "ber102")

for root, dirs, files in os.walk(membs_path):
    for name in files:
        if name.replace('.dat', '') in clusters:
            print('\n ' + name)
            membs_data = ascii.read(os.path.join(root, name))
            all_data = ascii.read(all_path + name)
            #
            id_lst = list(all_data['EDR3Name'])
            for star in membs_data['EDR3Name']:
                i = id_lst.index(star)
                try:
                    msk = all_data[i]['RVDR2'].mask.tolist()
                except AttributeError:
                    print(all_data[i]['RVDR2'], all_data[i]['e_RVDR2'])
                if msk is False:
                    print(all_data[i]['RVDR2'], all_data[i]['e_RVDR2'])
