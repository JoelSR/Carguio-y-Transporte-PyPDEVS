import pandas as pd
from datetime import datetime
from pathlib import Path
from os import mkdir

class OutFiles():
	def __init__(self,collector,nominal):
		self.camCols = ["Camion","Tiempo","Estado","Carga"]
		self.data = collector
		self.camiones = None
		self.nominal = nominal

	def metricas(self):
		aux = None
		metrics = {}
		for maquinaria in self.camiones["Camion"].unique():
			aux = self.camiones.loc[self.camiones["Camion"]==maquinaria]
			metrics[maquinaria] = {}
			if "pala"in maquinaria:
				metrics[maquinaria]["tons"]=aux.loc[(aux.Estado=="cargando")]["Carga"].sum()
				metrics[maquinaria]["TO"]=aux.loc[(aux.Estado=="cargando")]["Tiempo"].sum()
				metrics[maquinaria]["TD"]=self.nominal #-DEMORAS
				metrics[maquinaria]["Utilizacion"]=(metrics[maquinaria]["TO"]/metrics[maquinaria]["TD"])*100
			else:
				metrics[maquinaria]["tons"]=aux.loc[(aux.Estado=="descargando")]["Carga"].sum()
				metrics[maquinaria]["TDO"]=aux.loc[(aux.Estado=="esperando")]["Tiempo"].sum()
				metrics[maquinaria]["TD"]=self.nominal #-DEMORAS
				metrics[maquinaria]["TO"]=metrics[maquinaria]["TD"]-metrics[maquinaria]["TDO"]
				metrics[maquinaria]["Utilizacion"]=(metrics[maquinaria]["TO"]/metrics[maquinaria]["TD"])*100
				metrics[maquinaria]["Factor LLenado"]=(aux.loc[(aux.Estado=="descargando")]["Carga"].mean()/400)*100
		
		metricas = pd.DataFrame.from_dict(metrics)
		name = str(datetime.now())+"metricas.csv"
		metricas.to_csv("resultados/"+name)
		print("Archivo de metricas almacenado como",name)

	#creación de archivo con resultados
	def archivo(self):
		if(not Path("resultados").exists()):
			mkdir("resultados")
		self.camiones = pd.DataFrame(self.data,columns=self.camCols)
		name = str(datetime.now())+"resultados.csv"
		self.camiones.to_csv("resultados/"+name)
		print("Archivo almacenado como ",name)
		self.metricas()