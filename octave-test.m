### Si aspetta come parametri "File matrice" e "nome file dove salvare
### i risulati" in questo ordine.

args = argv();
matrix_file = args{1};
result_file = args{2};

load(matrix_file);

A = Problem.A; ## Standard per tutte le matrici
tic; ## inizio timer funzione
xe = ones(rows(A), 1); ## soluzione esatta
b = A * xe;
x = A \ b; ## Ottimizza in automatico, esattamente come Matlab

time = toc; ## tempo impiegato
er = norm(xe - x) / norm(xe); ## errore relativo
m_size = numel(A); ## dimensione matrice

fid = fopen(result_file, "a+");
fprintf(fid, "%d;%d;%d", m_size, er, time);
fclose(fid);

## Stampa messaggio di debug
## mex = sprintf("Matrice: %s, Dimensione: %d, Errore relativo: %d, Tempo: %d", matrix_file, m_size, er, time);
## disp(mex);
