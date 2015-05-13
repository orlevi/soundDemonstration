'''
' Created: May 12, 2015
'
' @author: Omer Cohen
'''

class Interface():

    def __init__(self, volume, frequency):
        self.vol = volume
        self.freq = frequency
        self.finetune = 0.1
        self.coarsetune = 1    

	def increaseVol(self):
		self.vol += 1

	def decreaseVol(self):
		self.vol -=1

    def muteVol(self):
        self.vol = 0

    def setTuneStep(self, val, fine=0):
        if fine:
            finetune = val
        else:
            coarsetune = val
            
	def increaseFreq(self, fine=0):
		if fine:
			self.freq += 0.5
		else:
			self.freq += 2

	def decreaseFreq(self, fine=0):
		if fine:
			self.freq -= finetune
		else:
			self.freq -= coarsetune