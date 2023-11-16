import numpy as np
import cv2 as cv
import sys
import math


def read_camera_parameters(filepath ='C:/Users/maria/Desktop/ControlLab/Control_lab_prog/Calibrazione/B.npz'):

    # Load previously saved data
    with np.load(filepath) as X:
        cmtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

    #cmtx = camera matrix, dist = distortion parameters
    return np.array(cmtx), np.array(dist)



def get_qr_coords(cmtx, dist, points):

    #Selected coordinate points for each corner of QR code.
    qr_edges = np.array([[0,0,0],
                         [0,1,0],
                         [1,1,0],
                         [1,0,0]], dtype = 'float32').reshape((4,1,3))

    #determine the orientation of QR code coordinate system with respect to camera coorindate system.
    ret, rvec, tvec = cv.solvePnP(qr_edges, points, cmtx, dist)
    
    #Define unit xyz axes. These are then projected to camera view using the rotation matrix and translation vector.
    unitv_points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]], dtype = 'float32').reshape((4,1,3))
    if ret:
        points, jac = cv.projectPoints(unitv_points, rvec, tvec, cmtx, dist)
        #the returned points are pixel coordinates of each unit vector.
        return points, rvec, tvec
    

    #return empty arrays if rotation and translation values not found
    else: return [], [], []



def show_axes(cmtx, dist, in_source, pixel_into_img, qr_size_cm):
    cap = cv.VideoCapture(in_source)

    qr = cv.QRCodeDetector()

    while True:

        ret, img = cap.read()
        if ret == False: break

        ret_qr, points = qr.detect(img)

        if ret_qr:

            # the position of the QR code with respect to the camera is saved in tvec
            axis_points, rvec, tvec = get_qr_coords(cmtx, dist, points)

            # print(axis_points)

            # the location of the camera from the new QR code coordinates is calculated as:
            rvec, jacobian = cv.Rodrigues(rvec)  # converte un vettore di rotazione in una matrice di rotazione
            camera_position = -rvec.transpose() @ tvec

            #BGR color format
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)]

            #check axes points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4,2))

                origin = (int(axis_points[0][0]),int(axis_points[0][1]) )
                first_row=axis_points[1]
                qr_code_pixel_size=math.sqrt((int(first_row[0]) - origin[0])**2 + (int(first_row[1]) - origin[1])**2)

                for p, c in zip(axis_points[1:], colors[:3]):
                    p = (int(p[0]), int(p[1]))

                    #Sometimes qr detector will make a mistake and projected point will overflow integer value. We skip these cases. 
                    if origin[0] > 5*img.shape[1] or origin[1] > 5*img.shape[1]:break
                    if p[0] > 5*img.shape[1] or p[1] > 5*img.shape[1]:break

                    cv.line(img, origin, p, c, 5)

        cv.line(img, pixel_into_img, pixel_into_img, 3, 10)     #print di pixel in the vide
        cv.imshow('frame', img)

        # Calcolo la posizione del pixel nel sistema di riferikento del qr code
        pixel_into_QRc=point_in_qr_reference_frame(pixel_into_img, rvec, tvec, qr_code_pixel_size, qr_size_cm)

        if pixel_into_QRc is not None:
            print("Posizione nel sistema di riferimento del QR code:", pixel_into_QRc)
        else:
           print("Impossibile trovare la posizione nel sistema di riferimento del QR code.")

        

        k = cv.waitKey(20)
        if k == 27: break #27 is ESC key.


    cap.release()
    cv.destroyAllWindows()
    return tvec, rvec, pixel_into_QRc



def point_in_qr_reference_frame(point, rvec, tvec, qr_code_pixel_size, qr_size_cm):

    # Punto da convertire nel sistema di riferimento del QR code
    point_homogeneous = np.append(point, 1)  # Aggiunge 1 per trattare il punto come coordinate omogenee

    # Applica la trasformazione inversa per ottenere il punto nel sistema di riferimento del QR code: P=tran.R*P'+T
    R_camera_to_qr = np.transpose(rvec)
    t_camera_to_qr = np.dot(-R_camera_to_qr, tvec)
    point_in_qr_frame = np.dot(R_camera_to_qr, point_homogeneous) + t_camera_to_qr

    ## Considera le dimensioni del QR code per convertire le coordinate
    #scale_factor = qr_code_pixel_size / qr_size_cm  # Dimensione del QR code rispetto al suo size standard (4.4 cm)
    #point_in_qr_frame[:3] *= scale_factor

    return point_in_qr_frame[:3]  # Restituisce le prime tre coordinate come coordinate non omogenee




if __name__ == '__main__':

    #read camera intrinsic parameters.
    cmtx, dist = read_camera_parameters()

    pixel_into_img = [840, 450]  # Coordinata x, y del pixel nel frame dell'immagine
    qr_size_cm=4.4
    

    input_source = 'C:/Users/maria/Desktop/ControlLab/Control_lab_prog/Calibrazione/Immagini_Calibrazione_2/Video1.mp4'
    # input_source = 2

    if len(sys.argv) > 1:
        input_source = int(sys.argv[1])

    # tvec, rvec= show_axes(cmtx, dist, input_source)
    tvec, rvec, pixel_into_QRc= show_axes(cmtx, dist, input_source, pixel_into_img, qr_size_cm)

    # ........................COSE DA FARE .....................................................................
    # Implementare il fattore di scala, 
    #           idea: metterlo nella quarrta posizione della posizione omogenea
    #           il riferimento hai centimetri è che la linee degli assi x e y sono di 4,4 cm
    #
    # Far funzionare la Camera come input USB in input surce
    # 
    # Capire prchè la posizione che mi stampa è 6x6 se il vettore di traslazione è 3x1.
    # Riferimento: https://temugeb.github.io/python/computer_vision/2021/06/15/QR-Code_Orientation.html 




    