from PIL import ImageGrab
import cv2
import numpy as np
import time
from PIL import Image

def capture_screenshot():
    screenshot = ImageGrab.grab()  # Captura una imagen de toda la pantalla
    screenshot = np.array(screenshot)  # Convierte la imagen en una matriz NumPy
    return screenshot

# Función para procesar la captura de pantalla
def process_screenshot(screenshot):
    game_region = screenshot[77:790, 135:920]  
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

def identify_candy(segment, reference_images):
    best_match = None
    best_match_score = float('-inf')
    segment = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)


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


def color_match_candy(segment):
    # Define los umbrales de color en RGB
    umbrales = {
        'rojo': (245, 1, 1),
        'verde': (75, 223, 19),
        'morado': (191, 31, 255),
        'azul': (33, 151, 255),
        'yellow': (252, 227, 5),
        'naranja': (255, 138, 11)
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

    return color_predominante

    
def process_game_board(game_board, reference_images_1):
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

    print(game_matrix_color_match)

# Función para guardar una imagen en un archivo (MODIFICADA)
def save_image(image, filename):
    image_pil = Image.fromarray(image)
    image_pil.save(filename)

# Ejemplo de uso
if __name__ == "__main__":
    var = True

    # Define las imágenes de referencia para cada tipo de dulce
    reference_images_1 = {
    'Verde': [
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/verde.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/verde2.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/verde3.png', cv2.IMREAD_GRAYSCALE),
        #cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Image/green.png', cv2.IMREAD_GRAYSCALE)
    ],
    'Rojo': [
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/rojo.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/rojo2.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/rojo3.png', cv2.IMREAD_GRAYSCALE),
        #cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Image/red.png', cv2.IMREAD_GRAYSCALE)

    ],
    'Naranja': [
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/naranja.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/naranja2.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/naranja3.png', cv2.IMREAD_GRAYSCALE),
        #cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Image/orange.png', cv2.IMREAD_GRAYSCALE)

    ],
    'Yellow': [
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/amarillo.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/amarillo2.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/amarillo3.png', cv2.IMREAD_GRAYSCALE),
        #cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Image/yellow.png', cv2.IMREAD_GRAYSCALE)

    ],
    'Azul': [
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/azul.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/azul2.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/azul3.png', cv2.IMREAD_GRAYSCALE),
        #cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Image/blue.png', cv2.IMREAD_GRAYSCALE)

    ],
    'Morado': [
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/morado.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/morado2.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/morado3.png', cv2.IMREAD_GRAYSCALE),
        #cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Image/purple.png', cv2.IMREAD_GRAYSCALE)

    ]
}



    while var:
        # #Para trabajar con la foto almacendada
        # image_path = 'D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/captura_procesada.png'
        # loaded_image = load_image(image_path)
        
        # process_game_board(loaded_image, reference_images_1)

        # save_image(loaded_image, "captura_procesada.png")


        # print("Matriz utilizando color_match_candy:")
        # print(game_matrix_color_match)

        #Para trabajar tomando capturas
        time.sleep(5)
        screenshot = capture_screenshot()
        processed_image = process_screenshot(screenshot)
        process_game_board(processed_image, reference_images_1)
        save_image(processed_image, "captura_procesada.png")

        var = False
