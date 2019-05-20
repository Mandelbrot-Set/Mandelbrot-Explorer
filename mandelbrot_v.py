import os
import time
from moviepy.editor import ImageSequenceClip
from utils import *


def gif(filename, array, fps=10, scale=1.0):
    """
    :param filename: 文件名
    :param array: 序列数组
    :param fps: 每秒帧数
    :param scale: 缩放比例
    :return: 返回gif文件
    """
    fname, _ = os.path.splitext(filename)
    filename = fname + '.gif'
    filename_v = fname + '.mp4'

    # copy into the color dimension if the images are black and white
    if array.ndim == 3:
        array = array[..., np.newaxis] * np.ones(3)

    clip = ImageSequenceClip(list(array), fps=fps).resize(scale)
    # clip.write_gif(filename, fps=fps)
    clip.write_videofile(filename_v, fps=fps)

    return clip


def get_region(start, end, frames=8, zoom_factor=0.1, delta=None):
    """
    在走frames步的情况下，计算出从起点到止点： x方向步长以及斜率；
    在zoom_factor和delta确定情况下（即确定的起点和止点为中心的方形区域），算出 起点为中心方形区域
    移动 止点方形区域：x, y方向每步缩放比例
    :param start: 起点坐标
    :param end: 止点坐标
    :param frames: 从起点到止点打算走的步数，每一步都回绘制一个图，一张图即一帧，所以也叫 总帧数
    :param zoom_factor: 缩放比例，取值在 0～1 之间，取 0.1 表示缩小10倍。
    :param delta: x, y方向增量，以此确定方形区域大小
    :return: 返回斜率，缩放比例，起始区域
    """
    k = (end[1] - start[1]) / (end[0] - start[0])
    x_delta = (end[0] - start[0]) / frames

    sx_min, sx_max = start[0] - delta[0], start[0] + delta[0]
    sy_min, sy_max = start[1] - delta[1], start[1] + delta[1]

    delta[0] *= zoom_factor
    delta[1] *= zoom_factor

    dx_min, dx_max = end[0] - delta[0], end[0] + delta[0]
    dy_min, dy_max = end[1] - delta[1], end[1] + delta[1]

    # print("目标区域：", dx_min, dx_max, dy_min, dy_max)

    scale_x = (abs(dx_max - dx_min) - abs(sx_max - sx_min)) / frames
    scale_y = (abs(dy_max - dy_min) - abs(sy_max - sy_min)) / frames

    return [k, x_delta], [abs(scale_x/2), abs(scale_y/2)], [sx_min, sx_max, sy_min, sy_max]


def seg_mov(start, end, frames=8, zoom_factor=0.1, delta=None):
    """
    计算由起点到止点点图形序列
    :param start: 起点坐标
    :param end: 止点坐标
    :param frames: 从起点到止点打算走的步数，每一步都回绘制一个图，一张图即一帧，所以也叫 总帧数
    :param zoom_factor: 缩放比例，取值在 0～1 之间，取 0.1 表示缩小10倍。
    :param delta: x, y方向增量，以此确定方形区域大小
    :return:  返回序列数组、当前的缩放比例
    """
    xc, yc = start[0], start[1]
    kd, scale, sr = get_region(start, end, frames, zoom_factor, delta)

    seqs = np.zeros([frames] + [ImageHeight, ImageWidth] + [3])
    for i in range(frames):
        sr[0] += scale[0]
        sr[1] -= scale[0]
        sr[2] += scale[1]
        sr[3] -= scale[1]

        xc += kd[1]
        yc += kd[0] * kd[1]

        xmin, xmax = sr[0] + xc - start[0], sr[1] + xc - start[0]
        ymin, ymax = sr[2] + yc - start[1], sr[3] + yc - start[1]
        iterations = round(50 * (math.log(ImageWidth / abs(xmin - xmax), 10) ** 1.25))

        # print("目标中心位置：", xc, yc)
        # print("迭代区域：", xmin, xmax, ymin, ymax)
        # print("复平面区域 ({},{}), 迭代次数:{}".format(abs(xmin - xmax), abs(ymin - ymax), iterations))
        # print('Generating {}/{}....'.format(i + 1, frames))

        n = mandelbrot_set(xmin, xmax, ymin, ymax, ImageWidth, ImageHeight, iterations)
        img = get_image(n, palette)
        seqs[i, :, :] = np.array(img)

    return seqs, delta


##############################################################################
ImageWidth = 1920
ImageHeight = 1080

palette = create_palette()

start_time = time.time()

the_delta = [1.6, 1]
pt_list = [
    [-0.75, 0],
    [-0.5425925925925927, 0.528888888888889],
    [-0.5414074074074076, 0.6093333333333334],
    [-0.5439555555555557, 0.6173481481481482],
    [-0.5445333333333335, 0.6179925925925926],
    [-0.5445943703703706, 0.6180641481481483],
    [-0.544605066666667, 0.6180734074074075],
    [-0.5446057511111114, 0.6180742414814816],
    [-0.5446058171851855, 0.6180743251851852],
    [-0.5446058243851856, 0.6180743343555557],
    [-0.5446058251348153, 0.6180743352844446],
    [-0.5446058250337782, 0.6180743353651853],
    [-0.5446058250228153, 0.6180743353740298],
    [-0.5446058250222997, 0.6180743353749587]
    ]

seqs_list = []
size = len(pt_list)-1
for index in range(size):
    print("{}/{}: {} {} ".format(index+1, size, pt_list[index], pt_list[index+1]))
    seqs, the_delta = seg_mov(pt_list[index],
                              pt_list[index+1],
                              frames=60,
                              zoom_factor=.1,
                              delta=the_delta)
    seqs_list.append(seqs)

current = round((time.time() - start_time)/60, 2)
print("执行时间 {} 分".format(current))
print('Make gif.....')
seqs_all = np.vstack(seqs_list)
gif('gif/mandelbrot_gif_{}.gif'.format(current), seqs_all, 8)
print('Please check gif/julia_gif_.gif...')
