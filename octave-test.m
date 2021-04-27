### Si aspetta come parametri "File matrice"

args = argv();
matrix_file = args{1};

load(matrix_file);

A = Problem.A; ## Standard per tutte le matrici
tic; ## inizio timer funzione
xe = ones(rows(A), 1); ## soluzione esatta
b = A * xe;
x = A \ b;

time = toc; ## tempo impiegato
er = norm(xe - x) / norm(xe); ## errore relativo
m_size = numel(A); ## dimensione matrice

filename = "prova.txt";
fid = fopen(filename, "a+");
fprintf(fid, "%d;%d;%d", m_size, er, time);
fclose(fid);

## mex = sprintf("Matrice: %s, Dimensione: %d, Errore relativo: %d, Tempo: %d", matrix_file, m_size, er, time);
## disp(mex);
