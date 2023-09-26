import cv2

reference_images = {
    'rojo': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Rojo/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Rojo/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Rojo/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'verde': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Verde/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Verde/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Verde/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'amarillo': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Amarillo/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Amarillo/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Amarillo/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'azul': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Azul/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Azul/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Azul/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'naranja': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Naranja/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Naranja/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Naranja/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'morado': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
}
