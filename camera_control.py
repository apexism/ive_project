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


def whole_scan():
    cap = cv2.VideoCapture(0)

    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         continue

    #     decoded_objects = decode(frame)
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

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    ret, frame = cap.read()
    if not ret:
        print("Failed to load camera!!")

    # 프레임의 너비와 높이 구하기
    height, width, _ = frame.shape

    # 프레임을 2행 3열로 나누기
    rows = 2
    cols = 3
    row_height = height / rows
    col_width = width / cols

    segments = []

    for i in range(rows):
        for j in range(cols):
            start_y = i * row_height
            end_y = (i + 1) * row_height
            start_x = j * col_width
            end_x = (j + 1) * col_width

            segment = frame[start_y:end_y, start_x:end_x]
            segments.append(segment)

    decoded_objects = decode(segments)
    if decoded_objects:
        for obj in decoded_objects:
            print('QR Code:', obj.data.decode())

            points = obj.polygon
            # Create convex hull around points if there are more than 4
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            n = len(hull)
            for j in range(n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
                cv2.putText(frame, f'({hull[j][0]}, {hull[j][1]})', hull[j], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Calculate the area of the polygon formed by the points of the QR code
            pixel_count = cv2.contourArea(np.array(hull))
            print(f"QR code pixel count: {pixel_count}")

            if pixel_count != 0:
                depth = math.sqrt((1600) / pixel_count) / 0.0016
                print(f"depth: {depth}")

    cv2.imshow("QR Code Scanner", frame)

    cap.release()
    cv2.destroyAllWindows()


def picking_scan():
    # QR코드 스캔하여 박스위치 파악하는 스캔 작업



    pass





def placing_scan():
    # 상자를 놓읗 위치를 스캔


    pass