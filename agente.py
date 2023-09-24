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
    ['Y', 'G', 'O', 'Y', 'A', 'J', 'Y', 'Y', 'R'],
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

        # Inicializar el tiempo de ejecución
        #st = time.time()
        #################################

        # Lista de dulces especiales
        special_candies = ['S', 'T', 'U', 'V', 'W', 'X', 'A', 'C', 'D', 'E', 'F', 'I', 'J']

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
                
                if state_matrix[i][j] in special_candies:
                    heuristic += 2 

                # Recompensar combinaciones en forma de T o L
                if i < 7 and j < 7:
                    if (state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j + 1]) or \
                       (state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j - 1]) or \
                       (state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i + 1][j + 2]) or \
                       (state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i + 1][j - 2]):
                        heuristic += 3

                # Penalizar movimientos innecesarios (sin combinaciones)
                if i < 8 and j < 8:
                    if state_matrix[i][j] != state_matrix[i + 1][j] and state_matrix[i][j] != state_matrix[i][j + 1]:
                        heuristic -= 1

        # Imprimir el tiempo de ejecución
        #et = time.time()
        #print("Tiempo de ejecución del cálculo de la heurística: ", et - st, "segundos")
        #################################

        return heuristic
    

    def generate_states_matrix(self):
        # Genera una lista de matrices de estado posibles a partir de la matriz de dulces actual.
        # Solo se generan los movimientos válidos.

        candy_coordinates = [(i, j) for i in range(9) for j in range(9)]
        possible_states = []

        for (x1, y1) in candy_coordinates:
            for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x2, y2 = x1 + dx, y1 + dy

                if 0 <= x2 < 9 and 0 <= y2 < 9:
                    # Intercambiar dulces solo si las coordenadas x2 e y2 son válidas
                    state = [row[:] for row in self.environment]  # Copiar la matriz actual
                    state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]
                    possible_states.append(state)

        return possible_states



    def choose_best_state(self):
        # Elige el mejor estado posible de la lista de estados posibles generados por la función 'generate_states_matrix'.
        # El mejor estado posible es el que tiene la puntuación heurística más alta.
        # Devuelve una tupla (x1, y1, x2, y2) que representa el movimiento de intercambio de dulces que genera el mejor estado posible.

        # Obtener la lista de estados posibles
        possible_states = self.generate_states_matrix()



        # Calcular la heurística de cada estado posible
        heuristics = [self.calc_heuritsic(state) for state in possible_states]
        print(len(heuristics))

        #print (heuristics)

        # Obtener el índice del estado con la heurística más alta
        best_state_index = heuristics.index(max(heuristics))
        print(best_state_index)

        # Obtener las coordenadas de los dulces que se intercambian para generar el estado con la heurística más alta
        candy_coordinates = [(i, j) for i in range(9) for j in range(9)]
        x1, y1 = candy_coordinates[best_state_index // 4]
        x2, y2 = x1 + (best_state_index % 4 - 1) % 2, y1 + (best_state_index % 4 - 2) % 2

        
        return (x1, y1, x2, y2)



agente = Agente(candies_matrix)

print((agente.generate_states_matrix())[171])

print(agente.choose_best_state())