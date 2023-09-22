import time



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
    ['Y', 'Y', 'Y', 'R', 'Y', 'R', 'A', 'B', 'B'],
    ['Y', 'G', 'Y', 'Y', 'G', 'R', 'Y', 'P', 'B'],
    ['R', 'Y', 'C', 'B', 'Y', 'O', 'Y', 'R', 'R'],
    ['R', 'B', 'G', 'G', 'R', 'G', 'R', 'R', 'R'],
]

# Clase Agente
class Agente:
    def __init__(self, environment):
        # Inicializa el agente con su entorno (matriz de dulces actual).
        self.environment = environment
    
    def calc_heuritsic(self, state_matrix ):
        # Función de evaluación (heurística) que calcula una puntuación heurística
        # para el estado  del juego representado por 'state_matrix'.
        st = time.time()
        heuristic = 0
        for i in range(9):
            for j in range(9):
                # Evaluar dulces coincidentes en fila o columna
                if i < 8:
                    if state_matrix[i][j] == state_matrix[i + 1][j]:
                        heuristic += 1
                if j < 8:
                    if state_matrix[i][j] == state_matrix[i][j + 1]:
                        heuristic += 1

                # Recompensar combinaciones especiales y dulces especiales
                special_candies = ['S', 'T', 'U', 'V', 'W', 'X', 'A', 'C', 'D', 'E', 'F', 'I', 'J']
                if state_matrix[i][j] in special_candies:
                    heuristic += 2 

                # Recompensar combinaciones en forma de T o L
                if i < 7 and j < 7:
                    if (state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j + 1]) or \
                       (state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j - 1]) or \
                       (state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i + 1][j + 2]) or \
                       (state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i + 1][j - 2]):
                        heuristic += 3  # Recompensa combinaciones en forma de T o L

        et = time.time()
        print("Tiempo de ejecución del cálculo de la heurística: ", et - st, "segundos")
        return heuristic





agente = Agente(candies_matrix)

print(agente.calc_heuritsic(candies_matrix))