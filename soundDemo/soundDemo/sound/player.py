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

class Player():
    '''
    '''
    def __init__(self, interface):
        '''
        '''
        self.interface = interface       
        self.player = pyaudio.PyAudio()
        self.last_val = 0
        
    def createWave(self):
        freq = self.interface.freq
        time_line = [t + self.last_val for t in range(CHUNK)]
        self.last_val = time_line[-1] + 1
        output_wave = []
        for t in time_line:
            audio_sine = self.interface.vol  * math.sin(2 * math.pi * freq * t / FS)
            strobe_sine = self.interface.vol * math.sin(2 * math.pi * (freq + FREQ_SHIFT) * t / FS)
            output_wave.append([audio_sine, strobe_sine])
            #output_wave.append(strobe_sine)
        
        return numpy.array(output_wave)
        
            
    def nextSegment(self, in_data, frame_count, time_info, status):
        chunk = self.createWave()
        data = chunk.astype(numpy.float32).tostring()
        return (data, pyaudio.paContinue)

    def playWave(self):
        self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, stream_callback = self.nextSegment)
        self.stream.start_stream()
       
        
    def stopWave(self):
        self.stream.stop_stream()
        self.stream.close()
        self.last_val = 0
        
 






    







    