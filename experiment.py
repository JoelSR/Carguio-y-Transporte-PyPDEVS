from pypdevs.simulator import Simulator
from OutFiles import OutFiles

# JSON FILES
import json

import sys
from pathlib import Path

# COUPLED MODEL
from OPMCT import OPMCTSystem

if(len(sys.argv) == 2):
    if(sys.argv[1] in ["--help","-h"]):
        print("uso: experiment.py [opción]")
        print("-h, --help\t\tMostrar esta ayuda.")
        print("-e,--example\t\tPara ver un ejemplo.")
        print("\t\t*Para utilizar un archivo json distinto al del ejemplo ingrese la dirección del archivo")
        exit()
    elif(sys.argv[1] in ["--example","-e"]):
        file = open("data.json")
        data = json.load(file)
        print("Estructura del archivo: ",data)
    else:
        path = Path(sys.argv[1])
        if(path.exists()):
            file = open(path)
            try:
                data = json.load(file)
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                print('Decoding JSON has failed')
                sys.exit()
        else:
            print("Error: Asegure que el archivo existe o que la dirección fue bien ingresada.")
            exit()

else:
    print("uso: experiment.py [opción]")
    print("-h, --help\t\tMostrar esta ayuda.")
    print("-e,--example\t\tPara ver un ejemplo")
    print("*Para utilizar un archivo json distinto al del ejemplo ingrese la dirección del archivo")
    exit()

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

#Verificar que los stocks corresponden a las cantidades respectivas
for i in palaToStock:
    if(len(i)>sQ):
        print("La cantidad de stocks no corresponde a los que se ingresaron en palaToStock")
        sys.exit()
    elif(max(i)>sQ or min(i)<=0):
        print("Los stocks van entre 1 y cantidad de stocks")
        sys.exit()
    else:
        continue

opmct = OPMCTSystem(cQ,pQ,sQ,palaToStock)

# PythonPDEVS specific setup and configuration
sim = Simulator(opmct)

# Termination time
sim.setTerminationTime(simTime)
sim.setVerbose("OUTPUT.txt")
sim.setClassicDEVS()
sim.simulate()

collector = opmct.collector.state.events

files = OutFiles(collector,simTime)
print("Cambios de estado almacenados como 'OUTPUT.txt'")
files.archivo()