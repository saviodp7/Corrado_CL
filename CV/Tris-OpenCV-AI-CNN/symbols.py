import cv2
import numpy as np


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
