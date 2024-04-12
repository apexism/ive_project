from pymycobot.mycobot import MyCobot
import time
import cv2
import os
import threading
from pyzbar import pyzbar
import socket

# 소켓 통신 코드(클라이언트)
def send_data_via_socket(data):
    # 서버의 IP 주소와 포트 번호
    server_ip = '192.168.137.162'  # 서버의 IP 주소 입력
    server_port = 8000  # 서버의 포트 번호 입력

    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 서버에 연결
        client_socket.connect((server_ip, server_port))

        # 데이터 전송
        client_socket.sendall(data.encode())

        print("Data sent successfully via socket.")
    except Exception as e:
        print("Error occurred while sending data via socket:", e)
    finally:
        # 소켓 닫기
        client_socket.close()

# 로봇 제어 함수
def control_robot(mc):
    mc.send_angles([0, 0, 0, 0, 0, 0], 60)
    time.sleep(5)
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()

    while True:
        print("angles", mc.get_angles())
        mc.send_angles([90, 0, 0, 0, -90, 0], 30)
        time.sleep(5)  # 로봇 각 동작 사이의 딜레이 설정
        mc.send_coords([-100, -250, 350, -89.99, 90, -179.91], 10)
        time.sleep(5)
        mc.set_eletric_gripper(0)
        mc.set_gripper_value(100, 20)
        time.sleep(5)
        mc.set_gripper_value(0, 20)
        time.sleep(5)
        

# 카메라 제어 함수
def capture_camera():
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


# 메인 함수
def main():
    mc = MyCobot('/dev/ttyACM0', 115200)

    # 로봇 제어 스레드 시작
    robot_thread = threading.Thread(target=control_robot, args=(mc,))
    robot_thread.start()

    # 카메라 제어 함수 실행
    capture_camera()

if __name__ == "__main__":
    main()
