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
    mc.send_angles([8.43, 22.06, -75.67, -31.64, 90, 0], 40)

    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()
    time.sleep(1)

    # Tool initialization
    mc.set_end_type(1)
    mc.set_tool_reference([0,-85,0,0,0,0])

    mc.send_coords([240.8, -52.3, 321.1, -174.81, 0.26, -81.45], 40)

    # gripper initialization
    # pp.init_gripper(mc)
    # gripper close
    # pp.close_gripper(mc)


    
    print(mc.get_gripper_value())
    
    time.sleep(5)
    
    x, y, w, h, ang = cd.c_detect()
    print(f"x:{x}, y:{y}, w:{w}, h:{h}, angle:{ang}")
    
    ang = ang - 90
    # w_px = 1
    # h_px = 1
    w_px = 26 / w
    h_px = 26 / h
    x = x * w_px
    y = y * h_px
    
    # ang = ang - 90

    print(f"x:{x}, y:{y}, w:{w}, h:{h}, angle:{ang}")

    # coords = mc.get_coords)
    # print(coords)

    
    # pp.open_gripper(mc)
    # print(mc.get_gripper_value())
    mc.set_end_type(1)
    mc.set_tool_reference([0,0,180,0,0,0])
    mc.send_coords([260.0 - y, -61.5 - x, 55.0, -174.9, 0.35, -81.61], 40)
    time.sleep(5)
    mc.send_angle(6, ang, 40)
    time.sleep(5)
    mc.send_coord(3, 5, 40)
    time.sleep(5)
    # pp.close_gripper(mc)
    # print(mc.get_gripper_value())
    # pp.open_gripper(mc)
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