import cv2 as cv
import glob
import numpy as np
 
images_folder ='C:/Users/maria/Desktop/ControlLab/Control_lab_prog/Calibrazione/Immagini_Calibrazione_4/*.jpg'
images_names = sorted(glob.glob(images_folder))
images = []


for imname in images_names:

    im = cv.imread(imname, 1)

    #frame dimensions. Frames should be the same size.
    width = im.shape[1]
    height = im.shape[0]
    min_dimension = min(height, width)
    new_dimension= min_dimension-2*min_dimension//10
    #print(width)
    #print(height)
    
    # Cut the immage 
    x, y, w, h = width//10, height//10, new_dimension, new_dimension
    cropped_im = im[y:y+h, x:x+w]

    ## Show the cut immage
    #cv.imshow('Immagine originale', im)
    #cv.imshow('Immagine tagliata', cropped_im)
    #cv.waitKey(500)

    # add the image to the list
    images.append(cropped_im)  

#criteria used by checkerboard pattern detector.
#Change this if the code can't find the checkerboard
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
rows = 5 #number of checkerboard rows.
columns = 8 #number of checkerboard columns.
world_scaling = 1. #change this to the real world square size. Or not.
 
#coordinates of squares in the checkerboard world space
objp = np.zeros((rows*columns,3), np.float32)
objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
objp = world_scaling* objp

#Pixel coordinates of checkerboards
imgpoints = [] # 2d points in image plane.
 
#coordinates of the checkerboard in checkerboard world space.
objpoints = [] # 3d point in real world space
 
 
for frame in images:
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
 
    #find the checkerboard
    ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)
    print(ret)

    if ret == True:
        #Convolution size used to improve corner detection. Don't make this too large.
        conv_size = (11, 11)
 
        #opencv can attempt to improve the checkerboard coordinates
        corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
        cv.drawChessboardCorners(frame, (rows,columns), corners, ret)

        cv.namedWindow('img', cv.WINDOW_NORMAL)
        cv.resizeWindow('img', 500, 500)
        cv.imshow('img', frame)
        k = cv.waitKey(500)
 
        objpoints.append(objp)
        imgpoints.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
        print(ret)
        print(mtx)
        print(dist)
        print(rvecs)
        print(tvecs)

        #salvataggio dei dati in un file .npz
        path = 'C:/Users/maria/Desktop/ControlLab/Control_lab_prog/Calibrazione/B.npz'
        np.savez(path, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)