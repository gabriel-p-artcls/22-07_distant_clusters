
import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
from adjustText import adjust_text


"""
Plot the distances estimated by ASteCA vs other distance estimates.

The median is obtained as 1000/median(plx_i) (for all members), the MAD is
obtained as MAD(1000 / plx). The 'plx_median_MAD.py' script obtains these
values

The 'ASteCA _16 _84' columns are obtained through Bayesian inference of the
parallaxes with a uniform prior, using ASteCA (the first column is the median).

The 'Kalkayotl _16K  _84K' columns are obtained with the Kalkayotl code
using a uniform prior.
"""

plx_corr_data = """
Cluster      plx_median plx_MAD ASteCA _16   _84   Kalkayotl _16K  _84K
arpm2        9734       5256    8038   7718  8401  8251      7380  9350
ber102       9840       5754    8029   7665  8438  8245      7346  9449
ber25        7447       3034    7147   6954  7357  7276      6619  8027
ber26        5412       2404    4940   4688  5217  5001      4562  5522
ber29        11315      5603    7930   7648  8234  8224      7332  9256
ber56        10068      4972    9318   9077  9589  9541      8524  10814
ber73        7577       3224    6881   6594  7196  6999      6326  7843
ber75        6586       2907    6894   6628  7189  6997      6351  7830
ber76        5242       1887    4559   4465  4657  4580      4320  4884
czernik30    5958       1588    5958   5813  6112  6035      5593  6558
eso09205     11355      6467    11514  10987 12108 11836     10191 13924
eso09218     9779       5548    7219   7094  7350  4510      4321  4709
eso09308     10011      5698    9807   9109  10660 10336     8856  12528
fsr1212      6504       2477    5297   5096  5507  5326      4924  5814
fsr1419      8732       4333    8611   8211  9057  8946      7953  10314
kronberger31 8468       5222    6871   6638  7115  6959      6336  7725
kronberger39 7941       4999    6337   5899  6825  6227      5566  7065
saurer1      7169       3193    6566   6057  7175  6692      5856  7821
saurer3      7117       3965    4528   4398  4668  4573      4274  4920
saurer6      9483       5683    9346   8762  9981  7841      7003  8872
tombaugh2    7342       3015    5513   5452  5574  4442      4254  4635
vdbh144      10495      5156    8330   8060  8621  8806      7881  9962
vdbh176      10660      4587    5211   5078  5352  4141      3968  4329
vdbh37       3459       408     3496   3461  3529  3509      3357  3675
vdbh4        7579       2916    7670   7238  8147  7989      7071  9158
"""


short_n = {
    'saurer1': 'SAU1', 'czernik30': 'CZER30', 'arpm2': 'ARPM2',
    'saurer3': 'SAUR3', 'ber102': 'BER102', 'eso09205': 'E9205',
    'saurer6': 'SAU6', 'ber25': 'BER25', 'ber26': 'BER26',
    'eso09218': 'E9218', 'tombaugh2': 'TOMB2', 'eso09308': 'E9308',
    'vdbh144': 'BH144', 'fsr1212': 'F1212', 'ber56': 'BER56',
    'fsr1419': 'F1419', 'ber73': 'BER73', 'kronberger31': 'KRON31',
    'vdbh37': 'BH37', 'ber75': 'BER75', 'kronberger39': 'KRON39',
    'vdbh4': 'BH4', 'ber76': 'BER76', 'ber29': 'BER29', 'vdbh176': 'BH176'}

root_f = '../2_pipeline/5_ASteCA/'
out_folder = 'tmp/'


def main(dpi=300):
    """
    """
    plx_data = ascii.read(plx_corr_data)

    # ASteCA output data
    asteca_data = ascii.read('../2_pipeline/5_ASteCA/out/asteca_output.dat')
    asteca_names = list([_[3:].upper() for _ in asteca_data['NAME']])

    asteca_dists, asteca_ages = [], []
    for cl in plx_data['Cluster']:
        idx = asteca_names.index(cl.upper())
        d_pc = 10**(.2 * (asteca_data[idx]['d_mean'] + 5))
        d_16th = 10**(.2 * (asteca_data[idx]['d_16th'] + 5))
        d_84th = 10**(.2 * (asteca_data[idx]['d_84th'] + 5))
        asteca_dists.append([d_pc, d_16th, d_84th])
        asteca_ages.append(asteca_data[idx]['a_mean'])
    asteca_dists = np.array(asteca_dists)

    # print(np.median(abs(asteca_dists - plx_data['plx_median'])))
    # print(np.median(abs(asteca_dists - plx_data['mode'])))
    # msk = asteca_dists < 10000
    # print(np.median(abs(asteca_dists[msk] - plx_data['plx_median'][msk])))
    # print(np.median(abs(asteca_dists[msk] - plx_data['mode'][msk])))
    # print(np.median(abs(asteca_dists[~msk] - plx_data['plx_median'][~msk])))
    # print(np.median(abs(asteca_dists[~msk] - plx_data['mode'][~msk])))

    for sol in ('ASteCA', 'plx_median', 'Kalkayotl'):
        print(sol)
        fig, ax = plt.subplots(figsize=(6, 6))
        texts = []
        for i, cl in enumerate(plx_data):
            x = cl[sol]
            y = asteca_dists[i][0]

            if sol == 'plx_median':
                xerr = plx_data['plx_MAD'][i]
            elif sol == 'Kalkayotl':
                _16 = cl['Kalkayotl'] - cl['_16K']
                _84 = cl['_84K'] - cl['Kalkayotl']
                xerr = np.array([[_16, _84]]).T
            else:
                _16, _84 = cl['ASteCA'] - cl['_16'], cl['_84'] - cl['ASteCA']
                xerr = np.array([[_16, _84]]).T

            d_16th, d_84th = y - asteca_dists[i][1], asteca_dists[i][2] - y
            yerr = np.array([[d_16th, d_84th]]).T
            ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='', c='grey', alpha=.7,
                        zorder=1)
            ax.scatter(x, y, c=asteca_ages[i], vmin=8.8, vmax=10,
                       alpha=.6, zorder=4)
            texts.append(plt.text(x, y, short_n[cl['Cluster']]))

        adjust_text(texts)
        # minimizeTextOverlap(texts, fig, ax)

        ax.plot((1000, 17000), (1000, 17000), ls='--', marker='', lw=.8)
        ax.set_xlim(2100, 16400)
        ax.set_ylim(2100, 16400)
        ax.set_xlabel("Plx [pc]", fontsize=14)
        ax.set_ylabel("ASteCA [pc]", fontsize=14)

        fig.tight_layout()
        plt.savefig(root_f + out_folder + "plx_dist_{}.png".format(sol),
                    dpi=dpi, bbox_inches='tight')


if __name__ == '__main__':
    plt.style.use('science')
    main()


# def minimizeTextOverlap(
#         texts, fig, ax, horizontal_only=False, vertical_only=False,
#         maxiter=1000, tolerance=0.001, annotate=False):
#     """

#     Source: https://github.com/Phlya/adjustText/issues/113#issue-851173745
#     """

#     # get text sizes
#     plt.draw()
#     r = fig.canvas.get_renderer()
#     expand = (1.0, 1.0)

#     class Box():
#         def __init__(self, position, left, right, bottom, top):
#             self.x = position[0]
#             self.y = position[1]

#             self.x0 = self.x
#             self.y0 = self.y

#             self.x_best = self.x
#             self.y_best = self.y

#             self.dl = self.x - left
#             self.dr = right - self.x
#             self.du = top - self.y
#             self.dd = self.y - bottom
#             self.to_be_moved = np.array((0, 0), dtype=float)

#         def move(self, dx, dy):
#             self.x += dx
#             self.y += dy

#         def reset(self):
#             self.to_be_moved = np.array((0, 0), dtype=float)

#         def do_move(self):
#             self.move(*self.to_be_moved)

#         def set_best(self):
#             self.x_best = self.x
#             self.y_best = self.y

#         # def move_to_best(self):
#         #     self.x = self.x_best
#         #     self.y = self.y_best

#         @property
#         def cx(self):
#             return self.x + 0.5 * self.dr - 0.5 * self.dl

#         @property
#         def cy(self):
#             return self.y + 0.5 * self.du - 0.5 * self.dd

#         @property
#         def width(self):
#             return self.dr + self.dl

#         @property
#         def height(self):
#             return self.du + self.dd

#         @property
#         def r(self):
#             return ((0.5 * self.width)**2 + (0.5 * self.height)**2) ** (0.5)

#         @property
#         def left(self):
#             return self.x - self.dl

#         @property
#         def right(self):
#             return self.x + self.dr

#         @property
#         def top(self):
#             return self.y + self.du

#         @property
#         def bottom(self):
#             return self.y - self.dd

#         def plot_home(self, ax):
#             ax.plot((self.x, self.x0),
#                     (self.y, self.y0))

#         def plot_box(self, ax):

#             if self.width == 0 or self.height == 0:
#                 ax.plot(self.cx, self.cy, 'r.')
#             else:
#                 ax.plot(
#                     [self.left, self.left, self.right, self.right, self.left],
#                     [self.bottom, self.top, self.top, self.bottom,
#                      self.bottom])

#         def add_force_to_home(self, factor=0.1):
#             dx = self.cx - self.x0
#             dy = self.cy - self.y0

#             self.to_be_moved[0] = self.to_be_moved[0] - factor * dx
#             self.to_be_moved[1] = self.to_be_moved[1] - factor * dy

#         def add_force_from(
#             self, other, factor=1.2, vertical_only=False,
#                 horionztal_only=False):

#             # if not overlap then we are done
#             if other.left > self.right:
#                 return 0
#             if other.right < self.left:
#                 return 0
#             if other.top < self.bottom:
#                 return 0
#             if other.bottom > self.top:
#                 return 0

#             ry = 0.5 * (other.height + self.height)
#             oy = self.cy - other.cy

#             rx = 0.5 * (other.width + self.width)
#             ox = self.cx - other.cx

#             dx = 0
#             dy = 0

#             if not vertical_only:
#                 ho = rx - abs(ox)  # horizontal overlap
#                 if ho > 0:
#                     if ox == 0:  # avoid div by 0
#                         ox = 1
#                     dx = factor * 0.5 * ox * ho / abs(ox)
#                     self.to_be_moved[0] += dx

#             if not horizontal_only:
#                 vo = ry - abs(oy)  # horizontal overlap
#                 if vo > 0:
#                     if oy == 0:  # avoid div by 0
#                         oy = 1
#                     dy = factor * 0.5 * oy * vo / abs(oy)
#                     self.to_be_moved[1] += dy

#             return (dx**2 + dy**2)**(0.5)

#     boxes, points = [], []
#     for i in texts:
#         ext = i.get_window_extent(r).expanded(
#             *expand).transformed(ax.transData.inverted())
#         x, y = i.get_position()

#         boxes.append(Box(i.get_position(), left=ext.xmin,
#                          right=ext.xmax, top=ext.ymax, bottom=ext.ymin))
#         points.append(Box(i.get_position(), x, x, y, y))

#     # initial positioning - position each box on the side of its target
#     # point where it has the lowest amount of overlap
#     for b in boxes:
#         xx = (-0.5 * b.width, 0, 0.5 * b.width, 0)
#         yy = (0, 0.5 * b.height, 0, -0.5 * b.height)

#         r = []
#         for dx, dy in zip(xx, yy):
#             ri = 0
#             for bb in boxes:
#                 if b == bb:
#                     continue
#                 b.move(dx, dy)
#                 ri += b.add_force_from(bb)
#                 b.move(-dx, -dy)

#             r.append(ri)
#         b.reset()
#         imin = np.argmin(r)
#         b.move(xx[imin], yy[imin])

#     best = 1e20
#     for i in range(maxiter):

#         # move text towards point
#         # for b in boxes:
#         #     dx = b.cx - b.x0
#         #     dy = b.cy - b.y0
#         #     b.move(-0.05*dx,-0.05*dy)

#         # repel from boxes and points
#         total_move = 0
#         for b in boxes:
#             for bb in boxes:
#                 if b == bb:
#                     continue
#                 total_move += b.add_force_from(
#                     bb, vertical_only=vertical_only,
#                     horionztal_only=horizontal_only)

#             for p in points:
#                 total_move += b.add_force_from(
#                     p, vertical_only=vertical_only,
#                     horionztal_only=horizontal_only)

#         if total_move <= tolerance:
#             break

#         # print(total_move)

#         # and do the actual move
#         for b in boxes:
#             b.do_move()
#             b.reset()

#         if total_move < best:  # more than a factor 2 worse
#             best = total_move
#             for b in boxes:
#                 b.set_best()
#             # print('best so far!')

#     # only in the end move the text elements
#     for t, b in zip(texts, boxes):
#         t.set_position((b.x_best, b.y_best))

#     # annotation arrows
#     if annotate:
#         for b in boxes:
#             b.plot_home(ax)
