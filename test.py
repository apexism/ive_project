from camera_control import *
# from pick_place import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket


mc = MyCobot('COM3', 115200)
# 로봇 제어 함 

# 로봇팔 home position
def init_position():
    print("go to home", mc.get_angles())
    # mc.send_angles([0, 0, 0, 0, 0, 0], 15)
    # time.sleep(10)
    coords = mc.get_coords()
    print(coords)
    mc.send_coords([35, 250, 220, -180, 0, 90], 15)
    # time.sleep(10)
    coords = mc.get_coords()
    print(coords)
    time.sleep(5)
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()

    mc.set_eletric_gripper(1)
    mc.set_gripper_value(0, 20)
    time.sleep(5)

init_position()