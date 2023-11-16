import cv2 as cv

def print_camera_info():
    # Stampa informazioni su tutte le webcam disponibili
    for i in range(0, 10):
        cap = cv.VideoCapture(i)
        if not cap.isOpened():
            break
        print(f"Webcam {i}: {cap.get(cv.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv.CAP_PROP_FRAME_HEIGHT)}")
        cap.release()

print_camera_info()