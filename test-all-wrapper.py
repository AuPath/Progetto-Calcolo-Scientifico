import argparse
import os
from os.path import isfile, join
import subprocess
import psutil
import time
import numpy as np
from threading import Thread
from sys import platform

# Script execution
SCRIPT_DIRECTORY = 'src'
OCTAVE_SCRIPT_NAME = 'octave_solver'
MATLAB_SCRIPT_NAME = 'matlab_solver'
PYTHON_SCRIPT_NAME = 'python_solver'

# Sampling rate
SAMPLING_RATE = 0.1

# Execution time limit (in minutes)
MINUTES_TIME_LIMIT = 30

# Check the number of columns
COLUMNS_NUMBER_CHECK = 6


SCRIPT_COMMAND = {
    'python': f'python {join(SCRIPT_DIRECTORY, PYTHON_SCRIPT_NAME)}.py ' + '{} {}',
    'matlab': f'matlab -batch ' +
              '"addpath(\''+SCRIPT_DIRECTORY+f'\');{MATLAB_SCRIPT_NAME}'
              + "('{}', '{}')" + ';exit;"',
    'octave': f'octave -W {join(SCRIPT_DIRECTORY, OCTAVE_SCRIPT_NAME)}.m ' + '{} {}',
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


class ScriptThread(Thread):

    def __init__(self, command):
        Thread.__init__(self)
        self.command = command
        self.finished = True
        self.process = None

    def run(self):
        if os.name == 'nt':
            # Windows
            self.process = subprocess.Popen(self.command, shell=True,
                                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            # Linux / MacOS
            self.process = subprocess.Popen(self.command, shell=True,
                                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        try:
            self.process.wait(timeout=MINUTES_TIME_LIMIT * 60)
        except subprocess.TimeoutExpired:
            self.finished = False
        finally:
            self.kill_subprocess()

    def kill_subprocess(self):
        if os.name == 'nt':
            # Windows
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            # Windows
            subprocess.call(['kill', '-9', str(self.process.pid)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        self.process.kill()
        self.process.terminate()

    def hasFinished(self):
        return self.finished


def wrapper(command, sampling=True):
    samples = []

    thread_wrapper = ScriptThread(command)
    thread_wrapper.setDaemon(True)
    thread_wrapper.start()

    while thread_wrapper.is_alive():
        time.sleep(SAMPLING_RATE)
        if sampling:
            samples.append(psutil.virtual_memory()[3])

    thread_wrapper.join()
    has_finished = thread_wrapper.hasFinished()

    if has_finished:
        return samples, True
    else:
        return samples, False


def log_error(filename, exception_type):
    print(f"\t\t\t>>> {filename} FAILED!")
    # Tracks failed tests
    with open(join(output_dir, '.errors.log'), "a") as file:
        file.write(f"{filename};{exception_type}\n")


def sanity_check(outpt_dir, filename, columns_number):
    # Sanity check
    with open(join(outpt_dir, filename), "r") as file:
        assert len(file.readline().split(';')) == columns_number


def test_all(matrices_name):
    for idx_matrix, matrix_name in enumerate(matrices_name, 1):
        for idx_type, (script_type, command) in enumerate(SCRIPT_COMMAND.items(), 1):
            for i_run in range(1, n_runs + 1):
                # Compose the name of the output file
                matrix_label = matrix_name.split('.')[0]
                filename = f'{os_name}-{matrix_label}-{script_type}-{i_run}.txt'
                # Execute script
                print(f'\nMATRIX: {matrix_label} - {idx_matrix} / {len(matrices_name)}\n'
                      f'\tSCRIPT: {script_type} - {idx_type} / {len(SCRIPT_COMMAND)}\n'
                      f'\t\tRUN ITER: {i_run} / {n_runs}')
                target_command = command.format(join(input_dir, matrix_name), join(output_dir, filename))

                #sampling = False if script_type == 'matlab' else True
                sampling = True

                samples, finished = wrapper(target_command, sampling=sampling)

                if finished:
                    # The script has finished its execution

                    try:
                        if sampling:
                            samples = np.array(samples)
                            samples_normalized = samples - min(samples)
                            memory_peak = max(samples_normalized)
                            memory_avg = np.average(samples_normalized)
                            del samples

                            # Append memory info
                            with open(join(output_dir, filename), "a") as file:
                                file.write(f";{memory_peak};{memory_avg}")

                        # Sanity check
                        sanity_check(output_dir, filename, COLUMNS_NUMBER_CHECK)
                    except (AssertionError, FileNotFoundError):
                        log_error(filename, 'format_exception')
                else:
                    print(f'\t\t\t>>> {filename} HAS NOT FINISHED THE EXECUTION')
                    log_error(filename, 'time_exception')
                    try:
                        # Garbage info
                        with open(join(output_dir, filename), "w+") as file:
                            file.write(f"{-1};" * 5 + f'{-1}')
                        # Sanity check
                        sanity_check(output_dir, filename, COLUMNS_NUMBER_CHECK)
                    except (AssertionError, FileNotFoundError):
                        log_error(filename, 'format_exception')
                    # Skip the remaining iterations
                    break


if __name__ == '__main__':
    input_dir, output_dir, n_runs, os_name = parse_arguments()

    matrices_list = [f for f in os.listdir(input_dir)
                     if isfile(join(input_dir, f)) and f[0] != '.']

    print("----- Start tests -----")
    test_all(matrices_list)
