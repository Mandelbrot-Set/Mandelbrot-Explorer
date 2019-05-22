# coding: utf-8
from utils import *
import ColourMap


class Mandelbrot:
    def __init__(self, canvas_w, canvas_h, x=-0.75, y=0, m=1, iterations=None, w=None, h=None, zoom_factor=0.1,
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
        self.iterations = 1000 if iterations is None else iterations
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

        print("图片尺寸:({},{}),画布尺寸:({},{})".format(self.w, self.h, canvas_w, canvas_h))
        print("屏幕坐标：({},{}) ->复平面Center：({},{})".format(x, y, self.xCenter, self.yCenter))
        print("系数:delta {} xDelta {} yDelta {} zoomFactor {})".format(self.delta, self.xDelta, self.yDelta, self.zoomFactor))
        print("xmin {} xmax {} ymin {}, ymax {} )".format(self.xmin, self.xmax, self.ymin, self.ymax))
        print("复平面区域 ({},{}), 迭代次数:{}".format(abs(self.xmin - self.xmax), abs(self.ymin - self.ymax), self.iterations))

        self.set_flag = spec_set
        self.n = None
        self.palette = create_palette()
        # self.palette = ColourMap.create_linear_palette(ColourMap.red, ColourMap.yellow, 100)

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
        print("屏幕坐标：({},{}) ->复平面Center：({},{})".format(event.x, event.y, self.xCenter, self.yCenter))

    def center(self, event):
        self.xCenter = translate(event.x * self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y * self.yScaleFactor, self.h, 0, self.ymin, self.ymax)

        return self.xCenter, self.yCenter

    def fuzhi(self):
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

        # 去一个合适的迭代次数
        # https://math.stackexchange.com/questions/16970/a-way-to-determine-the-ideal-number-of-maximum-iterations-for-an-arbitrary-zoom
        self.iterations = round(50 * (math.log(self.w / abs(self.xmin - self.xmax), 10) ** 1.25))
        print("系数:delta {} xDelta {} yDelta {} zoomFactor {})".format(self.delta, self.xDelta, self.yDelta, self.zoomFactor))
        print("xmin {} xmax {} ymin {}, ymax {})".format(self.xmin, self.xmax, self.ymin, self.ymax))
        print("复平面区域 ({},{}), 迭代次数:{}".format(abs(self.xmin - self.xmax), abs(self.ymin - self.ymax), self.iterations))

    def get_fractal(self, flag):
        """
        每次渲染调用的函数，
        :param flag: 是否使用颜色模版的标记，True使用，False不使用
        :return: 如果不使用模版，返回图片
        """

        self.n = mandelbrot_set(self.xmin, self.xmax, self.ymin, self.ymax, self.w, self.h, self.iterations)

        return get_image(self.n, self.palette)
