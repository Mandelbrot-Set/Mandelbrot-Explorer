
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