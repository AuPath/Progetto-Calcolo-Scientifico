#!/bin/bash

matrix_dir="$1" ## primo parametro passato, il path alla cartella che
                ## contiene le matrici.

for matrix in "$matrix_dir"/*
do
    /usr/bin/time -f "%M" octave octave-test.m "$matrix" &>> mem.txt
    echo "" >> prova.txt
done

truncate -s -1 prova.txt ## elimino ultima newline inutile
paste -d ";" prova.txt mem.txt > risultati.txt ## merge dei due file

