import subprocess
import psutil
import time
from threading import Thread

SAMPLING_RATE = 0.1

script_name = 'stress.py'


def call_script():
    process = subprocess.Popen(['python', script_name])
    process.wait()


def wrapper():
    samples = []
    thread_wrapper = Thread(target=call_script)
    thread_wrapper.start()

    while thread_wrapper.is_alive():
        time.sleep(SAMPLING_RATE)
        samples.append(psutil.virtual_memory())

    for i, sample in enumerate(samples, 1):
        print(f"Sample {i}: {sample}")
    print(f'#Samples: {len(samples)}')


wrapper()
