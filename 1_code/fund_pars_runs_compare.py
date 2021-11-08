
"""
Compare the ASteCA results from the original run (asteca_output.dat) with those
from 4 extra runs (asteca_output_2345.dat) performed with more time given
to the 'ptemecee' algorithm.
"""

from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt


root_f = '../2_pipeline/5_ASteCA/'
in_folder = root_f + 'out/'
out_folder = 'tmp/'


def main(dpi=300):
    """
    """
    asteca_data = ascii.read(in_folder + 'asteca_output.dat')
    asteca_data_2345 = ascii.read(in_folder + 'asteca_output_2345.dat')

    pars = ('z', 'a', 'E', 'd', 'M', 'b')

    for par in pars:
        print(par)
        cp, cp16, cp84 = '{}_median'.format(par), '{}_16th'.format(par),\
            '{}_84th'.format(par)

        par_lst = {}
        for cl in asteca_data:
            cl_u_name = cl['NAME'][3:].upper()

            if par == 'z':
                p, p16, p84 = ZtoFeH(np.array([cl[cp], cl[cp16], cl[cp84]]))
            elif par == 'd':
                p, p16, p84 = 10**(.2 * (np.array([
                    cl[cp], cl[cp16], cl[cp84]]) + 5))
            else:
                p, p16, p84 = cl[cp], cl[cp16], cl[cp84]
            par_lst[cl_u_name] = [(p16, p, p84)]

            for cl_2345 in asteca_data_2345:
                if cl_2345['NAME'][3:] == cl['NAME'][3:]:
                    if par == 'z':
                        p, p16, p84 = ZtoFeH(np.array([
                            cl_2345[cp], cl_2345[cp16], cl_2345[cp84]]))
                    elif par == 'd':
                        p, p16, p84 = 10**(.2 * (np.array([
                            cl_2345[cp], cl_2345[cp16], cl_2345[cp84]]) + 5))
                    else:
                        p, p16, p84 = cl_2345[cp], cl_2345[cp16], cl_2345[cp84]
                    par_lst[cl_u_name].append((p16, p, p84))

        #
        fig, ax = plt.subplots(figsize=(6, 3))
        plt.title("{}".format(par))
        x, offset, xl, labels = 1, .2, [], []
        for cl_n, cl_p in par_lst.items():
            xo = 0
            for runs in cl_p:
                p16, p, p84 = runs
                yerr = np.array([[p - p16, p84 - p]]).T
                plt.errorbar(x + xo * offset, p, yerr=yerr, c='grey', zorder=0)
                plt.scatter(x + xo * offset, p, zorder=5)
                xo += 1
            xl.append(x)
            labels.append(cl_n)
            x += 5
        plt.xticks(xl, labels, rotation=70)
        plt.show()


def ZtoFeH(Z):
    """
    Transform the z metallicity values to [Fe/H] using the approximation given
    in the CMD service:

    [M/H]=log(Z/X)-log(Z/X)_o,
    with (Z/X)_o=0.0207 and Y=0.2485+1.78Z for PARSEC tracks.
    """
    a, b = 0.2485, 1.78
    X = 1 - a - Z * (b + 1)
    feh = np.log10(Z / X) - np.log10(0.0207)
    return feh


if __name__ == '__main__':
    main()
