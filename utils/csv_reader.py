""" Clase para leer el contenido de los archivos transiciones_automata.csv y estados_automata.csv """

import csv

def leer_archivo_transiciones(csv_filename: str):
    """
    Lee un archivo .csv delimitado con ';'.
    * La primer columna contiene el estado de origin del automata.
    * La segunda columna contiene el valor que se lee de la cinta.
    * La tercera columna contiene el valor que se escribe en la cinta.
    * La cuarta columna contiene el movimiento que se realiza en la cinta (R derecha o L izquierda).
    * La quinta columna contiene el estado de destino del automata.
    """
    transiciones = {}
    with open(csv_filename, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=';')
        for fila in lector_csv:
            estado_origen = (fila[0])
            valor_leido = fila[1]
            valor_escribir = fila[2]
            movimiento = fila[3]
            estado_destino = fila[4]

            # Añadimos la transición al diccionario
            transiciones[(estado_origen, valor_leido)] = {
                'escribir': valor_escribir,
                'movimiento': movimiento,
                'destino': estado_destino
            }
    return transiciones

def leer_archivo_estados(csv_filename: str):
    """
    Lee un archivo .csv delimitado con ';' donde la primer columna tiene el nombre del estado y la segunda columna indica si el estado es aceptador o no.
    El valor 0 indica que no es aceptador y el valor 1 indica que es aceptador.

    Args:
        csv_filename (str): la ruta del archivo que se quiere leer.

    Returns:
        dict: un diccionario donde las claves indican los nombres de los estados y los valores indican si esos estado son aceptadores o no.
    """

    estados = {}
    with open(csv_filename, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=';')  # Especifica el delimitador
        for fila in lector_csv:
            estado = fila[0]  # Primer columna como clave (estado)
            es_aceptador = int(fila[1])  # Segunda columna como valor (0 o 1)
            estados[estado] = es_aceptador  # Agrega el estado y si es aceptador al diccionario
    return estados

def encontrar_estados_aceptadores(diccionario_estados: dict):
    estados_aceptadores = []
    for estado, es_aceptador in diccionario_estados.items():
        if es_aceptador == 1:
            estados_aceptadores.append(estado)
    
    return estados_aceptadores