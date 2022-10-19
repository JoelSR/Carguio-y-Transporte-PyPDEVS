from pypdevs.simulator import Simulator

import json

# TEST
from random import seed
from random import randint

# COUPLED MODEL
from OPMCT import OPMCTSystem

file = open("data.json")

data = json.load(file)

file.close()

# Número de camiones
cQ = data["camiones"]

# Número de palas
pQ = data["palas"]

# Número de stock piles
sQ = data["stock_piles"]

# Tiempo de simulación
simTime = float(data["simTime"])

# Stocks de pala
palaToStock = data["palaToStock"]

seed(1)
for _ in range(50):
	opmct = OPMCTSystem(randint(1,10),randint(1,10),sQ,palaToStock)

	# PythonPDEVS specific setup and configuration
	sim = Simulator(opmct)
	# Termination time
	sim.setTerminationTime(simTime)
	sim.setVerbose(None)
	sim.setClassicDEVS()
	sim.simulate()

"""sim_data = []

collector = opmct.collector.state.events
sim_data.append([e for e in evt_list])
print(sim_data)"""