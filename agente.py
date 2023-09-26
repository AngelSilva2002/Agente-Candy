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
['G','R','O','Y','G','G','O','R','G',],
['R','G','B','R','O','B','G','G','R',],
['G','O','P','O','G','O','Y','R','Y',],
['B','G','B','R','R','O','O','P','G',],
['G','Y','O','Y','R','G','Y','Y','O',],
['O','P','R','P','P','Y','G','O','Y',],
['B','P','G','G','O','B','P','G','B',],
['R','B','P','O','O','R','B','P','P',],
['O','P','O','P','Y','Y','G','B','G',],
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

        # Obtener el índice del estado con la heurística más alta
        best_state_index = heuristics.index(max(heuristics))
        print(best_state_index)

        # Obtener el estado con la puntuación heurística más alta
        best_state = possible_states[best_state_index]

        # Encontrar las coordenadas de los elementos que difieren entre la matriz original y el mejor estado
        coordx1 = None
        coordy1 = None
        coordx2 = None
        coordy2 = None
        

        for x in range(9):
            for y in range(9):
                if self.environment[x][y] != best_state[x][y]:
                    if coordx1 == None:
                        coordx1 = x
                        coordy1 = y
                    else:
                        coordx2 = x
                        coordy2 = y
                    

        # Devolver el movimiento (x1, y1, x2, y2)
        return (coordx1, coordy1, coordx2, coordy2)
    
    def generate_move(self):
        coord1x, coord1y, coord2x, coord2y = self.choose_best_state()

        coordIniciales = (coord1x, coord1y)
        coordFinales = (coord2x, coord2y)

        # Calcular la acción a realizar a partir de la primera coordenada (rigth, left, up, down)
        if coordIniciales[0] == coordFinales[0]:
            if coordIniciales[1] < coordFinales[1]:
                accion = "derecha"
            else:
                accion = "izquierda"
        else:
            if coordIniciales[0] < coordFinales[0]:
                accion = "abajo"
            else:
                accion = "arriba"
        
        return coordIniciales[0], coordIniciales[1], accion



agente = Agente(candies_matrix)


print(agente.generate_move())
