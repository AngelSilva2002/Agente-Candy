import cv2
import numpy as np

# Definir los rangos de colores para cada uno de los 6 colores de los dulces




# Cargar la imagen de ejemplo (asegúrate de que la imagen tenga un caramelo)
imagen_ejemplo = cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/8.jpg')

# Llamar a la función para verificar si el caramelo es envuelto o no
resultado = es_envuelto(imagen_ejemplo, "amarillo")

print("El caramelo es:", resultado)
