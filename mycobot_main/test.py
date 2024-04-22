from camera_control import *
# from pick_place import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket


mc = MyCobot('/dev/ttyACM0', 115200)
# 로봇 제어 함 

# 로봇팔 home position
def init_position():
    print("go to home", mc.get_angles())
    mc.send_angles([0, 0, 0, 0, 0, 0], 15)
    time.sleep(10)
    # coords = mc.get_coords()
    # print(coords)
    # mc.send_coords([119, -200, 195, -99, -5.63, -99.04], 15)       # 원래 책상보는 각도
    # mc.send_coords([119.5, -200.5, 195, -99.97, -5.63, -99.04], 15)     # 모니터 보는 각도

    # mc.send_coords([-10, -266, 250, 180, 0, -90],15)     # 지금 책상보는 각도


    # time.sleep(10)
    coords = mc.get_coords()
    print(coords)
    time.sleep(5)
    # m    # time.sleep(5)c.set_gripper_mode(0)
    # mc.init_eletric_gripper()

    # mc.set_eletric_gripper(1)
    # mc.set_gripper_value(0, 20)


init_position()