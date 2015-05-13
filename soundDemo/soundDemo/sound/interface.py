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
	

	def mute(self):
		self.vol = 0

	def increaseVol(self):
		self.vol += 1

	def decreaseVol(self):
		self.vol -=1

	def setTuneStep(self, val, fine=0):
		if fine:
			self.finetune = val
		else:
			self.coarsetune = val
            
	def increaseFreq(self, fine=0):
		if fine:
			self.freq += self.finetune
		else:
			self.freq += self.coarsetune

	def decreaseFreq(self, fine=0):
		if fine:
			self.freq -= self.finetune
		else:
			self.freq -= self.coarsetune
