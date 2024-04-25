from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)
# mc.send_angles([30, -5, -30, -55, 85, -65], 20)
# time.sleep(5)
mc.set_end_type(1)
# mc.set_tool_reference([0,-10,165,0,0,0])
mc.set_tool_reference([0,-10,165,0,0,0])
time.sleep(1)
print(mc.get_coords())
# mc.send_coord(6, -135, 20)
# mc.send_angle(6, 60, 20)
# mc.send_coords([-50, -350.2, 333.83, -90.0, 45.1, 180], 40)
# mc.send_angle(6, -43.5, 20)
# time.sleep(20)

# mc.send_coords([137.2, 1.5, 138.6, -177.64, -2.38, -87.68],5)

#찐막
# 피킹 위치 티칭
# mc.send_angles([30, -5, -30, -55, 85, -65], 20)
# time.sleep(5)
mc.send_coords([225, 20, 130, 180, 0, 0], 10)
time.sleep(5)

# 촬영 위치 티칭
# mc.send_angles([155.83, -29.09, 73.3, 42.62, -88.68, -27.59], 20)
# time.sleep(5)
# mc.send_coords([142.1, 4.5, 308.6, -180, 0.0, -90], 20)
# time.sleep(10)

# mc.set_end_type(1)
# mc.set_tool_reference([0,0,180,0,0,0])
print(mc.get_angles())
print(mc.get_coords())


# mc.set_gripper_mode(0)
# mc.init_eletric_gripper()
# time.sleep(1)

# mc.set_eletric_gripper(1)
# mc.set_gripper_value(70, 20, 1)
# time.sleep(5)
# print(mc.get_gripper_value())

# mc.set_eletric_gripper(0)
# mc.set_gripper_value(100, 20, 1)
# # print(mc.get_gripper_value())
# time.sleep(5)
# print(mc.get_gripper_value())

