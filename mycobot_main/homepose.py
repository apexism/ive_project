from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM1', 115200)
mc.send_angles([0,0,0,0,0,0], 20)
time.sleep(5)