import cv2
import os
import pyzbar.pyzbar as pyzbar


image_count = 0
cap = cv2.VideoCapture('/dev/video2')  # 카메라 장치 설정
save_directory = "img_capture"
os.makedirs(save_directory, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        continue

    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # QR 코드 디코딩
    qrcodes = pyzbar.decode(gray)

    for qrcode in qrcodes:
        # QR 코드의 위치 정보 가져오기
        (x, y, w, h) = qrcode.rect
        # QR 코드 주변에 네모 그리기
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # QR 코드 데이터를 소켓 통신을 통해 전송 (이 부분은 적용할 소켓 코드에 맞춰 작성)
        qrcode_data = qrcode.data.decode("utf-8")
        # QR 코드 데이터와 타입을 네모 위에 출력
        cv2.putText(frame, qrcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        print("Found QR code:", qrcode_data)

    # 화면에 웹캠 이미지와 QR 코드 표시
    cv2.imshow("webcam", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):  # 'c' 키를 누르면 화면 캡쳐
        img_path = os.path.join(save_directory, f"original_frame_{image_count}.png")
        cv2.imwrite(img_path, frame)
        print(f"Captured and saved original image to {img_path}")
        image_count += 1

cap.release()
cv2.destroyAllWindows()

