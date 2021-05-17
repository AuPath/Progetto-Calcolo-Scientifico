### Si aspetta come parametri "File matrice" e
### "nome file dove salvare i risulati"
### in questo ordine.

args = argv();
matrix_file = args{1};
result_file = args{2};

load(matrix_file);

A = Problem.A; ## Standard per tutte le matrici
xe = ones(rows(A), 1); ## soluzione esatta
b = A * xe;
tic; ## inizio timer funzione
x = A \ b; ## Ottimizza in automatico, esattamente come Matlab

time = toc; ## tempo impiegato
er = norm(xe - x) / norm(xe); ## errore relativo
m_size = numel(A); ## dimensione matrice
nnz = nnz(A);

fid = fopen(result_file, "a+"); ## scrittura nel file, a+ sta per append
fprintf(fid, "%d;%d;%d;%d", m_size, nnz, er, time);
fclose(fid);

## Stampa messaggio di debug
## mex = sprintf("Matrice: %s, Dimensione: %d, Errore relativo: %d, Tempo: %d", matrix_file, m_size, er, time);
## disp(mex);
