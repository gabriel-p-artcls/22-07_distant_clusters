
"""
Helper script, not for article plots.

Compare the ASteCA results from the main run (asteca_output.dat) with those
from N extra runs (asteca_output_extra.dat) performed with the following
characteristics:

00: (main) min_mass=0.01 + mass-binaries correction
01: 00 + b_fr=0.5
02: min_mass=0.01 + no mass-binaries correction
03: min_mass=0.08 + no mass-binaries correction
04: min_mass=0.08 + mass-binaries correction
05: 00 + Uniform prior in [Fe/H] (-0.57<[Fe/H]<0)
06: 00 + Uniform prior in [Fe/H] (-0.57<[Fe/H]<0.28)
07: 00 + b_fr=0.0
08: 00 + Z unif prior + raghavan q dist
09: 01 + 06: min_mass=0.01 + mass-binaries correction + b_fr=0.5 +
    raghavan q dist + Uniform prior in [Fe/H] (-0.57<[Fe/H]<0.28)
10: min_mass=0.08 + mass-binaries correction + raghavan q dist +
    Uniform prior in [Fe/H] (-0.57<[Fe/H]<0.28)


Results:

- 01: [Fe/H] values are very slightly lower than 00, while the remaining
  parameters show almost no change
- 02: [Fe/H] and binary fraction values are slightly lower than 00, but the
  b_f median is still above 0.5. Distance extinction, and age change within the
  uncertainties, while the mass is substantially lower for (which is expected)
- 03: very similar to 02
- 04: [Fe/H] and binary fraction values are slightly lower than 00 and the
  binary fraction is slightly larger. The remaining parameters are almost
  unchanged
- 05: uses a too stringent prior range and is discarded
- 06: gives better (smaller) [Fe/H] values than 00, b_f is slightly larger,
  the remaining parameters almost unchanged
- 07: [Fe/H] are lower (also lower than 01), distances are a bit lower (~1.5
  kpc on) average, masses are lower (also lower than 01), age and extinction
  show almost no change
- 08: [Fe/H] are slightly lower, b_f are larger (b_f~68% on average), distances
  are slightly lower (~500 pc on average) masses are smaller, age and
  extinction show almost no change
- 09: [Fe/H] is lower than 00 but larger than 06, distances are ~1 kpc lower,
  the mass is expectedly lower
-10: [Fe7H] is almost as low as 06, b_f is larger than 00 and 06, distance is
  ~1 kpc lower than 00, mass is lower than 00
"""

from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


root_f = '../2_pipeline/5_ASteCA/'
in_folder = root_f + 'out/'


def main(dpi=300, sol='median'):
    """
    """
    asteca_main = ascii.read(in_folder + 'asteca_output.dat')
    asteca_extra = ascii.read(in_folder + 'asteca_output_extra.dat')
    extra_names = list([_.upper() for _ in asteca_extra['NAME']])

    # all_runs = ('06', '00', '01', '02', '03', '04', '07', '08')
    all_runs = ('06', '00')
    pars = ('z', 'b', 'd', 'a', 'M', 'E')

    for par in pars:
        print(par)
        cp, cp16, cp84 = '{}_{}'.format(par, sol), '{}_16th'.format(par),\
            '{}_84th'.format(par)

        par_lst = {}
        for cl in asteca_main:
            cl_name = cl['NAME'][3:].upper()

            # Data for the main run
            if par == 'z':
                p, p16, p84 = np.array([cl[cp], cl[cp16], cl[cp84]])
            elif par == 'd':
                p, p16, p84 = 10**(.2 * (np.array([
                    cl[cp], cl[cp16], cl[cp84]]) + 5))
            else:
                p, p16, p84 = cl[cp], cl[cp16], cl[cp84]
            par_lst[cl_name] = [(p16, p, p84)]

            for run in all_runs[1:]:
                i = extra_names.index(run + '/' + cl_name)
                cl_extra = asteca_extra[i]

                if par == 'z':
                    if run not in ('05', '09', '10'):
                        p, p16, p84 = ZtoFeH(np.array([
                            cl_extra[cp], cl_extra[cp16], cl_extra[cp84]]))
                    else:
                        p, p16, p84 = cl_extra[cp], cl_extra[cp16],\
                            cl_extra[cp84]
                elif par == 'd':
                    p, p16, p84 = 10**(.2 * (np.array([
                        cl_extra[cp], cl_extra[cp16], cl_extra[cp84]]) + 5))
                else:
                    p, p16, p84 = cl_extra[cp], cl_extra[cp16], cl_extra[cp84]
                par_lst[cl_name].append((p16, p, p84))

                # if par in ('d', 'b') and run == '06':
                #     print(par, cl_name, "{:.4f}".format(cl[cp] - cl_extra[cp]))

        medians = np.array(list(par_lst.values()))
        # Median of medians
        par_medians = np.median(medians[:, :, 1], 0)

        #
        markers = ["${}$".format(int(_)) for _ in all_runs]
        colors = cm.rainbow(np.linspace(0, 1, len(all_runs)))

        fig, ax = plt.subplots(figsize=(6, 3))
        plt.title("{}".format(par))
        x, offset, xl, labels = 1, .5, [], []
        # For each cluster
        for cl_n, cl_p in par_lst.items():
            xo = -4
            # For each run
            for j, runs in enumerate(cl_p):
                p16, p, p84 = runs
                yerr = np.array([[p - p16, p84 - p]]).T
                plt.errorbar(x + xo * offset, p, yerr=yerr, c='grey', alpha=.3,
                             zorder=0)
                plt.scatter(
                    x + xo * offset, p, marker=markers[j], color=colors[j],
                    zorder=5, label='{:.3f}'.format(par_medians[j]))
                xo += 1
                if x == 1:
                    plt.axhline(par_medians[j], ls=':', color=colors[j])
            xl.append(x)
            labels.append(cl_n)
            if x == 1:
                plt.legend()
            x += 10
        plt.xticks(xl, labels, rotation=70)
        plt.show()


def ZtoFeH(Z):
    """
    Transform the z metallicity values to [Fe/H] using the approximation given
    in the CMD service:

    [M/H]=log(Z/X)-log(Z/X)_o,
    with (Z/X)_o=0.0207 and Y=0.2485+1.78Z for PARSEC tracks.
    """
    # return Z
    a, b = 0.2485, 1.78
    X = 1 - a - Z * (b + 1)
    feh = np.log10(Z / X) - np.log10(0.0207)
    return feh


if __name__ == '__main__':
    main()
