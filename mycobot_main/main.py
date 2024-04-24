from pymycobot.mycobot import MyCobot               #mycobot 라이브러리 import

import camera_control as cc                         #사용자 정의 모듈들(cc: 카메라 스캔 관련, pp: 로봇 움직임 관련, cd: 색상 및 객체 인식)                         
from pick_place import pp
import color_detect as cd

from pyzbar import pyzbar                           #바코드 인식 관련 모듈
from pyzbar.pyzbar import decode

import time
import cv2
import os
import socket                                       #소켓통신
import numpy as np
import math
import sys



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

# 환경별 포트 셋팅
def port_setting():                                                              
    if sys.platform == 'win32':
        return "COM3", 115200
    return "/dev/ttyACM0", 115200

# 메인 함수
def main():
    port, baud = port_setting()
    mc = MyCobot(port, baud)
    
   
    while True:

        # init_position(mc)
        # goto_photo(mc)
        # whole_scan()
        # goto_pick(mc)
        # open_gripper(mc)
        # picking_scan()
        # picking_control(mc)
        # close_gripper(mc)
        # goto_place(mc)
        # open_gripper(mc)
        # close_gripper(mc)



      

if __name__ == "__main__":
    main()
