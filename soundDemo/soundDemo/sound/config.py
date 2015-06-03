
#### FFT sampler configurations ####
MIN_USED_FREQUENCY = 600   
MAX_USED_FREQUENCY = 900
DELTA_FREQ_FOR_MAXIMA = 7  # minimal allowed distance (in Hz) of the second maxima from the first one

VOLUME_MAXIMUM = 1    # maximal volume (when the volume bar is dragged untill its end), should be enough to break the glass, but not violate the current/power limitations  
VOLUME_DEFAULT = 0.05 # fraction of the VOLUME_MAXIMUM that will be used when the volume bar is untouched, should be enough to show the glass movement but not break it 
