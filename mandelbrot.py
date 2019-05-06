from multiprocessing import Pool


class Mandelbrot:
    def __init__(self, canvas_w, canvas_h, x=-0.75, y=0, m=1.5, iterations=None,
                 w=None, h=None, zoom_factor=0.1, multi=True):
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
        :param multi: 多进程标记
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
        self.multi = multi
        self.xmin = x - self.xDelta
        self.xmax = x + self.xDelta
        self.ymin = y - self.yDelta
        self.ymax = y + self.yDelta
        self.zoomFactor = zoom_factor
        self.yScaleFactor = self.h/canvas_h
        self.xScaleFactor = self.w/canvas_w
        self.c, self.z = 0, 0
        self.pixels = []

    def shift_view(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoom_out(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoom_in(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def get_pixels(self):
        coordinates = []
        for x in range(self.w):
            for y in range(self.h):
                coordinates.append((x, y))
        if self.multi:
            pool = Pool()
            self.pixels = pool.starmap(self.get_escape_time, coordinates)
            pool.close()
            pool.join()
        else:
            print("Using 1 core...")
            pixels = []
            for coord in coordinates:
                pixels.append(self.get_escape_time(coord[0], coord[1]))
            self.pixels = pixels

    def get_escape_time(self, x, y):
        re = translate(x, 0, self.w, self.xmin, self.xmax)
        im = translate(y, 0, self.h, self.ymax, self.ymin)
        z, c = complex(re, im), complex(re, im)
        for i in range(1, self.iterations):
            if abs(z) > 2:
                return x, y, i
            z = z*z + c
        return x, y, 0


def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)
