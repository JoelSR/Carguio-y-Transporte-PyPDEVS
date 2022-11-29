from pypdevs.DEVS import CoupledDEVS

# Import all models to couple
from Camion import Camion
from Pala import Pala
from StockPile import StockPile
from collector import Collector
from Dispatcher import Dispatcher


class OPMCTSystem(CoupledDEVS):
	def __init__(self,cQ,pQ,sQ,palaToStock):
		CoupledDEVS.__init__(self,"OPMCTSystem")

		# CLASS DISPATCHER
		dispatcher = Dispatcher()

		#Creación de camiones
		self.camiones = []
		for i in range(cQ):
			name = "camion_"+str(i)
			self.camiones.append(self.addSubModel(Camion(sQ,pQ,name,dispatcher)))

		#Creación de palas
		self.palas = []
		if(palaToStock != []):
			for i in range(pQ):
				name = "pala_"+str(i)
				dispatcher.addPala(name)
				self.palas.append(self.addSubModel(Pala(name,cQ,palaToStock[i])))
		else:
			for i in range(pQ):
				name = "pala_"+str(i)
				dispatcher.addPala(name)
				self.palas.append(self.addSubModel(Pala(name,cQ)))

		#Creación de StockPiles
		self.stockPiles = []
		for i in range(sQ):
			self.stockPiles.append(self.addSubModel(StockPile("stock_"+str(i+1),cQ)))

		#Collector para datos
		self.collector = self.addSubModel(Collector(cQ,pQ))

		#Conexión de puertos para proceso de CARGA y TRANSPORTE
		for i in range(pQ):
			for j in range(cQ):
				self.connectPorts(self.camiones[j].notify["pala_"+str(i)],self.palas[i].CAMION)
				self.connectPorts(self.palas[i].out_load["camion_"+str(j)],self.camiones[j].INLOAD)
				self.connectPorts(self.camiones[j].DATA,self.collector.in_event)
			self.connectPorts(self.palas[i].DATA,self.collector.in_event)
		
		#Conexión de puertos para proceso de DESCARGA
		for j in range(sQ):
			for i in range(cQ):
				self.connectPorts(self.camiones[i].out_load["stock_"+str(j+1)],self.stockPiles[j].LOAD)
				self.connectPorts(self.stockPiles[j].ready["camion_"+str(i)],self.camiones[i].READY)
			self.connectPorts(self.stockPiles[j].DATA,self.collector.in_event)
				