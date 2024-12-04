from collections import deque
import tkinter as tk
from utils.cinta_logic import cargar_cinta_desde_archivo, escribir_cinta_en_archivo, get_color_simbolo, cargar_cinta_original
import tkinter.messagebox as mbox


velocidad_maquina = 50

class MaquinaTuring:
    def __init__(self, archivo_csv, estados: dict, estados_aceptadores: list, transiciones: dict, cinta: deque, estado_inicial: str, posicion_cabeza: int):
        self.estados = estados
        self.estados_aceptadores = estados_aceptadores
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.cinta = cinta
        self.posicion_cabeza = posicion_cabeza
        self.widgets_cinta = []  # Widgets que representan la cinta en la interfaz
        self.widget_cabeza = None  # Widget que representa el cabezal
        self.ajustar_espacios_cinta()  # Asegurarse de que haya 3 espacios a los extremos al inicio
        self.factor_zoom = 1  # Factor de zoom inicial
        self.archivo_csv = archivo_csv
        
        
    def cambiar_zoom(self, factor_zoom, canvas, frame_cinta):
        """Cambia el tamaño de los widgets de la cinta."""
        self.factor_zoom = factor_zoom
        self.actualizar_visualizacion(canvas, frame_cinta)

        
    def ajustar_espacios_cinta(self):
        """Asegura que siempre haya 3 espacios en los extremos de la cinta."""
        if len(self.cinta) == self.posicion_cabeza:  # Asegurar 3 espacios a la derecha
            self.cinta.append('▲')
        if self.posicion_cabeza < 0:
            self.cinta.appendleft('▲')
            self.posicion_cabeza += 1  # Ajustar posición del cabezal tras agregar a la izquierda


    def iniciar(self, canvas, frame_cinta, velocidad: int, boton_iniciar, boton_limpiar):
        """Ejecuta el autómata paso a paso utilizando Tkinter y actualiza la visualización."""
        self.actualizar_visualizacion(canvas, frame_cinta)  # Actualización final
        simbolo_actual = self.cinta[self.posicion_cabeza]

        # Deshabilitar los botones "Iniciar" y "Limpiar" al presionarlos
        boton_iniciar.config(state=tk.DISABLED)
        boton_limpiar.config(state=tk.DISABLED)

        if (self.estado_actual, simbolo_actual) in self.transiciones:
            self.realizar_transicion(simbolo_actual)
            self.ajustar_espacios_cinta()  # Verificar y ajustar los espacios después de cada movimiento
            self.actualizar_visualizacion(canvas, frame_cinta)

            if self.estado_actual in self.estados_aceptadores:
                print(f"\nAutómata ha aceptado en el estado {self.estado_actual}. Configuración de cinta al terminar:")
                self.imprimir_cinta()
                self.actualizar_visualizacion(canvas, frame_cinta)  # Actualización final
                escribir_cinta_en_archivo(self.cinta, self.archivo_csv)

                # Habilitar el botón "Limpiar" al finalizar
                boton_limpiar.config(state=tk.NORMAL)
            else:
                # Tiempo de espera dinámico ajustado según la velocidad
                canvas.after(velocidad, lambda: self.iniciar(canvas, frame_cinta, velocidad, boton_iniciar, boton_limpiar))  # Llama al siguiente paso
        else:
            print("Estado de error")
            self.mostrar_error()
            # Cuando hay un error, habilitar el botón "Limpiar" y deshabilitar "Iniciar"
            boton_limpiar.config(state=tk.NORMAL)



    def mostrar_error(self):
        """Muestra un diálogo de error si ocurre un problema con las transiciones."""
        mbox.showerror("Error", "La máquina de Turing ha encontrado un estado inválido o no tiene transición definida.")


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
        elif direccion == 'L':
            self.posicion_cabeza -= 1


    def imprimir_cinta(self):
        """Imprime la cinta, resaltando la posición del cabezal actual."""
        cinta_con_cabeza = [
            f"[{valor}]" if i == self.posicion_cabeza else str(valor)
            for i, valor in enumerate(self.cinta)
        ]
        print(''.join(cinta_con_cabeza))


   
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
   
   
    def actualizar_visualizacion(self, canvas, frame_cinta):
        """Actualiza la visualización de la cinta con colores, zoom y mantiene una posición relativa del scroll."""
        # Verificar si hay suficientes widgets en la lista
        while len(self.widgets_cinta) < len(self.cinta):
            simbolo = self.cinta[len(self.widgets_cinta)]
            etiqueta = tk.Label(
                frame_cinta,
                text=simbolo,
                font=("Arial", int(18 * self.factor_zoom)),
                borderwidth=2,
                relief="solid",
                width=4,
                height=2,
                bg=get_color_simbolo(simbolo),
            )
            etiqueta.grid(row=0, column=len(self.widgets_cinta), padx=0, pady=(50, 0))
            self.widgets_cinta.append(etiqueta)

        # Actualiza los widgets existentes
        for i, simbolo in enumerate(self.cinta):
            etiqueta = self.widgets_cinta[i]
            etiqueta.config(
                text=simbolo,
                font=("Arial", int(18 * self.factor_zoom)),
                bg=get_color_simbolo(simbolo)
            )

        # Actualizar la posición del cabezal
        if not self.widget_cabeza:
            self.widget_cabeza = tk.Label(frame_cinta, text="▲", font=("Arial", int(18 * self.factor_zoom)), fg="red")
            self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)
        else:
            self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)

        # Ajustar el área de scroll
        frame_cinta.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


        # Mantener la posición del scroll (código previo sigue siendo útil)
        self.mantener_scroll(canvas)

    def mantener_scroll(self, canvas):
        """Actualiza la región de desplazamiento solo cuando es necesario."""
        # Verificar si la posición de la cinta ha cambiado significativamente
        if self.posicion_cabeza % 10 == 0:  # Cada 10 pasos, actualiza el scroll
            canvas.config(scrollregion=canvas.bbox("all"))



    def limpiar_visualizacion(self):
        """Elimina los widgets de la cinta y el cabezal en la interfaz para limpiar la visualización."""
        # Eliminar los widgets de la cinta
        for widget in self.widgets_cinta:
            widget.grid_forget()  # Elimina el widget de la grilla
        self.widgets_cinta.clear()  # Limpiar la lista de widgets de la cinta
        
        # Eliminar el widget del cabezal
        if self.widget_cabeza:
            self.widget_cabeza.grid_forget()  # Elimina el widget del cabezal
            self.widget_cabeza = None


    # Limpiar la visualización y habilitar los botones nuevamente
    def limpiar_y_redibujar(self, canvas, frame_cinta, estado_inicial, botones_arr):
        """Limpia la visualización, recarga la cinta desde el archivo y redibuja la cinta en la interfaz."""
        self.limpiar_visualizacion()  # Limpiar los widgets actuales
        self.cinta = cargar_cinta_desde_archivo(self.archivo_csv)  # Cargar la cinta desde el archivo
        self.posicion_cabeza = 0  # Restablecer la posición del cabezal 0 HARDCODE
        self.estado_actual = estado_inicial  # Restablecer el estado inicial
        self.actualizar_visualizacion(canvas, frame_cinta)  # Redibujar la cinta con la nueva configuración
        
        botones_arr["iniciar"].config(state=tk.NORMAL)
        botones_arr["limpiar"].config(state=tk.DISABLED)
        botones_arr["cinta original"].config(state=tk.NORMAL)
        botones_arr["muy rapido"].config(state=tk.NORMAL)
        botones_arr["rapido"].config(state=tk.NORMAL)
        botones_arr["medio"].config(state=tk.NORMAL)
        botones_arr["lento"].config(state=tk.NORMAL)
        
    # Limpiar la visualización y habilitar los botones nuevamente
    def limpiar_y_redibujar_cinta_original(self, canvas, frame_cinta, estado_inicial, botones_arr):
        """Limpia la visualización, recarga la cinta desde el archivo y redibuja la cinta en la interfaz."""
        self.limpiar_visualizacion()  # Limpiar los widgets actuales
        self.cinta = cargar_cinta_original(self.archivo_csv)  # Cargar la cinta desde el archivo
        self.posicion_cabeza = 0  # Restablecer la posición del cabezal 0 HARDCODE
        self.estado_actual = estado_inicial  # Restablecer el estado inicial
        self.actualizar_visualizacion(canvas, frame_cinta)  # Redibujar la cinta con la nueva configuración
        
        botones_arr["iniciar"].config(state=tk.NORMAL)
        botones_arr["limpiar"].config(state=tk.DISABLED)
        botones_arr["muy rapido"].config(state=tk.NORMAL)
        botones_arr["rapido"].config(state=tk.NORMAL)
        botones_arr["medio"].config(state=tk.NORMAL)
        botones_arr["lento"].config(state=tk.NORMAL)

