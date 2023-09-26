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
['G','O','G','Y','Y','O','P','P','R',],
['P','Y','G','R','B','Y','O','Y','B',],
['Y','Y','R','B','Y','B','G','R','R',],
['O','G','G','Y','B','B','Y','Y','B',],
['B','G','R','R','P','P','O','G','B',],
['P','P','G','B','O','G','B','O','G',],
['Y','B','B','G','G','P','O','B','R',],
['O','G','B','Y','R','R','G','R','O',],
['R','Y','G','Y','O','O','Y','B','G',],
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

                # Premio por dulces coincidentes en columnas
                if i < 7:
                    if state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 3

        
        # Premio si hay dulces coincidentes en forma de L
        for i in range(9):
            for j in range(9):
                # Verificar si hay una L simétrica hacia la derecha (horizontal)
                if j < 6 and i < 7:
                    if state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i][j + 2] == \
                            state_matrix[i + 1][j + 2] == state_matrix[i + 2][j + 2]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 10  # Agregar una recompensa significativa

                # Verificar si hay una L simétrica hacia abajo (vertical)
                if j < 7 and i < 6:
                    if state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j] == \
                            state_matrix[i + 2][j + 1] == state_matrix[i + 2][j + 2]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 10  # Agregar una recompensa significativa
        

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

        possible_states.reverse()

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

#agente = Agente(candies_matrix)

#print(agente.generate_move())