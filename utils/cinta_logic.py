from collections import deque

def cargar_cinta_desde_archivo(archivo_csv):
    """
    Carga la cinta desde un archivo CSV que contiene la configuración de la máquina de Turing.
    Busca la línea que comienza con 'cinta;' para extraer su contenido.
    """
    cinta = None  # Variable para almacenar la cinta
    with open(archivo_csv, 'r') as archivo:
        for linea in archivo:
            # Buscar la línea que comienza con 'cinta;'
            if linea.startswith("ultima_cinta;"):
                cinta = linea.split(';', 1)[1].strip()  # Obtener el contenido después de 'cinta;'
                break

    if cinta is None:
        raise ValueError("No se encontró la cinta en el archivo CSV.")

    # Reducir los triángulos en los extremos a tres (por si acaso están mal formateados)
    cinta = cinta.lstrip('▲').rstrip('▲')  # Eliminar triángulos adicionales en los extremos
    cinta = f"▲{cinta}▲"  # Añadir exactamente tres triángulos a cada lado

    # Crear un deque a partir del contenido procesado
    return deque(cinta)


def cargar_cinta_original(archivo_csv):
    cinta = None  # Variable para almacenar la cinta
    with open(archivo_csv, 'r') as archivo:
        for linea in archivo:
            # Buscar la línea que comienza con 'cinta;'
            if linea.startswith("cinta_original;"):
                cinta = linea.split(';', 1)[1].strip()  # Obtener el contenido después de 'cinta;'
                break

    if cinta is None:
        raise ValueError("No se encontró la cinta en el archivo CSV.")

    # Reducir los triángulos en los extremos a tres (por si acaso están mal formateados)
    cinta = cinta.lstrip('▲').rstrip('▲')  # Eliminar triángulos adicionales en los extremos
    cinta = f"▲{cinta}▲"  # Añadir exactamente tres triángulos a cada lado

    # Crear un deque a partir del contenido procesado
    return deque(cinta)


def escribir_cinta_en_archivo(cinta, archivo_csv):
    """Guarda el contenido de la cinta en el archivo CSV, con exactamente 3 triángulos en cada extremo."""
    # Asegurarse de que la cinta tenga solo 3 triángulos a cada lado
    # Eliminar los triángulos extra en los extremos
    cinta_guardada = ''.join(map(str, cinta))

    # Eliminar los triángulos extra en los extremos
    cinta_guardada = cinta_guardada.lstrip('▲').rstrip('▲')

    # Añadir exactamente tres triángulos a cada lado
    cinta_guardada = f"▲{cinta_guardada}▲"

    # Abrir el archivo CSV y actualizar la línea que contiene la cinta
    with open(archivo_csv, "r") as archivo:
        lineas = archivo.readlines()

    # Buscar la línea que empieza con "cinta;"
    for i, linea in enumerate(lineas):
        if linea.startswith("ultima_cinta;"):
            lineas[i] = f"ultima_cinta;{cinta_guardada}\n"
            break

    # Guardar el archivo con la nueva cinta
    with open(archivo_csv, "w") as archivo:
        archivo.writelines(lineas)

        
def get_color_simbolo(simbolo):
    """Devuelve el color de fondo según el símbolo basado en las reglas genéricas."""
    if 'a' <= simbolo <= 'z':  # Letras minúsculas
        return '#D3F300'
    elif '0' <= simbolo <= '9':  # Números
        return '#5AB2DA'
    elif simbolo == '#':  # Símbolo específico: #
        return '#C9E9FC'
    elif simbolo == '*':  # Símbolo específico: *
        return '#E64663'
    elif simbolo == '▲':  # Símbolo específico: ▲
        return '#ADBAC0'
    elif not simbolo.isalnum():  # Cualquier carácter especial no alfanumérico
        return '#894dd1'
    else:  # Para cualquier otro caso (por ejemplo, espacio u otros caracteres desconocidos)
        return 'white'