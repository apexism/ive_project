import cv2 as cv
from pyzbar import pyzbar
import time
from cv2 import aruco
import numpy as np

def scan_qr_codes(image):
    """이미지에서 QR 코드를 스캔하고 검출된 QR 코드의 데이터를 반환합니다."""
    qr_codes = pyzbar.decode(image)
    return [qr_code.data.decode('utf-8') for qr_code in qr_codes]

def scan_frame(frame, height, width, scan_size, step_right, step_down, show=False):
    """ 주어진 이미지 프레임을 주기적으로 스캔하여 QR 코드를 탐색하고 위치를 반환합니다."""
    detected_qr_codes = set()
    qr_code_locations = []

    y = 0
    while y + scan_size[1] <= height:
        x = 0
        while x + scan_size[0] <= width:
            roi = frame[y:y+scan_size[1], x:x+scan_size[0]]
            qr_codes = scan_qr_codes(roi)
            for code in qr_codes:
                if code not in detected_qr_codes:
                    detected_qr_codes.add(code)
                    qr_code_locations.append((code, (x, y)))
            if show:
                display = cv.rectangle(frame.copy(), (x, y), (x + scan_size[0], y + scan_size[1]), (0, 255, 0), 2)
                cv.imshow("Scanning QR Codes", display)
                cv.waitKey(1)  # Refresh display
            x += step_right
        y += step_down
    return detected_qr_codes, qr_code_locations

def aruco_scan(frame, calib_data):
    """아르코 마커를 스캔하고 각 마커의 위치와 아이디 정보를 화면에 표시합니다."""
    cam_mat = calib_data["camMatrix"]
    dist_coef = calib_data["distCoef"]

    MARKER_SIZE = 0.03  # meters
    marker_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
    param_markers = cv.aruco.DetectorParameters_create()

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, _ = cv.aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    if marker_corners:
        rVec, tVec, _ = cv.aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        for ids, corners, rvec, tvec in zip(marker_IDs, marker_corners, rVec, tVec):
            cv.aruco.drawDetectedMarkers(frame, [corners])
            cv.aruco.drawAxis(frame, cam_mat, dist_coef, rvec, tvec, 0.03)
            cv.putText(frame, f"ID: {ids[0]} Distance: {np.linalg.norm(tvec):.2f}m", tuple(corners[0][0].astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(f"Detected ArUco marker ID: {ids[0]}, Position: {corners[0][0]}, Distance: {np.linalg.norm(tvec):.2f}m")
    cv.imshow("Aruco Markers", frame)
    cv.waitKey(1)

# 카메라 초기화 및 설정
cap = cv.VideoCapture(2)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

detected_qr_codes = set()

calib_data_path = "mycobot_main/calib_data/MultiMatrix.npz"
calib_data = np.load(calib_data_path)
print(calib_data.files)

try:
    while len(detected_qr_codes) < 6:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 캡쳐할 수 없습니다.")
            continue

        height, width, _ = frame.shape
        scan_size = (213, 240)
        step_right = 106
        step_down = 120

        new_scan_results, locations = scan_frame(frame, height, width, scan_size, step_right, step_down, show=True)
        detected_qr_codes.update(new_scan_results)

        print("Current detected QR Codes:", len(detected_qr_codes))

        aruco_scan(frame, calib_data)

        time.sleep(0.5)  # 각 스캔 사이에 간격을 둡니다.

except KeyboardInterrupt:
    print("Scanning stopped.")

finally:
    cap.release()
    cv.destroyAllWindows()

# QR 코드 데이터를 첫 번째 필드(고유 번호)를 기준으로 정렬
sorted_qr_codes = sorted(detected_qr_codes, key=lambda x: int(x.split(',')[0]))

# 최종 검출된 QR 코드 출력
print("Detected QR Codes:")
for qr in sorted_qr_codes:
    print(qr)
