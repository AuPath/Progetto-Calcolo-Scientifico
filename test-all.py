import argparse
import os
from os.path import isfile, join
import subprocess

parser = argparse.ArgumentParser(description='Matrix calculation analysis.')

parser.add_argument("--input", help="Input directory", required=True)
parser.add_argument("--output", help="Output directory", required=True)
parser.add_argument("--runs", help="Number of runs", required=True)
parser.add_argument("--os", help="Operating system of host machine", required=True)

# Get arguments
args = parser.parse_args()
input_dir = args.input
output_dir = args.output
n_runs = int(args.runs)
os_name = args.os

# Script execution
SCRIPT_DIRECTORY = ''
OCTAVE_SCRIPT_NAME = 'octave-test'
MATLAB_SCRIPT_NAME = 'matlab_test'
PYTHON_SCRIPT_NAME = 'python-test'

COMMAND_PREFIX = '/usr/bin/time -v'
#COMMAND_PREFIX = 'gtime -v'

SCRIPT_COMMAND = {
    'octave': f'{COMMAND_PREFIX} octave -W {join(SCRIPT_DIRECTORY, OCTAVE_SCRIPT_NAME)}.m ' +
              '{} {}',
    'python': f'{COMMAND_PREFIX} python {join(SCRIPT_DIRECTORY, PYTHON_SCRIPT_NAME)}.py ' +
              '{} {}',
    'matlab': f'{COMMAND_PREFIX} matlab -nosplash -nodesktop -wait -r ' +
              f'"{join(SCRIPT_DIRECTORY, MATLAB_SCRIPT_NAME)}' +
              "('{}', '{}')" + ';exit;"'
}

# List of matrices
matrices_name = [f for f in os.listdir(input_dir) if isfile(join(input_dir, f))]

for idx_matrix, matrix_name in enumerate(matrices_name, 1):
    for idx_type, (script_type, command) in enumerate(SCRIPT_COMMAND.items(), 1):
        for i_run in range(1, n_runs + 1):
            # Compose the name of the output file
            matrix_label = matrix_name.split('.')[0]
            filename = f'{os_name}-{matrix_label}-{script_type}-{i_run}.txt'
            # Execute script
            print(f'MATRIX: {matrix_label} - {idx_matrix} / {len(matrices_name)}\n'
                  f'\tSCRIPT: {script_type} - {idx_type} / {len(SCRIPT_COMMAND)}\n'
                  f'\t\tRUN ITER: {i_run} / {n_runs}\n')
            target_command = command.format(join(input_dir, matrix_name), join(output_dir, filename))
            process = subprocess.Popen(target_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # Memory usage output
            _, output = process.communicate()
            output = output.decode().split('\n')
            memory_peak = output[9].split(':')[-1].strip()
            memory_avg = output[10].split(':')[-1].strip()
            # Append memory info
            with open(join(output_dir, filename), "a") as file:
                file.write(f";{memory_peak};{memory_avg}")

