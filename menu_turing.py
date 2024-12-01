import tkinter as tk
from tkinter import filedialog, messagebox
import os

global label_archivo

# Función para seleccionar un archivo
def seleccionar_archivo():
    global archivo_seleccionado

    archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    if archivo:
        #print(f"Archivo seleccionado: {os.path.basename(archivo)}")
        label_archivo.config(text=f"Máquina seleccionada: {os.path.basename(archivo)}")
        archivo_seleccionado = os.path.basename(archivo)
        boton_crear.config(state="disabled")
        boton_olvidar_maquina.pack()
        boton_cargar_maquina.pack()

# Función para copiar al portapapeles utilizando tkinter (sin pyperclip)
def copiar_al_portapapeles():
    ventana.clipboard_clear()  # Limpiar el portapapeles
    ventana.clipboard_append("▲")  # Copiar el carácter ▲ al portapapeles

# Función para crear la tabla inicial
def crear_maquina():
    global tabla, filas, columnas
    filas, columnas = 1, 5  # Dimensiones iniciales
    tabla = []

    boton_archivo.config(state="disabled")
    boton_guardar.pack()

    # Crear encabezado no editable
    encabezados = ["Estado origen", "Leo de cinta", "Escribo en cinta", "Acción", "Estado destino"]
    for col, texto in enumerate(encabezados):
        etiqueta = tk.Label(frame_tabla, text=texto, bg="lightgray", font=("Arial", 10, "bold"), borderwidth=1, relief="solid")
        etiqueta.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    # Crear una fila editable
    for i in range(filas):
        fila = []
        for j in range(columnas):
            celda = tk.Entry(frame_tabla, width=15)
            celda.grid(row=i + 1, column=j, padx=5, pady=5)
            fila.append(celda)
        tabla.append(fila)

    # Deshabilitar el botón de crear máquina
    boton_agregar_fila.config(state="normal")
    boton_crear.config(state="disabled")
    boton_guardar.config(state="normal")

    # Crear campos para los valores adicionales
    crear_campos_adicionales()

def olvidar_maquina():
    archivo_seleccionado = None
    boton_olvidar_maquina.pack_forget()
    label_archivo.config(text="No se ha seleccionado una maquina de turing")
    boton_cargar_maquina.pack_forget()
    boton_crear.config(state="normal")
    boton_agregar_fila.config(state="normal")

# Función para crear campos adicionales
def crear_campos_adicionales():
    global entry_estado_inicial, entry_estado_aceptador, entry_nombre_maquina, entry_cinta

    # Etiquetas y campos para "Estado inicial"
    lbl_estado_inicial = tk.Label(frame_campos, text="Estado inicial:")
    lbl_estado_inicial.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_estado_inicial = tk.Entry(frame_campos, width=20)
    entry_estado_inicial.grid(row=0, column=1, padx=5, pady=5)

    # Etiquetas y campos para "Estado aceptador"
    lbl_estado_aceptador = tk.Label(frame_campos, text="Estado aceptador:")
    lbl_estado_aceptador.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_estado_aceptador = tk.Entry(frame_campos, width=20)
    entry_estado_aceptador.grid(row=2, column=1, padx=5, pady=5)

    # Etiquetas y campos para "Nombre de la maquina"
    lbl_nombre_maquina = tk.Label(frame_campos, text="Nombre de la máquina:")
    lbl_nombre_maquina.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_nombre_maquina = tk.Entry(frame_campos, width=20)
    entry_nombre_maquina.grid(row=3, column=1, padx=5, pady=5)

    # Etiquetas y campos para "Cinta"
    lbl_cinta = tk.Label(frame_campos, text="Contenido de la cinta:")
    lbl_cinta.grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_cinta = tk.Entry(frame_campos, width=20)
    entry_cinta.grid(row=4, column=1, padx=5, pady=5)

# Función para agregar una fila editable
def agregar_fila():
    global filas
    fila = []
    for j in range(columnas):
        celda = tk.Entry(frame_tabla, width=15)
        celda.grid(row=filas + 1, column=j, padx=5, pady=5)
        fila.append(celda)
    tabla.append(fila)
    filas += 1

def cargar_maquina():
    print("Maquina cargada")

def validar_tabla(tabla):
    """
    Valida si todas las celdas de una tabla (compuesta de widgets Entry) contienen valores no vacíos.
    :param tabla: Lista de listas con widgets Entry.
    :return: True si la tabla es válida, False si hay celdas vacías.
    """
    for fila_idx, fila in enumerate(tabla):
        for col_idx, celda in enumerate(fila):
            if not celda.get().strip():  # Obtener contenido y verificar si está vacío
                return False
    return True  # Si todas las celdas tienen contenido, devuelve True

def validar_columna_movimiento(tabla):
    """
    Valida que las celdas de la cuarta columna contengan valores válidos ('R', 'L', 'N').
    :param tabla: Lista de listas con widgets Entry.
    :return: True si la columna es válida, False si hay valores inválidos.
    """
    for fila_idx, fila in enumerate(tabla):
        if len(fila) < 4:  # Asegurarse de que la fila tiene al menos 4 columnas
            return False
        celda = fila[3]  # Cuarta columna (índice 3)
        valor = celda.get().strip()  # Obtener el contenido de la celda
        if valor not in {'R', 'L', 'N'}:  # Verificar si es uno de los valores permitidos
            return False
    return True  # Todas las celdas de la cuarta columna son válidas

def validar_estado_inicial(tabla, estado_inicial):
    """
    Verifica si el estado inicial se encuentra en la primera columna (estados de origen).
    :param tabla: Lista de listas con widgets Entry (representando la tabla).
    :param estado_inicial: Estado inicial a buscar.
    :return: True si el estado inicial está en la primera columna, False de lo contrario.
    """
    for fila_idx, fila in enumerate(tabla):
        if len(fila) > 0:  # Asegurarse de que la fila tiene al menos una columna
            estado_origen = fila[0].get().strip()  # Obtener valor de la primera columna
            if estado_origen == estado_inicial:
                return True  # Estado inicial encontrado
    return False  # Estado inicial no encontrado


# Función para guardar los datos y cargar la maquina creada
def guardar_datos():

    # Obtener valores de los campos
    estado_inicial = entry_estado_inicial.get()
    estado_aceptador = entry_estado_aceptador.get()
    nombre_maquina = entry_nombre_maquina.get()
    archivo_estados = f"estados_{nombre_maquina}.csv"
    cinta = entry_cinta.get()

    tabla_valida_sin_vacios = validar_tabla(tabla)
    tabla_valida_columna_movimiento = validar_columna_movimiento(tabla)

    if not tabla_valida_sin_vacios:
        messagebox.showerror("Error", "Hay celdas vacias en la tabla.")
        return
    
    if not tabla_valida_columna_movimiento:
        messagebox.showerror("Error", "Las celdas de la columna de movimiento deben ser 'R', 'L' o 'N'.")
        return

    if not estado_inicial.strip():
        messagebox.showerror("Error", "El campo 'Estado inicial' está vacío.")
        return
    
    estado_inicial_en_primera_columna = validar_estado_inicial(tabla, estado_inicial)
    if not estado_inicial_en_primera_columna:
        messagebox.showerror("Error", "El estado inicial debe estar al menos una vez en la columna de 'estados de origen'.")
        return
    
    if not estado_aceptador.strip():
        messagebox.showerror("Error", "El campo 'Estado aceptador' está vacío.")
        return

    # Validar nombre de la máquina
    if not nombre_maquina.strip():
        messagebox.showerror("Error", "El campo 'Nombre de la máquina' está vacío.")
        return
    
    if not cinta.strip():
        respuesta = messagebox.askokcancel(
            "Atención",
            "Si el campo 'Contenido de la cinta' está vacío, la cinta contendrá solo espacios vacíos. ¿Deseas continuar?"
        )
        if not respuesta:  # Si el usuario selecciona "Cancelar"
            return

    # Crear el contenido inicial del archivo
    contenido = (
        "# Configuración de la máquina de Turing\n"
        f"estado_inicial;{estado_inicial}\n"
        f"posicion_cabeza;{0}\n"
        f"archivo_estados;{archivo_estados}\n\n"
        "# Transiciones\n"
    )

    # Agregar contenido de la tabla (transiciones)
    for fila in tabla:
        valores = [celda.get() for celda in fila]  # Obtener valores de cada celda
        contenido += ";".join(valores) + "\n"  # Unir valores por ';' y agregar nueva línea

    # Guardar el archivo de la máquina de Turing
    try:
        with open(f"{nombre_maquina}.csv", "w") as archivo:
            archivo.write(contenido)
        print(f"Archivo '{nombre_maquina}.csv' guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

    # Generar el archivo de estados
    estados = set()  # Usamos un conjunto para evitar estados repetidos

    # Recorremos la primera columna para obtener los estados
    for fila in tabla:
        estado = fila[0].get()  # Estado está en la primera columna
        estados.add(estado)

    # Crear el contenido del archivo de estados
    contenido_estados = ""

    estados_aceptadores = [estado.strip() for estado in estado_aceptador.split(",")]

    # Variable para controlar si algún estado aceptador fue agregado
    estado_agregado = False

    # Crear el contenido de los estados
    contenido_estados = ""
    for estado in estados:
        if estado in estados_aceptadores:
            contenido_estados += f"{estado};1\n"  # Estado aceptador lleva '1'
            estado_agregado = True
        else:
            contenido_estados += f"{estado};0\n"  # Los demás estados llevan '0'

    # Verificar si algún estado aceptador no estaba en la tabla
    for estado_acept in estados_aceptadores:
        if estado_acept not in estados:
            contenido_estados += f"{estado_acept};1\n"  # Agregar el estado aceptador faltante

    # Guardar el archivo de estados
    try:
        with open(archivo_estados, "w") as archivo:
            archivo.write(contenido_estados)
        print(f"Archivo '{archivo_estados}' guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo de estados: {e}")

    # Guardar la cadena de la cinta en 'cinta.txt'
    try:
        with open("cinta.txt", "w") as archivo_cinta:
            archivo_cinta.write(cinta)  # Escribir el contenido de 'cinta'
        print("Archivo 'cinta.txt' guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar 'cinta.txt': {e}")

# Crear la ventana principal
ventana = tk.Tk()

# Configuración de la ventana
ventana.title("Simulador de Máquina de Turing")

# Obtener dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Establecer el tamaño de la ventana al tamaño de la pantalla
ventana.geometry(f"{ancho_pantalla}x{alto_pantalla}")

# Botón para seleccionar un archivo
boton_archivo = tk.Button(ventana, text="Seleccionar máquina", command=seleccionar_archivo)
boton_archivo.pack(pady=10)

# Label para mostrar el nombre del archivo seleccionado
label_archivo = tk.Label(ventana, text="No se ha seleccionado una maquina de turing")
label_archivo.pack(pady=10)

# Botón para seleccionar un archivo
boton_olvidar_maquina = tk.Button(ventana, text="Olvidar máquina", command=olvidar_maquina, bg="red", fg="white")
boton_olvidar_maquina.pack(pady=10)
boton_olvidar_maquina.pack_forget()

# Botón para seleccionar un archivo
boton_cargar_maquina = tk.Button(ventana, text="Cargar máquina", command=cargar_maquina, bg="lime green", fg="white")
boton_cargar_maquina.pack(pady=10)
boton_cargar_maquina.pack_forget()

# Frame para la tabla
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)

# Frame para los campos adicionales
frame_campos = tk.Frame(ventana)
frame_campos.pack(pady=10)

# Botón para crear la tabla
boton_crear = tk.Button(ventana, text="Crear máquina", command=crear_maquina)
boton_crear.pack(pady=5)

# Botones para agregar filas y columnas
boton_agregar_fila = tk.Button(ventana, text="Agregar fila", command=agregar_fila)
boton_agregar_fila.pack(pady=5)
boton_agregar_fila.config(state="disabled")

# Crear un botón que copie el carácter '▲' al portapapeles
boton_copiar = tk.Button(ventana, text="Copiar ▲ (espacio) al portapapeles", command=copiar_al_portapapeles)
boton_copiar.pack(pady=10)

# Botón "Guardar"
boton_guardar = tk.Button(ventana, text="Guardar y cargar maquina", command=guardar_datos, bg="green", fg="white", font=("Arial", 12, "bold"))
boton_guardar.pack(pady=20)
boton_guardar.pack_forget()

# Variables globales para la tabla
tabla = []
filas = 0
columnas = 0

# Bucle principal de la aplicación
ventana.mainloop()