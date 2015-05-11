"""
parts of the code were taken from http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/

"""
__author__ = 'netanel'

import matplotlib
matplotlib.use('TkAgg')  # <-- THIS MAKES IT FAST!
import numpy
import scipy
import struct
import pyaudio
import threading
import pylab
import struct
import time
import logging


class Sampler(object):
    def __init__(self, microphone_sampling_time=10):
        self._microphone_sampling_time = microphone_sampling_time
        self._peakFFT = None

        self._bitrate = 48100
        self._buffer_size = 1024  # pyAudio buffer size
        self._sec_to_record = 0.1
        self._stop_recording_thread = False
        self._new_audio = False

        self._logger = logging.getLogger('sampler_logger')

    def get_peak_fft(self):
        return self._peakFFT

    def start_microphone_sampling(self):
        # open microphone stream
        self._init_recorder()
        # start computing fft and store current fft in a member

        # update peakFFT ?

    def _init_recorder(self):
        self._buffers_to_record = max(1, int(self._bitrate * self._sec_to_record / self._buffer_size))
        self._samples_to_record = int(self._buffer_size * self._buffers_to_record)
        self._chunks_to_record = int(self._samples_to_record / self._buffer_size)
        self._sec_per_point = 1.0 / self._bitrate

        self._p = pyaudio.PyAudio()
        self._logger.debug("opening audio stream")
        self._inStream = self._p.open(format=pyaudio.paInt16, channels=1, rate=self._bitrate, input=True, frames_per_buffer=self._buffer_size)


if __name__ == '__main__':
    s = Sampler(microphone_sampling_time=4)
    s.start_microphone_sampling()