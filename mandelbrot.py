# coding: utf-8
from PIL import Image
import math
import opt


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
        opt.m_loop(self.w, self.h, self.delta, self.set_flag, flag, self.iterations, move_x, move_y,
                   self.pixels, pix, [self.xmin, self.xmax], [self.ymin, self.ymax])

        if not flag:
            return img


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
