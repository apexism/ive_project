from camera_control import *
from pick_place import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
import socket
import numpy as np
import math

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



# 메인 함수
def main():
    mc = MyCobot('/dev/ttyACM0', 115200)
   
    while True:

        init_position(mc)
        goto_photo(mc)
        whole_scan()
        goto_pick(mc)
        open_gripper(mc)
        picking_scan()
        picking_control(mc)
        close_gripper(mc)
        goto_place(mc)
        open_gripper(mc)
        close_gripper(mc)

      

if __name__ == "__main__":
    main()
