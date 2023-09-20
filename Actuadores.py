import pyautogui
import time

# Dimensiones del tablero y del espacio en la pantalla
filas = 9
columnas = 9
espacio_x_min = 75
espacio_x_max = 790
espacio_y_min = 125
espacio_y_max = 920

# Calcular el tamaño de cada celda en función del espacio en la pantalla y las dimensiones del tablero
celda_width = (espacio_x_max - espacio_x_min) // columnas
celda_height = (espacio_y_max - espacio_y_min) // filas

# Coordenadas del punto de inicio en la esquina superior izquierda del espacio en la pantalla
inicio_x = espacio_x_min + celda_width // 2
inicio_y = espacio_y_min + celda_height // 2

# Función para realizar un movimiento en una dirección
def hacer_movimiento(fila, columna, direccion):
    # Calcular la posición del centro de la celda deseada
    x = inicio_x + columna * celda_width
    y = inicio_y + fila * celda_height

    # Mover el mouse a la celda deseada en la región del juego
    pyautogui.moveTo(x, y)

    # Mantener clic presionado
    pyautogui.mouseDown()

    # Esperar un momento para simular el arrastre
    time.sleep(0.5)

    # Dependiendo de la dirección, mover el mouse
    if direccion == "arriba":
        pyautogui.move(0, -celda_height, duration=0.5)
    elif direccion == "abajo":
        pyautogui.move(0, celda_height, duration=0.5)
    elif direccion == "izquierda":
        pyautogui.move(-celda_width, 0, duration=0.5)
    elif direccion == "derecha":
        pyautogui.move(celda_width, 0, duration=0.5)

    # Liberar el clic
    pyautogui.mouseUp()

# Función para realizar todos los movimientos en cada celda
def todos_movimientos(filas, columnas):
    time.sleep(5)
    for fila in range(filas):
        for columna in range(columnas):
            # Realizar movimientos hacia todas las direcciones en cada celda
            hacer_movimiento(fila, columna, "arriba")
            hacer_movimiento(fila, columna, "abajo")
            hacer_movimiento(fila, columna, "izquierda")
            hacer_movimiento(fila, columna, "derecha")
            # Pausa entre movimientos (ajusta según sea necesario)
            time.sleep(1)

# Ejemplo de uso: Realizar todos los movimientos en un tablero 9x9
hacer_movimiento(0,4,"derecha")
hacer_movimiento(2,4, "derecha")
hacer_movimiento(2,7, "derecha")