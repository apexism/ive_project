# from pymycobot.mycobot import MyCobot
# import time
# import keyboard



# mc = MyCobot('/dev/ttyACM0', 115200)

# while True:
#     angles = mc.get_angles()
#     print("각도: ", angles)
#     time.sleep(1)

#     if keyboard.is_pressed('s'):
#         mc.release_all_servos()
#         print("release servo")

#     if keyboard.is_pressed('a'):
#         print("servo activated")
#         mc.power_on()
#         print("angle 각도: ", mc.get_angles())
#         print("coords 좌표: ", mc.get_coords())

    
from pymycobot.mycobot import MyCobot
import time
from pynput import keyboard

mc = MyCobot('/dev/ttyACM0', 115200)

mc.set_end_type(1)
mc.set_tool_reference([0,-10,165,0,0,0])
time.sleep(1)

def on_press(key):
    try:
        if key.char == 's':  # s 키를 눌렀을 때
            mc.release_all_servos()
            print("release servo")
        elif key.char == 'a':  # a 키를 눌렀을 때
            print("servo activated")
            mc.power_on()
            print("angle 각도: ", mc.get_angles())
            print("coords 좌표: ", mc.get_coords())
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    angles = mc.get_angles()
    coords = mc.get_coords()
    print("각도: ", angles)
    print("좌표: ", coords)
    time.sleep(1)



# servo activated
# angle 각도:  [155.83, -29.09, 73.3, 42.62, -88.68, -27.59]
# coords 좌표:  [142.8, 33.7, 317.7, -176.58, -0.29, -86.54]
# [227.2, 40.4, 309.7, 179.98, 1.29, -86.13]


# servo activated
# angle 각도:  [158.29, -4.21, 69.52, 23.9, -83.75, 61.87]
# coords 좌표:  [216.2, 16.0, 294.8, 174.86, 3.63, -173.7]