import pandas as pd

class OutFiles():
	def __init__(self,collector):
		self.camCols = ["Camión","Tiempo","Estado","Carga"]
		self.data = collector

	def archivo(self):
		camiones = pd.DataFrame(self.data,columns=self.camCols)
		camiones.to_csv("out.csv")
		print("Archivo almacenado como 'out.csv'")

	def metricas(self):
		print("OK")