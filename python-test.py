from scipy.io import loadmat
from scipy.sparse.linalg import spsolve
from scipy.linalg import norm
import numpy as np
import sys
import time

args = sys.argv
matrix_file = args[1]
result_file = args[2]

struct = loadmat(matrix_file)

# Matrix
A = struct['Problem']['A'][0, 0]
# Exact solution
xe = np.ones(A.shape[0])
# Compute b
b = A.dot(xe)
# Solve the linear system
start_time = time.time()
x = spsolve(A, b)

elapsed = time.time() - start_time
er = norm(xe - x) / norm(xe)
m_size = A.shape[0]
nnz = A.nnz

with open(result_file, 'a+') as f:
    f.write(f'{m_size};{nnz};{er};{elapsed}\n')
