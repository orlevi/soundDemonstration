'''
Created on May 11 2015

@author: Or Levi
'''
import pygame
from pygame.locals import *
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.backends.backend_agg as agg
import pylab
import numpy


#canvas size constants
WIDTH = 600
HEIGHT = 600
#drawing constants
OFFSET = 2
GRAY = (192,192,192)
LIGHT_GRAY = (224,224,224)
DARK_GRAY = (128,128,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
Y_SCALE = 2
#events constants
LEFT = 1

class Plotter():
    
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.font = pygame.font.SysFont("monospace", 10)
        
    def draw(self, canvas, freq, x_data, y_data_1, y_data_2 = []):
        self.draw_frame(canvas)
        self.draw_graphs(canvas, x_data, y_data_1, y_data_2)
        self.draw_labels(canvas, x_data)
        self.draw_ticks(canvas)
        self.draw_freq_marker(canvas, freq, x_data)
    
    def draw_freq_marker(self, canvas, freq, x_data):
        if x_data != []:
            x_pos = (float(freq - x_data[0]) / (x_data[-1] - x_data[0])) * self.size[0]
            pygame.draw.line(canvas, RED, (self.position[0] + x_pos, self.position[1] + self.size[1]-1), (self.position[0] + x_pos, self.position[1]), 3)   

    
    def draw_frame(self, canvas):
        pygame.draw.rect(canvas, WHITE, (self.position[0],self.position[1],self.size[0],self.size[1]), 0)        
        pygame.draw.rect(canvas, BLACK, (self.position[0],self.position[1],self.size[0],self.size[1]), 1)
     
    def draw_graphs(self, canvas, x_data, y_data_1, y_data_2): 
        if y_data_1 != []:
            graph_1 = self.create_graph_vector(x_data, y_data_1)
            pygame.draw.lines(canvas, BLUE, 0, graph_1)
        if y_data_2 != []:
            graph_2 = self.create_graph_vector(x_data, y_data_2)
            pygame.draw.lines(canvas, BLACK, 0, graph_2)
             
    def draw_labels(self, canvas, x_data):
        if x_data != []:
            label0 = self.font.render(str(x_data[0]), 1, BLACK)
            canvas.blit(label0, (self.position[0]-label0.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label1 = self.font.render(str(x_data[len(x_data)/4]), 1, BLACK)
            canvas.blit(label1, (self.position[0]+self.size[0]/4-label1.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label2 = self.font.render(str(x_data[len(x_data)/2]), 1, BLACK)  
            canvas.blit(label2, (self.position[0]+self.size[0]/2-label2.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label3 = self.font.render(str(x_data[3*len(x_data)/4]), 1, BLACK)  
            canvas.blit(label3, (self.position[0]+3*self.size[0]/4-label3.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label4 = self.font.render(str(x_data[len(x_data)-1]), 1, BLACK)  
            canvas.blit(label4, (self.position[0]+self.size[0]-label4.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))      
        
    def draw_ticks(self, canvas):
        pygame.draw.line(canvas, BLACK, (self.position[0] + self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + self.size[0]/4, self.position[1] + self.size[1]-1), (self.position[0] + self.size[0]/4,self.position[1] + 0.96*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 3*self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + 3*self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + self.size[0]/2, self.position[1] + self.size[1]-1), (self.position[0] + self.size[0]/2,self.position[1] + 0.96*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 5*self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + 5*self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 3*self.size[0]/4, self.position[1] + self.size[1]-1), (self.position[0] + 3*self.size[0]/4,self.position[1] + 0.96*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 7*self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + 7*self.size[0]/8,self.position[1] + 0.98*self.size[1]))    
      
    def create_graph_vector(self, x_data, y_data):
        x_scale = float(self.size[0]) / (len(x_data)+1)
        line = []
        real_x_pos = self.position[0]
        for y in y_data:
            real_x_pos = float(real_x_pos + x_scale)
            y_shift = y * Y_SCALE    
            if y_shift <= 0:      
                y_shift = 1     
            elif y_shift > self.size[1]:
                y_shift = self.size[1]
            real_y_pos = self.position[1] + self.size[1] - y_shift
            line.append((real_x_pos, real_y_pos))
        return line


class Button():
    
    def __init__(self, position, size, text, press_func = None, release_func = None):
        self.position = position
        self.size = size
        self.text = text
        self.is_clicked = False
        self.press_func = press_func
        self.release_func = release_func
        self.font = pygame.font.SysFont("monospace", 18)
                
    def check_click(self, pos):
        if (pos[1] >= self.position[0]) and (pos[1] <= self.position[0]+self.size[0]) and (pos[0] >= self.position[1]) and (pos[0] <= self.position[1]+self.size[1]):
            self.is_clicked = True
            if self.press_func != None:
                self.press_func()
                
            
    def click_release(self):
        if self.is_clicked:
            self.is_clicked = False
            if self.release_func != None:
                self.release_func()
            
    def draw(self, canvas):
        if self.is_clicked:
            color1 = DARK_GRAY
            color2 = LIGHT_GRAY
        else:
            color1 = LIGHT_GRAY
            color2 = DARK_GRAY              
        pygame.draw.polygon(canvas, color1, [(self.position[1]-OFFSET, self.position[0]-OFFSET), (self.position[1]+self.size[1]+OFFSET-1, self.position[0]-OFFSET), (self.position[1]-OFFSET,self.position[0]+self.size[0]+OFFSET-1)], 0)
        pygame.draw.polygon(canvas, color2, [(self.position[1]+self.size[1]+OFFSET-1, self.position[0]-OFFSET), (self.position[1]+self.size[1]+OFFSET-1, self.position[0]+self.size[0]+OFFSET-1), (self.position[1]-OFFSET,self.position[0]+self.size[0]+OFFSET-1)], 0)
        pygame.draw.rect(canvas, GRAY, (self.position[1],self.position[0],self.size[1],self.size[0]), 0)
        label = self.font.render(self.text, 1, BLACK)
        canvas.blit(label, (self.position[1]+(self.size[1]-label.get_width())/2,self.position[0]+(self.size[0]-self.font.get_height())/2))
        
    
        

class Gui():

    def __init__(self, interface, sampler, player):
        '''
        Constructor
        '''
        pygame.init()                                           # initialize pygame
        self.fps_Clock = pygame.time.Clock()                    # set the FPS clock
        self.canvas = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        pygame.display.set_caption('Sound Demonstrations')
        icon = pygame.transform.scale(pygame.image.load('glass.png'), (32, 32))
        pygame.display.set_icon(icon)
        self.done = False
        self.font = pygame.font.SysFont("monospace", 30)

        self.interface = interface
        self.sampler = sampler
        self.player = player
        
        self.buttons = []
        self.buttons.append(Button((50,50),(50,100),"Play", self.player.playWave))
        #self.buttons.append(Button((50,50),(50,100),"Play", self.player.playWave, self.player.stopWave))
        self.buttons.append(Button((110,50),(50,100),"+1Hz", self.interface.increaseFreq))
        self.buttons.append(Button((170,50),(50,100),"+0.1Hz", self.interface.increaseFreqFine))
        self.buttons.append(Button((230,50),(50,100),"-0.1Hz", self.interface.decreaseFreqFine))
        self.buttons.append(Button((290,50),(50,100),"-1Hz", self.interface.decreaseFreq))
        self.buttons.append(Button((350,50),(50,100),"FFT", self.sampler.start_microphone_sampling))
        self.buttons.append(Button((410,50),(50,100),"RESET MAX", self.sampler.reset_max_fft))

        self.plotter = Plotter((175,50), (400,400))
        
        self.x_line = []
        self.y_line = []
      
        self.main_loop()                                        # start the main loop of the gui
    
    def draw(self):
        if self.sampler.has_new_fft():
            self.x_line, self.y_line = self.sampler.get_fft_data()
        self.canvas.fill(GRAY)
        for button in self.buttons:
            button.draw(self.canvas) 
        self.plotter.draw(self.canvas, self.interface.freq, self.x_line, self.y_line)
        label = self.font.render("Current Freq  - "+str(self.interface.freq), 1, BLACK)
        self.canvas.blit(label, (50,500))
        label = self.font.render("Peak FFT Freq - "+str(self.sampler.get_peak_fft()[0]), 1, BLACK)
        self.canvas.blit(label, (50,550))

        
    def main_loop(self):
        while not self.done:
            for event in pygame.event.get():
                # exit if ESC pressed or 'x' clicked. 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):     
                    self.sampler.close_pyaudio_nicely()
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    for button in self.buttons:
                        button.check_click(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                    for button in self.buttons:
                        button.click_release()
                                   
            self.draw()         
            pygame.display.update()
            self.fps_Clock.tick(60)
            
            
            #self.demo_sine()####################################################################
            
        pygame.quit
        

#gui()        

                    
        
            