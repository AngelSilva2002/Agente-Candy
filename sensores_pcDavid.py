import random
from PIL import ImageGrab
import cv2
import numpy as np
import time
from PIL import Image
from Actuadores_David import hacer_movimiento
from reference_images import reference_images
from agente4 import Agente


def capture_screenshot():
    screenshot = ImageGrab.grab()  # Captura una imagen de toda la pantalla
    screenshot = np.array(screenshot)  # Convierte la imagen en una matriz NumPy
    return screenshot

# Función para procesar la captura de pantalla
def process_screenshot(screenshot):
    game_region = screenshot[100:673,  104:744]  
    return game_region

def color_match_candy(segment, i, j):
    # Define los umbrales de color en RGB
    umbrales = {
        'Red': (245, 1, 1),
        'Green': (75, 223, 19),
        'Purple': (191, 31, 255),
        'Blue': (33, 151, 255),
        'Yellow': (252, 227, 5),
        'Orange': (255, 138, 11),
        'J-Coffe': (101, 55, 0)
    }

    # Convierte el segmento a un arreglo NumPy para cálculos más eficientes
    segment_array = np.array(segment)

    # Inicializa contadores para cada color
    conteos_colores = {color: 0 for color in umbrales}

    # Itera a través de los umbrales de color y calcula el conteo de píxeles
    for color, umbral in umbrales.items():
        # Crea una máscara booleana para píxeles dentro del umbral
        mask = np.all(np.abs(segment_array - umbral) <= 30, axis=-1)  # Aplica tolerancia a cada canal RGB

        # Suma los valores True en la máscara para obtener el conteo
        pixel_count = np.sum(mask)

        # Actualiza el conteo en el diccionario
        conteos_colores[color] = pixel_count

    # Determina el color predominante en base a los conteos
    color_predominante = max(conteos_colores, key=lambda x: conteos_colores[x])
    
    if (color_predominante == 'J-Coffe'):
        return color_predominante

    if (i == 0 and j == 3) or (i == 0 and j == 4):

        return color_predominante
    
    else:
        dulce_final = es_dulce_rayado(segment, color_predominante, umbral_area=100, color_umbral=200)


    return dulce_final



def es_dulce_rayado(image, color_predominante, umbral_area=200, color_umbral=200):
    
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, thresholded = cv2.threshold(image_gray, color_umbral, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Calcular el área del contorno
        area = cv2.contourArea(contour)

        # Contar píxeles blancos dentro del contorno
        mask = np.zeros(image_gray.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
        pixels_blancos = cv2.countNonZero(mask)

        # Verificar si el contorno se ajusta a los criterios de dulce rayado
        if area > umbral_area and pixels_blancos > 0:
            if color_predominante == 'Yellow':
                return 'V'
            elif color_predominante == 'Blue':
                return 'W'
            elif color_predominante == 'Red':
                return 'T'
            elif color_predominante == 'Purple':
                return 'X'
            elif color_predominante == 'Green':
                return 'S'
            elif color_predominante == 'Orange':
                return 'U'
        
    return color_predominante
    
    
def process_game_board(game_board):
    rows, cols, _ = game_board.shape
    segment_size = (cols // 9, rows // 9)
    game_matrix_identify = np.empty((9, 9), dtype=str)
    game_matrix_color_match = np.empty((9, 9), dtype=str)  # Matriz para la coincidencia de color

    for i in range(9):
        for j in range(9):
            segment = game_board[i * segment_size[1]:(i + 1) * segment_size[1], 
                                j * segment_size[0]:(j + 1) * segment_size[0]]

            candy_type_color_match = color_match_candy(segment, i, j)

            game_matrix_color_match[i][j] = candy_type_color_match

    print(game_matrix_color_match)
    game_matrix_color_match = game_matrix_color_match.tolist()

    #print(game_matrix_color_match)
    return game_matrix_color_match

# Función para guardar una imagen en un archivo (MODIFICADA)
def save_image(image, filename):
    image_pil = Image.fromarray(image)
    image_pil.save(filename)

# Ejemplo de uso
if __name__ == "__main__":
    var = True

    
   
    while var:
        
        # # #Para trabajar con la foto almacendada
        # image_path = 'D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/captura_procesada.png'
        # loaded_image = load_image(image_path)
        
        # process_game_board(loaded_image)

        # save_image(loaded_image, "captura_procesada.png")


        time.sleep(1)
        screenshot = capture_screenshot()
        processed_image = process_screenshot(screenshot)
        candies_matrix = process_game_board(processed_image)
        save_image(processed_image, "captura_procesada.png")

        agente = Agente(candies_matrix)

        print(len(agente.generate_states_matrix()), "hola")

        print(agente.choose_best_state())
        print(agente.generate_move())
        hacer_movimiento(agente.generate_move()[0], agente.generate_move()[1], agente.generate_move()[2])