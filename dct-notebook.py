import math
import os
import time

import numpy as np
import pandas as pd
import seaborn as sns
from numpy.fft import fft


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

# piu di 14 e' troppo
for i in range(4, 15):
    N = 2 ** i
    print(str(i) + " di 14")
    a = np.random.rand(N, N)

    print("fft " + str(i) + " di 14")
    lib_ti = time.time()
    lib_dct = fft(fft(a, axis=1, norm="ortho"), axis=0, norm="ortho")
    lib_tf = time.time()
    lib_times.append(lib_tf - lib_ti)
    if i == 14:
        print('-'*15 + " FINE FFT " + '-'*15)

    if i < 12: # di piu non va
        print("my_dct " + str(i) + " di 11")
        my_ti = time.time()
        my_dct = dct2_personal(a)
        my_tf = time.time()
        my_times.append(my_tf - my_ti)
        if i == 11:
            print('-'*15 + " FINE MY_DCT " + '-'*15)

for i in range(12,15):
    my_times.append(0)

sns.set_theme(style="darkgrid")

data = pd.DataFrame(list(zip(lib_times, my_times)), columns=['Numpy FFT', 'HomeMade DCT'])
data.to_pickle(os.path.join(".", "out-dct", "data-dct.pkl"))

