from utils.csv_reader import leer_archivo_estados, leer_archivo_transiciones, encontrar_estados_aceptadores
from turing.MaquinaTuring import MaquinaTuring
import tkinter as tk
from tkinter import ttk
from collections import deque

def cargar_cinta_desde_archivo(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read().strip()  # Leer el contenido y eliminar espacios en blanco alrededor
    
    # Reducir los triángulos en los extremos a tres
    contenido = contenido.lstrip('▲').rstrip('▲')  # Eliminar todos los triángulos de ambos extremos
    contenido = f"▲▲▲{contenido}▲▲▲"  # Añadir exactamente tres triángulos a cada lado

    # Crear el deque a partir del contenido procesado
    cinta = deque(contenido)
    return cinta

# Ejemplo de uso
#cinta = cargar_cinta_desde_archivo("cinta.txt")
#print("".join(cinta))  # Imprime el resultado procesado


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

# Ventana principal
ventana = tk.Tk()
ventana.title("Máquina de Turing")

# Maximizar la ventana utilizando el tamaño de la pantalla disponible
ventana.attributes('-fullscreen', False)  # Desactivar pantalla completa
ventana.geometry(f"{ventana.winfo_screenwidth()}x{ventana.winfo_screenheight()}")  # Establecer el tamaño de la ventana al tamaño de la pantalla

# Crear un canvas y un frame para la cinta
canvas = tk.Canvas(ventana)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(ventana, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

canvas.configure(xscrollcommand=scrollbar.set)

# Frame que contiene la cinta
frame_cinta = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_cinta, anchor="nw")  # Ancla superior izquierda para la cinta

def centrar_cinta():
    """Centrar la cinta horizontal y verticalmente."""
    canvas.update_idletasks()  # Actualiza las dimensiones internas
    canvas_width = canvas.winfo_width()  # Ancho del canvas
    canvas_height = canvas.winfo_height()  # Alto del canvas
    cinta_width = frame_cinta.winfo_width()  # Ancho del frame que contiene la cinta
    cinta_height = frame_cinta.winfo_height()  # Alto del frame de la cinta

    # Calcular el desplazamiento horizontal y vertical para centrar la cinta
    if cinta_width < canvas_width:
        x_offset = (canvas_width - cinta_width) / 2  # Desplazamiento horizontal
        canvas.xview_moveto(x_offset / canvas_width)  # Mover el scroll horizontalmente
    else:
        canvas.xview_moveto(0)  # Asegurarse de que el scroll esté habilitado si la cinta es mayor

    if cinta_height < canvas_height:
        y_offset = (canvas_height - cinta_height) / 2  # Desplazamiento vertical
        canvas.yview_moveto(y_offset / canvas_height)  # Mover el scroll verticalmente
    else:
        canvas.yview_moveto(0)  # Asegurarse de que el scroll esté habilitado si la cinta es mayor

# Vincular redimensionado a la función de centrado
ventana.bind("<Configure>", lambda e: centrar_cinta())

def dibujar_cinta_inicial():
    """Dibuja la cinta inicial con el cabezal en su posición inicial."""
    # Crear los widgets de la cinta
    for i, simbolo in enumerate(cinta):
        etiqueta = tk.Label(frame_cinta, text=simbolo, font=("Arial", 16), borderwidth=2, relief="solid", width=2, height=1)
        etiqueta.grid(row=0, column=i, padx=2, pady=2)
        mt.widgets_cinta.append(etiqueta)

    # Crear el cabezal en su posición inicial
    mt.widget_cabeza = tk.Label(frame_cinta, text="▲", font=("Arial", 16), fg="red")
    mt.widget_cabeza.grid(row=1, column=mt.posicion_cabeza)

# Llamar a la función para dibujar la cinta inicial al abrir la ventana
dibujar_cinta_inicial()

def iniciar_maquina():
    """Inicia la máquina de Turing al presionar el botón 'Iniciar'."""
    velocidad_maquina = 100  # En milisegundos
    boton_iniciar.config(state=tk.DISABLED)  # Deshabilitar el botón
    ventana.after(100, lambda: mt.iniciar(canvas, frame_cinta, velocidad_maquina, boton_iniciar))  # Llama a iniciar


# Botón para iniciar la ejecución de la máquina de Turing
boton_iniciar = tk.Button(ventana, text="Iniciar", command=iniciar_maquina, font=("Arial", 14))
boton_iniciar.pack(side=tk.TOP, pady=20)

ventana.mainloop()
