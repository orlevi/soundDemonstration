'''
Created: May 12, 2015

@author: Omer Cohen
'''

class Interface():

	def __init__(self, volume, frequency):

		self.vol = volume
		self.freq = frequency
	def increaseVol(self):
		self.vol += 1
	def decreaseVol(self):

		self.vol -=1

	def increaseFreq(self, fine):

		if fine:
			self.freq += 0.5
		else:
			self.freq += 2
	def decreaseFreq(self, fine):

		if fine:

			self.freq -= 0.5

		else:

			self.freq -= 2