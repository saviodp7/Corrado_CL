import os
import cv2
import time

from PoseEstimator import PoseEstimator

if __name__ == '__main__':



    pixel_into_img = [840, 450]  # Coordinata x, y del pixel nel frame dell'immagine
    qr_size_cm = 4.4

    # Ricavo path della matrice di calibrazione e acquisizione video
    current_path = os.path.dirname(__file__)
    relative_path = 'Calibrazione\B.npz'
    calibration_matrix_path = os.path.join(current_path, relative_path)
    relative_path = 'QR_video.mp4'
    video_path = os.path.join(current_path, relative_path)

    # Camera initialization
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    #
    now = time.time()
    next_time = time.time()
    freq_samp = 5
    #
    pose_estimator = PoseEstimator(calibration_matrix_path)
    _ = None

    while True:

        ret, frame = cap.read()

        tvec, rvec = pose_estimator.show_axes(frame, _, _)
        print(f"tvec: {tvec}")
        # print(f"rvec: {rvec}")

        if ret:
            cv2.imshow("video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # x, y, _ = pose_estimator.recognize(args)
    # tvec, rvec, pixel_into_QRc = show_axes(cmtx, dist, video_path, pixel_into_img, qr_size_cm)




# ........................COSE DA FARE .....................................................................
# Implementare il fattore di scala,
#           idea: metterlo nella quarrta posizione della posizione omogenea
#           il riferimento hai centimetri è che la linee degli assi x e y sono di 4,4 cm
#
# Far funzionare la Camera come input USB in input surce
#
# Capire prchè la posizione che mi stampa è 6x6 se il vettore di traslazione è 3x1.
# Riferimento: https://temugeb.github.io/python/computer_vision/2021/06/15/QR-Code_Orientation.html
