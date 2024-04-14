from camera_control import *
from pick_place import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket



def whole_scan():
    image_count = 0
    cap = cv2.VideoCapture('/dev/video2')
    save_directory = "img_capture"
    os.makedirs(save_directory, exist_ok=True)

    while True:
        ret, frame = cap.read()

        # 그레이스케일 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # QR 코드 디코딩
        qrcodes = pyzbar.decode(gray)

        for qrcode in qrcodes:
            # QR 코드의 위치 정보 가져오기
            (x, y, w, h) = qrcode.rect
            # QR 코드 주변에 네모 그리기
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # QR 코드 데이터를 소켓 통신을 통해 전송
            qrcode_data = qrcode.data.decode("utf-8")
            # QR 코드 데이터와 타입을 네모 위에 출력
            cv2.putText(frame, qrcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print("Found QR code:", qrcode_data)

        # 화면에 웹캠 이미지와 QR 코드 표시
        cv2.imshow("webcam", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    pass



def picking_scan():
    # QR코드 스캔하여 박스위치 파악하는 스캔 작업



    pass


#


def placing_scan():
    # 상자를 놓읗 위치를 스캔


    pass