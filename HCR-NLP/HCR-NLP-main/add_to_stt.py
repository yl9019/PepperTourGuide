import pyaudio
import time, os, sys, contextlib

device_substring = "Microphone (USB Audio Device)"
#----------------PUT THIS BIT IN THE SETUP--------------------
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
device_id = []

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        #print(p.get_device_info_by_host_api_device_index(0, i).get('name'))

        #print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        if(device_substring in p.get_device_info_by_host_api_device_index(0, i).get('name')):
            device_id = i#names = names.append(p.get_device_info_by_host_api_device_index(0, i).get('name'))


if(device_id == []):
    print("DEVICE NOT FOUND - TRY DISCONNECTING AND RECONNECTING")
    assert(1 == 0)
#----------------END PUT THIS BIT IN THE SETUP--------------------

#print("DEVICE NAME: " +  p.get_device_info_by_host_api_device_index(0, device_id).get('name'))
#print("DEVICE ID: " + str(device_id))



