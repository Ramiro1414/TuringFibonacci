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

def crear_control_zoom():
    """Crea un control deslizante para cambiar el zoom de la cinta."""
    control_zoom = tk.Scale(ventana, from_=0.4, to=2, orient="horizontal", resolution=0.1, label="Zoom")
    control_zoom.set(mt.factor_zoom)  # Zoom inicial se adapta al valor interno de la máquina
    control_zoom.pack(side=tk.TOP, pady=10)
    control_zoom.bind("<ButtonRelease-1>", lambda e: mt.cambiar_zoom(control_zoom.get(), canvas, frame_cinta))

crear_control_zoom()


def limpiar_cinta():
    """Limpia la cinta y habilita el botón 'Iniciar'."""
    mt.limpiar_visualizacion()  # Limpiar la visualización de la cinta
    mt.cinta = cargar_cinta_desde_archivo("cinta.txt")  # Recargar la cinta desde el archivo
    mt.posicion_cabeza = 2  # Restablecer la posición del cabezal
    mt.estado_actual = '1'  # Restablecer el estado inicial
    mt.actualizar_visualizacion(canvas, frame_cinta)  # Redibujar la cinta

    # Habilitar el botón "Iniciar" y deshabilitar el botón "Limpiar"
    boton_iniciar.config(state=tk.NORMAL)
    boton_limpiar.config(state=tk.DISABLED)

def iniciar_maquina():
    """Inicia la máquina de Turing al presionar el botón 'Iniciar'."""
    boton_iniciar.config(state=tk.DISABLED)  # Deshabilitar el botón "Iniciar"
    boton_limpiar.config(state=tk.DISABLED)  # Deshabilitar el botón "Limpiar"
    ventana.after(50, lambda: mt.iniciar(canvas, frame_cinta, velocidad_maquina, boton_iniciar, boton_limpiar))  # Llama a iniciar


# Crear un Frame para los botones "Iniciar" y "Limpiar"
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.TOP, pady=10)

# Crear el botón "Iniciar"
boton_iniciar = ttk.Button(frame_botones, text="Iniciar", command=iniciar_maquina, style="TButton")
boton_iniciar.pack(side=tk.LEFT, padx=10)  # El botón "Iniciar" está a la derecha

# Crear el botón "Limpiar Cinta"
boton_limpiar = ttk.Button(frame_botones, text="Limpiar Cinta", command=limpiar_cinta, style="TButton")
boton_limpiar.pack(side=tk.LEFT, padx=10)  # El botón "Limpiar" está a la izquierda
boton_limpiar.config(state=tk.DISABLED)  # Inicialmente deshabilitado


# Definir las velocidades
velocidades = {
    "Muy rápido": 10,
    "Rápido": 50,
    "Medio": 100,
    "Lento": 500
}

# Label para mostrar la velocidad seleccionada
label_velocidad = tk.Label(ventana, text="Velocidad: Medio", font=("Arial", 12))
label_velocidad.pack(side=tk.TOP, pady=5)

# Variable para almacenar la velocidad seleccionada
velocidad_maquina = velocidades["Medio"]

# Función para actualizar la velocidad
def cambiar_velocidad(velocidad, texto):
    global velocidad_maquina
    velocidad_maquina = velocidad
    label_velocidad.config(text=f"Velocidad: {texto}")

# Crear un Frame para los botones de velocidad
frame_velocidades = tk.Frame(ventana)
frame_velocidades.pack(side=tk.TOP, pady=10)

# Botones para cambiar la velocidad (en línea)
boton_muy_rapido = ttk.Button(frame_velocidades, text="Muy rápido", command=lambda: cambiar_velocidad(velocidades["Muy rápido"], "Muy rápido"))
boton_muy_rapido.grid(row=0, column=0, padx=5)

boton_rapido = ttk.Button(frame_velocidades, text="Rápido", command=lambda: cambiar_velocidad(velocidades["Rápido"], "Rápido"))
boton_rapido.grid(row=0, column=1, padx=5)

boton_medio = ttk.Button(frame_velocidades, text="Medio", command=lambda: cambiar_velocidad(velocidades["Medio"], "Medio"))
boton_medio.grid(row=0, column=2, padx=5)

boton_lento = ttk.Button(frame_velocidades, text="Lento", command=lambda: cambiar_velocidad(velocidades["Lento"], "Lento"))
boton_lento.grid(row=0, column=3, padx=5)

def dibujar_cinta_inicial(tamano_fuente=18):
    """Dibuja la cinta inicial con el cabezal en su posición inicial y un tamaño de fuente variable."""
    for i, simbolo in enumerate(cinta):
        etiqueta = tk.Label(
            frame_cinta,
            text=simbolo,
            font=("Arial", 18),  # Mantén el tamaño de la fuente uniforme
            borderwidth=2,
            relief="solid",
            width=4,
            height=2  # Tamaño uniforme
        )
        etiqueta.grid(row=0, column=i, padx=0, pady=(50, 0))
        mt.widgets_cinta.append(etiqueta)

    # Crear el cabezal en su posición inicial, pegado a la cinta
    mt.widget_cabeza = tk.Label(frame_cinta, text="▲", font=("Arial", int(tamano_fuente * mt.factor_zoom)), fg="red")
    mt.widget_cabeza.grid(row=1, column=mt.posicion_cabeza, padx=0, pady=0)

# Llamar a la función para dibujar la cinta inicial al abrir la ventana
dibujar_cinta_inicial()



# Estilo de los botones
style = ttk.Style()
style.configure("TButton",
                font=("Arial", 14),
                padding=10,
                relief="flat",
                background="#4CAF50",  # Color verde
                foreground="white")

# Configuración del hover: color gris oscuro cuando el mouse esté sobre el botón
style.map("TButton",
          background=[('active', '#45a049'),  # Gris oscuro cuando está activado (hover)
                      ('!active', '#4CAF50')])  # Color verde cuando no está activado

ventana.mainloop()
