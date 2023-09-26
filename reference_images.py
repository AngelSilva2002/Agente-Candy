import cv2

reference_images = {
    'Red': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Rojo/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Rojo/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Rojo/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'Green': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Verde/' + 'rayado3.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Verde/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Verde/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'Yellow': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Amarillo/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Amarillo/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Amarillo/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'Blue': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Azul/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Azul/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Azul/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'Orange': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Naranja/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Naranja/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Naranja/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
    'Purple': {
        'rayado1': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'rayado1.png', cv2.IMREAD_GRAYSCALE),
        'rayado2': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'rayado2.png', cv2.IMREAD_GRAYSCALE),
        'envuelto': cv2.imread('D:/Trabajos UN/2023-2/Sistemas inteligentes/Agente-Candy/Images/Morado/' + 'envuelto.png', cv2.IMREAD_GRAYSCALE),
    },
}
