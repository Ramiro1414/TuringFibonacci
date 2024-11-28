from collections import deque
import tkinter as tk
from time import sleep

class MaquinaTuring:
    def __init__(self, estados: dict, estados_aceptadores: list, transiciones: dict, cinta: deque, estado_inicial: str, posicion_cabeza: int):
        self.estados = estados
        self.estados_aceptadores = estados_aceptadores
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.cinta = cinta
        self.posicion_cabeza = posicion_cabeza

    def iniciar(self, ventana, velocidad: int):
        """Ejecuta el autómata paso a paso utilizando Tkinter y actualiza la visualización."""
        simbolo_actual = self.cinta[self.posicion_cabeza]

        if (self.estado_actual, simbolo_actual) in self.transiciones:
            self.realizar_transicion(simbolo_actual)
            self.actualizar_visualizacion(ventana)

            if self.estado_actual in self.estados_aceptadores:
                print(f"\nAutómata ha aceptado en el estado {self.estado_actual}. Configuración de cinta al terminar:")
                self.imprimir_cinta()
                self.actualizar_visualizacion(ventana)  # Actualización final
            else:
                ventana.after(velocidad, self.iniciar, ventana, velocidad)  # Llama al siguiente paso
        else:
            print("Estado de error")

    def realizar_transicion(self, simbolo_actual):
        """Ejecuta la transición basada en el símbolo actual y el estado."""
        transicion = self.transiciones[(self.estado_actual, simbolo_actual)]
        
        self.escribir_en_cinta(transicion['escribir'])
        self.mover_cabezal(transicion['movimiento'])
        self.estado_actual = transicion['destino']

    def escribir_en_cinta(self, simbolo):
        """Escribe un símbolo en la posición actual de la cinta."""
        self.cinta[self.posicion_cabeza] = simbolo

    def mover_cabezal(self, direccion):
        """Mueve el cabezal a la izquierda (L) o a la derecha (R) según la dirección especificada."""
        if direccion == 'R':
            self.posicion_cabeza += 1
            if self.posicion_cabeza == len(self.cinta):
                self.cinta.append('▲')
        elif direccion == 'L':
            if self.posicion_cabeza == 0:
                self.cinta.appendleft('▲')
            else:
                self.posicion_cabeza -= 1

    def imprimir_cinta(self):
        """Imprime la cinta, resaltando la posición del cabezal actual."""
        cinta_con_cabeza = [
            f"[{valor}]" if i == self.posicion_cabeza else str(valor)
            for i, valor in enumerate(self.cinta)
        ]
        print(''.join(cinta_con_cabeza))

    def actualizar_visualizacion(self, ventana):

        # Si no existe el atributo `widgets_cinta`, lo creamos para almacenar las referencias
        if not hasattr(self, "widgets_cinta"):
            self.widgets_cinta = []  # Lista para almacenar los widgets de la cinta

        # Expandir o contraer la lista de widgets según el tamaño de la cinta
        while len(self.widgets_cinta) < len(self.cinta):
            etiqueta = tk.Label(ventana, font=("Arial", 14), borderwidth=2, relief="solid", width=2)
            etiqueta.grid(row=0, column=len(self.widgets_cinta))
            self.widgets_cinta.append(etiqueta)

        while len(self.widgets_cinta) > len(self.cinta):
            widget = self.widgets_cinta.pop()
            widget.destroy()

        # Actualizar los textos de los widgets para reflejar el contenido de la cinta
        for i, simbolo in enumerate(self.cinta):
            self.widgets_cinta[i].config(text=simbolo)

        # Si ya existe el widget para la cabeza, solo actualizamos su posición
        if hasattr(self, "widget_cabeza"):
            self.widget_cabeza.grid_forget()  # Ocultamos el widget actual
        else:
            # Si no existe, lo creamos
            self.widget_cabeza = tk.Label(ventana, text="▲", font=("Arial", 14), fg="red")

        # Posicionar la cabeza en la nueva ubicación
        self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)