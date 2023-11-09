import cv2
from grid import find_game_grid
from symbols import find_color
import time
import tkinter as tk
from tkinter import messagebox
from MinMaxSolver import MinMaxSolver
import keyboard
from letter_recog_class import LetterRecognition

# Intervallo desiderato in secondi tra le azioni
intervallo_desiderato = 2

# Inizializza la webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("config", cv2.WINDOW_NORMAL)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)

cv2.createTrackbar("threshold", "mask", 44, 255, lambda x: None)
cv2.createTrackbar("kernel_dim", "mask", 10, 15, lambda x: None)

# Crea una finestra principale per la gestione degli errori
root = tk.Tk()
root.withdraw()  # Nasconde la finestra principale

# prossima esecuzione
next_time = time.time()
accuracy_count = 0
prec_config = [0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    now = time.time()
    # Crea un'istanza della classe con il percorso dei pesi del modello
    LetterRecognizer = LetterRecognition("C:\\Users\\Savio Del Peschio\\Desktop\\Tris-OpenCV-AI-CNN\\weights.best.xo.hdf5")
            
    if now > next_time:
        config = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Errore", "Camera non trovata!")

        threshold = cv2.getTrackbarPos("threshold", "mask")
        kernel_dim = cv2.getTrackbarPos("kernel_dim", "mask")

        # Trova e disegna la griglia del tris
        grid_frame, thresholded, corners = find_game_grid(frame, threshold, kernel_dim)
        extracted_frame = 0
        
        for index, cell in enumerate(corners):
            extracted_frame = grid_frame[cell[0][1]:cell[1][1], cell[0][0]:cell[1][0]]

            cv2.imwrite("quadrato.jpg", extracted_frame)

            if find_color(extracted_frame):
            # Utilizza la classe per riconoscere le lettere
                recognized_letter = LetterRecognizer.recognize_letter("quadrato.jpg")
                if recognized_letter=='х':
                    config[index] = 2
                elif recognized_letter=='о':
                    config[index] = 1
            else:
                config[index] = 0


        # Mostra il frame elaborato
        cv2.imshow("config", grid_frame)
        ## DEBUG
        cv2.imshow("mask", thresholded)

        # Assicuriamoci dell'accuratezza della rilevazione
        if config == prec_config:
            accuracy_count += 1
        else:
            accuracy_count = 0
        prec_config = config
        print(config)

        # Rileva la pressione sul fronte di discesa del tasto "m"
        if keyboard.is_pressed('m') and accuracy_count > 10:
            print("Sto cercando la mossa ...")
            solver = MinMaxSolver(config)
            print(solver.findBestMove())

        next_time += 0.2

    if cv2.waitKey(1) & 0xFF == 27:  # Esc per uscire
        break

cap.release()
cv2.destroyAllWindows()