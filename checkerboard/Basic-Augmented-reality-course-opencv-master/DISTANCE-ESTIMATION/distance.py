import cv2 as cv
from cv2 import aruco
import numpy as np

calib_data_path = "../calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data['camMatrix']
dist_coef = calib_data['distCoef']
r_vectors = calib_data['rVector']
t_vectors = calib_data['tVector']

MARKER_SIZE = 8  # centimeters

# Correctly getting the ArUco dictionary
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            # Various drawing and text functions...
            pass

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
