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


def get_region(start, end, frames=8, zoom_factor=0.1, delta=None):
    k = (end[1] - start[1]) / (end[0] - start[0])
    x_delta = (end[0] - start[0]) / frames

    sx_min, sx_max = start[0] - delta[0], start[0] + delta[0]
    sy_min, sy_max = start[1] - delta[1], start[1] + delta[1]

    delta[0] *= zoom_factor
    delta[1] *= zoom_factor

    dx_min, dx_max = end[0] - delta[0], end[0] + delta[0]
    dy_min, dy_max = end[1] - delta[1], end[1] + delta[1]

    print("目标区域：", dx_min, dx_max, dy_min, dy_max)
    scale_x = (abs(dx_max - dx_min) - abs(sx_max - sx_min)) / frames
    scale_y = (abs(dy_max - dy_min) - abs(sy_max - sy_min)) / frames

    return [k, x_delta], [abs(scale_x/2), abs(scale_y/2)], [sx_min, sx_max, sy_min, sy_max]


# scale factor per each delta
def seg_mov(start, end, frames=8, zoom_factor=0.1, delta=None):
    xc, yc = start[0], start[1]
    kd, scale, sr = get_region(start, end, frames, zoom_factor, delta)

    seqs = np.zeros([frames] + [ImageHeight, ImageWidth] + [3])
    for i in range(frames):
        sr[0] += scale[0]
        sr[1] -= scale[0]
        sr[2] += scale[1]
        sr[3] -= scale[1]

        xc += kd[1]
        yc += kd[0] * kd[1]

        xmin, xmax = sr[0] + xc - start[0], sr[1] + xc - start[0]
        ymin, ymax = sr[2] + yc - start[1], sr[3] + yc - start[1]
        iterations = round(50 * (math.log(ImageWidth / abs(xmin - xmax), 10) ** 1.25))

        # print("目标中心位置：", xc, yc)
        # print("迭代区域：", xmin, xmax, ymin, ymax)
        # print("复平面区域 ({},{}), 迭代次数:{}".format(abs(xmin - xmax), abs(ymin - ymax), iterations))
        # print('Generating {}/{}....'.format(i + 1, frames))

        img = Image.new("RGB", (ImageWidth, ImageHeight), "white")
        pix = img.load()
        pixels = []

        opt.m_loop(ImageWidth, ImageHeight, 1., 'M', True, iterations, 0, 0, pixels, [], [xmin, xmax], [ymin, ymax])
        opt.get_colors(pix, pixels, palette)

        seqs[i, :, :] = np.array(img)

    return seqs, end, delta


##############################################################################


ImageWidth = 1080
ImageHeight = 768

palette = get_palette()

start = time.time()
# seqs1, end1, delta1 = seg_mov([-0.75, 0.0], [-0.5471555555555554, 0.6215555555555556],
#                               frames=150, zoom_factor=.1, delta=[1.6, 1])

tip = "from [1.6, 1]"
print(tip)
seqs1, end1, delta1 = seg_mov([-0.75, 0.0], [-0.5396296296296295, 0.528888888888889],
                              frames=50, zoom_factor=.1, delta=[1.6, 1])
tip += "->" + str(delta1)
print(tip)
seqs2, end2, delta2 = seg_mov(end1, [-0.541111111111111, 0.6143703703703705],
                              frames=50, zoom_factor=.1, delta=delta1)

tip += "->" + str(delta2)
print(tip)
seqs3, end3, delta3 = seg_mov(end2, [-0.5471555555555554, 0.6215555555555556],
                              frames=50, zoom_factor=.1, delta=delta1)

tip += "->" + str(delta3)
print(tip)

current = round(time.time() - start, 2)
print("执行时间 {} 秒".format(current))
print('Make gif.....')
seqs_all = np.vstack((seqs1, seqs2, seqs3))
# seqs_all = seqs1
gif('gif/mandelbrot_gif_{}.gif'.format(current), seqs_all, 8)
print('Please check gif/julia_gif_.gif...')

