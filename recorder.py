import time
import math
import wave
import pyaudio
import scipy.io.wavfile
import sounddevice as sd

SAMPLERATE = 44100
CHANNELS = 1
sd.default.samplerate = SAMPLERATE
sd.default.channels = CHANNELS


class Recorder:
    MAX_DURATION = 30

    def __init__(self):
        self._start_time = None
        self._recording = None

    def start(self):
        self._start_time = time.time()
        self._recording = sd.rec(int(self.MAX_DURATION * sd.default.samplerate), dtype='int16')

    def stop(self, path='output.wav'):
        sd.stop()
        duration = int(math.ceil(time.time() - self._start_time))
        data = self._recording[:duration * sd.default.samplerate]
        # save audio
        audio = pyaudio.PyAudio()
        format = pyaudio.paInt16
        
        wavfile = wave.open(path, 'wb')
        wavfile.setnchannels(CHANNELS)
        wavfile.setsampwidth(audio.get_sample_size(format))
        wavfile.setframerate(SAMPLERATE)
        wavfile.writeframes(data.tostring())
        wavfile.close()