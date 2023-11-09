import cv2
import numpy as np


def find_circles(frame):

    # Converti l'immagine in scala di grigi
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Applica la trasformata di Hough per i cerchi
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=30, param2=30, minRadius=10, maxRadius=30)

    # Verifica se sono stati trovati cerchi
    if circles is not None:
        # Disegna i cerchi trovati
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(frame, center, radius, (0, 0, 255), 2)
        return True
    return False


def find_color(frame):
    lower_color = np.array([0, 83, 109])  # Valori HSV minimi per il rosso
    upper_color = np.array([20, 144, 255])  # Valori HSV massimi per il rosso

    # Converte l'immagine in spazio dei colori BGR in HSV
    hsv_cell = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crea una maschera per il colore desiderato (rosso)
    mask = cv2.inRange(hsv_cell, lower_color, upper_color)

    # Conta i pixel che soddisfano la maschera (colore rilevato)
    if cv2.countNonZero(mask) > 20:
        return True
    else:
        return False
