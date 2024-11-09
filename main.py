from utils.csv_reader import leer_archivo_estados, leer_archivo_transiciones, encontrar_estados_aceptadores
from turing.MaquinaTuring import MaquinaTuring

from collections import deque

def cargar_cinta_desde_archivo(archivo):
    with open(archivo, 'r') as f:
        # Leer el contenido del archivo y eliminar cualquier salto de línea al final
        contenido = f.read().strip()  # O usa .splitlines() si hay varias líneas
        # Cargar los símbolos en una deque
        cinta = deque(contenido)
    return cinta

estados = leer_archivo_estados("estados_automata_suma_binaria.csv")
transiciones = leer_archivo_transiciones("suma_binaria.csv")
estados_aceptadores = encontrar_estados_aceptadores(estados)

archivo = "cinta.txt"
cinta = cargar_cinta_desde_archivo(archivo)

# Inicializo la maquina de Turing
mt = MaquinaTuring(estados, estados_aceptadores, transiciones, cinta)

mt.iniciar()