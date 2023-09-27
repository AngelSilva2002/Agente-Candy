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
                current_candy = state_matrix[i][j]
                if current_candy in ['G', 'R', 'O', 'Y', 'B', 'P']:
                    normal_color = current_candy
                    special_candy = None
                    wrapped_candy = None

                    # Identificar el tipo de dulce especial correspondiente al color normal
                    if normal_color == 'G':
                        special_candy = 'S'
                        wrapped_candy = 'A'
                    elif normal_color == 'R':
                        special_candy = 'T'
                        wrapped_candy = 'C'
                    elif normal_color == 'O':
                        special_candy = 'U'
                        wrapped_candy = 'D'
                    elif normal_color == 'Y':
                        special_candy = 'V'
                        wrapped_candy = 'E'
                    elif normal_color == 'B':
                        special_candy = 'W'
                        wrapped_candy = 'F'
                    elif normal_color == 'P':
                        special_candy = 'X'
                        wrapped_candy = 'I'

                    # Premio por dulces coincidentes en filas
                    if j < 7:
                        count_in_row = 1  # Inicializar el contador de dulces coincidentes en fila
                        special_count_in_row = 0  # Inicializar el contador de dulces especiales en fila
                        wrapped_count_in_row = 0  # Inicializar el contador de dulces envueltos en fila
                        for k in range(j + 1, min(j + 3, 9)):
                            if state_matrix[i][k] == current_candy:
                                count_in_row += 1
                            elif state_matrix[i][k] == special_candy:
                                special_count_in_row += 1
                            elif state_matrix[i][k] == wrapped_candy:
                                wrapped_count_in_row += 1
                            else:
                                break

                        total_count_in_row = count_in_row + special_count_in_row + wrapped_count_in_row
                        if total_count_in_row >= 3:
                            if total_count_in_row == 3:
                                heuristic += 5
                            elif total_count_in_row == 4:
                                heuristic += 8
                            elif total_count_in_row >= 5:
                                heuristic += 20

                    # Premio por dulces coincidentes en columnas
                    if i < 7:
                        count_in_column = 1  # Inicializar el contador de dulces coincidentes en columna
                        special_count_in_column = 0  # Inicializar el contador de dulces especiales en columna
                        wrapped_count_in_column = 0  # Inicializar el contador de dulces envueltos en columna
                        for k in range(i + 1, min(i + 3, 9)):
                            if state_matrix[k][j] == current_candy:
                                count_in_column += 1
                            elif state_matrix[k][j] == special_candy:
                                special_count_in_column += 1
                            elif state_matrix[k][j] == wrapped_candy:
                                wrapped_count_in_column += 1
                            else:
                                break

                        total_count_in_column = count_in_column + special_count_in_column + wrapped_count_in_column
                        if total_count_in_column >= 3:
                            if total_count_in_column == 3:
                                heuristic += 5
                            elif total_count_in_column == 4:
                                heuristic += 8
                            elif total_count_in_column >= 5:
                                heuristic += 20



        
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
        

        # Premio si hay dulces coincidentes en forma de T
        for i in range(9):
            for j in range(9):
                # Verificar si hay una T hacia la derecha (horizontal)
                if j < 5 and i < 7:
                    if state_matrix[i][j] == state_matrix[i][j + 1] == state_matrix[i][j + 2] == \
                            state_matrix[i + 1][j + 1] == state_matrix[i + 2][j + 1]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 10  # Agregar una recompensa significativa

                # Verificar si hay una T hacia abajo (vertical)
                if j < 7 and i < 5:
                    if state_matrix[i][j] == state_matrix[i + 1][j] == state_matrix[i + 2][j] == \
                            state_matrix[i + 1][j + 1] == state_matrix[i + 1][j + 2]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 10  # Agregar una recompensa significativa

                # Verificar si hay una T hacia la izquierda (horizontal)
                if j > 1 and i < 7:
                    if state_matrix[i][j] == state_matrix[i][j - 1] == state_matrix[i][j - 2] == \
                            state_matrix[i + 1][j - 1] == state_matrix[i + 2][j - 1]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 10  # Agregar una recompensa significativa

                # Verificar si hay una T hacia arriba (vertical)
                if j < 7 and i > 1:
                    if state_matrix[i][j] == state_matrix[i - 1][j] == state_matrix[i - 2][j] == \
                            state_matrix[i - 1][j + 1] == state_matrix[i - 1][j + 2]:
                        if state_matrix[i][j] in ['G', 'R', 'O', 'Y', 'B', 'P']:
                            heuristic += 10  # Agregar una recompensa significativa

        # Detectar combinaciones de dulces especiales en el estado actual y premiarlas
        for i in range(9):
            for j in range(9):
                if self.environment[i][j] != state_matrix[i][j]:
                    # Verificar si se ha combinado un dulce especial
                    if self.environment[i][j] in ['S', 'T', 'U', 'V', 'W', 'X'] and \
                            state_matrix[i][j] in ['S', 'T', 'U', 'V', 'W', 'X']:
                        heuristic += 15  # Combinación de dulces rayados (15 puntos)
                    elif self.environment[i][j] in ['A', 'C', 'D', 'E', 'F', 'I'] and \
                            state_matrix[i][j] in ['A', 'C', 'D', 'E', 'F', 'I']:
                        heuristic += 20  # Combinación de dulces envueltos (20 puntos)
                    elif self.environment[i][j] in ['S', 'T', 'U', 'V', 'W', 'X'] and \
                            state_matrix[i][j] in ['A', 'C', 'D', 'E', 'F', 'I']:
                        heuristic += 30 # Combinación de dulces rayados y envueltos (30 puntos)
                    elif self.environment[i][j] in ['S', 'T', 'U', 'V', 'W', 'X'] and \
                            state_matrix[i][j] in ['J']:
                        heuristic += 40 # Combinación de dulces rayados y bomba de color (40 puntos)
                    elif self.environment[i][j] in ['A', 'C', 'D', 'E', 'F', 'I'] and \
                            state_matrix[i][j] in ['J']:
                        heuristic += 40 # Combinación de dulces envueltos y bomba de color (40 puntos)
                    elif self.environment[i][j] in ['J'] and state_matrix[i][j] in ['J']:
                        heuristic += 50 # Combinación de bombas de color (50 puntos)

        """# Verificar combinación de bomba de color con el dulce normal más repetido
        bomba_de_color = None
        dulce_normal_mas_repetido = None
        max_repeticiones = 0

        # Calcular el recuento de dulces en el estado actual
        count = {}
        for i in range(9):
            for j in range(9):
                dulce = state_matrix[i][j]
                if dulce in count:
                    count[dulce] += 1
                else:
                    count[dulce] = 1

        for dulce, repeticiones in count.items():
            if repeticiones > max_repeticiones and dulce not in ['S', 'T', 'U', 'V', 'W', 'X']:
                dulce_normal_mas_repetido = dulce
                max_repeticiones = repeticiones

        # Verificar si hay combinación de bomba de color con el dulce normal más repetido
        for i in range(9):
            for j in range(9):
                if state_matrix[i][j] == 'J' and dulce_normal_mas_repetido is not None:
                    heuristic += 40  # Combinación de bomba de color con el dulce normal más repetido (40 puntos)"""


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