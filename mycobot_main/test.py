from camera_control import *
import pick_place as pp
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket
import color_detect as cd

yellow_flag = 0
red_flag = 0
blue_flag = 0
green_flag = 0

mc = MyCobot('/dev/ttyACM1', 115200)
# 로봇 제어 함

# 로봇팔 home position
def init_position(yellow_flag, red_flag, green_flag):
    print("go to home")
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()
    mc.send_angles([0,0,0,0,0,0], 100)
    time.sleep(2)
    

    # Tool initialization
    mc.set_end_type(1)
    mc.set_tool_reference([0,0,0,0,0,0])

    # mc.send_angles([155.83, -29.09, 73.3, 42.62, -88.68, -27.59], 20)
    # mc.send_angles([155.83, -29.09, 63.3, 42.62, -88.68, -27.59], 100)
    # time.sleep(2)
    # mc.send_angles([30, -10, -10, -55, 85, -65], 100)
    # time.sleep(1)
    
    # 촬영 모션
    mc.send_coords([142.1, 4.5, 320, -180, 0.0, -90], 100)
    time.sleep(5)
    
    color, x, y, w, h, ang = cd.c_detect()
    if color == "b":
        # plc에 동작 신호 보내기
        mc.set_basic_output(1,0)
        # time.sleep(1)
        mc.set_basic_output(1,1)
        # time.sleep(1)
        mc.set_basic_output(2,1)
        # time.sleep(1)
    else:
        print(f"x:{x}px, y:{y}px, w:{w}, h:{h}, angle:{ang}")

        w_px = 26 / w
        h_px = 26 / h
        x = x * w_px
        y = y * h_px

        print(f"x:{x}mm, y:{y}mm, w:{w}, h:{h}, angle:{ang}")
        
        # mc.send_angles([0,0,0,0,0,0], 100)
        # time.sleep(2)
        # mc.send_angles([30, -10, -10, -55, 85, -65], 100)
        # time.sleep(2)
        
        # 툴 세팅
        mc.set_end_type(1)
        mc.set_tool_reference([0,-15,165,0,0,0])
        # time.sleep(1)

        # 피킹 진입 모션
        mc.send_coords([235 - y, -5 - x, 170, 180, 0, -ang], 100)
        print(f"@@@@@@@: {mc.get_coords()}")
        time.sleep(2.5)

        mc.set_eletric_gripper(1)
        mc.set_gripper_value(50, 20, 1)
        time.sleep(1)

        # 피킹 포지션
        mc.send_coords([235 - y, -5 - x, 140, 180, 0, -ang], 60)
        time.sleep(4)
        pp.close_gripper(mc)
        # time.sleep(1)

        # 피킹 후 빠져나오는 모션
        mc.send_coords([235 - y, -5 - x, 180, 180, 0, -ang], 100)
        time.sleep(3)

        # plc에 동작 신호 보내기
        mc.set_basic_output(1,0)
        # time.sleep(1)
        mc.set_basic_output(1,1)
        # time.sleep(1)
        mc.set_basic_output(2,1)
        # time.sleep(1)

        mc.send_angles([66, -5, 50, 45, -90, -25], 100)
        time.sleep(2)

        print(f"yellow_flag: {yellow_flag}, red_flag: {red_flag}, green_flag: {green_flag}, blue_flag: {blue_flag}")

        if color == "y":
            if yellow_flag == 0:
                z_offset = 0
            elif yellow_flag == 1:
                z_offset = 26
            elif yellow_flag == 2:
                z_offset = 26 * 2
            else:
                z_offset = 26 * 2
            x_offset = -80
            yellow_flag += 1
        elif color == "r":
            if red_flag == 0:
                z_offset = 0
            elif red_flag == 1:
                z_offset = 26
            elif red_flag == 2:
                z_offset = 26 * 2
            else:
                z_offset = 26 * 2
            x_offset = -5
            red_flag += 1
        elif color == "g":
            if green_flag == 0:
                z_offset = 0
            elif green_flag == 1:
                z_offset = 24
            elif green_flag == 2:
                z_offset = 24 * 2
            else:
                z_offset = 24 * 2
            x_offset = 70
            green_flag += 1
        # else:
        #     if blue_flag == 0:
        #         z_offset = 0
        #     elif blue_flag == 1:
        #         z_offset = 26
        #     elif blue_flag == 2:
        #         z_offset = 26 * 2
        #     else:
        #         z_offset = 26 * 2
        #     x_offset = 70
        #     blue_flag += 1

        # 플레이싱 진입 모션
        mc.send_coords([0 + x_offset, -230 , 150, -180, -0, -90], 100)
        time.sleep(2)

        # 플레이싱 포지션
        mc.send_coords([0 + x_offset, -230 , 25 + z_offset, -180, -0, -90], 70)
        time.sleep(5)
        
        pp.open_gripper(mc)

        print(f"yellow_flag: {yellow_flag}, red_flag: {red_flag}, green_flag: {green_flag}, blue_flag: {blue_flag}")

        # 플레이싱 후 빠져 나오는 모션
        mc.send_coords([0 + x_offset, -230 , 150, -180, -0, -90], 100)
        time.sleep(1)
        
        # mc.set_eletric_gripper(0)
        # mc.set_gripper_value(20, 20, 1)
        # time.sleep(1)

        coords = mc.get_coords()
        print(coords)
        angles = mc.get_angles()
        print(angles)

        # mc.send_angle(3, 30, 80)
        # time.sleep(3)
        # print("Relaease angle!")
        
        # m    # time.sleep(5)c.set_gripper_mode(0)
        # mc.init_eletric_gripper()

        # mc.set_eletric_gripper(1)
        # mc.set_gripper_value(0, 20)
    return (yellow_flag, red_flag, green_flag)

while True:

    yellow_flag, red_flag, green_flag = init_position(yellow_flag, red_flag, green_flag)