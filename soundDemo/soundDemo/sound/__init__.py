import interface
import gui
import sampler
import player
import pyaudio
import time

pa = pyaudio.PyAudio()
interface_i = interface.Interface(761)
sampler_i = None #sampler.Sampler(pa=pa)
time.sleep(1)
player_i = player.Player(interface=interface_i, pa=pa)
time.sleep(1)
gui_i = gui.Gui(interface_i, sampler_i, player_i)
