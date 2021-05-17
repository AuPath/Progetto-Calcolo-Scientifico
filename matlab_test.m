function [] = matlab_test(matrix_file, result_file)

% da cmd
% matlab  -nodisplay -nosplash -nodesktop -r "matlab_test('Matrici-test/nome-matrice.mat', 'nome-matrice-result.txt');exit;"

% Si aspetta come parametri "File matrice" e
% "nome file dove salvare i risulati"
% in questo ordine.
profile('-memory','on');

load(matrix_file);
A = Problem.A;

% preparo il sistema
xe = ones(length(A(:,1)), 1); % soluzione esatta
b = A * xe;

tic; % inizio timer funzione
x = A \ b; % ottimizza in automatico
time = toc; % tempo impiegato

% statistiche
er = norm(xe - x) / norm(xe); % errore relativo
m_size = numel(A); % dimensione matrice
nnzero = nnz(A);

peak_mem = profile('info').FunctionTable.PeakMem;

fid = fopen(result_file, "a+"); % scrittura nel file, a+ sta per append
fprintf(fid, "%d;%d;%d;%d;%d", m_size, nnzero, er, time, peak_mem);
fclose(fid);

end
