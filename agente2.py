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
    ['R', 'G', 'B', 'Y', 'O', 'P', 'R', 'G', 'B'],
    ['G', 'B', 'Y', 'O', 'P', 'R', 'G', 'B', 'Y'],
    ['B', 'Y', 'O', 'P', 'R', 'G', 'B', 'Y', 'O'],
    ['Y', 'O', 'P', 'R', 'G', 'B', 'Y', 'O', 'P'],
    ['O', 'P', 'R', 'G', 'B', 'Y', 'O', 'P', 'R'],
    ['P', 'R', 'G', 'B', 'Y', 'O', 'P', 'R', 'G'],
    ['R', 'G', 'B', 'Y', 'O', 'P', 'R', 'G', 'B'],
    ['G', 'B', 'Y', 'O', 'P', 'R', 'G', 'B', 'Y'],
    ['B', 'Y', 'O', 'P', 'R', 'G', 'B', 'Y', 'O']
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

        # Generar estados posibles
        possible_states = []
        generated_states = set()

        for (x1, y1) in candy_coordinates:
            for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x2, y2 = x1 + dx, y1 + dy

                if 0 <= x2 < 9 and 0 <= y2 < 9:
                    # Realizar una copia profunda de la matriz actual
                    state = copy.deepcopy(self.environment)
                    # Intercambiar dulces solo si las coordenadas x2 e y2 son válidas
                    state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]

                    # Verificar si el estado generado ya ha sido generado antes
                    state_key = str(state)
                    if state_key not in generated_states:
                        # Agregar el estado generado a la lista de estados posibles
                        possible_states.append(state)
                        generated_states.add(state_key)

        return possible_states


    def choose_best_state(self):
        # Elige el mejor estado posible de la lista de estados posibles generados por la función 'generate_states_matrix'.
        # El mejor estado posible es el que tiene la puntuación heurística más alta.
        # Devuelve una tupla (x1, y1, x2, y2) que representa el movimiento de intercambio de dulces que genera el mejor estado posible.

        # Obtener la lista de estados posibles
        candy_coordinates = [(i, j) for i in range(9) for j in range(9)]
        possible_states = []
        for (x1, y1) in candy_coordinates:
            for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x2, y2 = x1 + dx, y1 + dy

                if 0 <= x2 < 9 and 0 <= y2 < 9:
                    # Realizar una copia profunda de la matriz actual
                    state = copy.deepcopy(self.environment)
                    # Intercambiar dulces solo si las coordenadas x2 e y2 son válidas
                    state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]
                    # Calcular la heurística del estado generado y agregarlo a la lista de estados posibles
                    heapq.heappush(possible_states, (self.calc_heuristic(state), x1, y1, x2, y2))

        if not possible_states:
            # No hay movimientos válidos disponibles
            return None

        # Obtener las coordenadas de los dulces que se intercambian para generar el estado con la heurística más alta
        _, x1, y1, x2, y2 = heapq.heappop(possible_states)

        return (x1, y1, x2, y2)



agente = Agente(candies_matrix)

print(agente.choose_best_state())

print(len(agente.generate_states_matrix()))