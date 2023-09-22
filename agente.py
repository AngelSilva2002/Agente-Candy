# Convención de colores:
"""
    G = Verde
    R = Rojo
    O = Naranja
    Y = Amarillo
    B = Azul
    P = Morado

    S = Verde a rayas
    T = Rojo a rayas
    U = Naranja a rayas
    V = Amarillo a rayas
    W = Azul a rayas
    X = Morado a rayas

    A = Verde envuelto
    C = Rojo envuelto
    D = Naranja envuelto
    E = Amarillo envuelto
    F = Azul envuelto
    I = Morado envuelto

    J = Bomba de color
"""

# Matriz de prueba
candies_matrix = [
    ['Y', 'Y', 'R', 'O', 'O', 'G', 'G', 'G', 'B'],
    ['O', 'O', 'O', 'G', 'R', 'B', 'R', 'O', 'B'],
    ['G', 'O', 'Y', 'R', 'Y', 'R', 'Y', 'Y', 'O'],
    ['Y', 'Y', 'R', 'G', 'Y', 'Y', 'O', 'Y', 'B'],
    ['Y', 'G', 'O', 'Y', 'Y', 'Y', 'Y', 'Y', 'R'],
    ['Y', 'Y', 'Y', 'R', 'Y', 'R', 'Y', 'B', 'B'],
    ['Y', 'G', 'Y', 'Y', 'G', 'R', 'Y', 'P', 'B'],
    ['R', 'Y', 'G', 'B', 'Y', 'O', 'Y', 'R', 'R'],
    ['R', 'B', 'G', 'G', 'R', 'G', 'R', 'R', 'R'],
]

# Clase Agente: Define la clase del agente que jugará Candy Crush.
class Agente:
    def __init__(self, environment):
        # Inicializa el agente con su entorno (matriz de dulces actual).
        self.environment = environment
    
    def calc_heuritsic(self, state_matrix):
        # Función de evaluación (heurística) que calcula una puntuación heurística
        # para el estado actual del juego representado por 'state_matrix'.
        heuristic = 0
        for i in range(9):
            for j in range(9):
                if i < 8:
                    if state_matrix[i][j] == state_matrix[i + 1][j]:
                        heuristic += 1
                if j < 8:
                    if state_matrix[i][j] == state_matrix[i][j + 1]:
                        heuristic += 1
                

        return heuristic
