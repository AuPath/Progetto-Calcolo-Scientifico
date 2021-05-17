function [] = analisi_matlab(matrix_dir, matlab_file, mem_file, result_file)

% SU WINDOWS OK, DA TESTARE SU LINUX

% per Windows: analisi_matlab('Testdeltest', '', '', '')
% per Linux: specificare tutti i parametri

% Come parametri si aspetta:
% path cartella matrici 
% file dove salvare i risultati dello script Matlab
% file dove salvare i risultati della memoria
% file dove salvare i risultati complessivi
% devono essere dati in questo ordine

matrices = dir(strcat(matrix_dir,'/*.mat'));
script2 = strcat("truncate --size=1 ", matlab_file); % elimino ultima newline inutile
script3 = strcat("paste -d ';' ", matlab_file, " ", mem_file, " > ", result_file); % merge dei due file
script4 = strcat("echo '' >> ", matlab_file); % aggiungo newline nel file prodotto dallo script Matlab

for i = 1:length(matrices)
    matrix_name = strcat(matrix_dir, "/", matrices(i).name);
    % Misurazione memoria
    if ispc % Windows
        matlab_test(matrix_name, strcat(extractBefore(matrix_name,'.mat'), "_results.txt"));
    elseif isunix % Linux (o Mac)
        script1 = strcat("/usr/bin/time -f '%M' matlab -W matlab-test(", matrix_name, ", ", matlab_file, ") &>> ", mem_file);
        system(script1,'-echo');
        system(script2, '-echo'); 
        system(script3,'-echo'); 
        system(script4,'-echo'); 
    end       
end

% Merge dei risultati in un unico file - in Linux già fatto
if ispc % Windows
    files=dir(strcat(matrix_dir, '/*.txt'));
    fileout='merged.txt';
    fout=fopen(fileout,'w');
    for cntfiles=1:length(files)
        fin=fopen(files(cntfiles).name);
        while ~feof(fin)
            fprintf(fout,strcat(extractBefore(files(cntfiles).name, '.txt'), ' %s %d\n'),fgetl(fin),cntfiles);
        end
        fclose(fin);
    end
end

end
