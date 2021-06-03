import numpy as np
from PIL import Image
import math

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
 
def pseudo_jpeg(img_path, f, d):
    img = Image.open(img_path)
    img_mat = np.array(img)
    c_mat = np.zeros_like(img_mat)
    rows, columns = img_mat.shape
    blocks = []

    for i in range(math.floor(rows / f)):
        for j in range(math.floor(columns / f)):
            ## a[0:8,0:3] 8 righe 3 colonne
            c_mat[i*f : (i+1)*f, j*f : (j+1)*f] = dct2_personal(img_mat[i*f : (i+1)*f, j*f : (j+1)*f])

    return c_mat
    

