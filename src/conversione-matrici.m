### in ingresso si aspetta:
### Path alla matrice da convertire
### Path al file dove salvare la matrice convertita (senza estensione .mat)

args = argv();
matrix_file = args{1};
converted_matrix_file = args{2};

load(matrix_file);

## Trasformo da vettori 0-based a 1-based
Problem.A.ir += 1;
Problem.A.jc += 1;

## Preallocation
i = ones(1, length(Problem.A.ir));
j = ones(1, length(Problem.A.ir));
v = ones(1, length(Problem.A.ir));

for k = 1:(length(Problem.A.jc) - 1)

  start = Problem.A.jc(k);
  stop = Problem.A.jc(k + 1) - 1;

  i(start:stop) = Problem.A.ir(start:stop);
  j(start:stop) = k * ones(1, stop - start + 1);
  v(start:stop) = Problem.A.data(start:stop);
end

A = sparse(i,j,v);
Problem.A = A;

filename=sprintf('%s.mat', converted_matrix_file);

save("-7", filename, "Problem"); ## matlab 7 binary format
