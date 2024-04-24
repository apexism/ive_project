from camera_control import *
import pick_place as pp
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket
import color_detect as cd


mc = MyCobot('/dev/ttyACM0', 115200)
# 로봇 제어 함 

# 로봇팔 home position
def init_position():
    print("go to home", mc.get_angles())
    time.sleep(5)

    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()
    time.sleep(1)

    # Tool initialization
    # mc.set_end_type(1)
    # mc.set_tool_reference([0,-85,0,0,0,0])

    mc.send_angles([155.83, -29.09, 73.3, 42.62, -88.68, -27.59], 20)
    time.sleep(5)
    mc.send_coords([142.1, 4.5, 308.6, -180, 0.0, -90], 20)
        
    time.sleep(5)
    # mc.set_eletric_gripper(1)
    # mc.set_gripper_value(50, 20, 1)
    # time.sleep(3)
    
    x, y, w, h, ang = cd.c_detect()
    print(f"x:{x}, y:{y}, w:{w}, h:{h}, angle:{ang}")
    
    # ang = ang 
    w_px = 26 / w
    h_px = 26 / h
    x = x * w_px
    y = y * h_px
    
    # ang = ang - 90

    print(f"x:{x}, y:{y}, w:{w}, h:{h}, angle:{ang}")

    # coords = mc.get_coords)
    # print(coords)

    
    
    # print(mc.get_gripper_value())
    # mc.set_end_type(1)
    # mc.set_tool_reference([0,0,180,0,0,0])
    mc.send_angles([158.29, -4.21, 69.52, 23.9, -83.75, 61.87], 20)
    time.sleep(5)
    mc.send_coords([215, -50, 285, 160, 5, -180], 20)
    time.sleep(10)
    # mc.send_coords([277.0 - y, 10.0 - x, 120.0, -180.0, 0.0, 0.0 + ang], 20)
    # time.sleep(5)
    pp.close_gripper(mc)
    # print(mc.get_gripper_value())
    pp.open_gripper(mc)
    # print(mc.get_gripper_value())

    coords = mc.get_coords()
    print(coords)
    angles = mc.get_angles()
    print(angles)
    
    # m    # time.sleep(5)c.set_gripper_mode(0)
    # mc.init_eletric_gripper()

    # mc.set_eletric_gripper(1)
    # mc.set_gripper_value(0, 20)


init_position()