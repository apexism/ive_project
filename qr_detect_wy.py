import cv2
import os
import pyzbar.pyzbar as pyzbar
import numpy as np
import math

image_count = 0
cap = cv2.VideoCapture('/dev/video2')  # 카메라 장치 설정
save_directory = "img_capture"
os.makedirs(save_directory, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qrcodes = pyzbar.decode(gray)

    for qrcode in qrcodes:
        (x, y, w, h) = qrcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        qrcode_data = qrcode.data.decode("utf-8")
        cv2.putText(frame, qrcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        print("Found QR code:", qrcode_data)

        # QR 코드의 픽셀 수 계산 및 출력
        pixel_count = w * h
        print(f"QR code pixel count: {pixel_count}")

        if pixel_count !=0 :


            depth = math.sqrt((1600)/pixel_count)/0.0016
            print(f"depth: {depth}")
        print(w,h)


    cv2.imshow("webcam", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        img_path = os.path.join(save_directory, f"original_frame_{image_count}.png")
        cv2.imwrite(img_path, frame)
        print(f"Captured and saved original image to {img_path}")
        image_count += 1

cap.release()
cv2.destroyAllWindows()
