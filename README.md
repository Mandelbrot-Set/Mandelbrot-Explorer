# Interactive-Python-Mandelbrot
A clickable interactive mandelbrot set, made with Python 3, PIL, and Tkinter. Uses multiprocessing, colour palette is randomly generated.

# 性能优化
1、采用Cython优化迭代部分代码，性能提高了10倍， 并暂时取消了多进程方式，也许多进程方式使用不当，反而不及不用多进程方式

2、增加了朱丽亚集合的绘制，同样进行了迭代的优化

3、初步优化了对颜色对处理

# Fix
1. 调整了窗口大小
2. 调整了交互的按键操作，避免鼠标点击按钮引起的卡顿
3. 增加了鼠标位置监控事件

## Usage
1. Install required modules with `pip install -r requirements.txt`.
2. Run the program with `python3 framework.py`
3. Control+left-click the image where you want to zoom in
4. Control+right-click the image to zoom out
5. Left-click to change the image colour-palette
6. Right-click to save the image
7. Left-click drag to shit view

## Commandline options
    -h, --help               Command-line help dialogue.
    -i, --iterations         Number of iterations done for each pixel. Higher is more accurate but slower.
    -x                       The x-center coordinate of the frame.
    -y                       The y-center coordinate of the frame.
    -m, --magnification      The magnification level of the frame. Scientific notation (e.g. 3E-4) is permitted.
    -wi, --width             The number of pixels wide the image is.
    -he, --height            The number of pixels high the image is.
    -s, --save               Flag to save the generated image.
    -nm, --noMulti           Flag to not use multiprocessing.

## Mandelbrot Set feature rendered by this program
<img src="https://raw.githubusercontent.com/rosslh/Interactive-Python-Mandelbrot/master/pictures/image.png" width="100%">
