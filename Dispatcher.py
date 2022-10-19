class Dispatcher():
	def __init__(self):
		self.camiones = []
		self.palas    = []
		self.pala     = 0 

	# Añadir camión
	def addCamion(self,camion):
		self.camiones.append(camion)

	# Añadir pala
	def addPala(self,pala):
		self.palas.append(pala)

	# Despacho circular
	def asignarPalaRR(self):
		try:
			return "pala_"+str(self.pala)
		finally:
			if(self.pala == len(self.palas)-1):
				self.pala = 0
			else:
				self.pala += 1

	# Getters
	def getPalas(self):
		return self.palas

	def getCamiones(self):
		return self.camiones