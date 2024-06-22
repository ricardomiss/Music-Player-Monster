from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def get_audio_endpoint_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def get_volume():
    volume = get_audio_endpoint_volume()
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def set_volume(volume):
    endpoint_volume = get_audio_endpoint_volume()
    endpoint_volume.SetMasterVolumeLevelScalar(volume / 100.0, None)
