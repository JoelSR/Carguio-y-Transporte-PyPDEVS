from pypdevs.DEVS import *
from scipy.stats import gamma
import random

class PalaState:
	def __init__(self, current="esperando"):
		self.set(current)

	def set(self, value="esperando"):
		self.__state=value

	def get(self):
		return self.__state

	def __str__(self):
		return self.get()

class Pala(AtomicDEVS):
	def __init__(self, name=None, cQ=0,stocks=None):
		# Class constructor
		AtomicDEVS.__init__(self, name)

		# Initial State
		self.state = PalaState("esperando")
		self.remaining_time = float("inf")

		# Cola
		self.camiones = []
		# Tiempo de Carga
		self.loadTime = 0.0
		# Pala ocupada
		self.busy = False
		# Stocks a los que se pueden ir
		self.toStocks = 0

		self.adv_time = 0

		if stocks != None:
			self.toStocks = stocks
		else:
			self.toStocks = 0

		self.out_load = {}

		# PORTS:
		#  Declare as many input and output ports as desired
		#  (usually store returned references in local variables):
		self.CAMION = self.addInPort(name="CAMION")
		self.DATA = self.addOutPort(name="DATA")
		for i in range(cQ):
			self.out_load["camion_"+str(i)] = self.addOutPort(name="CARGAR_camion_"+str(i))


	def intTransition(self):
		"""
		Internal Transition Function
		"""
		state = self.state.get()

		if(state == "cargando"):
			self.camiones.pop(0)
			self.busy = False
			return PalaState("salida")
		elif(state == "iniciarCarga"):
			self.camion = self.camiones[0]
			self.busy = True
			return PalaState("cargando")
		elif(state == "salida"):
			if len(self.camiones) != 0 and self.busy == False:
				return PalaState("iniciarCarga")
			else:
				return PalaState("esperando")
			
		else:
			raise DEVSException(\
				"unknown state <%s> in PALA internal transition function"\
				% state)

	def extTransition(self,inputs):
		inputC = inputs.get(self.CAMION)[0]

		state = self.state.get()

		if(inputC):
			self.camiones.append(inputC)
			return PalaState("iniciarCarga")

	def timeAdvance(self):
		state = self.state.get()


		if state == "esperando":
			return float("inf")
		elif state == "cargando":
			self.adv_time = 0.0
			return 0.0
		elif state == "iniciarCarga":
			self.loadTime = gamma.rvs(8, scale=31.62,size=1)+gamma.rvs(3, scale=32.42,size=1)
			self.adv_time = 0.0
			return 0.0
		elif state == "salida":
			return self.loadTime[0]
		else:
			raise DEVSException(\
				"unknown state <%s> in PALA time advance transition function"\
				% state)

	def outputFnc(self):
		state = self.state.get()

		if(state == "cargando"):
			return {self.out_load[self.camion]: [random.randrange(321,340),self.loadTime[0],self.toStocks],
					self.DATA: [self.name,self.adv_time,self.state.get(),random.randrange(321,340)]}
		elif(state == "iniciarCarga"):
			return {self.DATA: [self.name,self.elapsed,self.state.get(),0]}
		elif(state == "salida"):
			return {self.DATA: [self.name,self.adv_time,self.state.get(),0]}
		else:
			raise DEVSException(\
				"unknown state <%s> in PALA outputFnc"\
				% state)