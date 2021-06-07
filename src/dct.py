import math

import numpy as np
from PIL import Image
from scipy.fft import dct
from scipy.fft import idct


## fissa un range di valori possibili per n
def clamp(n, smallest, largest): return max(smallest, min(n, largest))


## forza n ad un valore intero tra 0 e 255
def fix_number(n): return clamp(round(n), 0, 255)


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

            block = img_mat[i * f: (i + 1) * f, j * f: (j + 1) * f]
            block = dct(dct(block, axis=1, norm="ortho"), axis=0, norm="ortho")

            ## eliminazione elementi sotto diagonale

            block_rows, block_columns = block.shape
            for k in range(block_rows):
                for l in range(block_columns):
                    if (k + l) >= d:
                        block[k, l] = 0  ## per eliminare la frequenza intende mettere a 0 ?

            block = idct(idct(block, axis=1, norm="ortho"), axis=0, norm="ortho")

            ## fix dei numeri
            for k in range(block.shape[0]):
                for l in range(block.shape[1]):
                    block[k, l] = fix_number(block[k, l])

            c_mat[i * f: (i + 1) * f, j * f: (j + 1) * f] = block

    return c_mat


def save_compressed_image(img_path, f, d):
    img = Image.fromarray(pseudo_jpeg(img_path, int(f), int(d)))
    cmpr_img_path = img_path.replace(".bmp", "-compressed-{f}-{d}.bmp".format(f=f,d=d))
    img.save(cmpr_img_path)
