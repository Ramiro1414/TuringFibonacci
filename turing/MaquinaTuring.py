from collections import deque
import tkinter as tk

class MaquinaTuring:
    def __init__(self, estados: dict, estados_aceptadores: list, transiciones: dict, cinta: deque, estado_inicial: str, posicion_cabeza: int):
        self.estados = estados
        self.estados_aceptadores = estados_aceptadores
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.cinta = cinta
        self.posicion_cabeza = posicion_cabeza
        self.widgets_cinta = []  # Widgets que representan la cinta en la interfaz
        self.widget_cabeza = None  # Widget que representa el cabezal
        self.ajustar_espacios_cinta()  # Asegurarse de que haya 3 espacios a los extremos al inicio

    def ajustar_espacios_cinta(self):
        """Asegura que siempre haya 3 espacios en los extremos de la cinta."""
        while len(self.cinta) - self.posicion_cabeza <= 3:  # Asegurar 3 espacios a la derecha
            self.cinta.append('▲')
        while self.posicion_cabeza < 3:  # Asegurar 3 espacios a la izquierda
            self.cinta.appendleft('▲')
            self.posicion_cabeza += 1  # Ajustar posición del cabezal tras agregar a la izquierda

    def iniciar(self, canvas, frame_cinta, velocidad: int, boton_iniciar):
        """Ejecuta el autómata paso a paso utilizando Tkinter y actualiza la visualización."""
        simbolo_actual = self.cinta[self.posicion_cabeza]

        # Deshabilitar el botón "Iniciar" al presionarlo
        boton_iniciar.config(state=tk.DISABLED)

        if (self.estado_actual, simbolo_actual) in self.transiciones:
            self.realizar_transicion(simbolo_actual)
            self.ajustar_espacios_cinta()  # Verificar y ajustar los espacios después de cada movimiento
            self.actualizar_visualizacion(canvas, frame_cinta)

            if self.estado_actual in self.estados_aceptadores:
                print(f"\nAutómata ha aceptado en el estado {self.estado_actual}. Configuración de cinta al terminar:")
                self.imprimir_cinta()
                self.actualizar_visualizacion(canvas, frame_cinta)  # Actualización final
            else:
                canvas.after(velocidad, lambda: self.iniciar(canvas, frame_cinta, velocidad, boton_iniciar))  # Llama al siguiente paso
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
        elif direccion == 'L':
            self.posicion_cabeza -= 1

    def imprimir_cinta(self):
        """Imprime la cinta, resaltando la posición del cabezal actual."""
        cinta_con_cabeza = [
            f"[{valor}]" if i == self.posicion_cabeza else str(valor)
            for i, valor in enumerate(self.cinta)
        ]
        print(''.join(cinta_con_cabeza))

    def actualizar_visualizacion(self, canvas, frame_cinta):
        """Actualiza la cinta y el cabezal en la interfaz gráfica sin destruir todo."""
        # Actualizar los widgets de la cinta
        if not self.widgets_cinta:  # Crear los widgets solo la primera vez
            for i, simbolo in enumerate(self.cinta):
                etiqueta = tk.Label(frame_cinta, text=simbolo, font=("Arial", 16), borderwidth=2, relief="solid", width=2, height=1)
                etiqueta.grid(row=0, column=i, padx=2, pady=2)
                self.widgets_cinta.append(etiqueta)
        else:  # Actualizar el texto de los widgets existentes
            for i, simbolo in enumerate(self.cinta):
                if i < len(self.widgets_cinta):
                    self.widgets_cinta[i].config(text=simbolo)
                else:  # Si la cinta crece, agregar nuevos widgets
                    etiqueta = tk.Label(frame_cinta, text=simbolo, font=("Arial", 16), borderwidth=2, relief="solid", width=2, height=1)
                    etiqueta.grid(row=0, column=i, padx=2, pady=2)
                    self.widgets_cinta.append(etiqueta)

        # Actualizar la posición del cabezal
        if not self.widget_cabeza:
            self.widget_cabeza = tk.Label(frame_cinta, text="▲", font=("Arial", 16), fg="red")
            self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)
        else:
            self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)

        # Calcular el espacio disponible y centrar la cinta si es necesario
        canvas.update_idletasks()  # Actualiza las dimensiones internas
        canvas_width = canvas.winfo_width()  # Ancho del canvas
        cinta_width = frame_cinta.winfo_width()  # Ancho del frame que contiene la cinta

        # Si la cinta es más pequeña que el canvas, centrarla horizontalmente
        if cinta_width < canvas_width:
            x_offset = (canvas_width - cinta_width) / 2  # Calcular desplazamiento para centrar
            canvas.xview_moveto(x_offset / canvas_width)  # Mover el scroll horizontalmente
        else:
            canvas.xview_moveto(0)  # Asegurarse de que el scroll esté habilitado si la cinta es mayor

        # Actualizar la barra de scroll solo si la cinta se extiende
        frame_cinta.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Centrar la cinta también verticalmente
        canvas_height = canvas.winfo_height()  # Altura del canvas
        cinta_height = frame_cinta.winfo_height()  # Altura del frame de la cinta

        if cinta_height < canvas_height:
            y_offset = (canvas_height - cinta_height) / 2  # Desplazamiento vertical
            canvas.yview_moveto(y_offset / canvas_height)  # Mover el scroll verticalmente
        else:
            canvas.yview_moveto(0)  # Asegurarse de que el scroll esté habilitado si la cinta es mayor
