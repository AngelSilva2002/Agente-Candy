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
    game_region = screenshot[100:673,  104:744]  # Ajusta las coordenadas según tu juego (vertical-horizontal)

    # Convierte la región del juego a escala de grises
    game_region_gray = cv2.cvtColor(game_region, cv2.COLOR_BGR2GRAY)

    return game_region_gray

# Función para identificar el tipo de dulce en un segmento
def identify_candy(segment, reference_images):
    best_match = None
    best_match_score = float('-inf')

    for candy, reference_list in reference_images.items():
        best_candy_score = float('-inf')
        
        for reference_image in reference_list:
            # Realizar la coincidencia de plantillas
            result = cv2.matchTemplate(segment, reference_image, cv2.TM_CCOEFF_NORMED)

            # Ajustar el umbral aquí para controlar la coincidencia
            threshold = 0.01  # Ajusta este valor según tus necesidades
            loc = np.where(result >= threshold)

            # Calcula la mejor coincidencia para esta imagen de referencia
            if np.max(result) > best_candy_score:
                best_candy_score = np.max(result)

        # Actualiza el mejor tipo de dulce si es necesario
        if best_candy_score > best_match_score:
            best_match_score = best_candy_score
            best_match = candy

    return best_match
# Función para procesar el tablero del juego
def process_game_board(game_board, reference_images):
    rows, cols = game_board.shape
    segment_size = (cols // 9, rows // 9)  # Tamaño de cada segmento
    game_matrix = np.empty((9, 9), dtype=str)

    for i in range(9):
        for j in range(9):
            # Obtener el segmento actual
            segment = game_board[i * segment_size[1]:(i + 1) * segment_size[1], 
                                j * segment_size[0]:(j + 1) * segment_size[0]]

            # Identificar el tipo de dulce en el segmento
            candy_type = identify_candy(segment, reference_images)
            game_matrix[i][j] = candy_type

    print(game_matrix) 

# Función para guardar una imagen en un archivo
def save_image(image, filename):
    image_pil = Image.fromarray(image)
    image_pil.save(filename)

# Ejemplo de uso
if __name__ == "__main__":
    var = True

    # Define las imágenes de referencia para cada tipo de dulce
    """reference_images = {
        'G-Verde': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/verde.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/verde2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/verde3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'R-Rojo': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/rojo.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/rojo2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/rojo3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'O-Naranja': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/naranja.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/naranja2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/naranja3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'Y-Amarillo': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/amarillo.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/amarillo2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/amarillo3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'B-Azul': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/azul.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/azul2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/azul3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'P-Morado': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/morado.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/morado2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/morado3.png', cv2.IMREAD_GRAYSCALE)
        ]
    }"""

    reference_images = {
        'G-Verde': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Image/green.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/verde2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/verde3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'R-Rojo': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Image/red.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/rojo2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/rojo3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'O-Naranja': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Image/orange.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/naranja2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/naranja3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'Y-Amarillo': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Image/yellow.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/amarillo2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/amarillo3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'B-Azul': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Image/blue.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/azul2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/azul3.png', cv2.IMREAD_GRAYSCALE)
        ],
        'P-Morado': [
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Image/purple.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/morado2.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread('/home/davidrg02/Documentos/UNAL/SEMESTRE VIII/Sistemas inteligentes/Agente-Candy/Images/morado3.png', cv2.IMREAD_GRAYSCALE)
        ]
    }

    while var:
        time.sleep(2)
        screenshot = capture_screenshot()
        processed_image = process_screenshot(screenshot)
        process_game_board(processed_image, reference_images)
        # Guardar la imagen procesada en un archivo (ajusta el nombre de archivo según sea necesario)
        save_image(processed_image, "captura_procesada.png")

        # Aquí puedes realizar más análisis o procesamiento de la imagen según tus necesidades.

        # Pausa antes de tomar otra captura (ajusta según sea necesario)
        # time.sleep(5)

        var = False
