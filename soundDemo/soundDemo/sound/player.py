'''
Created on May 13 2015

@author: Or Levi
'''
import interface
import pyaudio
import time
import numpy
import math
import threading


FS = 44100
CHUNK = 1024
FREQ_SHIFT = 1
MIN_VALUE_TO_ALLOW_CHANGE = 0.98
MAX_VOL_CHANGE = 0.001

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
        chunk = self.createWave()
        data = chunk.astype(numpy.float32).tostring()
        return (data, pyaudio.paContinue)

    def playWave(self):

        self.is_playing = True

        self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, frames_per_buffer = CHUNK)
        #self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, stream_callback = self.nextSegment, frames_per_buffer = CHUNK)
        #self.stream.start_stream()
        creator_t = threading.Thread(target=self.create_chunk)
        creator_t.start()
        t = threading.Thread(target=self.player_t)
        t.start()

    def player_t(self):
        while self.is_playing:
            if self.has_chunk:
                a = self.chunk
                self.has_chunk = False
                #print a
                self.stream.write(a)

    def create_chunk(self):
        while self.is_playing:
            if not self.has_chunk:
                chunk = self.createWave()
                self.chunk = chunk.astype(numpy.float32).tostring()
                self.has_chunk = True


    def stopWave(self):
        self.stream.stop_stream()
        self.stream.close()
        self.last_val = 0
        self.is_playing = False
    
    def close_nicely(self):
        if self.is_playing:
            self.stopWave()
        
 






    







    