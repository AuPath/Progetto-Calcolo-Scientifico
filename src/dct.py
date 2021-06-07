import math

import numpy as np
from PIL import Image
from PyQt5.QtCore import (QObject, pyqtSignal)
from PyQt5.QtWidgets import QProgressBar
from scipy.fft import dct
from scipy.fft import idct


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, progress_bar: QProgressBar, img_path, f, d):
        super(Worker, self).__init__()
        self.img_path = img_path
        self.f = int(f)
        self.d = int(d)
        self.progress_bar = progress_bar

    def run(self):
        img = Image.fromarray(self.pseudo_jpeg(self.img_path, self.f, self.d))
        cmpr_img_path = self.img_path.replace(".bmp", "-compressed.bmp")
        img.save(cmpr_img_path)
        self.finished.emit()

    ## fissa un range di valori possibili per n
    def clamp(self, n, smallest, largest):
        return max(smallest, min(n, largest))

    ## forza n ad un valore intero tra 0 e 255
    def fix_number(self, n):
        return self.clamp(round(n), 0, 255)

    ### Per le posizioni che non rientrano nei blocchi fxf viene usato l'approccio
    ### a "cornice" visto a lezione, cioé c'é un bordo nero.
    def pseudo_jpeg(self, img_path, f, d):
        img = Image.open(img_path)
        img_mat = np.array(img)
        c_mat = np.zeros_like(img_mat)
        rows, columns = img_mat.shape

        max_i = math.floor(rows / f)
        max_j = math.floor(columns / f)

        blocks_computed = 0
        self.progress_bar.setMaximum(max_i * max_j)

        for i in range(max_i):
            for j in range(max_j):

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
                        block[k, l] = self.fix_number(block[k, l])

                c_mat[i * f: (i + 1) * f, j * f: (j + 1) * f] = block

                blocks_computed += 1
                self.progress.emit(blocks_computed)

        return c_mat
