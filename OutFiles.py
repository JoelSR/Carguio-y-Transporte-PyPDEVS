import pandas as pd

class OutFiles():
	def __init__(self,collector):
		self.camCols = ["Camion","Tiempo","Estado","Carga"]
		self.data = collector
		self.camiones = None

	def metricas(self):
		aux = None
		metrics = {}
		for maquinaria in self.camiones["Camion"].unique():
			aux = self.camiones.loc[self.camiones["Camion"]==maquinaria]
			metrics[maquinaria] = {}
			if "pala"in maquinaria:
				metrics[maquinaria]["tons"]=aux.loc[(aux.Estado=="cargando")]["Carga"].sum()
				metrics[maquinaria]["TO"]=aux.loc[(aux.Estado=="cargando")]["Tiempo"].sum()
				metrics[maquinaria]["TD"]=metrics[maquinaria]["TO"]
				metrics[maquinaria]["U"]=metrics[maquinaria]["TO"]/metrics[maquinaria]["TD"]
			else:
				metrics[maquinaria]["tons"]=aux.loc[(aux.Estado=="descargando")]["Carga"].sum()
				metrics[maquinaria]["TDO"]=aux.loc[(aux.Estado=="esperando")]["Tiempo"].sum()
				metrics[maquinaria]["TD"]=aux.loc[(aux.Estado=="transportando")]["Tiempo"].sum()+aux.loc[(aux.Estado=="descargando")]["Tiempo"].sum()+aux.loc[(aux.Estado=="ocupado")]["Tiempo"].sum()
				metrics[maquinaria]["TO"]=metrics[maquinaria]["TD"]-metrics[maquinaria]["TDO"]
				metrics[maquinaria]["U"]=metrics[maquinaria]["TO"]/metrics[maquinaria]["TD"]
				metrics[maquinaria]["Fq"]=aux.loc[(aux.Estado=="descargando")]["Carga"].mean()/400
		
		metricas = pd.DataFrame.from_dict(metrics)
		metricas.to_csv("metricas.csv")
		print("Archivo de metricas almacenado como 'metricas.csv'")

	def archivo(self):
		self.camiones = pd.DataFrame(self.data,columns=self.camCols)
		self.camiones.to_csv("out.csv")
		print("Archivo almacenado como 'out.csv'")
		self.metricas()