import numpy as np
from PIL import Image
import math

## fissa un range di valori possibili per n
def clamp(n, smallest, largest): return max(smallest, min(n, largest))

## forza n ad un valore intero tra 0 e 255
def fix_number(n): return clamp(round(n), 0, 255)  

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

### Per le posizioni che non rientrano nei blocchi fxf viene usato l'approccio
### a "cornice" visto a lezione, cioé c'é un bordo nero.
def pseudo_jpeg(img_path, f, d):
    img = Image.open(img_path)
    img_mat = np.array(img)
    c_mat = np.zeros_like(img_mat)
    rows, columns = img_mat.shape
    
    for i in range(math.floor(rows / f)):
        for j in range(math.floor(columns / f)):

            ## a[0:8,0:3] 8 righe 3 colonne
            block = dct2_personal(img_mat[i*f : (i+1)*f, j*f : (j+1)*f])

            ## eliminazione elementi sotto diagonale
            for k in range(block.shape[0]):
                for l in range(block.shape[1]):
                    if (k + l) >= d :
                        block[k,l] = 0 ## per eliminare la frequenza intende mettere a 0 ?
                        
            ## block = idct2_personal(block);

            ## fix dei numeri
            for k in range(block.shape[0]):
                for l in range(block.shape[1]):
                    fix_number(block[k,l])
                    
            c_mat[i*f : (i+1)*f, j*f : (j+1)*f] = block                    

    return c_mat
    

