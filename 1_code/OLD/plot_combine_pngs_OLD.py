
from os import listdir
from os.path import isfile
from PIL import Image


"""
Combine output PNG files into a few larger files
"""


def combImg(infiles, num):
    print(num)
    N = int(len(infiles) * .5)
    images = [Image.open(_) for _ in infiles]
    widths, heights = list(zip(*(i.size for i in images)))
    width, height = max(widths), max(heights)
    total_width = 2 * width
    max_height = N * height
    #
    new_im = Image.new('RGB', (total_width, max_height))
    for row in range(N):
        new_im.paste(images[2 * row], (0, row * height))
        new_im.paste(images[2 * row + 1], (width, row * height))
    new_im.save(inout_folder + 'struct_{}.png'.format(num))


inout_folder = '../2_pipeline/structure/'
in_files = listdir(inout_folder)
in_files.sort()
in_files.remove('ber29_A23.png')
in_files = [inout_folder + _ for _ in in_files if isfile(inout_folder + _)]

combImg(in_files[:10], 1)
combImg(in_files[10:20], 2)
combImg(in_files[20:], 3)
