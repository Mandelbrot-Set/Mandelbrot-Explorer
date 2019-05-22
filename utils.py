import math
import random
import numpy as np
from numba import jit, guvectorize, complex128, int32, double
from PIL import Image


def translate(value, left_min, left_max, right_min, right_max):
    """
    是把canvas上的坐标值转化为复平面上对应的一个坐标值。鼠标点击屏幕后转换次序：
    屏幕坐标->canvas坐标->复平面坐标。
    :param value: 传入的需要转换的值
    :param left_min: x方向最小值或y方向最大值
    :param left_max: x方向最大值或y方向最小值
    :param right_min: 当前迭代复平面x方向或y方向最小值
    :param right_max: 当前迭代复平面x方向或y方向最大值
    :return: 返回转换后的值
    """
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)


def get_image(n, palette=None):
    if palette is None:
        r, g, b = np.frompyfunc(get_color(create_palette()), 1, 3)(n)
    else:
        r, g, b = np.frompyfunc(get_color(palette), 1, 3)(n)
    img_array = np.dstack((r, g, b))
    # return Image.fromarray(np.uint8(img_array * 255), mode='RGB')
    return Image.fromarray(np.uint8(img_array * 255), mode='RGB')


def clamp(x):
    return max(0, min(x, 255))


def create_palette():
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


def get_color(palette):
    colours = len(palette)

    def color(i):
        return palette[i % colours]

    return color


def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    re = np.linspace(xmin, xmax, width, dtype=np.float64)
    im = np.linspace(ymin, ymax, height, dtype=np.float64)
    c = re + im[:, None]*1j

    n3 = mandelbrot_numpy(c, maxiter)

    # To handle row exchange issue.
    rows, row = n3.shape[0], math.floor(n3.shape[0]/2)
    for i in range(row):
        n3[[i, rows - 1 - i], :] = n3[[rows - 1 - i, i], :]

    return n3


@jit(int32(complex128, int32))
def mandelbrot(c, maxiter):
    real = 0
    imag = 0
    for n in range(maxiter):
        nreal = real * real - imag * imag + c.real
        imag = 2 * real * imag + c.imag
        real = nreal
        if real * real + imag * imag > 4.0:
            return n
    return 0


@guvectorize([(complex128[:], int32[:], int32[:])], '(n),()->(n)', target='parallel')
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot(c[i], maxiter)

