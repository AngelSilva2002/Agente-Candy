import time
import copy
import heapq
import re

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

    def find_combinations(self, candies):
        # Encuentra todas las combinaciones de dulces en una cadena de dulces.
        # Devuelve una lista de conjuntos que contienen las posiciones de los dulces que forman cada combinación.

        # Crear un diccionario para almacenar la puntuación de cada combinación de dulces
        combination_scores = {
            'RRR': 100,
            'RR': 10,
            'GGG': 100,
            'GG': 10,
            'BBB': 100,
            'BB': 10,
            'YYY': 100,
            'YY': 10,
            'PPP': 100,
            'PP': 10,
            'OOO': 100,
            'OO': 10,
            'LLL': 1000,
            'TTT': 1000,
            'L': 100,
            'T': 100,
        }

        combinations = []

        # Buscar combinaciones en filas y columnas
        for i in range(9):
            row_candies = candies[i*9:(i+1)*9]
            col_candies = candies[i::9]
            for candy, score in combination_scores.items():
                if candy in row_candies:
                    positions = set([j for j in range(i*9, (i+1)*9) if row_candies[j-i*9] == candy[0]])
                    combinations.append(positions)
                if candy in col_candies:
                    positions = set([j*9+i for j in range(9) if col_candies[j] == candy[0]])
                    combinations.append(positions)

        # Buscar combinaciones en forma de L y T
        for i in range(7):
            for j in range(7):
                if (i+1)*9+j-1 >= 0 and (i+1)*9+j+1 < len(candies) and candies[i*9+j] == candies[(i+1)*9+j] == candies[(i+2)*9+j] and candies[(i+1)*9+j-1] == candies[(i+1)*9+j+1] == candies[(i+1)*9+j]:
                    positions = set([(i+1)*9+j, (i+1)*9+j-1, (i+1)*9+j+1, i*9+j, (i+2)*9+j])
                    combinations.append(positions)
                if i*9+j+2 < len(candies) and candies[i*9+j] == candies[i*9+j+1] == candies[i*9+j+2] and (i-1)*9+j+1 >= 0 and (i+1)*9+j+1 < len(candies) and candies[(i+1)*9+j+1] == candies[(i-1)*9+j+1] == candies[i*9+j+1]:
                    positions = set([i*9+j+1, (i+1)*9+j+1, (i-1)*9+j+1, i*9+j, i*9+j+2])
                    combinations.append(positions)

        # Buscar combinaciones utilizando expresiones regulares
        for candy, score in combination_scores.items():
            pattern = re.compile(candy)
            for match in pattern.finditer(candies):
                positions = set(range(match.start(), match.end()))
                combinations.append(positions)

        return combinations

    def count_unnecessary_moves(self, state):
        # Cuenta el número de movimientos innecesarios en un estado de la matriz de dulces.
        # Un movimiento es innecesario si no forma parte de una combinación de dulces.

        # Crear un conjunto para almacenar los dulces que forman parte de una combinación
        combined_candies = set()

        # Buscar combinaciones en filas y columnas
        for i in range(9):
            row_candies = ''.join(state[i])
            col_candies = ''.join([state[j][i] for j in range(9)])
            for candy in self.find_combinations(row_candies):
                combined_candies.update(candy)
            for candy in self.find_combinations(col_candies):
                combined_candies.update(candy)

        # Buscar combinaciones en forma de L y T
        for i in range(7):
            for j in range(7):
                if state[i][j] == state[i+1][j] == state[i+2][j] and state[i+1][j+1] == state[i+1][j-1] == state[i+1][j]:
                    combined_candies.update([(i+1, j), (i+1, j+1), (i+1, j-1), (i, j), (i+2, j)])
                if state[i][j] == state[i][j+1] == state[i][j+2] and state[i+1][j+1] == state[i-1][j+1] == state[i][j+1]:
                    combined_candies.update([(i, j+1), (i+1, j+1), (i-1, j+1), (i, j), (i, j+2)])

        # Contar el número de movimientos innecesarios
        count = 0
        for i in range(9):
            for j in range(9):
                if state[i][j] != ' ' and (i, j) not in combined_candies:
                    count += 1

        return count
    
    def calc_heuristic(self, state):
        # Calcula la puntuación heurística de un estado de la matriz de dulces.
        # La puntuación heurística se utiliza para evaluar qué tan bueno es un estado particular de la matriz de dulces.

        # Crear un diccionario para almacenar la puntuación heurística de cada combinación de dulces
        heuristic_scores = {
            'RRR': 100,
            'RR': 10,
            'GGG': 100,
            'GG': 10,
            'BBB': 100,
            'BB': 10,
            'YYY': 100,
            'YY': 10,
            'PPP': 100,
            'PP': 10,
            'OOO': 100,
            'OO': 10,
            'LLL': 1000,
            'TTT': 1000,
            'L': 100,
            'T': 100,
        }

        score = 0

        # Evaluar la puntuación heurística de cada fila y columna
        for i in range(9):
            row_candies = ''.join(state[i])
            col_candies = ''.join([state[j][i] for j in range(9)])
            score += heuristic_scores.get(row_candies, 0)
            score += heuristic_scores.get(col_candies, 0)

        # Evaluar la puntuación heurística de las combinaciones en forma de L y T
        for i in range(7):
            for j in range(7):
                if state[i][j] == state[i+1][j] == state[i+2][j] and state[i+1][j+1] == state[i+1][j-1] == state[i+1][j]:
                    score += heuristic_scores.get('T', 0)
                if state[i][j] == state[i][j+1] == state[i][j+2] and state[i+1][j+1] == state[i-1][j+1] == state[i][j+1]:
                    score += heuristic_scores.get('L', 0)

        # Evaluar la puntuación heurística de los dulces especiales
        for i in range(9):
            for j in range(9):
                if state[i][j] == 'S':
                    score += 50
                elif state[i][j] == 'B':
                    score += 200
                elif state[i][j] == 'C':
                    score += 300

        # Evaluar la puntuación heurística de los movimientos innecesarios
        score -= self.count_unnecessary_moves(state)

        return score
    

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
        heuristics = [self.calc_heuristic(state) for state in possible_states]

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