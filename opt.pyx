cimport cython
import math

cdef int mandelbrot(double creal, double cimag, int maxiter):
    cdef:
        double real2, imag2
        double real = 0., imag = 0.
        int n

    for n in range(maxiter):
        real2 = real*real
        imag2 = imag*imag
        if real2 + imag2 > 4.0:
            return n
        imag = 2* real*imag + cimag
        real = real2 - imag2 + creal

    return 0

cdef int julia_escape_time(complex z, complex c, int iterations):
    cdef:
        int i = iterations

    while z.real * z.real + z.imag * z.imag < 4 and i > 0:
        tmp = z.real * z.real - z.imag * z.imag + c.real
        z.imag, z.real = 2.0 * z.real * z.imag + c.imag, tmp
        i -= 1

    return i

cdef double translate(double value, double left_min, double left_max,
               double right_min, double right_max):
    cdef:
        double left_span, right_span, value_scaled

    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef get_colors(pixels_map, pixels, palette):
    cdef int index
    for index, p in enumerate(pixels):
        pixels_map[int(p[0]), int(p[1])] = palette[p[2] % 256]


cdef render_color(int e_i, int iterations):
    cdef:
        int rgb_increments, case_num, remain_num, value

    if e_i <= 2:
        return 0, 0, 0
    elif e_i == iterations-1:
        return 0, 25, 0

    rgb_increments = math.floor((iterations / 7))
    case_num = math.floor(e_i / rgb_increments)
    remain_num = e_i % rgb_increments
    value = math.floor(256 / rgb_increments) * remain_num

    if case_num == 0:
        return 0, value, 0

    if case_num == 1:
        return 0, 255, value

    if case_num == 2:
        return value, 255, 255

    if case_num == 3:
        return value, 0, 255

    if case_num == 4:
        return 255, value, 255

    if case_num == 5:
        return 255, value, 0

    if case_num == 6:
        return 255, 255, value

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef m_loop(int w, int h, double delta, set_flag, flag, int iterations,
             double move_x, double move_y, pixels, pix, xm, ym):
    cdef:
        int x, y, i
        double zx, zy, re, rm
        complex z, c

    for x in range(w):
        for y in range(h):
            if set_flag == 'J':
                zx = 1.5 * (x - w / 2) / (0.5 * delta * w)
                zy = 1.0 * (y - h / 2) / (0.5 * delta * h)
                i = julia_escape_time(complex(zx, zy), complex(move_x, move_y), iterations)
            else:
                # Mandelbrot
                re = translate(x, 0, w, xm[0], xm[1])
                im = translate(y, 0, h, ym[1], ym[0])
                i = mandelbrot(re, im, iterations)
                # z, c = complex(re, im), complex(re, im)
                # i = get_escape_time(c, iterations)

            if flag:
                pixels.append((x, y, i))
            else:
                # pix[x, y] = render_color(i, iterations)
                pix[x, y] = (i << 21) + (i << 10) + i * 8
