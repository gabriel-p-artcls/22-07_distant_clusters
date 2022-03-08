
"""
Plot the binary fraction values
"""

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np


in_folder = '../2_pipeline/5_ASteCA/out/'


def main():
    """
    """
    asteca_data = ascii.read(in_folder + 'asteca_output.dat')
    names = list([_.split('/')[1].upper() for _ in asteca_data['NAME']])

    b_50, b_16, b_84 = asteca_data['b_median'], asteca_data['b_16th'],\
        asteca_data['b_84th']
    print(np.median(b_50))
    plt.errorbar(range(25), b_50, yerr=(b_16, b_84), c='r', ecolor='grey',
                 fmt='o')
    plt.axhline(.3, lw=2, ls=':')
    plt.axhline(.5, lw=2, ls=':')
    plt.xticks(range(25), names, rotation=45)
    plt.ylabel("b_f")
    plt.ylim(0, 1)
    plt.show()


if __name__ == '__main__':
    plt.style.use('science')
    main()
