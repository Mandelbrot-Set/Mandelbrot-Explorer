# coding: utf-8
from PIL import Image

import opt


class Mandelbrot:
    def __init__(self, canvas_w, canvas_h, x=-0.75, y=0, m=1, iterations=None,
                 w=None, h=None, zoom_factor=0.1, color_palette=False, spec_set='J'):
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
        :param zoom_factor: 缩放系数
        :param color_palette: 是否使用颜色模版
        :param spec_set: 指定画Julia还是mandelbrot, M or J
        """
        self.w, self.h = (round(canvas_w*0.9), round(canvas_h*0.9)) if None in {w, h} else w, h
        self.iterations = 200 if iterations is None else iterations
        self.xCenter, self.yCenter = x, y
        if canvas_w > canvas_h:
            self.xDelta = m/(canvas_h/canvas_w)
            self.yDelta = m
        else:
            self.yDelta = m/(canvas_w/canvas_h)
            self.xDelta = m
        self.delta = m
        self.color_palette = color_palette
        self.xmin = x - self.xDelta
        self.xmax = x + self.xDelta
        self.ymin = y - self.yDelta
        self.ymax = y + self.yDelta
        self.zoomFactor = zoom_factor
        self.yScaleFactor = self.h/canvas_h
        self.xScaleFactor = self.w/canvas_w
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
        self.center(event)
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.fuzhi()

    def center(self, event):
        self.xCenter = translate(event.x * self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y * self.yScaleFactor, self.h, 0, self.ymin, self.ymax)

    def fuzhi(self):
        print("当前坐标 (x, y, m): {}, {}, {}".format(self.xCenter, self.yCenter, self.delta))
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def get_color_pixels(self, flag):
        """
        根据指定的分辨率w，h生成w, h 范围内所有像素点的像素信息，
        这函数被框架的 draw 调用。
        :return: 返回像素列表
        """

        self.pixels = []
        img = Image.new('RGB', (self.w, self.h), "black")
        pix = img.load()  # create the pixel map

        move_x, move_y = 0.0, 0.0
        opt.m_loop(self.w, self.h, self.delta, self.set_flag, flag, self.iterations, move_x, move_y,
                   self.pixels, pix, [self.xmin, self.xmax], [self.ymin, self.ymax])

        if not flag:
            return img


def translate(value, left_min, left_max, right_min, right_max):
    """"
    把传入的value影射到right_min, right_max之间到一个值，只被get_escape_time调用
    """
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)
