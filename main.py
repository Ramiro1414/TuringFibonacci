from utils.csv_reader import leer_archivo_estados, leer_archivo_transiciones, encontrar_estados_aceptadores
from turing.MaquinaTuring import MaquinaTuring
import tkinter as tk

from collections import deque

def cargar_cinta_desde_archivo(archivo):
    with open(archivo, 'r') as f:
        # Leer el contenido del archivo y eliminar cualquier salto de línea al final
        contenido = f.read().strip()  # O usa .splitlines() si hay varias líneas
        # Cargar los símbolos en una deque
        cinta = deque(contenido)
    return cinta

configuracion, transiciones = leer_archivo_transiciones("fibonacci.csv")
estados = leer_archivo_estados(configuracion['archivo_estados'])
estados_aceptadores = encontrar_estados_aceptadores(estados)

cinta = cargar_cinta_desde_archivo("cinta.txt")

# Inicializo la máquina de Turing usando la configuración del CSV
mt = MaquinaTuring(
    estados=estados,
    estados_aceptadores=estados_aceptadores,
    transiciones=transiciones,
    cinta=cinta,
    estado_inicial=configuracion['estado_inicial'],
    posicion_cabeza=configuracion['posicion_cabeza']
)

# Crear la ventana de Tkinter
ventana = tk.Tk()
ventana.title("Máquina de Turing")

# Ejecutar la máquina
velocidad_maquina = 100 # En milisegundos
ventana.after(100, lambda: mt.iniciar(ventana, velocidad_maquina))
ventana.mainloop()