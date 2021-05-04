#!/bin/bash

### Come parametri si aspetta:
### path cartella matrici 
### file dove salvare i risultati dello script octave
### file dove salvare i risultati della memoria
### file dove salvare i risultati complessivi
### devono essere dati in questo ordine

matrix_dir="$1" # primo parametro passato, il path alla cartella che
                # contiene le matrici.

oct_file="$2"
mem_file="$3"
result_file="$4"

for matrix in "$matrix_dir"/*
do
    ## Misurazione memoria
    /usr/bin/time -f "%M" octave -W octave-test.m "$matrix" "$oct_file" &>> "$mem_file"
    ## aggiungo newline nel file prodotto dallo script octave
    echo "" >> "$oct_file"
done

truncate -s -1 "$oct_file" ## elimino ultima newline inutile
paste -d ";" "$oct_file" "$mem_file" > "$result_file" ## merge dei due file

