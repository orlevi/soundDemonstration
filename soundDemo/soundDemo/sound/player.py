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
MIN_VALUE_TO_ALLOW_CHANGE = 0.98
MAX_VOL_CHANGE = 0.001

class Player(object):
    '''
    '''
    def __init__(self, interface, pa):
        '''
        '''
        self.interface = interface       
        self.player = pa
        self.is_playing = False
        self.last_val = 0
        self.vol = self.interface.vol
        self.freq = self.interface.freq
        
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
        '''
        freq = self.interface.freq
        time_line = [t +self.last_val for t in xrange(CHUNK)]
        self.last_val = time_line[-1] + 1
        output_wave = []
        for t in time_line:
            audio_sine = self.interface.vol * math.sin(2 * math.pi * freq * t / FS)
            strobe_sine = 0.0 * math.sin(2 * math.pi * (freq + FREQ_SHIFT) * t / FS)
            output_wave.append([audio_sine, strobe_sine])
        '''
        return numpy.array(output_wave)
        
            
    def nextSegment(self, in_data, frame_count, time_info, status):
        if status:
            print ('playback error %s' % status)
        chunk = self.createWave()
        data = chunk.astype(numpy.float32).tostring()
        return (data, pyaudio.paContinue)

    def playWave(self):
        self.is_playing = True
        self.stream = self.player.open(format = pyaudio.paFloat32, channels = 2, rate = FS, output = True, stream_callback = self.nextSegment, frames_per_buffer=CHUNK)
        self.stream.start_stream()
             
    def stopWave(self):
        self.stream.stop_stream()
        self.stream.close()
        self.last_val = 0
        self.is_playing = False
    
    def close_nicely(self):
        if self.is_playing:
            self.stopWave()
        
 
if __name__ == '__main__':

    import sampler
    import random
    pa = pyaudio.PyAudio()
    i = interface.Interface(frequency=760)
    s = sampler.Sampler(pa=pa)
    time.sleep(1)
    p = Player(interface=i, pa=pa)
    p.playWave()
    s.start_microphone_sampling()
    test_time = 60*30
    t0 = tc = tf = tv = time.clock()

    while tc - t0 < test_time:
        a = s.get_peak_fft()
        s.get_fft_data()
        if tc - tf > 15:
            s.reset_max_fft()
            print 'peak freq {}'.format(a)
            new_freq = random.randint(300, 800)
            print 'setting freq {}'.format(new_freq)
            i.setFreq(freq=new_freq)
            tf = time.clock()

        if tc - tv > 3:
            new_vol = random.random()
            print 'setting vol {}'.format(new_vol)
            i.setVol(new_vol)
            tv = time.clock()

        time.sleep(1/60)
        tc = time.clock()

    p.close_nicely()
    s.close_pyaudio_nicely()
    time.sleep(1)
