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
        
        
def get_color_simbolo(simbolo):
    """Devuelve el color de fondo según el símbolo."""
    colores = {
    '0': 'lightgreen',
    '1': 'lightgreen',
    '#': 'orange',
    '▲': 'darkgray',
    '*': 'violet',
    }
    return colores.get(simbolo, 'white')  # Por defecto, blanco