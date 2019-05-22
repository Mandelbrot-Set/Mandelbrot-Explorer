# ==============================================================
# (c) John Whitehouse 2002-2003
# htpp://www.eddaardvark.co.uk/
# ==============================================================
# 1、迭代次数来为模式着色
# 2、Star着色算法迭代与标准方案相同的方程，但它在迭代期间也记录|Z|的值 。最小的|Z|的值用于决定颜色。这会产生一种模式，其中整个集合中发
#    现的迷你 mandelbrot 看起来被发光的晕圈包围
# 3、'Bands' Colouring Algorithm
#    在波段着色算法中，而不是计算|Z|的最小值 在迭代期间遇到我们独立的实部和虚部，找到|r|的最小值 和|i|。然后，我们根据两者的组合计算颜色。
#    调色板4和5排列颜色以强调乐队
# 4、Imaginary and Real Bands
#    用于生成带图案的着色方案可以分成两个单独的组件，显示来自实部和虚部的贡献。 “-tMI”将绘制虚部，“-tMR”将绘制实部
#    （“-jJI”和“-JJR”用于Julia集）。 这种分离可以在以下三个图像中看到，从上面的颜色方案表中再现
# 5、Quadrants Colouring Scheme Bands
#    我称之为象限，就像我第一次想到的那样，我只有4种颜色，每个象限对应一个复杂的平面。 但从那时起我将其扩展为包含255种颜色。 在此方案中，
#    您将继续迭代z，直到达到模数大于2（x2 + y2> 4）的点（x + iy）。 然后计算y / x的反正切并将其用作颜色图的索引。 结果是左侧的图像。

# Some predefined colours

red = chr(0) + chr(0) + chr(255)
blue = chr(255) + chr(0) + chr(0)
green = chr(0) + chr(255) + chr(0)
cyan = chr(255) + chr(255) + chr(0)
yellow = chr(0) + chr(255) + chr(255)
magenta = chr(255) + chr(0) + chr(255)
white = chr(255) + chr(255) + chr(255)
black = chr(0) + chr(0) + chr(0)
orange = chr(0) + chr(128) + chr(255)

dk_red = chr(0) + chr(0) + chr(128)
dk_blue = chr(128) + chr(0) + chr(0)
dk_green = chr(0) + chr(128) + chr(0)
dk_cyan = chr(128) + chr(128) + chr(0)
dk_yellow = chr(0) + chr(128) + chr(128)
dk_magenta = chr(128) + chr(0) + chr(128)
dk_grey = chr(128) + chr(128) + chr(128)
dk_orange = chr(0) + chr(64) + chr(128)

vdk_red = chr(0) + chr(0) + chr(64)
vdk_blue = chr(64) + chr(0) + chr(0)
vdk_green = chr(0) + chr(64) + chr(0)
vdk_cyan = chr(64) + chr(64) + chr(0)
vdk_yellow = chr(0) + chr(64) + chr(128)
vdk_magenta = chr(64) + chr(0) + chr(64)
vdk_grey = chr(64) + chr(64) + chr(64)

lt_red = chr(128) + chr(128) + chr(255)
lt_blue = chr(255) + chr(128) + chr(128)
lt_green = chr(128) + chr(255) + chr(128)
lt_cyan = chr(255) + chr(255) + chr(128)
lt_yellow = chr(128) + chr(255) + chr(255)
lt_magenta = chr(255) + chr(128) + chr(255)
lt_grey = chr(192) + chr(192) + chr(192)
lt_orange = chr(128) + chr(192) + chr(255)

vlt_grey = chr(224) + chr(224) + chr(224)


def makeColour(r, g, b):
    """Make a colour string from the RGB values"""
    return chr(b) + chr(g) + chr(r)


def create_linear_palette(start, end, num):
    """
    Create a set of colours, starting at 'start' and ending
    at 'end'. Colours are three character strings representing
    blue, green and red - 'bgr'
    """

    r0 = ord(start[2])
    g0 = ord(start[1])
    b0 = ord(start[0])

    palette = [(0, 0, 0)]

    if num > 1:
        r_inc = float(ord(end[2]) - r0) / (num - 1)
        g_inc = float(ord(end[1]) - g0) / (num - 1)
        b_inc = float(ord(end[0]) - b0) / (num - 1)

        for i in range(0, num):
            r = r0 + int(i * r_inc)
            g = g0 + int(i * g_inc)
            b = b0 + int(i * b_inc)
            palette.append((r, g, b))
    else:
        palette[0] = (r0, b0, g0)

    return palette


def create_linear(start, end, num):
    """
    Create a set of colours, starting at 'start' and ending
    at 'end'. Colours are three character strings representing
    blue, green and red - 'bgr'
    """

    r0 = ord(start[2])
    g0 = ord(start[1])
    b0 = ord(start[0])

    if num > 1:
        colour_map = ['xxx'] * num

        r_inc = float(ord(end[2]) - r0) / (num - 1)
        g_inc = float(ord(end[1]) - g0) / (num - 1)
        b_inc = float(ord(end[0]) - b0) / (num - 1)

        for i in range(0, num):
            r = r0 + int(i * r_inc)
            g = g0 + int(i * g_inc)
            b = b0 + int(i * b_inc)

            colour_map[i] = chr(b) + chr(g) + chr(r)
    else:
        colour_map = [chr(b0) + chr(g0) + chr(r0)]

    return colour_map

