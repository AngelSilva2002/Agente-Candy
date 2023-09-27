import random
from PIL import ImageGrab
import cv2
import numpy as np
import time
from PIL import Image
from Actuadores_David import hacer_movimiento
from agente4 import Agente


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

        
        es_envu = es_envuelto(image, color_predominante)

        if es_envu == "Envuelto":
            if color_predominante == 'Yellow':
                return 'E'
            elif color_predominante == 'Blue':
                return 'F'
            elif color_predominante == 'Red':
                return 'C'
            elif color_predominante == 'Purple':
                return 'I'
            elif color_predominante == 'Green':
                return 'G'
            elif color_predominante == 'Orange':
                return 'D'

    return color_predominante
    

def verificar_envoltura(image_gray, contour):

    
    # Encuentra el centro del contorno
    M = cv2.moments(contour)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Crea un círculo alrededor del centro del contorno
    radius = 10
    circle = cv2.circle(image_gray, (cx, cy), radius, (0, 255, 0), 2)

    # Verifica si hay un cambio de color significativo entre el círculo y el fondo
    pixel_gray = image_gray[cy, cx]
    pixel_center = circle[cy, cx]

    return pixel_gray != pixel_center

# def detectar_dulce_envuelto(image):
#     # Convierte la imagen a escala de grises
#     image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Aplica el detector de bordes Canny
#     edges = cv2.Canny(image_gray, 100, 200)

#     # Encuentra contornos en los bordes detectados
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Copia de la imagen original para dibujar contornos
#     image_with_contours = image.copy()

#     # Itera a través de los contornos y verifica si alguno tiene un área significativa
#     resultado = ""
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area > 10:
#             # Aproxima el contorno a un polígono con menos vértices (triángulo, cuadrado, etc.)
#             epsilon = 0.04 * cv2.arcLength(contour, True)
#             approx = cv2.approxPolyDP(contour, epsilon, True)

#             # Si el polígono tiene cuatro lados, es muy probable que sea un rectángulo
#             if len(approx) == 4:
#                 # Si el contorno es un rectángulo, es un dulce envuelto
#                 resultado = "envuelto"
#                 cv2.drawContours(image_with_contours, [contour], 0, (0, 255, 0), 2)
#             else:
#                 # Si el contorno no es un rectángulo, es un dulce normal
#                 resultado = "normal"
#                 cv2.drawContours(image_with_contours, [contour], 0, (0, 255, 0), 2)

#     return resultado

def es_envuelto(imagen, color):

    colores_dulces = {
    "Red": ([0, 0, 100], [80, 80, 255]),  # Rango de color para el rojo
    "Green": ([0, 100, 0], [80, 255, 80]),  # Rango de color para el verde
    "Blue": ([100, 0, 0], [255, 80, 80]),  # Rango de color para el azul
    "Yellow": ([0, 100, 100], [80, 255, 255]),  # Rango de color para el amarillo
    "Orange": ([0, 50, 100], [80, 150, 255]),  # Rango de color para el naranja
    "Purple": ([50, 0, 100], [150, 80, 255])  # Rango de color para el morado
}

    lower_bound, upper_bound = colores_dulces[color]
    
    # Convertir la imagen a formato HSV
    hsv_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    
    # Crear una máscara para el rango de color especificado
    mask = cv2.inRange(hsv_imagen, np.array(lower_bound), np.array(upper_bound))
    
    # Calcular el porcentaje de píxeles que caen dentro del rango de color
    total_pixeles = mask.shape[0] * mask.shape[1]
    pixeles_en_rango = cv2.countNonZero(mask)
    porcentaje_en_rango = (pixeles_en_rango / total_pixeles) * 100
    #print(porcentaje_en_rango)
    
    # Determinar si el porcentaje en el rango es mayor o igual al 90%
    if porcentaje_en_rango >= 70:
        return "Envuelto"
    else:
        return "Normal"



def process_game_board(game_board):
    rows, cols, _ = game_board.shape
    segment_size = (cols // 9, rows // 9)
    game_matrix_identify = np.empty((9, 9), dtype=str)
    game_matrix_color_match = np.empty((9, 9), dtype=str)  # Matriz para la coincidencia de color

    for i in range(9):
        for j in range(9):
            segment = game_board[i * segment_size[1]:(i + 1) * segment_size[1], 
                                j * segment_size[0]:(j + 1) * segment_size[0]]
            
            #save_image(segment, "dulce " + str(i) +str(j) + ".png")
            candy_type_color_match = color_match_candy(segment, i, j)
           
            game_matrix_color_match[i][j] = candy_type_color_match

    #print(game_matrix_color_match)
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


        screenshot = capture_screenshot()
        processed_image = process_screenshot(screenshot)
        candies_matrix = process_game_board(processed_image)
        #save_image(processed_image, "captura_procesada.png")

        agente = Agente(candies_matrix)

        # print(len(agente.generate_states_matrix()), "hola")

        # print(agente.choose_best_state())
        # print(agente.generate_move())
        hacer_movimiento(agente.generate_move()[0], agente.generate_move()[1], agente.generate_move()[2])
        #var = False
        