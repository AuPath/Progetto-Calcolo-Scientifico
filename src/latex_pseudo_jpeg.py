import math
import numpy as np
from PIL import Image
from numpy.fft import fft
from numpy.fft import ifft

## fissa un range di valori possibili per n
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

## forza n ad un valore intero tra 0 e 255
def fix_number(n):
    return clamp(round(n), 0, 255)

def pseudo_jpeg(img_path, f, d):
    img = Image.open(img_path)
    img_mat = np.array(img)
    c_mat = np.zeros_like(img_mat)
    rows, columns = img_mat.shape
    
    max_i = math.floor(rows / f)
    max_j = math.floor(columns / f)

    for i in range(max_i):
        for j in range(max_j):

            ## Applicazione DCT2
            ## Slice della matrice fxf
            block = img_mat[i * f: (i + 1) * f, j * f: (j + 1) * f]
            block = fft(fft(block, axis=1, norm="ortho"),axis=0, norm="ortho").real
            
            ## Eliminazione elementi sotto diagonale
            block_rows, block_columns = block.shape
            for k in range(block_rows):
                for l in range(block_columns):
                    if (k + l) >= d:
                        block[k, l] = 0

            ## Applicazione IDCT2
            block = ifft(ifft(block, axis=1, norm="ortho"),axis=0, norm="ortho").real

            ## fix dei numeri
            for k in range(block.shape[0]):
                for l in range(block.shape[1]):
                    block[k, l] = fix_number(block[k, l])

            c_mat[i * f: (i + 1) * f, j * f: (j + 1) * f] = block
    
    return c_mat
