
#### FFT sampler configurations ####
MIN_USED_FREQUENCY = 600   
MAX_USED_FREQUENCY = 900
DELTA_FREQ_FOR_MAXIMA = 7  # minimal allowed distance (in Hz) of the second maxima from the first one

VOLUME_MAXIMUM = 1          # maximal volume (when the volume bar is dragged to its end), should be value between 0 to 1, enough to break the glass, but not to violate the current/power limitations
VOLUME_DEFAULT = 0.05       # fraction of the VOLUME_MAXIMUM that will be used when the volume bar is untouched, should be enough to show the glass movement but not break it 
KEYBOARD_VOLUME_JUMP = 0.05 # fraction of the VOLUME_MAXIMUM that will be added by keyboard up/down arrow press
KEYBOARD_VOLUME_TIMEOUT = 3 # time in seconds between leaving the volume keyboard key and until the volume drops to its default

#### Chladni Plate fixed frquencies ####
CHLADNI_FIXED_1 = 350
CHLADNI_FIXED_2 = 450

#### Ruben's Tube fixed frquencies ####
TUBE_FIXED_1 = 550
TUBE_FIXED_2 = 650
TUBE_FIXED_3 = 750

