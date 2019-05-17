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


def clamp(x):
    return max(0, min(x, 255))


def get_palette():
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

    return palette


ImageWidth = 1050
ImageHeight = 1050
max_iterations = 300
xmin, xmax, ymin = -2.0, .5, -1.25
ymax = ymin + (xmax-xmin) * ImageHeight / ImageWidth
delta = 0.02
delta_k = 0.02
print(np.tan(np.pi/4)*.01)

xc = xmin + abs((xmin-xmax)/2)
n = math.floor(abs(xmin - xc) / delta)
print(n)
seqs = np.zeros([n+1] + [ImageHeight, ImageWidth] + [3])
palette = get_palette()
start = time.time()
for i in range(n):
    print('Generating {}/{}....'.format(i + 1, n))
    print(xmin, xmax, ymin, ymax)
    print("复平面区域 ({},{}), 迭代次数:{}".format(abs(xmin - xmax), abs(ymin - ymax), max_iterations))
    img = Image.new("RGB", (ImageWidth, ImageHeight), "white")
    pix = img.load()
    pixels = []
    opt.m_loop(ImageWidth, ImageHeight, 1., 'M', True, max_iterations, 0, 0, pixels, [], [xmin, xmax], [ymin, ymax])
    opt.get_colors(pix, pixels, palette)

    xmin += delta
    xmax -= delta
    print(np.sin(np.pi / 4 * i))
    ymin += delta/2 + np.sin(np.pi/4*i)
    ymax = ymin + (xmax - xmin) * ImageHeight / ImageWidth

    # ymin += np.tan(np.pi/4) * delta_k
    # ymax += np.tan(np.pi/4) * delta_k
    # print(xmin, xmax, ymin, ymax)
    # print("复平面区域 ({},{}), 迭代次数:{}".format(abs(xmin - xmax), abs(ymin - ymax), max_iterations))

    # img.show()
    seqs[i, :, :] = np.array(img)

current = round(time.time() - start, 2)
print("执行时间 {} 秒".format(current))
print('Make gif.....')
gif('gif/mandelbrot_gif_{}.gif'.format(current), seqs, 8)
print('Please check gif/julia_gif_.gif...')
