import numpy as np
from setting import *
import cv2

def find_game_grid(frame, threshold, kernel_dim):
    """Riconoscimento della griglia di gioco e restituisce i corners ordinati"""

    # Estrai la ROI dall'immagine
    frame = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

    # Converti l'immagine in scala di grigi
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Applica la soglia per rilevare i bordi
    _, thresholded = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Noise removal
    kernel_erosion = np.ones((kernel_dim, kernel_dim), np.uint8)
    thresholded = cv2.erode(thresholded, kernel_erosion)

    # Trova i contorni
    contours, hiers = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    corners = find_corners(contours, hiers)
    sorted_corners = sort_corners(corners)

    # Trasforma i contorni ordinati in una lista
    corners = [corner for row in sorted_corners for corner in row]

    for index, corner in enumerate(corners):
        cv2.rectangle(frame, corner[0], corner[1], (0, 255, 0), thickness=2)
        cv2.putText(frame, str(index), corner[0], cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=1)

    return frame, thresholded, corners


def sort_corners(corners):
    """Ordinamento corners"""
    num_rows = 3
    num_cols = 3
    sorted_corners = []
    for row in range(num_rows):
            sorted_by_y = sorted(corners, key=lambda corners: (corners[0][1]))
            sorted_corners.append(sorted_by_y[0:num_cols])
            sorted_corners[row] = sorted(sorted_corners[row],  key=lambda sorted_corners: (sorted_corners[0][0]))
            for corner in sorted_corners[row]:
                    corners.remove(corner)
    return sorted_corners


def find_corners(contours, hiers):
    """Trova i corners della griglia"""
    corners = []  # List of corners

    # Iterate contours and hiers, find bounding rectangles, and add corners to a list
    for cont, hier in zip(contours, hiers[0]):
        # If contours has no child
        if hier[2] == -1:
            # Get bounding rectangle
            brec_x, brec_y, brec_width, brec_height = cv2.boundingRect(cont)
            # Append corner to list of corners
            brec_top_left = (brec_x, brec_y)
            brec_bot_right = (brec_x + brec_width, brec_y + brec_height)
            corners.append((brec_top_left, brec_bot_right))
    return corners

def find_color(frame):
    lower_color = np.array([127, 10, 135])  # Valori HSV minimi per il rosso
    upper_color = np.array([180, 49, 175])  # Valori HSV massimi per il rosso

    # Converte l'immagine in spazio dei colori BGR in HSV
    hsv_cell = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crea una maschera per il colore desiderato (rosso)
    mask = cv2.inRange(hsv_cell, lower_color, upper_color)

    # Conta i pixel che soddisfano la maschera (colore rilevato)
    if cv2.countNonZero(mask) > 25:
        return True
    else:
        return False

#This function is used to draw the board's current state every time the user turn arrives.
def print_board(config):
    print("Griglia di gioco:")
    for i in range(0, 9):
        if i > 0 and i % 3 == 0:
            print("\n")
        if config[i] == 0:
            print("- ", end=" ")
        if config[i] == O_SYM:
            print("O ", end=" ")
        if config[i] == X_SYM:
            print("X ", end=" ")
    print("\n")
