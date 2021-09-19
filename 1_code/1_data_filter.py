
from os import listdir
from astropy.io import ascii
from astropy.table import Table

"""
Remove not used columns from a data file. Makes the file smaller and more
manageable.
"""


cols = (
    'EDR3Name', '_x', '_y', 'RA_ICRS', 'DE_ICRS', 'Plx', 'e_Plx', 'pmRA',
    'e_pmRA', 'pmDE', 'e_pmDE', 'Gmag', 'e_Gmag', 'BP-RP', 'e_BP-RP')

in_folder = '../0_data/'
out_folder = '../2_pipeline/1_data_filter/out/'
files = listdir(in_folder)

for file in files:
    if file == 'dont_read':
        continue
    print(file)
    data = Table.read(in_folder + file, format='ascii')
    print("Total number of stars in file", len(data))

    data.rename_column('e_BPmag-RPmag', 'e_BP-RP')
    # Filter out columns
    data = data[cols]

    ascii.write(data, out_folder + file, format='csv', overwrite=True)
