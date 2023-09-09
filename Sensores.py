from PIL import ImageGrab
import cv2
import numpy as np
import time
from PIL import Image


# Función para capturar una imagen del juego
def capture_screenshot():
    screenshot = ImageGrab.grab()  # Captura una imagen de toda la pantalla
    screenshot = np.array(screenshot)  # Convierte la imagen en una matriz NumPy
    return screenshot

# Función para procesar la captura de pantalla
def process_screenshot(screenshot):
    # Aquí puedes implementar el procesamiento de la imagen según tus necesidades.
    # Por ejemplo, puedes recortar la imagen para obtener solo el área del juego,
    # identificar elementos en el juego, como dulces y obstáculos, y extraer información relevante.
    # Esta parte dependerá de la estructura del juego y lo que deseas analizar.

    # Ejemplo: Recortar la imagen para obtener solo una región específica
    game_region = screenshot[75:790, 125:920]  # Ajusta las coordenadas según tu juego verticaul-horizontal

    # Ejemplo: Aplicar un filtro de suavizado
    #game_region = cv2.GaussianBlur(game_region, (15, 15), 0)


    return game_region

def calculate_dominant_color(segment):

    color_to_candy = {
        (52, 177, 1): 'Verde',
        (255, 1, 0): 'Rojo',
        (252, 220, 3): 'Amarillo',
        (18, 138, 255): 'Azul',
        (255, 138, 13): 'Naranja',
        (187, 37, 255): 'Morado',
    }
    
    candy_type = 'Desconocido'

    # Convertir el segmento a formato HSV (Hue, Saturation, Value)
    hsv_segment = cv2.cvtColor(segment, cv2.COLOR_BGR2HSV)

    for color, candy in color_to_candy.items():
        lower_bound = np.array([color[0] - 10, 100, 100])
        upper_bound = np.array([color[0] + 10, 255, 255])

        # Crear una máscara para el color específico
        mask = cv2.inRange(hsv_segment, lower_bound, upper_bound)

        # Encuentra los contornos en la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Si se encuentra al menos un contorno, consideramos que el color está presente
        if len(contours) > 0:
            candy_type = candy
            break


    return candy_type


def process_game_board(game_board):

    rows, cols, _ = game_board.shape
    segment_size = (cols // 9, rows // 9)  # Tamaño de cada segmento
    game_matrix = np.zeros((9, 9), dtype=int)

    for i in range(9):
        for j in range(9):
            # Obtener el segmento actual

            segment = game_board[i * segment_size[1]:(i + 1) * segment_size[1], 
                                j * segment_size[0]:(j + 1) * segment_size[0]]



            # Calcular el color predominante en el segmento
            color_mode = calculate_dominant_color(segment)

            print(color_mode)
            # Asignar un valor único a cada tipo de dulce basado en el color predominante
            # Esto es un ejemplo; debes ajustarlo según tus colores y tipos de dulces
            # if color_mode == 0:
            #     game_matrix[i][j] = 1  # Tipo de dulce 1
            # elif color_mode == 1:
            #     game_matrix[i][j] = 2  # Tipo de dulce 2
            # # Agrega más condiciones para otros colores y tipos de dulces

    print(game_matrix) 
# Función para guardar una imagen en un archivo
def save_image(image, filename):
    image_pil = Image.fromarray(image)
    image_pil.save(filename)

# Ejemplo de uso
if __name__ == "__main__":
    var = True
    while var:
        #time.sleep(5)
        screenshot = capture_screenshot()
        processed_image = process_screenshot(screenshot)
        process_game_board = process_game_board(processed_image)
        # Guardar la imagen procesada en un archivo (ajusta el nombre de archivo según sea necesario)
        save_image(processed_image, "captura_procesada.png")

        # Aquí puedes realizar más análisis o procesamiento de la imagen según tus necesidades.

        # Pausa antes de tomar otra captura (ajusta según sea necesario)
        time.sleep(5)

        var = False; 
