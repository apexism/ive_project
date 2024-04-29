from pymycobot.mycobot import MyCobot
# from pymycobot.genre import Angle, Coord
import time

# myCobot 객체 초기화
mc = MyCobot('/dev/ttyACM0', 115200)  # 시리얼 포트에 따라 적절히 변경 필요

# # 핀 모드 설정 (핀 1을 출력으로 설정)
# mc.set_pin_mode(1, 1)


# # 작업 완료 후 디지털 출력을 통해 신호 전송
# mc.set_digital_output(1, 1)  # 핀 1에 HIGH 신호 출력
# time.sleep(1)  # 신호 지속 시간
# mc.set_digital_output(2, 0)  # 핀 1에 LOW 신호 출력
mc.set_basic_output(1,0)
time.sleep(1)
mc.set_basic_output(1,1)
time.sleep(1)
mc.set_basic_output(2,1)
time.sleep(1)
