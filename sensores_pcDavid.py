import random
from PIL import ImageGrab
import cv2
import numpy as np
import time
from PIL import Image
from Actuadores_David import hacer_movimiento
from reference_images import reference_images
from agente3 import Agente


def capture_screenshot():
    screenshot = ImageGrab.grab()  # Captura una imagen de toda la pantalla
    screenshot = np.array(screenshot)  # Convierte la imagen en una matriz NumPy
    return screenshot

# Función para procesar la captura de pantalla
def process_screenshot(screenshot):
    game_region = screenshot[100:673,  104:744]  
    return game_region

# Función para cargar una imagen desde un archivo
def load_image(file_path):
    image = cv2.imread(file_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

# Función para procesar la imagen
def process_image(image):
    # Ajusta las coordenadas según tu imagen
    game_region = image[75:790, 125:920]
    return game_region


def color_match_candy(segment):
    # Define los umbrales de color en RGB
    umbrales = {
        'Red': (245, 1, 1),
        'Green': (75, 223, 19),
        'Purple': (191, 31, 255),
        'Blue': (33, 151, 255),
        'Yellow': (252, 227, 5),
        'Orange': (255, 138, 11)
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
    #dulce_final = identify_type(segment,color_predominante)


    return color_predominante

def identify_type(segment, color):
    segment_gray = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)

    # Obtener la lista de imágenes de referencia para el color y tipo de dulce
    reference_list = reference_images.get(color, {})

    # Inicializar el tipo de dulce como "normal"
    dulce_type = "normal"

    # Iterar a través de los tipos de dulces (rayado, envuelto)
    for tipo in ["rayado", "envuelto"]:
        for reference_image in reference_list.get(tipo, []):
            # Realizar la coincidencia de plantillas con cada imagen de referencia
            result = cv2.matchTemplate(segment_gray, reference_image, cv2.TM_CCOEFF_NORMED)
            threshold = 0.9  # Ajusta este umbral según tus necesidades

            # Si la coincidencia supera el umbral, asignar el tipo de dulce y salir del bucle
            if np.max(result) >= threshold:
                dulce_type = tipo
                break

    return dulce_type

    
    
def process_game_board(game_board):
    rows, cols, _ = game_board.shape
    segment_size = (cols // 9, rows // 9)
    game_matrix_identify = np.empty((9, 9), dtype=str)
    game_matrix_color_match = np.empty((9, 9), dtype=str)  # Matriz para la coincidencia de color

    for i in range(9):
        for j in range(9):
            segment = game_board[i * segment_size[1]:(i + 1) * segment_size[1], 
                                j * segment_size[0]:(j + 1) * segment_size[0]]

            candy_type_color_match = color_match_candy(segment)

            game_matrix_color_match[i][j] = candy_type_color_match

    game_matrix_color_match = game_matrix_color_match.tolist()

    print(game_matrix_color_match)
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


        #Para trabajar tomando capturas
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

        # i  = i+1

        var = False
