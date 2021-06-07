args = argv();                  # Argomenti da linea di comando
matrix_file = args{1};          # Path matrice input
result_file = args{2};          # Path matrice output

load(matrix_file);              # Carica la matrice dato il path

A = Problem.A;                  # Accesso effettivo alla matrice
xe = ones(rows(A), 1);          # Ground truth soluzione
b = A * xe;                     # Calcolo termine noto data soluzione

tic;                            # Inizio timer
x = A \ b;                      # Calcolo della soluzione
time = toc;                     # Tempo impiegato

er = norm(xe - x) / norm(xe);   # Errore relativo
m_size = numel(A);              # Dimensione della matrice
m_nnz = nnz(A)                  # Elementi non zero

fid = fopen(result_file, "a+"); # Apri file
fprintf(fid, "%d;%d;%d;%d", m_size, m_nnz, er, time);
fclose(fid);                    # Chiudi file