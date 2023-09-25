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
    ['G', 'P', 'R', 'P', 'G', 'Y', 'P', 'R', 'G'],
    ['Y', 'O', 'G', 'R', 'P', 'O', 'W', 'P', 'P'],
    ['B', 'G', 'P', 'P', 'Y', 'Y', 'P', 'Y', 'O'],
    ['O', 'B', 'Y', 'G', 'P', 'P', 'Y', 'R', 'G'],
    ['B', 'B', 'R', 'P', 'R', 'G', 'B', 'G', 'G'],
    ['B', 'R', 'G', 'G', 'R', 'R', 'O', 'P', 'P'],
    ['P', 'R', 'O', 'G', 'O', 'P', 'O', 'B', 'O'],
    ['O', 'O', 'G', 'O', 'P', 'P', 'R', 'G', 'Y'],
    ['P', 'P', 'Y', 'R', 'P', 'Y', 'P', 'O', 'B'],
]

# Clase Agente
class Agente:
    def __init__(self, environment):
        # Inicializa el agente con su entorno (matriz de dulces actual).
        self.environment = environment
    
    def calc_heuritsic(self, state_matrix ):
        # Función de evaluación (heurística) que calcula una puntuación heurística
        # para el estado  del juego representado por 'state_matrix'.

        heuristic = 0

        # Premio por dulces coincidentes en filas y columnas
        for i in range(9):
            for j in range(9):
                # Premio por dulces coincidentes en filas
                if j < 7:
                    if state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i][j + 2]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 3
                        elif state_matrix[i][j] in ['S', 'T', 'U', 'V', 'W', 'X']:
                            heuristic += 4
                        elif state_matrix[i][j] in ['A', 'C', 'D', 'E', 'F', 'I']:
                            heuristic += 5
                        elif state_matrix[i][j] == 'J':
                            heuristic += 6

                # Premio por dulces coincidentes en columnas
                if i < 7:
                    if state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 3
                        elif state_matrix[i][j] in ['S', 'T', 'U', 'V', 'W', 'X']:
                            heuristic += 4
                        elif state_matrix[i][j] in ['A', 'C', 'D', 'E', 'F', 'I']:
                            heuristic += 5
                        elif state_matrix[i][j] == 'J':
                            heuristic += 6
        
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
        
        return coordIniciales, accion




agente = Agente(candies_matrix)

print(agente.generate_move())