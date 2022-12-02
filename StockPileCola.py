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

class StockPileQueue(AtomicDEVS):
	def __init__(self, name,cQ):
		# Class constructor
		AtomicDEVS.__init__(self, name)

		# Initial State
		self.state = StockPileState("esperando")

		self.toneladas = 0
		self.camiones = []
		self.busy = False
		self.unloadT = 0.0

		# PORTS:
		#  Declare as many input and output ports as desired
		#  (usually store returned references in local variables):
		self.ready   = {}

		self.LOAD = self.addInPort(name="LOAD")
		self.DATA = self.addOutPort(name="DATA")

		for i in range(cQ):
			self.ready["camion_"+str(i)] = self.addOutPort(name="READY_CAMION_"+str(i))

	def intTransition(self):
		state = self.state.get()

		if(state == "stockOcupado"):
			return StockPileState("salidaStock")
		elif(state == "darPaso"):
			self.camion = self.camiones[0][0]
			self.unloadT = self.camiones[0][2]
			self.busy = True
			self.camiones.pop(0)
			return StockPileState("stockOcupado")
		elif(state == "salidaStock"):
			self.busy = False
			if len(self.camiones) != 0:
				return StockPileState("darPaso")
			else:
				return StockPileState("esperando")
		else:
			raise DEVSException(\
				"unknown state <%s> in STOCKPILE internal transition function"\
				% state)

	def extTransition(self,inputs):
		input = inputs.get(self.LOAD)

		if(self.busy):
			self.camiones.append(input)
			self.unloadT -= self.elapsed
			return StockPileState("salidaStock")
		else:
			self.camiones.append(input)
			return StockPileState("darPaso")

	def timeAdvance(self):
		state = self.state.get()

		if state == "esperando":
			return float("inf")
		elif state == "stockOcupado":
			return 0.0
		elif state == "darPaso":
			return 0.0
		elif state == "salidaStock":
			return self.unloadT
		else:
			raise DEVSException(\
				"unknown state <%s> in STOCKPILE outputFnc"\
				% state)
	

	def outputFnc(self):

		state = self.state.get()

		if(state == "salidaStock"):
			return {self.DATA: [self.name,0.0,self.state.get(),0]}
		elif(state == "darPaso"):
			return {self.DATA: [self.name,0.0,self.state.get(),0]}
		elif(state == "stockOcupado"):
			return {self.ready[self.camion]: [self.camion]}
		else:
			raise DEVSException(\
				"unknown state <%s> in STOCK PILE outputFnc"\
				% state)