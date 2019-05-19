import math
import random
import numpy as np
from numba import jit, guvectorize, complex128, int32, double
from PIL import Image


def get_image(n, palette):
    r, g, b = np.frompyfunc(get_color(palette), 1, 3)(n)
    img_array = np.dstack((r, g, b))
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
    # palette = create_palette()

    def color(i):
        return palette[i % 256]

    return color


def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    re = np.linspace(xmin, xmax, width, dtype=np.float64)
    im = np.linspace(ymin, ymax, height, dtype=np.float64)
    c = re + im[:, None]*1j

    n3 = mandelbrot_numpy(c, maxiter)

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
