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

mc = MyCobot('/dev/ttyACM0', 115200)
angles = mc.get_angles()
coords = mc.get_coords()
# 로봇 제어 함

# def gripper_tool_setting():
#     mc.set_end_type(1)
#     mc.set_tool_reference([0,-15,165,0,0,0])
#     pass

# def normal_tool_setting():
#     mc.set_end_type(1)
#     mc.set_tool_reference([0,0,0,0,0,0])
#     pass
def get_angle_wait(a1,a2,a3,a4,a5,a6):
    error = 1.5
    max_a1, min_a1 = a1 + error, a1 - error
    max_a2, min_a2 = a2 + error, a2 - error
    max_a3, min_a3 = a3 + error, a3 - error
    max_a4, min_a4 = a4 + error, a4 - error
    max_a5, min_a5 = a5 + error, a5 - error
    max_a6, min_a6 = a6 + error, a6 - error
    while(1):
        angles = mc.get_angles()
        print(angles[0],angles[1],angles[2],angles[3],angles[4],angles[5])
        if (min_a1 < angles[0] < max_a1 and min_a2 < angles[1] < max_a2 and
            min_a3 < angles[2] < max_a3 and min_a4 < angles[3] < max_a4 and
            min_a5 < angles[4] < max_a5 and min_a6 < angles[5] < max_a6) :
            break

def get_coords_wait(x,y,z,roll,pitch,yaw):
    error = 3
    max_x, min_x = x + error, x - error
    max_y, min_y = y+ error, y - error
    max_z, min_z = z + error, z - error
    max_roll, min_roll = roll + error, roll - error
    max_pitch, min_pitch = pitch + error, pitch - error
    max_yaw, min_yaw = yaw + error, yaw - error
    while(1):
        coords = mc.get_coords()
        print(coords)
        if (min_x < coords[0] < max_x and min_y < coords[1] < max_y and
            min_z < coords[2] < max_z and min_roll < coords[3] < max_roll and
            min_pitch < coords[4] < max_pitch and min_yaw < coords[5] < max_yaw) :
            break

# 로봇팔 home position
def init_position(yellow_flag, red_flag, green_flag):
    print("go to home")
    mc.send_angles([0,0,0,0,0,0], 100)
    get_angle_wait(0,0,0,0,0,0)
    #time.sleep(2)
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()
    time.sleep(1)

    # Tool initialization
    mc.set_end_type(1)
    mc.set_tool_reference([0,0,0,0,0,0])

    mc.send_angles([30, -10, -10, -55, 85, -65], 100)
    get_angle_wait(30, -10, -10, -55, 85, -65)
    #time.sleep(2)
    
    # 촬영 모션
    mc.send_coords([142.1, 4.5, 308.6, -180, 0.0, -90], 100)
    get_coords_wait(142.1, 4.5, 308.6, -180, 0.0, -90)
    #time.sleep(8)
    
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
        x = x * w_px + 12
        y = y * h_px - 7

        print(f"x:{x}mm, y:{y}mm, w:{w}, h:{h}, angle:{ang}")
        
        # 툴 세팅
        mc.set_end_type(1)
        mc.set_tool_reference([0,-15,165,0,0,0])
        time.sleep(1)

        # 피킹 진입 모션
        mc.send_coords([225 - y, 20 - x, 170, 180, 0, -ang], 100)
        print(f"@@@@@@@: {mc.get_coords()}")
        get_coords_wait(225 - y, 20 - x, 170, 180, 0, -ang)
        #time.sleep(3)

        mc.set_eletric_gripper(1)
        mc.set_gripper_value(50, 20, 1)
        time.sleep(1)

        # 피킹 포지션
        mc.send_coords([225 - y, 20 - x, 135, 180, 0, -ang], 60)
        get_coords_wait(225 - y, 20 - x, 135, 180, 0, -ang)
        #time.sleep(5)
        pp.close_gripper(mc)
        time.sleep(1)

        # 피킹 후 빠져나오는 모션
        mc.send_coords([225 - y, 20 - x, 170, 180, 0, -ang], 100)
        get_coords_wait(225 - y, 20 - x, 170, 180, 0, -ang)
        #time.sleep(2)

        # plc에 동작 신호 보내기
        mc.set_basic_output(1,0)
        # time.sleep(1)
        mc.set_basic_output(1,1)
        # time.sleep(1)
        mc.set_basic_output(2,1)
        # time.sleep(1)

        mc.send_angles([66, -5, 50, 45, -90, -25], 100)
        get_angle_wait(66, -5, 50, 45, -90, -25)
        #time.sleep(2)

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
                z_offset = 26
            elif green_flag == 2:
                z_offset = 26 * 2
            else:
                z_offset = 26 * 2
            x_offset = 70
            green_flag += 1

        # 플레이싱 진입 모션
        mc.send_coords([0 + x_offset, -230 , 150, -180, -0, -90], 100)
        get_coords_wait(0 + x_offset, -230 , 150, -180, -0, -90)
        #time.sleep(3)

        # 플레이싱 포지션
        mc.send_coords([0 + x_offset, -230 , 27 + z_offset, -180, -0, -90], 70)
        get_coords_wait(0 + x_offset, -230 , 27 + z_offset, -180, -0, -90)
        #time.sleep(7)
        
        pp.open_gripper(mc)
        time.sleep(1)

        print(f"yellow_flag: {yellow_flag}, red_flag: {red_flag}, green_flag: {green_flag}, blue_flag: {blue_flag}")

        # 플레이싱 후 빠져 나오는 모션
        mc.send_coords([0 + x_offset, -230 , 150, -180, -0, -90], 100)
        #get_coords_wait(0 + x_offset, -230 , 150, -180, -0, -90)
        time.sleep(2)
        
        mc.set_eletric_gripper(0)
        mc.set_gripper_value(30, 20, 1)
        time.sleep(1)

        coords = mc.get_coords()
        print(coords)
        angles = mc.get_angles()
        print(angles)

    return (yellow_flag, red_flag, green_flag)




while True:

    yellow_flag, red_flag, green_flag = init_position(yellow_flag, red_flag, green_flag)