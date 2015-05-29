'''
Created on May 13 2015

@author: Or Levi
'''
import interface
import pyaudio
import time
import numpy
import math


FS = 44100
CHUNK = 1024
FREQ_SHIFT = 1
MAX_VALUE_TO_ALLOW_CHANGE = 0.025
MAX_VOL_CHANGE = 0.01

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
        
    def createWave(self):
        time_line = [t + self.last_val for t in range(CHUNK)]
        self.last_val = time_line[-1] + 1
        output_wave = []
        for t in time_line:
            if (self.vol != self.interface.vol) and (math.fabs(math.sin(2 * math.pi * self.freq * t / FS)) < MAX_VALUE_TO_ALLOW_CHANGE):
                if (self.interface.vol - self.vol) > MAX_VOL_CHANGE:
                    self.vol = self.vol + MAX_VOL_CHANGE
                elif (self.interface.vol - self.vol) < -MAX_VOL_CHANGE:
                    self.vol = self.vol - MAX_VOL_CHANGE
                else:
                    self.vol = self.interface.vol
            if (self.freq != self.interface.freq) and (math.fabs(math.sin(2 * math.pi * self.freq * t / FS)) < MAX_VALUE_TO_ALLOW_CHANGE) and (math.fabs(math.sin(2 * math.pi * self.interface.freq * t / FS)) < MAX_VALUE_TO_ALLOW_CHANGE):
                self.freq = self.interface.freq
            audio_sine = self.vol * math.sin(2 * math.pi * self.freq * t / FS)
            strobe_sine = 0.5 * math.sin(2 * math.pi * (self.freq + FREQ_SHIFT) * t / FS)
            output_wave.append([audio_sine, strobe_sine])
        
        return numpy.array(output_wave)
        
            
    def nextSegment(self, in_data, frame_count, time_info, status):
        chunk = self.createWave()
        data = chunk.astype(numpy.float32).tostring()
        return (data, pyaudio.paContinue)

    def playWave(self):
        self.is_playing = True
        self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, stream_callback = self.nextSegment)
        self.stream.start_stream()
             
    def stopWave(self):
        self.stream.stop_stream()
        self.stream.close()
        self.last_val = 0
        self.is_playing = False
    
    def close_nicely(self):
        if self.is_playing:
            self.stopWave()
        
 






    







    