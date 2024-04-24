# import cv2 as cv
# import numpy as np
# from cv2 import aruco

# def get_marker_transform(rvec, tvec):
#     R, _ = cv.Rodrigues(rvec)
#     tvec = tvec.reshape(3, 1)
#     T = np.hstack((R, tvec))
#     T = np.vstack((T, [0, 0, 0, 1]))
#     return T

# def compute_relative_position(ref_transform, other_transform):
#     ref_inv = np.linalg.inv(ref_transform)
#     relative_transform = ref_inv @ other_transform
#     return relative_transform[:3, 3]

# def move_robot_to_marker(marker_position):
#     # 로봇 팔 제어 코드를 여기에 구현
#     # 예: robot_arm.move_to(marker_position)
#     print("Moving robot to:", marker_position)

# calib_data_path = "mycobot_main/calib_data/MultiMatrix.npz"
# calib_data = np.load(calib_data_path)
# cam_mat = calib_data["camMatrix"]
# dist_coef = calib_data["distCoef"]
# MARKER_SIZE = 3  # centimeters
# marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
# param_markers = aruco.DetectorParameters_create()

# cap = cv.VideoCapture(2)
# ref_transform = None
# marker_positions = {}

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     marker_corners, marker_IDs, _ = aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
    
#     if marker_corners:
#         rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cam_mat, dist_coef)
#         for ids, corners, rvec, tvec in zip(marker_IDs, marker_corners, rVec, tVec):
#             if ids[0] == 0:
#                 ref_transform = get_marker_transform(rvec, tvec)
#             elif ref_transform is not None:
#                 current_transform = get_marker_transform(rvec, tvec)
#                 relative_position = compute_relative_position(ref_transform, current_transform)
#                 marker_positions[ids[0]] = relative_position

#             cv.aruco.drawDetectedMarkers(frame, [corners])
#             cv.aruco.drawAxis(frame, cam_mat, dist_coef, rvec, tvec, MARKER_SIZE / 100)

#     cv.imshow("frame", frame)
#     key = cv.waitKey(1)
#     if key in [ord(str(num)) for num in range(1, 7)]:  # 숫자 1-6 키 입력 감지
#         marker_id = key - ord('0')
#         if marker_id in marker_positions:
#             move_robot_to_marker(marker_positions[marker_id])
#         else:
#             print(f"Marker {marker_id} not detected.")
#     elif key == ord("q"):
#         break

# cap.release()
# cv.destroyAllWindows()


import cv2 as cv
import numpy as np
from cv2 import aruco
from pymycobot.mycobot import MyCobot

# MyCobot 로봇 초기화
mc = MyCobot('/dev/ttyACM0', 115200)

def get_marker_transform(rvec, tvec):
    R, _ = cv.Rodrigues(rvec)  # 회전 벡터를 회전 행렬로 변환
    tvec = tvec.reshape(3, 1)  # tvec 차원 변경: (1, 3, 3) -> (3, 1)
    T = np.hstack((R, tvec))  # 회전 행렬과 변환 벡터를 수평 결합
    T = np.vstack((T, [0, 0, 0, 1]))  # 변환 행렬을 4x4 동차 좌표 변환 행렬로 확장
    return T

def compute_relative_position(ref_transform, other_transform):
    ref_inv = np.linalg.inv(ref_transform)
    relative_transform = ref_inv @ other_transform
    return relative_transform[:3, 3]

def move_robot_to_marker(marker_position):
    # 로봇 팔의 위치 조정
    # 예시로 변환을 적용하지 않고 직접 좌표를 전달
    x, y, z = marker_position * 100  # 변환: 미터를 센티미터로
    coords = [x, y, z, -90, 0, -90]  # 로봇팔의 좌표 설정
    mc.send_coords(coords, 15)  # 속도 15로 좌표로 이동
    print("Moving robot to:", coords)

calib_data_path = "mycobot_main/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
MARKER_SIZE = 3  # centimeters
marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(2)
ref_transform = None
marker_positions = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, _ = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        for ids, corners, rvec, tvec in zip(marker_IDs, marker_corners, rVec, tVec):
            if ids[0] == 0:
                ref_transform = get_marker_transform(rvec, tvec)
            elif ref_transform is not None:
                current_transform = get_marker_transform(rvec, tvec)
                relative_position = compute_relative_position(ref_transform, current_transform)
                marker_positions[ids[0]] = relative_position

            cv.aruco.drawDetectedMarkers(frame, [corners])
            cv.aruco.drawAxis(frame, cam_mat, dist_coef, rvec, tvec, MARKER_SIZE / 100)

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key in [ord(str(num)) for num in range(1, 7)]:  # 숫자 1-6 키 입력 감지
        marker_id = key - ord('0')
        if marker_id in marker_positions:
            move_robot_to_marker(marker_positions[marker_id])
            
        else:
            print(f"Marker {marker_id} not detected.")
    elif key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
