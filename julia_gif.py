import math
import os
import random
import time

import numpy as np
from PIL import Image
from moviepy.editor import ImageSequenceClip

import opt


def gif(filename, array, fps=10, scale=1.0):
    # ensure that the file has the .gif extension
    fname, _ = os.path.splitext(filename)
    filename = fname + '.gif'

    # copy into the color dimension if the images are black and white
    if array.ndim == 3:
        array = array[..., np.newaxis] * np.ones(3)

    # make the moviepy clip
    clip = ImageSequenceClip(list(array), fps=fps).resize(scale)
    clip.write_gif(filename, fps=fps)

    return clip


ImageWidth = 1920
ImageHeight = 1080
max_iterations = 400

delta = 0.1
x_base = -1.7
y_base = -1.0
xmax, ymax = 25, 21


def clamp(x):
    return max(0, min(x, 255))


palette = [(0, 0, 0)]
red_b = 2 * math.pi / (random.randint(0, 128) + 128)
red_c = 256 * random.random()
green_b = 2 * math.pi / (random.randint(0, 128) + 128)
green_c = 256 * random.random()
blue_b = 2 * math.pi / (random.randint(0, 128) + 128)
blue_c = 256 * random.random()
for i in range(256):
    r = clamp(int(256 * (0.5 * math.sin(red_b * i + red_c) + 0.5)))
    g = clamp(int(256 * (0.5 * math.sin(green_b * i + green_c) + 0.5)))
    b = clamp(int(256 * (0.5 * math.sin(blue_b * i + blue_c) + 0.5)))
    palette.append((r, g, b))

seqs = np.zeros([xmax*ymax] + [ImageHeight, ImageWidth] + [3])
print(seqs.shape)
start = time.time()
for x in range(xmax):
    re = x_base + x * delta
    cont = x*ymax
    for y in range(ymax):
        rm = y_base + y * delta
        img = Image.new("RGB", (ImageWidth, ImageHeight), "white")
        pix = img.load()

        print('x: {} y:{}'.format(x, y))
        pixels = []
        opt.m_loop(ImageWidth, ImageHeight, 1., 'J', True, max_iterations, re, rm, pixels, [], [0, 0], [0, 0])

        opt.get_colors(pix, pixels, palette)

        # img.save("pictures/{}_{}_{}.png".format(time.strftime("%Y-%m-%d-%H:%M:%S"), round(re, 2),
        #                                         round(rm, 2)), "PNG", optimize=True)
        # img.show()
        seqs[cont, :, :] = np.array(img)
        cont += 1
#
current = round(time.time() - start, 2)
print("执行时间 {} 秒".format(current))
print('Make gif.....')
gif('julia_gif_{}.gif'.format(current), seqs, 4)
print('Please check julia_gif.gif...')
