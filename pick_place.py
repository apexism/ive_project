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
def init_position():
    print("go to home", mc.get_angles())
    mc.send_angles([0, 0, 0, 0, 0, 0], 60)
    time.sleep(5)
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()

# 전체 상자 스캔 위치로 이동
def goto_photo():
    print("go to scanplace", mc.get_angles())
    mc.send_angles([90, 0, 0, 0, -90, 0], 30)
    time.sleep(5)  # 로봇 각 동작 사이의 딜레이 설정
    mc.send_coords([-100, -250, 350, -89.99, 90, -179.91], 10)
    time.sleep(5)

def goto_pick():
    print("go to pick place", mc.get_angles())



def picking_control():
    print("", mc.get_angles())



def goto_place():
    print("go to scanplace", mc.get_angles())



def open_gripper():
    print("go to scanplace", mc.get_angles())
    mc.set_eletric_gripper(0)
    mc.set_gripper_value(100, 20)

def close_gripper():
    print("go to scanplace", mc.get_angles())
    mc.set_gripper_value(0, 20)
    
    
