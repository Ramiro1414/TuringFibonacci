from collections import deque

class MaquinaTuring:
    def __init__(self, estados: dict, estados_aceptadores: list, transiciones: dict, cinta: deque, estado_inicial: str, posicion_cabeza: int):
        self.estados = estados
        self.estados_aceptadores = estados_aceptadores
        self.transiciones = transiciones
        self.estado_actual = estado_inicial
        self.cinta = cinta
        self.posicion_cabeza = posicion_cabeza

    def iniciar(self):
        """Ejecuta el autómata, realizando transiciones hasta llegar a un estado aceptador o un estado de error."""
        self.imprimir_cinta()

        while True:
            simbolo_actual = self.cinta[self.posicion_cabeza]

            if (self.estado_actual, simbolo_actual) in self.transiciones:
                self.realizar_transicion(simbolo_actual)
                if self.estado_actual in self.estados_aceptadores:
                    print(f"\nAutómata ha aceptado en el estado {self.estado_actual}. Configuración de cinta al terminar:")
                    self.imprimir_cinta()
                    break
                self.imprimir_cinta()
            else:
                print("Estado de error")
                break

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
            if self.posicion_cabeza == len(self.cinta):
                self.cinta.append('▲')
        elif direccion == 'L':
            if self.posicion_cabeza == 0:
                self.cinta.appendleft('▲')
            else:
                self.posicion_cabeza -= 1

    def imprimir_cinta(self):
        """Imprime la cinta, resaltando la posición del cabezal actual."""
        cinta_con_cabeza = [
            f"[{valor}]" if i == self.posicion_cabeza else str(valor)
            for i, valor in enumerate(self.cinta)
        ]
        print(''.join(cinta_con_cabeza))
