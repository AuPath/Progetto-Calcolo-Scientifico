function [] = matlab_solver(matrix_file, result_file)

    load(matrix_file);              % Carica matrice dato il path
    A = Problem.A;                  % Accesso effettivo alla matrice

    xe = ones(length(A(:,1)), 1);   % Ground truth soluzione
    b = A * xe;                     % Calcolo termine noto data soluzione

    tic;                            % Inizio timer
    x = A \ b;                      % Calcolo della soluzione
    time = toc;                     % Tmpo impiegato

    % Statistice
    er = norm(xe - x) / norm(xe);   % Errore relativo
    m_size = numel(A);              % Dimensione matrice
    m_nnz = nnz(A)                  % Elementi non zero matrice

    fid = fopen(result_file, "a+"); % Apri file in append
    fprintf(fid, "%d;%d;%d;%d", m_size, m_nnz, er, time);
    fclose(fid);                    % Chiudi il file

end
