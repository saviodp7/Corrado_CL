import cv2
import numpy as np

# Crea una finestra per mostrare l'immagine originale
cv2.namedWindow("original")

# Crea una finestra per mostrare l'immagine mascherata
cv2.namedWindow("mask")

# Crea una trackbar per regolare i valori di tonalità, saturazione e valore
cv2.createTrackbar("Hue min", "mask", 0, 180, lambda x: None)
cv2.createTrackbar("Hue max", "mask", 0, 180, lambda x: None)
cv2.createTrackbar("Sat min", "mask", 0, 255, lambda x: None)
cv2.createTrackbar("Sat max", "mask", 0, 255, lambda x: None)
cv2.createTrackbar("Val min", "mask", 0, 255, lambda x: None)
cv2.createTrackbar("Val max", "mask", 0, 255, lambda x: None)

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    # Converti l'immagine in spazio colore HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Leggi i valori attuali delle trackbar
    hue_min = cv2.getTrackbarPos("Hue min", "mask")
    hue_max = cv2.getTrackbarPos("Hue max", "mask")
    sat_min = cv2.getTrackbarPos("Sat min", "mask")
    sat_max = cv2.getTrackbarPos("Sat max", "mask")
    val_min = cv2.getTrackbarPos("Val min", "mask")
    val_max = cv2.getTrackbarPos("Val max", "mask")

    # Isola i pixel dell'immagine che appartengono all'intervallo di colori specificato
    lower_color = np.array([hue_min, sat_min, val_min])
    upper_color = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Mostra l'immagine originale e l'immagine mascherata
    cv2.imshow("original", frame)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
