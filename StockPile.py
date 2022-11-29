from pypdevs.DEVS import *

class StockPileState:
	def __init__(self, current="esperando"):
		self.set(current)

	def set(self, value="esperando"):
		self.__state=value

	def get(self):
		return self.__state


	def __str__(self):
		return self.get()

class StockPile(AtomicDEVS):
	def __init__(self, name=None):
		# Class constructor
		AtomicDEVS.__init__(self, name)

		# Initial State
		self.state = StockPileState("esperando")

		self.toneladas = 0

		# PORTS:
		#  Declare as many input and output ports as desired
		#  (usually store returned references in local variables):
		self.LOAD = self.addInPort(name="LOAD")

	def intTransition(self):
		state = self.state.get()

		if(state == "ocupado"):
			return StockPileState("esperando")
		else:
			raise DEVSException(\
				"unknown state <%s> in STOCKPILE internal transition function"\
				% state)

	def extTransition(self,inputs):
		input = inputs.get(self.LOAD)[0]

		self.toneladas += input
		return self.state

	def timeAdvance(self):
		state = self.state.get()

		if state == "esperando":
			return float("inf")
		elif state == "ocupado":
			return 0.0
		else:
			raise DEVSException(\
				"unknown state <%s> in STOCKPILE outputFnc"\
				% state)
