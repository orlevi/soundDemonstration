"""
parts of the code were taken from http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/

"""
__author__ = 'netanel'

import matplotlib.pyplot as plt
import numpy
import pyaudio
import threading
import time
import logging

################# Global Consts
BITRATE = 48100
PYAUDIO_FORMAT = pyaudio.paInt16
NUMPY_DATA_FORMAT = numpy.int16
PYAUDIO_BUFFER_SIZE = 4096
TIME_TO_RECORD = 0.1  # time to record before calculating fft


class Sampler(object):
    def __init__(self, microphone_sampling_time=10):
        self._microphone_sampling_time = microphone_sampling_time
        self._peakFFT = None
        self._stop_recording_thread = False  # flag to kill recorder and fft computer threads
        self._new_audio = False  # flag to inform about new audio data from recorder thread
        self._new_fft = False

        self._bitrate = BITRATE
        self._buffer_size = PYAUDIO_BUFFER_SIZE
        self._sec_to_record = TIME_TO_RECORD

        self._log_scale = False  # should FFT be represented in dB
        self._fft_data = None  # hold computed fft
        self._audio = None  # hold recorded audio

        self._time_sampling_start = None  # hold the time start_microphone_sampling() was called and started to sample microphone

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("finished init")

    def has_new_fft(self):
        return self._new_fft

    def get_fft_data(self):
        self._new_fft = False
        return self._fft_data

    def get_peak_fft(self):
        return self._peakFFT

    def start_microphone_sampling(self):
        # open microphone stream
        self._init_recorder()

        # open recorder thread
        recorder_thread = threading.Thread(target=self._record)
        recorder_thread.start()

        # open fft computer thread
        fft_thread = threading.Thread(target=self._fft_computer)
        fft_thread.start()

        self._time_sampling_start = time.clock()

        # update peakFFT ?

    def _init_recorder(self):
        """
        initialize all kind of buffers
        open stream to microphone
        :return:
        """
        self._buffers_to_record = max(1, int(self._bitrate * self._sec_to_record / self._buffer_size))
        self._samples_to_record = int(self._buffer_size * self._buffers_to_record)
        self._chunks_to_record = int(self._samples_to_record / self._buffer_size)
        self._sec_per_point = 1.0 / self._bitrate

        self._p = pyaudio.PyAudio()
        logging.debug("opening audio stream")

        self._inStream = self._p.open(format=PYAUDIO_FORMAT, channels=1, rate=self._bitrate, input=True, frames_per_buffer=self._buffer_size)
        self._xs_buffer = numpy.arange(self._buffer_size) * self._sec_per_point
        self._xs = numpy.arange(self._chunks_to_record * self._buffer_size) * self._sec_per_point
        self._audio = numpy.empty((self._chunks_to_record * self._buffer_size), dtype=NUMPY_DATA_FORMAT)

    def _record(self):
        """record secToRecord seconds of audio."""

        logging.debug("started recorder thread")

        while not self._stop_recording_thread:
            if not self._new_audio:
                for i in range(self._chunks_to_record):
                    self._audio[i * self._buffer_size: (i+1) * self._buffer_size] = self._get_audio()
                #logging.debug("read new audio data, {}".format(time.clock()))
                self._new_audio = True
                t = time.clock()
                if t - self._time_sampling_start > self._microphone_sampling_time:
                    self._stop_recording_thread = True
        logging.debug("ended recorder thread")

    def _get_audio(self):
        """get a single buffer size worth of audio."""
        audio_string = self._inStream.read(self._buffer_size)
        return numpy.fromstring(audio_string, dtype=NUMPY_DATA_FORMAT)

    def _fft_computer(self):
        """
        compute fft on self._audio
        store new fft in self._current_fft
        update self._new_fft
        :return:
        """
        logging.debug("started fft thread")
        while not self._stop_recording_thread:
            if self._new_audio:
                self._fft()
                self._new_audio = False
                #logging.debug("wrote new fft data")
        logging.debug("ended fft thread")

    def _fft(self, trimBy=10, logScale=True, divBy=100):
        '''
        data = self._audio
        #logging.debug("data length: {}".format(len(data)))
        ys = numpy.fft.fftshift(numpy.fft.fft(data))
        s = 2048
        ys = ys[s:]
        #logging.debug("f length: {}".format(len(ys)))
        xs = numpy.linspace(0, BITRATE/2, 2048)
        '''


        data = self._audio.flatten()
        left, right = numpy.split(numpy.abs(numpy.fft.fft(data)), 2)
        ys = numpy.add(left, right[::-1])
        if logScale:
            ys = numpy.multiply(20, numpy.log10(ys))
        xs = numpy.arange(self._buffer_size/2, dtype=float)
        if trimBy:
            i = int((self._buffer_size/2)/trimBy)
            ys = ys[:i]
            xs = xs[:i]*self._bitrate/self._buffer_size
        if divBy:
            ys = ys/float(divBy)
        self._fft_data = [xs, ys]
        self._new_fft = True

if __name__ == '__main__':
    plt.ion()
    fig, ax = plt.subplots()
    data, = ax.plot([], [])
    ax.set_autoscaley_on(True)
    ax.grid()
    ax.set_ylim([0.5, 2])
    ax.set_xlim([0, 2500])
    ax.set_title('momentary FFT')
    ax.set_xlabel('frequency [Khz]')
    ax.set_ylabel('power [Log]')


    # create Sampler object
    s = Sampler(microphone_sampling_time=6)

    # when wanted, call start_microphone_sampling()
    s.start_microphone_sampling()

    t0 = tc = time.clock()
    while tc - t0 < 10:
        tc = time.clock()
        if s.has_new_fft():  # check if new FFT data is ready
            try:
                x, y = s.get_fft_data()  # get new FFT data
                data.set_xdata(x)
                data.set_ydata(y)
                ax.relim()
                #ax.autoscale_view()
                fig.canvas.draw()
                fig.canvas.flush_events()
            except Exception:
                pass
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.05)



