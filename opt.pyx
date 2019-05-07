
def get_escape_time(complex c, iterations):
    cdef complex z = c
    cdef int i
    for i in range(1, iterations):
        if z.real*z.real + z.imag*z.imag > 2:
            return i
        z = z * z + c

    return 0