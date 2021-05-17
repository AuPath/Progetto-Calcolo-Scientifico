import argparse
import os
from os.path import isfile, join
import subprocess
import psutil
import time
import numpy as np
from threading import Thread

# Script execution
SCRIPT_DIRECTORY = 'src'
OCTAVE_SCRIPT_NAME = 'octave_solver'
MATLAB_SCRIPT_NAME = 'matlab_solver'
PYTHON_SCRIPT_NAME = 'python_solver'

# Sampling rate
SAMPLING_RATE = 0.1

# Script command
PREFIX_COMMAND = []

if os.name == 'posix': # MacOS
    MATLAB_PATH = "/Applications/Matlab\ R2020b.app/bin/matlab"
else:
    MATLAB_PATH = 'matlab'

SCRIPT_COMMAND = {
    'octave': f'octave -W {join(SCRIPT_DIRECTORY, OCTAVE_SCRIPT_NAME)}.m ' + '{} {}',
    'python': f'python {join(SCRIPT_DIRECTORY, PYTHON_SCRIPT_NAME)}.py ' + '{} {}',
    'matlab': f'{MATLAB_PATH} -batch ' +
              '"addpath(\''+SCRIPT_DIRECTORY+f'\');{MATLAB_SCRIPT_NAME}'
              + "('{}', '{}')" + ';exit;"'
}


def parse_arguments():
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

    return input_dir, output_dir, n_runs, os_name


def call_script(command):
    time.sleep(SAMPLING_RATE * 5)
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.wait()


def wrapper(command, sampling=True):
    samples = []
    thread_wrapper = Thread(target=call_script, args=(command,))
    thread_wrapper.start()

    while thread_wrapper.is_alive():
        time.sleep(SAMPLING_RATE)
        if sampling:
            samples.append(psutil.virtual_memory()[3])

    return samples


def log_error(filename):
    print(f"\n>>> ------- {filename} FAILED! -------\n")
    # Tracks failed tests
    with open(join(output_dir, '.errors.log'), "a") as file:
        file.write(f"{filename}\n")


def test_all(matrices_name):
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

                # Skip sampling and memory analysis for matlab
                if script_type == 'matlab':
                    wrapper(target_command, sampling=False)
                    try:
                        # Sanity check
                        with open(join(output_dir, filename), "r") as file:
                            assert len(file.readline().split(';')) == 6
                    except (AssertionError, FileNotFoundError):
                        log_error(filename)

                    continue

                samples = wrapper(target_command)
                samples = np.array(samples)
                samples_normalized = samples - min(samples)
                memory_peak = max(samples_normalized)
                memory_avg = np.average(samples_normalized)
                n_samples = len(samples)
                del samples

                try:
                    # Sanity check
                    with open(join(output_dir, filename), "r") as file:
                        assert len(file.readline().split(';')) == 4
                    # Append memory info
                    with open(join(output_dir, filename), "a") as file:
                        file.write(f";{memory_peak};{memory_avg}")
                except (AssertionError, FileNotFoundError):
                    log_error(filename)


if __name__ == '__main__':
    input_dir, output_dir, n_runs, os_name = parse_arguments()

    matrices_list = [f for f in os.listdir(input_dir)
                     if isfile(join(input_dir, f)) and f[0] != '.']

    test_all(matrices_list)
