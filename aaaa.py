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

    # Copia de la imagen original para dibujar contornos
    image_with_contours = image.copy()

    # Itera a través de los contornos y verifica si alguno tiene un área significativa
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10:
            # Aproxima el contorno a un polígono con menos vértices (triángulo, cuadrado, etc.)
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Si el polígono tiene cuatro lados, es muy probable que sea un rectángulo
            if len(approx) == 4:
                # Si el contorno es un rectángulo, es un dulce envuelto
                resultado = "Dulce envuelto"
                cv2.drawContours(image_with_contours, [contour], 0, (0, 255, 0), 2)
            else:
                # Si el contorno no es un rectángulo, es un dulce normal
                resultado = "Dulce normal"
                cv2.drawContours(image_with_contours, [contour], 0, (0, 255, 0), 2)

    # Muestra la imagen con los contornos
    cv2.imshow("Imagen Procesada", image_with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return resultado

# Carga la imagen del dulce envuelto o normal
image_path = 'D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/envuelto.png'
image = cv2.imread(image_path)

# Detecta si el dulce está envuelto o es normal
resultado = detectar_dulce_envuelto(image)

# Imprime el resultado
print(resultado)
