# Modelo Carguío y Transporte PyPDEVS
Modelo de carguio y transporte implementado en PyPDEVS

![image](https://user-images.githubusercontent.com/44043395/200244095-9333ccc1-2b60-4828-bde8-118958a39f8d.png)

## Instalación PyPDEVS
El paquete de simulación y modelado PyPDEVS se encuentra en [Repositorio PythonPDEVS](https://msdl.uantwerpen.be/git/yentl/PythonPDEVS), para encontrar trabajos y documentación se debe dirigir a la [Página oficial de PythonPDEVS](http://msdl.cs.mcgill.ca/projects/DEVS/PythonPDEVS).

Este paquete se puede instalar facilmente con los siguientes comandos en la carpeta descargada (Python3).
```
cd src
python3 setup.py install --user
python3 -c "import pypdevs"
```
## Utilización modelo carguío y transporte

Para la utilización del simulador se necesita instalar [Numpy](https://numpy.org/install/) y [Pandas](https://pandas.pydata.org/docs/getting_started/install.html).
Teniendo las librerías instaladas, el uso del simulador consiste en los siguientes comandos:
* Ejemplo
```
python3 experiment -e
```
```
python3 experiment --example
```
* Ayuda
```
python3 experiment -h
```
```
python3 experiment --help
```
* Archivo de configuración
```
python3 experiment [path/to/file]
```
