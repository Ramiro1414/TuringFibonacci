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
        self.factor_zoom = 1  # Factor de zoom inicial
        
    def cambiar_zoom(self, factor_zoom, canvas, frame_cinta):
        """Cambia el tamaño de los widgets de la cinta."""
        self.factor_zoom = factor_zoom
        self.actualizar_visualizacion(canvas, frame_cinta)

        
    def ajustar_espacios_cinta(self):
        """Asegura que siempre haya 3 espacios en los extremos de la cinta."""
        while len(self.cinta) - self.posicion_cabeza <= 3:  # Asegurar 3 espacios a la derecha
            self.cinta.append('▲')
        while self.posicion_cabeza < 3:  # Asegurar 3 espacios a la izquierda
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
                self.escribir_cinta_en_archivo()

                # Habilitar el botón "Limpiar" al finalizar
                boton_limpiar.config(state=tk.NORMAL)
            else:
                canvas.after(velocidad, lambda: self.iniciar(canvas, frame_cinta, velocidad, boton_iniciar, boton_limpiar))  # Llama al siguiente paso
        else:
            print("Estado de error")
            # Cuando hay un error, habilitar el botón "Limpiar" y deshabilitar "Iniciar"
            boton_limpiar.config(state=tk.NORMAL)



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

    def escribir_cinta_en_archivo(self):
        """Guarda el contenido de la cinta en el archivo cinta.txt, con exactamente 3 triángulos en cada extremo."""
        # Asegurarse de que la cinta tenga solo 3 triángulos a cada lado
        # Eliminar cualquier triángulo adicional
        cinta_guardada = ''.join(map(str, self.cinta))

        # Eliminar los triángulos extra en los extremos
        cinta_guardada = cinta_guardada.lstrip('▲').rstrip('▲')

        # Añadir exactamente tres triángulos a cada lado
        cinta_guardada = f"▲▲▲{cinta_guardada}▲▲▲"

        # Abrir el archivo en modo escritura (borrará su contenido previo)
        with open("cinta.txt", "w") as archivo:
            archivo.write(cinta_guardada)

    def actualizar_visualizacion(self, canvas, frame_cinta):
        """Actualiza la visualización de la cinta con el zoom en el canvas y las etiquetas."""        
        # Aplicar el zoom al canvas, escalando el contenido
        # canvas.scale("all", 0, 0, self.factor_zoom, self.factor_zoom)  # Comentado porque los widgets están fuera del canvas
        
        # Redibujar los widgets de la cinta (etiquetas) con el nuevo tamaño de fuente
        for i, simbolo in enumerate(self.cinta):
            etiqueta = self.widgets_cinta[i] if i < len(self.widgets_cinta) else None
            if etiqueta:
                etiqueta.config(text=simbolo, font=("Arial", int(18 * self.factor_zoom)))
            else:
                etiqueta = tk.Label(frame_cinta, text=simbolo, font=("Arial", int(18 * self.factor_zoom)), borderwidth=2, relief="solid", width=4, height=2)
                etiqueta.grid(row=0, column=i, padx=0, pady=(50, 0))
                self.widgets_cinta.append(etiqueta)

        # Actualizar la posición del cabezal
        if not self.widget_cabeza:
            self.widget_cabeza = tk.Label(frame_cinta, text="▲", font=("Arial", int(18 * self.factor_zoom)), fg="red")
            self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)
        else:
            self.widget_cabeza.grid(row=1, column=self.posicion_cabeza)

        # Ajuste del scroll
        frame_cinta.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Ajustar el canvas (en términos de scroll)
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        cinta_width = frame_cinta.winfo_width()
        cinta_height = frame_cinta.winfo_height()

        # Si la cinta es más pequeña que el canvas, centrarla horizontalmente
        if cinta_width < canvas_width:
            x_offset = (canvas_width - cinta_width) / 2  # Calcular desplazamiento para centrar
            canvas.xview_moveto(x_offset / canvas_width)  # Mover el scroll horizontalmente
        else:
            canvas.xview_moveto(0)  # Asegurarse de que el scroll esté habilitado si la cinta es mayor

        # Centrado vertical
        if cinta_height < canvas_height:
            y_offset = (canvas_height - cinta_height) / 2
            canvas.yview_moveto(y_offset / canvas_height)
        else:
            canvas.yview_moveto(0)

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


    def cargar_cinta_desde_archivo(self, archivo):
        """Carga la cinta desde el archivo, asegurándose de que haya exactamente 3 triángulos en cada extremo."""
        with open(archivo, 'r') as f:
            contenido = f.read().strip()  # Leer el contenido y eliminar espacios en blanco alrededor

        # Eliminar los triángulos adicionales en los extremos (si hay más de 3)
        contenido = contenido.lstrip('▲').rstrip('▲')

        # Asegurarse de que haya exactamente tres triángulos en cada extremo
        contenido = f"▲▲▲{contenido}▲▲▲"

        # Crear el deque a partir del contenido procesado
        cinta = deque(contenido)
        return cinta

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
    def limpiar_y_redibujar(self, canvas, frame_cinta, boton_iniciar, boton_limpiar):
        """Limpia la visualización, recarga la cinta desde el archivo y redibuja la cinta en la interfaz."""
        self.limpiar_visualizacion()  # Limpiar los widgets actuales
        self.cinta = self.cargar_cinta_desde_archivo("cinta.txt")  # Cargar la cinta desde el archivo
        self.posicion_cabeza = 2  # Restablecer la posición del cabezal
        self.estado_actual = '1'  # Restablecer el estado inicial
        self.actualizar_visualizacion(canvas, frame_cinta)  # Redibujar la cinta con la nueva configuración
        boton_iniciar.config(state=tk.NORMAL)  # Habilitar el botón "Iniciar" nuevamente
        boton_limpiar.config(state=tk.NORMAL)  # Habilitar el botón "Limpiar" después de que se termine

