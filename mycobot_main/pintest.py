from pymycobot.mycobot import MyCobot
# from pymycobot.genre import Angle, Coord
import time

# myCobot 객체 초기화
mc = MyCobot('/dev/ttyACM0', 115200)  # 시리얼 포트에 따라 적절히 변경 필요

mc.set_basic_output(1,0)
# time.sleep(1)
mc.set_basic_output(1,1)
# time.sleep(1)
mc.set_basic_output(2,1)
# time.sleep(1)
