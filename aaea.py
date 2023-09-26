import cv2
import numpy as np

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
    
def detectar_dulce_envuelto(image):
    # Convierte la imagen a escala de grises
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica el detector de bordes Canny
    edges = cv2.Canny(image_gray, 100, 200)

    # Encuentra contornos en los bordes detectados
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Itera a través de los contornos y verifica si alguno tiene un área significativa
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:  # Ajusta el umbral de área según tus necesidades
            # Si el contorno tiene un área significativa, verifica si tiene una envoltura
            envoltura = verificar_envoltura(image_gray, contour)

            # Si el contorno tiene una envoltura, el dulce está envuelto
            if envoltura:
                return True

    # Si no se detecta un dulce envuelto, devuelve False
    return False

# Carga la imagen del dulce envuelto
image_path = 'D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'envuelto.png'
image = cv2.imread(image_path)

# Detecta si el dulce está envuelto
is_wrapped = detectar_dulce_envuelto(image)

# Imprime el resultado
print(is_wrapped)
