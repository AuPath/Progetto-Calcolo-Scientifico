function [] = analisi_matlab(matrix_dir, matlab_file, mem_file, result_file)

%%%%%%%%%%%%%%% DA TESTARE %%%%%%%%%%%%%%%

% da cmd
% matlab -nodisplay -nosplash -nodesktop -r "matlab_test('Matrici-test/nome-matrice.mat', 'nome-matrice-result.txt');exit;"

% Come parametri si aspetta:
% path cartella matrici 
% file dove salvare i risultati dello script Matlab
% file dove salvare i risultati della memoria
% file dove salvare i risultati complessivi
% devono essere dati in questo ordine

matrices = dir(strcat(matrix_dir,'/*.mat'));
script2 = strcat("truncate -size -1 '", matlab_file, "'"); % elimino ultima newline inutile
script3 = strcat("paste -d ';' '", matlab_file, "' '", mem_file, "' > '", result_file, "'"); % merge dei due file
script4 = strcat("echo '' >> '", matlab_file, "'"); % aggiungo newline nel file prodotto dallo script Matlab

for i = 1:length(matrices)
    matrix_name = strcat(matrix_dir, "/", matrices(i).name);
    script1 = strcat("/usr/bin/time -f '%M' matlab -W matlab-test(", matrix_name, ", ", matlab_file, ") &>> '", mem_file, "'");
    % Misurazione memoria
    if ispc % Windows
        system(strcat("C:\cygwin64\bin\bash.exe --login -c ", script1), '-echo');
        system(strcat("C:\cygwin64\bin\bash.exe --login -c ", script2), '-echo');
        system(strcat("C:\cygwin64\bin\bash.exe --login -c ", script3), '-echo');
        system(strcat("C:\cygwin64\bin\bash.exe --login -c ", script4), '-echo');
    elseif isunix % Linux (o Mac)
        system(script1,'-echo');
        system(script2, '-echo'); 
        system(script3,'-echo'); 
        system(script4,'-echo'); 
    end       
end

end