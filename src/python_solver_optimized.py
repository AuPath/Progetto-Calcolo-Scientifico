from scipy.io import loadmat
from sksparse.cholmod import cholesky, CholmodNotPositiveDefiniteError
from scipy.sparse.linalg import spsolve
from scipy.linalg import norm
import numpy as np
import sys
import time

matrix_file = sys.argv[1]           # Path matrice input
result_file = sys.argv[2]           # Path matrice output

struct = loadmat(matrix_file)

A = struct['Problem']['A'][0, 0]    # Accesso matrice
xe = np.ones(A.shape[0])            # Ground truth soluzione
b = A.dot(xe)                       # Termine noto dato xe

start_time = time.time()            # Start timer
try:
    # Calcolo soluzione con Cholesky
    factor = cholesky(A)            # Fattorizzazione con Cholesky
    x = factor(b)                   # Calcolo soluzione con fattorizzazione
except CholmodNotPositiveDefiniteError:
    # Eccezione: La matrice non e' definita positiva
    # Calcolo soluzione utilizzando fattorizzazione LU
    x = spsolve(A, b, use_umfpack=False)
elapsed = time.time() - start_time  # Tempo trascorso

er = norm(xe - x) / norm(xe)        # Errore relativo
m_size = A.shape[0] * A.shape[1]    # Dimensione matrice
nnz = A.nnz                         # Elementi non zero della matrice

# Scrittura risultati su file
with open(result_file, 'a+') as f:
    f.write(f'{m_size};{nnz};{er};{elapsed}')
