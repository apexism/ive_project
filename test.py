from camera_control import *
from pick_place import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket


mc = MyCobot('/dev/ttyACM0', 115200)
# 로봇 제어 함 

# 로봇팔 home position

# print("go to home", mc.get_angles())
# mc.send_angles([0, 0, 0, 0, 0, 0], 15)
# time.sleep(10)
coords = mc.get_coords()
print(coords)
mc.send_coords([35, 250, 210, -180, 0, 90], 15)
# time.sleep(10)
coords = mc.get_coords()
print(coords)
time.sleep(5)
# mc.set_gripper_mode(0)
# mc.init_eletric_gripper()
