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


ImageWidth = 860
ImageHeight = 480
max_iterations = 400


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

n = 500
cl = np.linspace(-.7, .7, n, dtype=np.float64)
seqs = np.zeros([n] + [ImageHeight, ImageWidth] + [3])
start = time.time()

zoomFactor = 0.9
xDelta = 1.6
yDelta = 1.
delta = 1.

for i in range(n):
    print('Generating {}/{}....'.format(i + 1, n))
    img = Image.new("RGB", (ImageWidth, ImageHeight), "white")
    pix = img.load()

    pixels = []

    xc, yc = -0.6818518518518517, 0.3185185185185184
    xDelta *= zoomFactor
    yDelta *= zoomFactor
    delta *= zoomFactor
    
    xmin, xmax = xc - xDelta, xc + xDelta
    ymin, ymax = yc - yDelta, yc + yDelta

    print("复平面Center：({},{})".format(xc, yc))
    print("系数:delta {} xDelta {} yDelta {} zoomFactor {})".format(delta, xDelta, yDelta, zoomFactor))
    print("(xmin,xmax,ymin,ymax) ({},{},{},{})".format(xmin, xmax, ymin, ymax))

    max_iterations = round(50 * (math.log(ImageWidth / abs(xmin - xmax), 10) ** 1.25))
    print("复平面区域 ({},{}), 迭代次数:{}".format(abs(xmin - xmax), abs(ymin - ymax), max_iterations))
    if abs(ymin - ymax) < 2.098321516541546e-14:
        print('exit.. limited arrived!')
        break

    opt.m_loop(ImageWidth, ImageHeight, 1., 'M', True, max_iterations, 0, 0, pixels, [], [xmin, xmax], [ymin, ymax])
    opt.get_colors(pix, pixels, palette)

    seqs[i, :, :] = np.array(img)

current = round(time.time() - start, 2)
print("执行时间 {} 秒".format(current))
print('Make gif.....')
gif('gif/mandelbrot_gif_{}.gif'.format(current), seqs, 8)
print('Please check gif/julia_gif_.gif...')

