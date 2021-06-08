import numpy as np
from scipy.fft import dct
import time
import math


def dct2_personal(a):
    n = len(a)  # rows
    m = len(a[0])  # columns
    c = np.zeros((n, m))  # result matrix
    # dct by rows
    for i in range(n):
        c[i] = dct_personal(a[i])  # i-th row
    # dct by columns
    for j in range(m):
        c[:, j] = dct_personal(c[:, j])

    return c


def dct_personal(v):
    n = len(v)
    c = np.zeros(n)
    for k in range(n):
        if k == 0:
            alpha = n
        else:
            alpha = n / 2
        sum = 0
        for i in range(n):
            sum = sum + v[i] * math.cos(k * math.pi * ((2 * i + 1) / (2 * n)))
        c[k] = (1 / math.sqrt(alpha)) * sum

    return c


lib_times = []
my_times = []

for i in range(4, 12):
    N = 2 ** i
    a = np.random.rand(N, N)

    lib_ti = time.time()
    lib_dct = dct(dct(a, axis=1, norm="ortho"), axis=0, norm="ortho")
    lib_tf = time.time()
    lib_times.append(lib_tf - lib_ti)

    my_ti = time.time()
    my_dct = dct2_personal(a)
    my_tf = time.time()
    my_times.append(my_tf - my_ti)
