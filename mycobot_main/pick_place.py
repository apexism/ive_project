# from camera_control import *
from pymycobot.mycobot import MyCobot
import time
import cv2
import os
from pyzbar import pyzbar
import socket



# 로봇 제어 함 

# 로봇팔 home position
def init_gripper(mc):
    # print("go to home", mc.get_angles())
    # mc.send_angles([0, 0, 0, 0, 0, 0], 15)
    # time.sleep(10)
    mc.set_gripper_mode(0)
    mc.init_eletric_gripper()
    # time.sleep(1)

# 전체 상자 스캔 위치로 이동
def goto_photo(mc):
    
    # mc.send_angles([90, 0, 0, 0, -90, 0], 90)
    # time.sleep(5)  # 로봇 각 동작 사이의 딜레이 설정
    # mc.send_coords([-100, -250, 350, -89.99, 90, -179.91], 90)
    coords = mc.get_coords()
    print(coords)
    mc.send_coords([119.5, -200.5, 195, -99.97, -5.63, -99.04], 15)
    time.sleep(5)
    print("go to take photo", mc.get_angles())


def goto_pick(mc):
    print("go to pick place", mc.get_angles())




def picking_control(mc):
    print("on the picking area", mc.get_angles())



def goto_place(mc):
    print("go to scanplace", mc.get_angles())




def open_gripper(mc):
    print("open gripper")
    mc.set_eletric_gripper(0)
    mc.set_gripper_value(100, 20, 1)
    # print(mc.get_gripper_value())
    time.sleep(3)
    # print(mc.get_gripper_value())

def close_gripper(mc):
    print("close gripper")
    mc.set_eletric_gripper(1)
    mc.set_gripper_value(16, 20, 1)
    # print(mc.get_gripper_value())
    time.sleep(3)
    # print(mc.get_gripper_value())
    
    
