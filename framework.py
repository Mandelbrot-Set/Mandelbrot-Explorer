# coding: utf-8
import argparse
import time
from tkinter import *
from PIL import Image, ImageTk
from mandelbrot import Mandelbrot
from utils import *


class Framework(Frame):
    def __init__(self, parent, h, x=-0.75, y=0, m=1, iterations=None, img_width=6000,
                 img_height=4000, save=True, color_palette=False, spec_set='M'):
        Frame.__init__(self, parent)
        self.zoom_num = 0
        self.parent = parent
        self.parent.title("Mandelbrot && Julia")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.palette = None
        self.color_palette = color_palette
        self.background = None

        if None in {img_width, img_height}:
            img_width, img_height = int(h*1.6), h

        if img_width > img_height:
            ratio = img_height/img_width
            self.canvasW, self.canvasH = h, round(h*ratio)
        else:
            ratio = img_width/img_height
            self.canvasW, self.canvasH = round(h*ratio), h

        print(img_width, img_height)
        self.fractal = Mandelbrot(self.canvasW, self.canvasH, x=x, y=y, m=m, iterations=iterations,
                                  w=img_width, h=img_height, color_palette=color_palette, spec_set=spec_set)
        self.img = None
        self.save = save
        self.draw(color_palette)

        # fix the issue: clicking on window's title bar will generate event
        self.canvas.bind("<Control-1>", self.zoom_in)
        self.canvas.bind("<Control-2>", self.zoom_out)
        # self.canvas.bind("<B1-Motion>", self.shift_view)
        self.canvas.bind("<Button-1>", self.change_palette)
        self.canvas.bind("<Button-2>", self.save_image)
        self.canvas.bind("<Motion>", self.mouse_pos)

    def mouse_pos(self, event):
        # print("鼠标状态：", event.type)
        print("屏幕坐标：({},{}), 复平面坐标：({})".format(event.x, event.y, self.fractal.center(event)))
        pass

    def zoom_in(self, event):
        self.zoom_num += 1
        print('放大次数:', self.zoom_num)
        self.fractal.zoom_in(event)
        self.draw(self.color_palette)

    def zoom_out(self, event):
        print('Tip: zoom_out')
        self.fractal.zoom_out(event)
        self.draw(self.color_palette)

    def shift_view(self, event):
        print('Tip: shift_view')
        self.fractal.shift_view(event)
        self.draw()

    def change_palette(self, event):

        if self.fractal.n is not None:
            self.img = get_image(self.fractal.n)
            self.background = ImageTk.PhotoImage(self.img.resize((self.canvasW, self.canvasH)))
            self.canvas.create_image(0, 0, image=self.background, anchor=NW)
            self.canvas.pack(fill=BOTH, expand=1)
            print('change_palette')
        else:
            print('change_palette error!')

    def save_image(self, event):
        print('Tip: save_image')
        self.img.save("pictures/{}.png".format(time.strftime("%Y-%m-%d-%H:%M:%S")), "PNG", optimize=True)

    def draw(self, color_flag=False):
        """
        绘制图片主功能
        :return:
        """
        print('-' * 60)
        start = time.time()
        self.img = self.fractal.get_fractal(color_flag)
        print("迭代执行时间 {} 秒".format(round(time.time() - start, 2)))
        start = time.time()
        self.background = ImageTk.PhotoImage(self.img.resize((self.canvasW, self.canvasH)))
        self.canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.canvas.pack(fill=BOTH, expand=1)
        print("渲染时间 {} 秒".format(round(time.time() - start, 2)))


def main():
    master = Tk()
    width = round(master.winfo_screenwidth())
    height = round(master.winfo_screenheight())
    print('屏幕分辨率: ({},{})'.format(width, height))

    parser = argparse.ArgumentParser(description='Generate the Mandelbrot set')
    parser.add_argument('-i', '--iterations', type=int, help='The number of iterations done for each pixel. '
                                                             'Higher is more accurate but slower.')
    parser.add_argument('-x', type=float, help='The x-center coordinate of the frame.')
    parser.add_argument('-y', type=float, help='The y-center coordinate of the frame.')
    parser.add_argument('-m', '--magnification', type=float, help='The magnification level of the frame.')
    parser.add_argument('-wi', '--width', type=int, help='The width of the image.')
    parser.add_argument('-he', '--height', type=int, help='The width of the image.')
    parser.add_argument('-s', '--save', action='store_true', help='Save the generated image.')
    parser.add_argument('-c', '--color_palette', action='store_false', help="if color palette is used.")
    parser.add_argument('-spec_set', type=str, help='J for Julia, M for mandelbrot. default is M')
    args = parser.parse_args()
    if None not in [args.x, args.y, args.magnification]:
        render = Framework(master, height, x=args.x, y=args.y, m=args.magnification, color_palette=args.color_palette,
                           iterations=args.iterations, img_width=args.width, img_height=args.height, save=args.save)
    else:
        if not all(arg is None for arg in [args.x, args.y, args.magnification]):
            print("Arguments ignored. Please provide all of x, y, & m.")
        render = Framework(master, height, color_palette=args.color_palette, iterations=args.iterations,
                           img_width=args.width, img_height=args.height, save=args.save)
    # 设置窗口的大小，这里使用画布的大小进行设置，如果使用  width, height 怎会铺满屏幕，不友好。
    # master.geometry("{}x{}".format(width, height))
    master.geometry("{}x{}".format(render.canvasW, render.canvasH))
    master.mainloop()

main()
