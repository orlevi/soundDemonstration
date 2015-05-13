import interface
import gui
import sampler
import player
import pyaudio

interface_i = interface.Interface(0.5, 440)
sampler_i = sampler.Sampler()
player_i = player.Player(interface_i)
gui_i = gui.Gui(interface_i, sampler_i, player_i)
