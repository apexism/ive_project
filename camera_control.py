from camera_control import *
from pick_place import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
import numpy as np
import math
import socket


# def whole_scan():
#     cap = cv2.VideoCapture(0)

#     # while True:
#     #     ret, frame = cap.read()
#     #     if not ret:
#     #         continue

#     #     decoded_objects = decode(frame)
#     #     if decoded_objects:
#     #         for obj in decoded_objects:
#     #             print('QR Code:', obj.data.decode())

#     #             points = obj.polygon
#     #             # Create convex hull around points if there are more than 4
#     #             if len(points) > 4:
#     #                 hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
#     #                 hull = list(map(tuple, np.squeeze(hull)))
#     #             else:
#     #                 hull = points

#     #             n = len(hull)
#     #             for j in range(n):
#     #                 cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
#     #                 cv2.putText(frame, f'({hull[j][0]}, {hull[j][1]})', hull[j], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     #             # Calculate the area of the polygon formed by the points of the QR code
#     #             pixel_count = cv2.contourArea(np.array(hull))
#     #             print(f"QR code pixel count: {pixel_count}")

#     #             if pixel_count != 0:
#     #                 depth = math.sqrt((1600) / pixel_count) / 0.0016
#     #                 print(f"depth: {depth}")

#     #     cv2.imshow("QR Code Scanner", frame)

#     #     if cv2.waitKey(1) & 0xFF == ord('q'):
#     #         break

#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to load camera!!")

#     # 프레임의 너비와 높이 구하기
#     height, width, _ = frame.shape

#     # 프레임을 2행 3열로 나누기
#     rows = 2
#     cols = 3
#     row_height = height / rows
#     col_width = width / cols

#     segments = []

#     for i in range(rows):
#         for j in range(cols):
#             start_y = i * row_height
#             end_y = (i + 1) * row_height
#             start_x = j * col_width
#             end_x = (j + 1) * col_width

#             segment = frame[start_y:end_y, start_x:end_x]
#             segments.append(segment)

#     decoded_objects = decode(segments)
#     if decoded_objects:
#         for obj in decoded_objects:
#             print('QR Code:', obj.data.decode())

#             points = obj.polygon
#             # Create convex hull around points if there are more than 4
#             if len(points) > 4:
#                 hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
#                 hull = list(map(tuple, np.squeeze(hull)))
#             else:
#                 hull = points

#             n = len(hull)
#             for j in range(n):
#                 cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
#                 cv2.putText(frame, f'({hull[j][0]}, {hull[j][1]})', hull[j], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             # Calculate the area of the polygon formed by the points of the QR code
#             pixel_count = cv2.contourArea(np.array(hull))
#             print(f"QR code pixel count: {pixel_count}")

#             if pixel_count != 0:
#                 depth = math.sqrt((1600) / pixel_count) / 0.0016
#                 print(f"depth: {depth}")

#     cv2.imshow("QR Code Scanner", frame)

#     cap.release()
#     cv2.destroyAllWindows()

def scan_qr_codes(image):
    """이미지에서 QR 코드를 스캔하고 검출된 QR 코드의 데이터를 반환합니다."""
    qr_codes = pyzbar.decode(image)
    return [qr_code.data.decode('utf-8') for qr_code in qr_codes]

def scan_frame(frame, height, width, scan_size, step_right, step_down, show=False):
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
                display = cv2.rectangle(frame.copy(), (x, y), (x + scan_size[0], y + scan_size[1]), (0, 255, 0), 2)
                cv2.imshow("Scanning QR Codes", display)
                cv2.waitKey(1)  # Refresh display
            x += step_right
        y += step_down
    return detected_qr_codes, qr_code_locations

def whole_scan(camera_index=2):
    # 카메라 초기화
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detected_qr_codes = set()

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

            # 스캔 (이미지 표시)
            new_scan_results, locations = scan_frame(frame, height, width, scan_size, step_right, step_down, show=True)
            detected_qr_codes.update(new_scan_results)

            print("Current detected QR Codes:", len(detected_qr_codes))
            time.sleep(1)  # 각 스캔 사이에 간격을 둡니다.

    except KeyboardInterrupt:
        print("Scanning stopped.")

    finally:
        cap.release()
        cv2.destroyAllWindows()

    # QR 코드 데이터를 첫 번째 필드(고유 번호)를 기준으로 정렬
    sorted_qr_codes = sorted(detected_qr_codes, key=lambda x: int(x.split(',')[0]))

    # 최종 검출된 QR 코드 출력
    print("Detected QR Codes:")
    for qr in sorted_qr_codes:
        print(qr)


def picking_scan():
    # QR코드 스캔하여 박스위치 파악하는 스캔 작업



    pass





def placing_scan():
    # 상자를 놓읗 위치를 스캔


    pass