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
CHUNK = 2048

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
        frequency = self.interface.freq
        time_line = [t + self.last_val for t in range(CHUNK)]
        self.last_val = time_line[-1] + 1
        factor = float(frequency) * (math.pi) / FS
        for i in range(len(time_line)):
            time_line[i] = time_line[i] * factor
        return numpy.sin(time_line) * self.interface.vol
        
            
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
        
 






    







    