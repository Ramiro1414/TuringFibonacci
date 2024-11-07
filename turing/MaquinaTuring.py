from collections import deque

class MaquinaTuring:
    def __init__(self, estados: dict, estados_aceptadores: list, transiciones: dict, cinta: deque):
        self.cinta = deque()
        self.estados = estados
        self.estados_aceptadores = estados_aceptadores
        self.transiciones = transiciones
        self.estado_actual = '1' # HARDCODED. Pero siempre deberia ser el estado 1 por convencion
        self.cinta = cinta
        self.posicion_cabeza = 0

    def iniciar(self):

        self.imprimirCinta()

        while True:
            # Se obtiene el símbolo actual en la cinta
            simbolo_actual = self.cinta[self.posicion_cabeza]

            # Verificamos si hay una transición disponible para el estado actual y el símbolo leído
            if (self.estado_actual, simbolo_actual) in self.transiciones:
                # Obtenemos las acciones de la transición
                transicion = self.transiciones[(self.estado_actual, simbolo_actual)]
                
                # Escribir el nuevo símbolo en la cinta
                self.cinta[self.posicion_cabeza] = transicion['escribir']
                
                # Mover el cabezal
                if transicion['movimiento'] == 'R':
                    self.posicion_cabeza += 1
                elif transicion['movimiento'] == 'L':
                    self.posicion_cabeza -= 1

                #print(self.posicion_cabeza)

                # Cambiar al estado destino
                self.estado_actual = transicion['destino']

                # Verificar si estamos en un estado aceptador
                if self.estado_actual in self.estados_aceptadores:
                    print(f"Autómata ha aceptado en el estado {self.estado_actual}.")
                    break

                # Imprimir la cinta después de la operación
                self.imprimirCinta()
            else:
                # Si no hay transiciones, el autómata se detiene
                print("Estado de error")
                break
    
    def imprimirCinta(self):
        # Usamos la posición de la cabeza para agregar los corchetes
        cinta_con_cabeza = []
        for i, valor in enumerate(self.cinta):
            if i == self.posicion_cabeza:
                cinta_con_cabeza.append(f"[{valor}]")  # Añadir corchetes alrededor del valor
            else:
                cinta_con_cabeza.append(str(valor))
        # Unimos la lista en una cadena y la imprimimos
        print(''.join(cinta_con_cabeza))

    def moverDerecha(self):
        self.posicion_cabeza += 1

    def moverIzquierda(self):
        self.posicion_cabeza -= 1