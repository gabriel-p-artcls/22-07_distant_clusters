
from os import listdir
from os.path import join
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox

# HARDCODED figure size and grid distribution
figsize_x, figsize_y = 30, 30
# figsize(x1, y1), GridSpec(y2, x2)
grid_x, grid_y = 12, 12


in_folder = '../2_pipeline/xx_members_select/out/'
in_folder_all = '../2_pipeline/1_data_filter/out/'
out_folder = '../2_pipeline/xx_members_select/'

in_files = listdir(in_folder)
for file in in_files:
    print(file)
    fig = plt.figure(figsize=(figsize_x, figsize_y))
    gs = gridspec.GridSpec(grid_y, grid_x)

    # pmRA,pmDE,Gmag,BP-RP,membs_select
    data_all = ascii.read(in_folder_all + file)
    data = ascii.read(in_folder + file)

    name = file.replace('.dat', '').replace('_MANUAL', '')
    if name == 'tombaugh2':
        name = 'TOMB2'
    elif name == 'czernik30':
        name = 'CZER30'
    elif name == 'kronberger31':
        name = 'KRON31'
    elif name == 'kronberger39':
        name = 'KRON39'
    elif "fsr" in name:
        name = name.replace('fsr', 'F').upper()
    elif "eso" in name:
        name = name.replace('eso', 'E').upper()
    elif "vdbh" in name:
        name = name.replace('vd', '').upper()
    elif "saurer" in name:
        name = name.replace('saurer', 'sau').upper()
    else:
        name = name.upper()

    ax1 = plt.subplot(gs[0:2, 0:2])
    plt.scatter(
        data_all['pmRA'], data_all['pmDE'], c='grey', alpha=.5, s=5, zorder=0)
    plt.scatter(
        data['pmRA'], data['pmDE'], c='green', s=20, alpha=.8, zorder=3)
    # plt.gca().invert_xaxis()
    medra, medde = np.median(data_all['pmRA']), np.median(data_all['pmDE'])
    stdra, stdde = np.std(data_all['pmRA']), np.std(data_all['pmDE'])
    plt.xlim(medra + 2 * stdra, medra - 2 * stdra)
    plt.ylim(medde - 2 * stdde, medde + 2 * stdde)
    ob = offsetbox.AnchoredText(name, pad=0.2, loc=2)
    ax1.add_artist(ob)
    plt.xlabel('pmRA')
    plt.ylabel('pmDE')

    if name == 'BER29':
        ax2 = plt.subplot(gs[2:4, 0:2])
    else:
        ax2 = plt.subplot(gs[0:2, 2:4])
    plt.scatter(
        data_all['BP-RP'], data_all['Gmag'], c='grey', alpha=.5, s=5,
        zorder=0)
    plt.scatter(
        data['BP-RP'], data['Gmag'], c='green', s=20, alpha=.5, zorder=3)
    ymin, ymax = ax2.get_ylim()
    # plt.gca().invert_yaxis()
    plt.ylim(21, ymin)
    xmin, xmax = np.percentile(data_all['BP-RP'], (1, 99.9))
    plt.xlim(xmin, xmax)
    plt.xlabel('BP-RP')
    plt.ylabel('G')

    fig.tight_layout()
    fname = join(out_folder, name + '_membs.png')
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.clf()
    plt.close("all")
