import numpy as np
import cv2
import math


class PoseEstimator:

    def __init__(self, calibration_matrix_path):
        self.cmtx, self.dist = self.read_camera_parameters(calibration_matrix_path)

    def read_camera_parameters(self, calibration_matrix_path):
        """ Read camera intrinsic parameters."""
        # Load previously saved data
        with np.load(calibration_matrix_path) as X:
            cmtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]

        # cmtx = camera matrix, dist = distortion parameters
        return np.array(cmtx), np.array(dist)

    def get_qr_coords(self, points):
        # Selected coordinate points for each corner of QR code.
        qr_edges = np.array([[0, 0, 0],
                             [0, 1, 0],
                             [1, 1, 0],
                             [1, 0, 0]], dtype='float32').reshape((4, 1, 3))

        # determine the orientation of QR code coordinate system with respect to camera coorindate system.
        ret, rvec, tvec = cv2.solvePnP(qr_edges, points, self.cmtx, self.dist)

        # Define unit xyz axes. These are then projected to camera view using the rotation matrix and translation vector.
        unitv_points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype='float32').reshape((4, 1, 3))
        if ret:
            points, jac = cv2.projectPoints(unitv_points, rvec, tvec, self.cmtx, self.dist)
            # the returned points are pixel coordinates of each unit vector.
            return points, rvec, tvec

        # return empty arrays if rotation and translation values not found
        else:
            return [], [], []


    def show_axes(self, frame, pixel_into_img, qr_size_cm):

        qr = cv2.QRCodeDetector()
        ret_qr, points = qr.detect(frame)

        if ret_qr:
            # the position of the QR code with respect to the camera is saved in tvec
            axis_points, rvec, tvec = self.get_qr_coords(points)

            # the location of the camera from the new QR code coordinates is calculated as:
            # rvec, jacobian = cv2.Rodrigues(rvec)  # converte un vettore di rotazione in una matrice di rotazione
            # camera_position = -rvec.transpose() @ tvec

            # BGR color format
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]

            # check axes points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4, 2))

                origin = (int(axis_points[0][0]), int(axis_points[0][1]))
                first_row = axis_points[1]
                qr_code_pixel_size = math.sqrt(
                    (int(first_row[0]) - origin[0]) ** 2 + (int(first_row[1]) - origin[1]) ** 2)

                for p, c in zip(axis_points[1:], colors[:3]):
                    p = (int(p[0]), int(p[1]))

                    # Sometimes qr detector will make a mistake and projected point will overflow integer value. We skip these cases.
                    if origin[0] > 5 * frame.shape[1] or origin[1] > 5 * frame.shape[1]: break
                    if p[0] > 5 * frame.shape[1] or p[1] > 5 * frame.shape[1]: break

                    cv2.line(frame, origin, p, c, 5)

            cv2.line(frame, pixel_into_img, pixel_into_img, 3, 10)  # print di pixel in the vide
            cv2.imshow('frame', frame)

        # # Calcolo la posizione del pixel nel sistema di riferikento del qr code
        # pixel_into_QRc = point_in_qr_reference_frame(pixel_into_img, rvec, tvec, qr_code_pixel_size, qr_size_cm)
        #
        # if pixel_into_QRc is not None:
        #     print("Posizione nel sistema di riferimento del QR code:", pixel_into_QRc)
        # else:
        #     print("Impossibile trovare la posizione nel sistema di riferimento del QR code.")
    #

            return tvec, rvec#, pixel_into_QRc
        return [], []
    #
    #
    # def point_in_qr_reference_frame(point, rvec, tvec, qr_code_pixel_size, qr_size_cm):
    #     # Punto da convertire nel sistema di riferimento del QR code
    #     point_homogeneous = np.append(point, 1)  # Aggiunge 1 per trattare il punto come coordinate omogenee
    #
    #     # Applica la trasformazione inversa per ottenere il punto nel sistema di riferimento del QR code: P=tran.R*P'+T
    #     R_camera_to_qr = np.transpose(rvec)
    #     t_camera_to_qr = np.dot(-R_camera_to_qr, tvec)
    #     point_in_qr_frame = np.dot(R_camera_to_qr, point_homogeneous) + t_camera_to_qr
    #
    #     ## Considera le dimensioni del QR code per convertire le coordinate
    #     # scale_factor = qr_code_pixel_size / qr_size_cm  # Dimensione del QR code rispetto al suo size standard (4.4 cm)
    #     # point_in_qr_frame[:3] *= scale_factor
    #
    #     return point_in_qr_frame[:3]  # Restituisce le prime tre coordinate come coordinate non omogenee