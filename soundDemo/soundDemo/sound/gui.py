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
Y_SCALE = 1
#events constants
LEFT = 1

class Plotter():
    
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.font = pygame.font.SysFont("monospace", 20)
        
    def draw(self, canvas, x_data, y_data):
        pygame.draw.rect(canvas, WHITE, (self.position[0],self.position[1],self.size[0],self.size[1]), 0)        
        pygame.draw.rect(canvas, BLACK, (self.position[0],self.position[1],self.size[0],self.size[1]), 1)
        x_scale = float(self.size[0]) / (len(x_data)+1)
        line = []
        real_x_pos = self.position[0]
        for y in y_data:
            real_x_pos = float(real_x_pos + x_scale)
            real_y_pos = self.position[1] + self.size[1] - y * Y_SCALE
            line.append((real_x_pos, real_y_pos))
        pygame.draw.lines(canvas, BLACK, 0, line)
        pygame.draw.line(canvas, BLACK, (self.position[0] + self.size[0]/4, self.position[1] + self.size[1]-1), (self.position[0] + self.size[0]/4,self.position[1] + 0.96*self.size[1]))   
        label1 = self.font.render(str(x_data[len(x_data)/4]), 1, BLACK)
        canvas.blit(label1, (self.position[0]+self.size[0]/4-label1.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
        pygame.draw.line(canvas, BLACK, (self.position[0] + self.size[0]/2, self.position[1] + self.size[1]-1), (self.position[0] + self.size[0]/2,self.position[1] + 0.96*self.size[1]))   
        label2 = self.font.render(str(x_data[len(x_data)/2]), 1, BLACK)  
        canvas.blit(label2, (self.position[0]+self.size[0]/2-label1.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
        pygame.draw.line(canvas, BLACK, (self.position[0] + 3*self.size[0]/4, self.position[1] + self.size[1]-1), (self.position[0] + 3*self.size[0]/4,self.position[1] + 0.96*self.size[1]))   
        label3 = self.font.render(str(x_data[3*len(x_data)/4]), 1, BLACK)  
        canvas.blit(label3, (self.position[0]+3*self.size[0]/4-label1.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))      
        pygame.draw.line(canvas, BLACK, (self.position[0] + self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 3*self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + 3*self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 5*self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + 5*self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        pygame.draw.line(canvas, BLACK, (self.position[0] + 7*self.size[0]/8, self.position[1] + self.size[1]-1), (self.position[0] + 7*self.size[0]/8,self.position[1] + 0.98*self.size[1]))   
        

class Button():
    
    def __init__(self, position, size, text, func = None, *args):
        self.position = position
        self.size = size
        self.text = text
        self.is_clicked = False
        self.func = func
        self.args = args
        self.font = pygame.font.SysFont("monospace", 20)
                
    def check_click(self, pos):
        if (pos[1] >= self.position[0]) and (pos[1] <= self.position[0]+self.size[0]) and (pos[0] >= self.position[1]) and (pos[0] <= self.position[1]+self.size[1]):
            self.is_clicked = True
            if self.func != None:
                self.func(self.args)
                
            
    def click_release(self):
        self.is_clicked = False
            
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
        
    
        

class gui():

    def __init__(self):
        '''
        Constructor
        '''
        pygame.init()                                           # initialize pygame
        self.fps_Clock = pygame.time.Clock()                    # set the FPS clock
        self.canvas = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        pygame.display.set_caption('Sound Demonstrations')
        self.done = False
        self.buttons = []
        
        self.buttons.append(Button((50,50),(50,100),"Play"))
        self.buttons.append(Button((110,50),(50,100),"+1Hz"))
        self.buttons.append(Button((170,50),(50,100),"+0.1Hz"))
        self.buttons.append(Button((230,50),(50,100),"-0.1Hz"))
        self.buttons.append(Button((290,50),(50,100),"-1Hz"))
        self.buttons.append(Button((350,50),(50,100),"FFT"))
        
        self.plotter = Plotter((175,50), (400,400))
        
        self.phase = 0 ####################################################################################
        self.x_line = range(1000)####################################################################################
        self.y_line = []####################################################################################
        for i in self.x_line:####################################################################################
            self.y_line.append(i/50.0)####################################################################################
      
        self.main_loop()                                        # start the main loop of the gui
        
    def draw(self):
        
        self.canvas.fill(GRAY)
        for button in self.buttons:
            button.draw(self.canvas)########################################################## 
        self.plotter.draw(self.canvas, self.x_line, self.y_line)
        
    def demo_sine(self):#########################################################################
        self.phase = self.phase + 0.05
        for i in range(len(self.x_line)):
            self.y_line[i] = 60*(numpy.sin(self.x_line[i]/50.0+self.phase) + 1)
        
    def main_loop(self):
        while not self.done:
            for event in pygame.event.get():
                # exit if ESC pressed or 'x' clicked. 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):     
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
            
            
            self.demo_sine()####################################################################
            
        pygame.quit
        

gui()        

                    
        
            