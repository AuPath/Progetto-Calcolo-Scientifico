import math

import numpy as np
from PIL import Image
from PyQt5.QtCore import (QObject, pyqtSignal)
from PyQt5.QtWidgets import QProgressBar
from numpy.fft import fft
from numpy.fft import ifft
import os


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    out_path = pyqtSignal(str)

    def __init__(self, progress_bar: QProgressBar, img_path, out_dir, f, d):
        super(Worker, self).__init__()
        self.img_path = img_path.strip()
        self.out_dir = out_dir.strip()
        self.f = int(f)
        self.d = int(d)
        self.progress_bar = progress_bar

    def run(self):
        img = Image.fromarray(self.pseudo_jpeg(self.img_path, self.f, self.d))
        cmpr_img_path = self.img_path.replace(".bmp", "-compressed-{f}-{d}.bmp".format(f=self.f, d=self.d))

        out_path = cmpr_img_path
        if self.out_dir:
            filename = os.path.split(cmpr_img_path)[-1]
            out_path = os.path.join(self.out_dir, filename)
        img.save(out_path)
        self.out_path.emit(out_path)
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
                block = fft(fft(block, axis=1, norm="ortho"), axis=0, norm="ortho")

                ## eliminazione elementi sotto diagonale

                block_rows, block_columns = block.shape
                for k in range(block_rows):
                    for l in range(block_columns):
                        if (k + l) >= d:
                            block[k, l] = 0  ## per eliminare la frequenza intende mettere a 0 ?

                block = ifft(ifft(block, axis=1, norm="ortho"), axis=0, norm="ortho")

                ## fix dei numeri
                for k in range(block.shape[0]):
                    for l in range(block.shape[1]):
                        block[k, l] = self.fix_number(block[k, l])

                c_mat[i * f: (i + 1) * f, j * f: (j + 1) * f] = block

                blocks_computed += 1
                self.progress.emit(blocks_computed)

        return c_mat
