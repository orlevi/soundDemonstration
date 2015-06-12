'''
Created on May 11 2015

@author: Or Levi
'''
import pygame
import config as config
from pygame.locals import *


#canvas size constants
WIDTH = 600
HEIGHT = 600

#drawing constants
OFFSET = 1
GRAY = (192,192,192)
LIGHT_GRAY = (224,224,224)
DARK_GRAY = (128,128,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

Y_SCALE = 2.0/600

#events constants
LEFT = 1

class Plotter():
    
    def __init__(self, pos_factor, size_factor):
        self.pos_factor = pos_factor
        self.size_factor = size_factor
        self.update_layout(WIDTH, HEIGHT)
        self.font = pygame.font.SysFont("monospace", 10)
        
    def update_layout(self, width, height):
        self.position = (self.pos_factor[0] * width, self.pos_factor[1] * height)
        self.size = (self.size_factor[0] * width, self.size_factor[1] * height)
        self.y_scale = Y_SCALE * self.size[1] 

        
    def draw(self, canvas, freq, x_data, y_data_1, y_data_2 = []):
        self.draw_frame(canvas)
        self.draw_freq_marker(canvas, freq, x_data)
        self.draw_graphs(canvas, x_data, y_data_1, y_data_2)
        self.draw_labels(canvas, x_data)
        self.draw_ticks(canvas)
    
    def draw_freq_marker(self, canvas, freq, x_data):
        if x_data != [] and freq >= x_data[0] and freq <= x_data[-1]:
            x_pos = (float(freq - x_data[0]) / (x_data[-1] - x_data[0])) * self.size[0]
            pygame.draw.line(canvas, RED, (self.position[0] + x_pos, self.position[1] + self.size[1]-1), (self.position[0] + x_pos, self.position[1]), 2)   

    
    def draw_frame(self, canvas):
        pygame.draw.rect(canvas, WHITE, (self.position[0],self.position[1],self.size[0],self.size[1]), 0)        
        pygame.draw.rect(canvas, BLACK, (self.position[0],self.position[1],self.size[0],self.size[1]), 1)
     
    def draw_graphs(self, canvas, x_data, y_data_1, y_data_2): 
        if y_data_2 != []:
            graph_2 = self.create_graph_vector(x_data, y_data_2)
            pygame.draw.lines(canvas, DARK_GRAY, 0, graph_2)
        if y_data_1 != []:
            graph_1 = self.create_graph_vector(x_data, y_data_1)
            pygame.draw.lines(canvas, BLUE, 0, graph_1)
             
    def draw_labels(self, canvas, x_data):
        if x_data != []:
            label0 = self.font.render("{0:.1f}".format(x_data[0]), 1, BLACK)
            canvas.blit(label0, (self.position[0]-label0.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label1 = self.font.render("{0:.1f}".format(x_data[len(x_data)/4]), 1, BLACK)
            canvas.blit(label1, (self.position[0]+self.size[0]/4-label1.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label2 = self.font.render("{0:.1f}".format(x_data[len(x_data)/2]), 1, BLACK)  
            canvas.blit(label2, (self.position[0]+self.size[0]/2-label2.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label3 = self.font.render("{0:.1f}".format(x_data[3*len(x_data)/4]), 1, BLACK)  
            canvas.blit(label3, (self.position[0]+3*self.size[0]/4-label3.get_width()/2,self.position[1]+(self.size[1]+self.font.get_height()/8)))
            label4 = self.font.render("{0:.1f}".format(x_data[len(x_data)-1]), 1, BLACK)  
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
        x_scale = float(self.size[0]-2) / (len(x_data)+1)
        line = []
        real_x_pos = self.position[0]+1
        for y in y_data:
            real_x_pos = float(real_x_pos + x_scale)
            y_shift = y * self.y_scale    
            if y_shift <= 0:      
                y_shift = 1     
            elif y_shift > self.size[1]:
                y_shift = self.size[1]
            real_y_pos = self.position[1] + self.size[1] - y_shift
            line.append((real_x_pos, real_y_pos))
        return line
    
    def check_click(self, pos, x_data):
        if x_data != []:
            if (pos[0] >= self.position[0]) and (pos[0] <= self.position[0]+self.size[0]) and (pos[1] >= self.position[1]) and (pos[1] <= self.position[1]+self.size[1]):
                return self.get_click_x_pos(pos, x_data)
        return 0

    def get_click_x_pos(self, pos, x_data):
        x_pos = int(x_data[0] + (x_data[-1] - x_data[0]) * (pos[0] - self.position[0]) / float(self.size[0]))
        return x_pos
        

class Scroll():
    
    def __init__(self, pos_factor, size_factor, drag_func, untouched_factor = 0, max_value = 1, color = LIGHT_GRAY):
        self.pos_factor = pos_factor
        self.size_factor = size_factor
        self.drag_function = drag_func
        self.color = color
        self.update_layout(WIDTH, HEIGHT)
        self.is_clicked = False
        self.key_was_pressed = False
        self.timeout_count = False
        self.timeout_value = 0.0
        self.control_key_pressed = 0
        self.click_height = 0
        self.untouched_value = untouched_factor * self.size[1]
        self.max_value = max_value
        self.height_offset = self.untouched_value
        
    def update_layout(self, width, height):
        self.position = (self.pos_factor[0] * width, self.pos_factor[1] * height)
        self.size = (self.size_factor[0] * width, self.size_factor[1] * height)
        
    def draw(self, canvas):
        if self.is_clicked:
            self.mouse_position_update()
            self.drag_function(float(self.max_value * self.height_offset / self.size[1]))  
        if self.key_was_pressed:
            self.keyboard_position_update()
            self.key_was_pressed = False
            self.drag_function(float(self.max_value * self.height_offset / self.size[1]))   
        pygame.draw.line(canvas, DARK_GRAY, (self.position[0], self.position[1]), (self.position[0], self.position[1] + self.size[1]), 3)
        pygame.draw.rect(canvas, self.color, (self.position[0] - self.size[0]/2, self.position[1] + 39.0/40*self.size[1] - self.height_offset, self.size[0],self.size[1]/20), 0)
        
    def mouse_position_update(self):
        pos = pygame.mouse.get_pos()
        self.height_offset = self.click_height - pos[1] + self.untouched_value
        self.update_scroll_position()
        
    def keyboard_position_update(self):
        self.height_offset = self.untouched_value + self.control_key_pressed * config.KEYBOARD_VOLUME_JUMP * self.size[1]
        self.update_scroll_position()
    
    def update_scroll_position(self):
        if self.height_offset < 0:
            self.height_offset = 0
        elif self.height_offset > self.size[1]:
            self.height_offset = self.size[1]

    def check_click(self, pos):
        if not self.is_clicked and (pos[0] >= self.position[0]-self.size[0]/2) and (pos[0] <= self.position[0]+self.size[0]/2) and (pos[1] >= self.position[1]+(39.0/40)*self.size[1] - self.untouched_value) and (pos[1] <= self.position[1]+(41.0/40)*self.size[1] - self.untouched_value):
            self.click_height = pos[1]
            self.is_clicked = True
              
    def click_release(self):
        if self.is_clicked:
            self.is_clicked = False       
            self.click_height = 0
            self.height_offset = self.untouched_value
            self.drag_function(float(self.height_offset / self.size[1]))
            
    def change_key_pressed(self, value):
        self.control_key_pressed = self.control_key_pressed + value
        self.key_was_pressed = True
        self.timeout_count = False
        self.timeout_value = 0.0
            
    def change_key_released(self, value):
        self.timeout_count = True
        
    def handle_control_timeout(self, ms):
        if self.timeout_count:
            self.timeout_value = self.timeout_value + ms / 1000.0
            if self.timeout_value > config.KEYBOARD_VOLUME_TIMEOUT:
                self.control_key_pressed = 0
                self.keyboard_position_update()
                self.drag_function(float(self.height_offset / self.size[1]))

class Button():
    
    def __init__(self, pos_factor, size_factor, text, press_func = None, release_func = None, color = GRAY):
        self.pos_factor = pos_factor
        self.size_factor = size_factor
        self.update_layout(WIDTH, HEIGHT)
        self.text = text
        self.color = color
        self.is_clicked = False
        self.press_func = press_func
        self.release_func = release_func
        self.font = pygame.font.SysFont("monospace", 18)
        
    def update_layout(self, width, height):
        self.position = (self.pos_factor[0] * width, self.pos_factor[1] * height)
        self.size = (self.size_factor[0] * width, self.size_factor[1] * height)
                
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
                       
        pygame.draw.lines(canvas, color1, 0, [(self.position[1]-OFFSET,self.position[0]+self.size[0]+OFFSET-1), (self.position[1]-OFFSET, self.position[0]-OFFSET), (self.position[1]+self.size[1]+OFFSET-1, self.position[0]-OFFSET)])
        pygame.draw.lines(canvas, color2, 0, [(self.position[1]+self.size[1]+OFFSET-1, self.position[0]-OFFSET), (self.position[1]+self.size[1]+OFFSET-1, self.position[0]+self.size[0]+OFFSET-1), (self.position[1]-OFFSET,self.position[0]+self.size[0]+OFFSET-1)])
        pygame.draw.rect(canvas, self.color, (self.position[1],self.position[0],self.size[1],self.size[0]), 0)
        label = self.font.render(self.text, 1, BLACK)
        canvas.blit(label, (self.position[1]+(self.size[1]-label.get_width())/2,self.position[0]+(self.size[0]-self.font.get_height())/2))
        
    
        

class Gui():

    def __init__(self, interface, sampler, player):
        '''
        Constructor
        '''
        pygame.init()                                           # initialize pygame
        self.fps_Clock = pygame.time.Clock()                    # set the FPS clock
        self.width = WIDTH
        self.height = HEIGHT
        self.canvas = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        pygame.display.set_caption('Sound Demonstrations')
        icon = pygame.transform.scale(pygame.image.load('glass.png'), (32, 32))
        pygame.display.set_icon(icon)
        self.done = False
        self.font = pygame.font.SysFont("monospace", 30)

        self.interface = interface
        self.sampler = sampler
        self.player = player
        
        self.is_playing = False
        self.is_playing_wav_file = False
        
        self.in_glass = True
        self.in_chladni = False
        self.in_ruben = False
        
        self.time=0#####################################################################################################################S
        self.first_peak = 0
        self.second_peak = 0
        self.first_peak_button_text = ''
        self.second_peak_button_text = ''
        
        
        self.top_buttons = []
        self.glass_buttons = []
        self.chladni_buttons = []
        self.ruben_buttons = []  
        
        self.top_buttons.append(Button((1.0/60, 5.0/60),(3.0/60, 15.0/60),"Wine Glass", self.set_glass))
        self.top_buttons.append(Button((1.0/60, 22.0/60),(3.0/60, 15.0/60),"Chladni Plate", self.set_chladni))
        self.top_buttons.append(Button((1.0/60, 39.0/60),(3.0/60, 15.0/60),"Ruben's Tube", self.set_ruben))

        self.top_buttons.append(Button((5.0/60,5.0/60),(5.0/60,10.0/60),"Play", self.play_stop_wave)) 
        self.top_buttons.append(Button((11.0/60,5.0/60),(5.0/60,10.0/60),"+1Hz", self.interface.increaseFreq))
        self.top_buttons.append(Button((17.0/60,5.0/60),(5.0/60,10.0/60),"-1Hz", self.interface.decreaseFreq))
        self.top_buttons.append(Button((23.0/60,5.0/60),(5.0/60,10.0/60),"+0.1Hz", self.interface.increaseFreqFine))
        self.top_buttons.append(Button((29.0/60,5.0/60),(5.0/60,10.0/60),"-0.1Hz", self.interface.decreaseFreqFine))
              
        self.glass_buttons.append(Button((35.0/60,5.0/60),(5.0/60,10.0/60),"FFT", self.sampler.stop_start_FFT_computation))
        self.glass_buttons.append(Button((41.0/60,5.0/60),(5.0/60,10.0/60),"RESET MAX", self.sampler.reset_max_fft))
        self.glass_buttons.append(Button((47.0/60,17.5/60),(5.0/60,40.0/60),'1st peak', self.set_first_peak))
        self.glass_buttons.append(Button((53.0/60,17.5/60),(5.0/60,40.0/60),'2nd peak', self.set_second_peak))
        
        self.chladni_buttons.append(Button((5.0/60,17.0/60),(8.0/60,33.0/60),"Chladni fixed freq I", self.chladni_fixed_1))
        self.chladni_buttons.append(Button((14.0/60,17.0/60),(8.0/60,33.0/60),"Chladni fixed freq II", self.chladni_fixed_2))
        self.chladni_buttons.append(Button((23.0/60,17.0/60),(8.0/60,33.0/60),"Chladni fixed freq III", self.chladni_fixed_3))
        self.chladni_buttons.append(Button((32.0/60,17.0/60),(8.0/60,33.0/60),"Chladni fixed freq IV", self.chladni_fixed_4))
        self.chladni_buttons.append(Button((41.0/60,17.0/60),(8.0/60,33.0/60),"Chladni fixed freq V", self.chladni_fixed_5))
        self.chladni_buttons.append(Button((50.0/60,17.0/60),(8.0/60,33.0/60),"Chladni fixed freq VI", self.chladni_fixed_6))
        
        self.ruben_buttons.append(Button((5.0/60,17.0/60),(10.0/60,33.0/60),"Rubn's tube fixed freq I", self.ruben_fixed_1))
        self.ruben_buttons.append(Button((16.0/60,17.0/60),(10.0/60,33.0/60),"Rubn's tube fixed freq II", self.ruben_fixed_2))
        self.ruben_buttons.append(Button((27.0/60,17.0/60),(10.0/60,33.0/60),"Rubn's tube fixed freq III", self.ruben_fixed_3))
        self.ruben_buttons.append(Button((38.0/60,17.0/60),(10.0/60,33.0/60),"wav fike", self.player.play_stop_wav_file))

        self.plotter = Plotter((17.5/60,5.0/60), (40.0/60,40.0/60))
        
        self.volume_scroll = Scroll((25.0/600,50.0/600), (25.0/600,400.0/600), self.interface.setVol, config.VOLUME_DEFAULT, config.VOLUME_MAXIMUM)
        
        self.freq_line = []
        self.fft_data = []
        self.fft_peak_data = []
      
        self.main_loop()                                        # start the main loop of the gui
    
    def draw(self):
        self.first_peak = self.sampler.get_peak_fft()[0][0]
        self.second_peak = self.sampler.get_peak_fft()[0][1]
        self.glass_buttons[2].text = "1st peak " + "{0:.1f}".format(self.first_peak) + "Hz"
        self.glass_buttons[3].text = "2nd peak " + "{0:.1f}".format(self.second_peak) + "Hz"        
        freq_label = self.font.render("{0:.1f}".format(self.interface.freq) + "Hz", 1, BLACK)
        if self.sampler.has_new_fft():
            self.freq_line, self.fft_data = self.sampler.get_fft_data()
            self.freq_line, self.fft_peak_data = self.sampler.get_peak_waveform()
        self.canvas.fill(GRAY)
        for button in self.top_buttons:
            button.draw(self.canvas) 
        self.volume_scroll.draw(self.canvas)
        if self.in_glass:
            for button in self.glass_buttons:
                button.draw(self.canvas) 
            self.plotter.draw(self.canvas, self.interface.freq, self.freq_line, self.fft_data, self.fft_peak_data)
            self.canvas.blit(freq_label, (5.0/60*self.width,50.0/60*self.height))
        elif self.in_chladni:
            for button in self.chladni_buttons:
                button.draw(self.canvas)
            self.canvas.blit(freq_label, (50.0/600*self.width,500.0/600*self.height))
        elif self.in_ruben:
            for button in self.ruben_buttons:
                button.draw(self.canvas)
            self.canvas.blit(freq_label, (50.0/600*self.width,500.0/600*self.height))
                             
    def play_stop_wave(self):
        if self.is_playing:
            self.player.stopWave()
        else:
            self.player.playWave()
        self.is_playing = not self.is_playing
        
    def set_first_peak(self):
        self.interface.setFreq(self.first_peak)
        
    def set_second_peak(self):
        self.interface.setFreq(self.second_peak)
        
    def update_locations(self, size):
        self.width = size[0]
        self.height = size[1]
        for button in self.top_buttons:
            button.update_layout(self.height, self.width)
        for button in self.glass_buttons:
            button.update_layout(self.height, self.width)
        for button in self.chladni_buttons:
            button.update_layout(self.height, self.width)
        for button in self.ruben_buttons:
            button.update_layout(self.height, self.width)
        self.plotter.update_layout(self.width, self.height)
        self.volume_scroll.update_layout(self.width, self.height)

    def set_freq_from_plotter(self, pos):
        freq = self.plotter.check_click(pos, self.freq_line)
        if freq != 0:
            self.interface.setFreq(freq)
            
    def set_glass(self):
        self.in_glass = True
        self.in_chladni = False
        self.in_ruben = False
        
    def set_chladni(self):
        self.in_glass = False 
        self.in_chladni = True
        self.in_ruben = False
        
    def set_ruben(self):
        self.in_glass = False
        self.in_chladni = False
        self.in_ruben = True 
        
    def chladni_fixed_1(self):
        self.interface.setFreq(config.CHLADNI_FIXED_1[0])
        self.interface.setVol(config.CHLADNI_FIXED_1[1])

    def chladni_fixed_2(self):
        self.interface.setFreq(config.CHLADNI_FIXED_2[0])
        self.interface.setVol(config.CHLADNI_FIXED_2[1])
    
    def chladni_fixed_3(self):
        self.interface.setFreq(config.CHLADNI_FIXED_3[0])
        self.interface.setVol(config.CHLADNI_FIXED_3[1])
    
    def chladni_fixed_4(self):
        self.interface.setFreq(config.CHLADNI_FIXED_4[0])
        self.interface.setVol(config.CHLADNI_FIXED_4[1])
    
    def chladni_fixed_5(self):
        self.interface.setFreq(config.CHLADNI_FIXED_5[0])
        self.interface.setVol(config.CHLADNI_FIXED_5[1])
    
    def chladni_fixed_6(self):
        self.interface.setFreq(config.CHLADNI_FIXED_6[0])
        self.interface.setVol(config.CHLADNI_FIXED_6[1])
      
    def ruben_fixed_1(self):
        self.interface.setFreq(config.TUBE_FIXED_1[0]) 
        self.interface.setVol(config.TUBE_FIXED_1[1])
         
    def ruben_fixed_2(self):
        self.interface.setFreq(config.TUBE_FIXED_2[0])
        self.interface.setVol(config.TUBE_FIXED_1[1])
                
    def ruben_fixed_3(self):
        self.interface.setFreq(config.TUBE_FIXED_3[0])
        self.interface.setVol(config.TUBE_FIXED_1[1])

    '''
    def play_stop_wav_file(self):
        if not self.is_playing_wav_file:
            self.is_playing_wav_file = True
            self.player.play_wav_file()
        else:
            self.is_playing_wav_file = False
            self.player.stop_wav_file_play()
    '''
    def main_loop(self):
        while not self.done:
            for event in pygame.event.get():
                # exit if ESC pressed or 'x' clicked. 
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):     
                    self.sampler.close_pyaudio_nicely()
                    self.player.close_nicely()
                    self.done = True
                
                # change window size event
                elif event.type==VIDEORESIZE:
                    self.canvas=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                    pygame.display.flip()
                    self.update_locations(event.dict['size'])
                
                # left mouse button clicked events
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    for button in self.top_buttons:
                        button.check_click(event.pos)
                    self.volume_scroll.check_click(event.pos)
                        
                    if self.in_glass:
                        for button in self.glass_buttons:
                            button.check_click(event.pos)
                        self.set_freq_from_plotter(event.pos)
                        
                    elif self.in_chladni:
                        for button in self.chladni_buttons:
                            button.check_click(event.pos)
                            
                    elif self.in_ruben:
                        for button in self.ruben_buttons:
                            button.check_click(event.pos)
                
                # left mouse button released events
                elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                    self.volume_scroll.click_release()
                    for button in self.top_buttons:
                        button.click_release()
                    for button in self.glass_buttons:
                        button.click_release()
                    for button in self.chladni_buttons:
                        button.click_release()
                    for button in self.ruben_buttons:
                        button.click_release()
                        
                # keyboard keys events
                elif event.type == KEYDOWN: 
                    if event.key == K_LEFT:
                        self.interface.decreaseFreqFine()
                    elif event.key == K_RIGHT:
                        self.interface.increaseFreqFine()
                    elif event.key == K_UP:
                        self.volume_scroll.change_key_pressed(1)
                    elif event.key == K_DOWN:
                        self.volume_scroll.change_key_pressed(-1)
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        self.volume_scroll.change_key_released(1)
                    elif event.key == K_DOWN:
                        self.volume_scroll.change_key_released(-1)
                    
                                   
            self.draw()         
            pygame.display.update()
            ms = self.fps_Clock.tick(60)
            
            self.volume_scroll.handle_control_timeout(ms)
                
            self.time = self.time + (ms/1000.0)
            if self.time > 1:
                self.time = self.time - 1
                print self.fps_Clock.get_fps()
            
            
            
        pygame.quit
        

#gui()        

                    
        
            