# coding: utf-8
from PIL import Image
import math
import random
import numpy as np
from numba import jit, guvectorize, complex64, int32


class Mandelbrot:
    def __init__(self, canvas_w, canvas_h, x=-0.75, y=0, m=1, iterations=None, w=None, h=None, zoom_factor=0.2,
                 color_palette=False, spec_set='J'):
        """
        初始化实例
        :param canvas_w:
        :param canvas_h:
        :param x: 帧的中心坐标点 x 坐标
        :param y: 帧的中心坐标点 y 坐标
        :param m: 放大比例
        :param iterations: 迭代次数，次数越高越精确，但是速度慢
        :param w: 图像的宽
        :param h: 图像的高
        :param zoom_factor: 缩放系数，越小的话越精细
        :param color_palette: 是否使用颜色模版
        :param spec_set: 指定画Julia还是mandelbrot, M or J
        """
        self.w, self.h = (round(canvas_w * 0.9), round(canvas_h * 0.9)) if None in {w, h} else w, h
        self.iterations = 400 if iterations is None else iterations
        self.xCenter, self.yCenter = x, y
        if canvas_w > canvas_h:
            self.xDelta = m / (canvas_h / canvas_w)
            self.yDelta = m
        else:
            self.yDelta = m / (canvas_w / canvas_h)
            self.xDelta = m
        self.delta = m
        self.color_palette = color_palette
        self.xmin = x - self.xDelta
        self.xmax = x + self.xDelta
        self.ymin = y - self.yDelta
        self.ymax = y + self.yDelta
        self.zoomFactor = zoom_factor
        self.yScaleFactor = self.h / canvas_h
        self.xScaleFactor = self.w / canvas_w
        print(x, y, self.xDelta, self.yDelta, self.xCenter, self.yCenter)
        print(
               "初始复平面区域 ({},{},{},{})".format(self.xmin, self.ymin, self.xmax, self.ymax))
        print("初始复平面区域 ({},{}), 迭代次数:{}".format(abs(self.xmin - self.xmax), abs(self.ymin - self.ymax),
                                                self.iterations))
        print("图片尺寸:({},{}),画布尺寸:({},{})".format(self.w, self.h, canvas_w, canvas_h))
        self.c, self.z = 0, 0
        self.pixels = []
        self.set_flag = spec_set

    def shift_view(self, event):
        self.center(event)
        self.fuzhi()

    def zoom_out(self, event):
        self.center(event)
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.fuzhi()

    def zoom_in(self, event):
        """
        坐标变换：事件->屏幕坐标->canvas坐标->复平面坐标。
        :param event: 鼠标事件
        :return: 计算出本次的 xmin，xmax，ymin，ymax
        """
        self.center(event)
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.fuzhi()

    def center(self, event):
        self.xCenter = translate(event.x * self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y * self.yScaleFactor, self.h, 0, self.ymin, self.ymax)

        return self.xCenter, self.yCenter

    def fuzhi(self):
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta
        self.w / abs(self.xmin - self.xmax)
        # 去一个合适的迭代次数
        # https://math.stackexchange.com/questions/16970/a-way-to-determine-the-ideal-number-of-maximum-iterations-for-an-arbitrary-zoom
        self.iterations = round(50 * (math.log(self.w / abs(self.xmin - self.xmax), 10) ** 1.25))
        print("本次中心坐标 ({}, {}, {})".format(self.xCenter, self.yCenter, self.delta))
        print("复平面区域 ({},{}), 迭代次数:{}".format(abs(self.xmin-self.xmax), abs(self.ymin-self.ymax), self.iterations))

    def get_color_pixels(self, flag):
        """
        每次渲染调用的函数，
        :param flag: 是否使用颜色模版的标记，True使用，False不使用
        :return: 如果不使用模版，返回图片
        """

        self.pixels = []
        img = Image.new('RGB', (self.w, self.h), "black")
        pix = img.load()

        move_x, move_y = -0.7, 0.27015
        print(0.9*self.delta)

        # 注意：delta在mandelbrot绘制中没有用到，仅用在了Julia集合绘制
        # opt.m_loop(self.w, self.h, self.delta, self.set_flag, flag, self.iterations, move_x, move_y,
        #            self.pixels, pix, [self.xmin, self.xmax], [self.ymin, self.ymax])

        n = mandelbrot_set(self.xmin, self.xmax, self.ymin, self.ymax, self.w, self.h, self.iterations)
        r, g, b = np.frompyfunc(get_color(), 1, 3)(n)
        img_array = np.dstack((r, g, b))
        img = Image.fromarray(np.uint8(img_array * 255), mode='RGB')

        return img


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


def get_color():
    palette = create_palette()

    def color(i):
        return palette[i % 256]

    return color


def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    # should not be repeated!
    # re = np.linspace(xmin, xmax, width, dtype=np.float32)
    # r1 = [translate(x, 0, width, xmin, xmax) for x in re]
    # im = np.linspace(ymin, ymax, height, dtype=np.float32)
    # r2 = [translate(y, 0, height, ymax, ymin) for y in im]

    re = np.linspace(xmin, xmax, width, dtype=np.float32)
    im = np.linspace(ymin, ymax, height, dtype=np.float32)
    c = re + im[:, None]*1j
    n3 = mandelbrot_numpy(c, maxiter)

    return n3


@jit(int32(complex64, int32))
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


@guvectorize([(complex64[:], int32[:], int32[:])], '(n),()->(n)', target='parallel')
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit[0]
    for i in range(c.shape[0]):
        output[i] = mandelbrot(c[i], maxiter)


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