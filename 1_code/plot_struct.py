
from . import prep_plots
import pickle


"""
First function to produce the 'structure' plots for the article on the distant
clusters.

This function must be inside the 'ASteCA/packages/out/' folder,
and called from 'func_caller()' with:

    from .out import plot_struct
    plot_struct.main(npd, cld_i, pd, clp)

after the call to the 'king_profile()' function. When all the clusters are
processed, a file called "struct.pickle" will be generated with all the data.

The input files must be those with all the stars in the frame, not the ones
with just the members.

This file then needs to be processed with the 'plot_struct_pickle.py' code
to generate the final images.

"""


def main(npd, cld_i, pd, clp):
    """
    """
    x_min, x_max, y_min, y_max = prep_plots.frame_max_min(
        cld_i['x'], cld_i['y'])
    st_sizes_arr = prep_plots.star_size(cld_i['mags'][0])
    rdp_radii, rdp_points, rdp_stddev, rad_max = prep_plots.RDPCurve(
        pd['kp_ndim'], clp['xy_filtered'], clp['xy_cent_dist'],
        clp['kde_cent'], clp['clust_rad'], clp['KP_Bys_ecc'][3],
        clp['KP_Bys_theta'][3])

    if npd['clust_name'] == 'tombaugh2':
        name = 'TOMB2'
    elif npd['clust_name'] == 'czernik30':
        name = 'CZER30'
    elif npd['clust_name'] == 'kronberger31':
        name = 'KRON31'
    elif npd['clust_name'] == 'kronberger39':
        name = 'KRON39'
    elif "fsr" in npd['clust_name']:
        name = npd['clust_name'].replace('fsr', 'F').upper()
    elif "eso" in npd['clust_name']:
        name = npd['clust_name'].replace('eso0', 'E').upper()
    elif "vdbh" in npd['clust_name']:
        name = npd['clust_name'].replace('vd', '').upper()
    elif "saurer" in npd['clust_name']:
        name = npd['clust_name'].replace('saurer', 'sau').upper()
    else:
        name = npd['clust_name'].upper()

    arglist = [
        # pl_full_frame: x,y finding chart of full frame.
        [x_min, x_max, y_min, y_max, clp['kde_cent'],
         cld_i['x'], cld_i['y'], st_sizes_arr, clp['clust_rad']],
        # pl_densmap: 2D Gaussian convolved histogram.
        [clp['kde_cent'], clp['frame_kde_cent'], clp['clust_rad']],
        # pl_rad_dens: Radial density plot.
        [rdp_radii, rdp_points, rdp_stddev,
         rad_max, clp['field_dens'], clp['field_dens_std'], clp['clust_rad'],
         pd['kp_ndim'], clp['KP_Bys_rc'], clp['KP_Bys_rt'], clp['KP_plot'],
         name]
    ]

    with open("struct.pickle", 'ab') as fp:
        pickle.dump({name: arglist}, fp)
