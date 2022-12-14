from pypdevs.DEVS import *
from numpy.random import normal
from numpy.random import lognormal
from math import sqrt
from math import log

#Asignación de estados de pala
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
	#Atributos
	def __init__(self, name=None, cQ=0,stocks=None):
		# Class constructor
		AtomicDEVS.__init__(self, name)

		# Initial State
		self.state = PalaState("esperando")

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
			return PalaState("salida")
		elif(state == "iniciarCarga"):
			self.camion = self.camiones[0]
			self.busy = True
			self.camiones.pop(0)
			return PalaState("cargando")
		elif(state == "salida"):
			self.busy = False
			if len(self.camiones) != 0:
				return PalaState("iniciarCarga")
			else:
				return PalaState("esperando")
		else:
			raise DEVSException(\
				"unknown state <%s> in PALA internal transition function"\
				% state)

	def extTransition(self,inputs):
		inputC = inputs.get(self.CAMION)[0]

		if(self.busy):
			self.camiones.append(inputC)
			self.loadTime -= self.elapsed
			return PalaState("salida")
		else:
			self.camiones.append(inputC)
			return PalaState("iniciarCarga")

	def timeAdvance(self):
		state = self.state.get()

		if state == "esperando":
			return float("inf")
		#Envio de carga
		elif state == "cargando":
			self.adv_time = 0.0
			return 0.0
		elif state == "iniciarCarga":
			#https://blogs.sas.com/content/iml/2014/06/04/simulate-lognormal-data-with-specified-mean-and-variance.html
			phi = sqrt(4.41**2+2.54**2)
			self.loadTime = (lognormal(log(4.41**2/ phi),sqrt(log((phi**2)/4.41**2))))*60 #carguio
			return 0.0
		#Espera de salida
		elif state == "salida":
			return self.loadTime
		else:
			raise DEVSException(\
				"unknown state <%s> in PALA time advance transition function"\
				% state)

	def outputFnc(self):
		state = self.state.get()

		if(state == "cargando"):
			carga = normal(331,16.06,1)[0]
			return {self.out_load[self.camion]: [carga,self.loadTime,self.toStocks],
					self.DATA: [self.name,self.loadTime,self.state.get(),carga,len(self.camiones)]}
		elif(state == "iniciarCarga"):
			return {self.DATA: [self.name,0.0,self.state.get(),0]}
		elif(state == "salida"):
			return {self.DATA: [self.name,self.adv_time,self.state.get(),0]}
		else:
			raise DEVSException(\
				"unknown state <%s> in PALA outputFnc"\
				% state)