
def get_escape_time(complex c, iterations):
    cdef complex z = c
    cdef int i
    for i in range(1, iterations):
        if z.real*z.real + z.imag*z.imag > 2:
            return i
        z = z * z + c

    return 0

def julia_escape_time(complex z, complex c, int iterations):
    cdef int i = iterations
    while z.real * z.real + z.imag * z.imag < 4 and i > 1:
        tmp = z.real * z.real - z.imag * z.imag + c.real
        z.imag, z.real = 2.0 * z.real * z.imag + c.imag, tmp
        i -= 1

    return i

def get_colors(pixels_map, pixels, palette):
    cdef int index
    for index, p in enumerate(pixels):
        pixels_map[int(p[0]), int(p[1])] = palette[p[2] % 256]

def m_loop(w, h, delta, set_flag, flag, iterations, move_x, move_y, pixels, pix, xm, ym):
    cdef int x
    cdef int y
    for x in range(w):
        for y in range(h):
            if set_flag == 'J':
                zx = 1.5 * (x - w / 2) / (0.5 * delta * w) + move_x
                zy = 1.0 * (y - h / 2) / (0.5 * delta * h) + move_y
                i = julia_escape_time(complex(zx, zy), complex(-0.7, 0.27015), 255)
            else:
                # Mandelbrot
                re = translate(x, 0, w, xm[0], xm[1])
                im = translate(y, 0, h, ym[1], ym[0])
                z, c = complex(re, im), complex(re, im)
    
                # 采用 Cython 优化迭代效率
                i = get_escape_time(c, iterations)
            if flag:
                pixels.append((x, y, i))
            else:
                pix[x, y] = (i << 21) + (i << 10) + i * 8

def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)