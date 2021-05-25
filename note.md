# Cose utili da inserire nella slide

## Cose utili da aggiungere per gli script slide
- Numero di elementi diversi da zero nella matrice oltre che la dimenisone della matrice  


## Cose utili da aggiungere nelle slide
- Come vengono caricate le matrici? 
    - Matrici sparse vengono tenute spare?
        - In python mi sembra di si
    

## Domande generali
- Nel file `octave-test.m` la soluzione esatta viene settata come il vettore di tutti 1. Il file matlab che viene importato è una struct contenente tante variabili oltre che l'effettiva matrice, tra cui la soluzione esatta del sistema. Perché non viene usata quella variabile come soluzione esatta del sistema anziché il valore di tutti 1? 
## Python: scipy + numpy + sksparse
- Le matrici sono in formato `.mat` ma con la libreria scipy è facile leggere le matrici, quindi esiste una compatibilità con questi tipi di file.
- Workflow:
  1. Prova cholesky
        1. Se funziona finisce
    2. Se fallise usa LU
        1. Usa risultato LU
- `spsolve(A, b, use_umfpack=False)` il parametro `use_umfpack=Flase` serve per usare la fattorizzazione LU per risolvere il sistema
- Per la matrice Hookk, la libreria che usa cholesy fallisce generando l'eccezione `sksparse.cholmod.CholmodTooLargeError`. Interessante notare come questo succede solo su windows ma non su linux.

## Picco di matlab
`src/matlab_solver`

Picco guardando il massimo

## Todo
Tutte le matrici tranne: bundle_adj; Hook; ifiss