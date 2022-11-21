import pandas as pd
from datetime import datetime
from pathlib import Path
from os import mkdir

class OutFiles():
	def __init__(self,collector,nominal):
		self.camCols = ["Maquinaria","Tiempo","Estado","Carga","Cola"]
		self.data = collector
		self.camiones = None
		self.nominal = nominal

	def metricas(self):
		aux = None
		metrics = {}
		for maquinaria in self.camiones["Maquinaria"].unique():
			aux = self.camiones.loc[self.camiones["Maquinaria"]==maquinaria]
			metrics[maquinaria] = {}
			metrics[maquinaria]["TD"]=self.nominal #-MANTENIMIENTO
			if "pala" in maquinaria:
				metrics[maquinaria]["tons"]=aux.loc[(aux.Estado=="cargando")]["Carga"].sum()
				metrics[maquinaria]["TO"]=aux.loc[(aux.Estado=="cargando")]["Tiempo"].sum()
				metrics[maquinaria]["TDO"]=metrics[maquinaria]["TD"]-metrics[maquinaria]["TO"]
			else:
				metrics[maquinaria]["tons"]=aux.loc[(aux.Estado=="descargando")]["Carga"].sum()
				metrics[maquinaria]["TDO"]=aux.loc[(aux.Estado=="esperando")]["Tiempo"].sum()
				metrics[maquinaria]["TO"]=metrics[maquinaria]["TD"]-metrics[maquinaria]["TDO"]
				metrics[maquinaria]["Fq"]=(aux.loc[(aux.Estado=="descargando")]["Carga"].mean()/400)*100
			metrics[maquinaria]["U"]=(metrics[maquinaria]["TO"]/metrics[maquinaria]["TD"])*100
		
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