'''
Created on May 13 2015

@author: Or Levi
'''
#from reportlab.graphics.charts.piecharts import PL
import interface
import pyaudio
import time
import numpy
import math
import threading
import Queue


FS = 44100
CHUNK = 1024
FREQ_SHIFT = 1
MIN_VALUE_TO_ALLOW_CHANGE = 0.98
MAX_VOL_CHANGE = 0.001
SLEEP_TIME_BUFFER_UNDERRUN = 0.1
BUFFER_QUEUE_SIZE = 10

class Player():
    '''
    '''
    def __init__(self, interface):
        '''
        '''
        self.interface = interface       
        self.player = pyaudio.PyAudio()
        self.is_playing = False
        self.last_val = 0
        self.vol = self.interface.vol
        self.freq = self.interface.freq
        self.chunk = None
        self.need_chunk = True
        self.has_chunk = False
        self.chunk_queue = Queue.Queue(maxsize=BUFFER_QUEUE_SIZE)

    def createWave(self):
        t = self.last_val
        output_wave = []
        for i in range(CHUNK):
            t = t + 1
            
            if (math.fabs(self.freq - self.interface.freq) >= 0.1) and (math.fabs(math.sin(2 * math.pi * self.freq * t / FS)) > MIN_VALUE_TO_ALLOW_CHANGE) :
                print "freq change , self- " + str(self.freq) + " , interface- " + str(self.interface.freq)
                t = int(t * self.freq / self.interface.freq)
                self.freq = self.interface.freq
              
            if (self.vol != self.interface.vol):
                if (self.interface.vol - self.vol) > MAX_VOL_CHANGE:
                    self.vol = self.vol + MAX_VOL_CHANGE
                elif (self.interface.vol - self.vol) < -MAX_VOL_CHANGE:
                    self.vol = self.vol - MAX_VOL_CHANGE
                else:
                    self.vol = self.interface.vol
            
            audio_sine = self.vol * math.sin(2 * math.pi * self.freq * t / FS)
            strobe_sine = 0.0 * math.sin(2 * math.pi * (self.freq + FREQ_SHIFT) * t / FS)
            output_wave.append([audio_sine, strobe_sine])
        
        self.last_val = t
        
        return numpy.array(output_wave)
        
            
    def nextSegment(self, in_data, frame_count, time_info, status):
        if status:
            print ('playback error %s' % status)
        chunk = self.createWave()
        data = chunk.astype(numpy.float32).tostring()
        return (data, pyaudio.paContinue)

    def playWave(self):

        self.is_playing = True

        self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, frames_per_buffer = CHUNK)
        #self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, stream_callback = self.nextSegment, frames_per_buffer = CHUNK)
        #self.stream.start_stream()
        self.creator_t = threading.Thread(target=self.create_chunk)
        self.creator_t.start()
        self.player_t = threading.Thread(target=self.play_chunk)
        self.player_t.start()

    def play_chunk(self):
        while self.is_playing:
            if self.chunk_queue.qsize() > 0:
                a = self.chunk_queue.get_nowait()
                self.stream.write(a)
            else:
                time.sleep(SLEEP_TIME_BUFFER_UNDERRUN)

    def create_chunk(self):
        while self.is_playing:
            if self.chunk_queue.qsize() < BUFFER_QUEUE_SIZE:
                chunk = self.createWave()
                chunk = chunk.astype(numpy.float32).tostring()
                self.chunk_queue.put_nowait(chunk)


    def stopWave(self):
        self.is_playing = False
        time.sleep(0.1)
        self.stream.stop_stream()
        self.stream.close()
        self.last_val = 0
    
    def close_nicely(self):
        if self.is_playing:
            self.stopWave()
        
 
if __name__ == '__main__':

    import sampler
    i = interface.Interface(frequency=760)
    s = sampler.Sampler()
    p = Player(interface=i)
    p.playWave()
    s.start_microphone_sampling()
    test_time = 60
    t0 = tc = time.clock()

    while tc - t0 < test_time:
        a = s.get_peak_fft()
        s.get_fft_data()
        tc= time.clock()

        time.sleep(1/60)

    p.close_nicely()
    s.close_pyaudio_nicely()
    time.sleep(1)




    







    