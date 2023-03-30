import pyaudio
import time, os, sys, contextlib



@contextlib.contextmanager
def ignore_stdout():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stdout = os.dup(1)
    sys.stdout.flush()
    os.dup2(devnull, 1)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stdout, 1)
        os.close(old_stdout)

ignore_stdout()

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
