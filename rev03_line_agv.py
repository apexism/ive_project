#!/usr/bin/env python

from __future__ import print_function

import cv2
import numpy as np
from pymycobot.myagv import MyAgv

import threading
import time
import roslib; roslib.load_manifest('myagv_teleop')
import rospy

from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


TwistMsg = Twist

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

anything else : stop

Line Tracer : T

Exit: v

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

agv = MyAgv("/dev/ttyAMA2", 115200)

def process_frame(frame):
    height, width, _ = frame.shape
    roi_height = int(height / 5)
    roi_top = height - roi_height
    roi = frame[roi_top:, :]
    left_line= width // 2 - 120
    right_line = width // 2 + 120
    center_line = width // 2

    # cv2.line(roi, (width // 2, 0), (width // 2, roi_height), (255, 0, 0), 2)
    # cv2.line(roi, (left_line, 0), (left_line, roi_height), (0, 255, 0), 2)
    # cv2.line(roi, (right_line, 0), (right_line, roi_height), (0, 255, 0), 2)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 50, 100], dtype=np.uint8)
    upper_blue = np.array([10, 255, 255], dtype=np.uint8)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if blue_contours:

        max_contour = max(blue_contours, key=cv2.contourArea)
        M = cv2.moments(max_contour) #

        if M["m00"] != 0 :
                # cx = int(M["m10"] / M["m00"])
            cx = int(M["m10"] / M["m00"])
            #####
            if cx: #
                cv2.drawContours(roi, [max_contour], -1, (255, 0, 0), 2)
            cv2.line(roi, (cx, 0), (cx, roi_height), (255, 0, 0), 2) 

            if cx < center_line - 50:
                return "LEFT", cx

            elif cx > center_line + 50:
                return "RIGHT", cx
            
            else :
                return "GO", cx
        else:
            return "STOP", 0
        return None, 0
    return None, 0

def camera_thread():
    cap = cv2.VideoCapture(0)
    set_time = 0
    status = 0
    while True:
        ret, frame = cap.read()
        _, width, _ = frame.shape
        if not ret:
            print("Camera error")
            break

        result, cx = process_frame(frame)
        dx = abs((cx-width/2)/(width/2))*0.43
        if result:
            print(result)
            if result == "LEFT":
                pub_thread.update(1, 0, 0, 1, 0.08, dx)
            elif result == "RIGHT":
                pub_thread.update(1, 0, 0, -1, 0.08, dx)
            elif result == "GO":
                pub_thread.update(1, 0, 0, 0, 0.08, 0.00)
            elif result == "STOP":
                pub_thread.update(0, 0, 0, 0, 0.00, 0.00)
            
        # if status == 0:
        #     if result == "LEFT": status = 1
        #     elif result =="LEFT_H": status = 2
        #     elif result == "RIGHT": status = 3
        #     elif result == "RIGHT_H": status = 4
        #     elif result == "go": status = 5
        #     elif result == "STOP": status = 6
            
        # if set_time == 0:
        #     set_time = time.time()
        # else:
        #     current_time = time.time()
        #     timer = current_time - set_time
        #     print(result)
            # if status == 1:
            #     if timer > 0 and timer <= 0.05:
            #         pub_thread.update(1, 0, 0, 1, 0.08, 0.38)
            #     else: set_time, timer, status = 0, 0, 0
            # elif status == 2:
            #     if timer > 0 and timer <= 0.05:
            #         pub_thread.update(1, 0, 0, 1, 0.05, 0.38)
            #     else: set_time, timer, status = 0, 0, 0
            # elif status == 3:
            #     if timer > 0 and timer <= 0.05:
            #         pub_thread.update(1, 0, 0, -1, 0.08, 0.38)
            #     else: set_time, timer, status = 0, 0, 0
            # elif status == 4:
            #     if timer > 0 and timer <= 0.05:
            #         pub_thread.update(1, 0, 0, -1, 0.05, 0.38)
            #     else: set_time, timer, status = 0, 0, 0
            # elif status == 5:
            #     if timer > 0 and timer <= 0.05:
            #         pub_thread.update(1, 0, 0, 0, 0.1, 0.00)
            #     else: set_time, timer, status = 0, 0, 0
            # elif status == 6:
            #     if timer > 0 and timer <= 0.05:
            #         pub_thread.update(0, 0, 0, 0, 0.00, 0.00)
            #     else: set_time, timer, status = 0, 0, 0
        
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

moveBindings = {
        'i':(1,0,0,0),
        'o':(0,0,0,-1),
        'j':(0,1,0,0),
        'l':(0,-1,0,0),
        'u':(0,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,-1),
        'm':(-1,0,0,1),
        'O':(0,0,0,-1),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(0,0,0,1),
        '<':(-1,0,0,0),
        '>':(-1,0,0,-1),
        'M':(-1,0,0,1),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', TwistMsg, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def run(self):
        twist_msg = TwistMsg()

        if stamped:
            twist = twist_msg.twist
            twist_msg.header.stamp = rospy.Time.now()
            twist_msg.header.frame_id = twist_frame
        else:
            twist = twist_msg
        while not self.done:
            if stamped:
                twist_msg.header.stamp = rospy.Time.now()
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist_msg)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist_msg)


def getKey(settings, timeout):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = saveTerminalSettings()

    rospy.init_node('teleop_twist_keyboard')

    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 0.5)
    speed_limit = rospy.get_param("~speed_limit", 0.5)
    turn_limit = rospy.get_param("~turn_limit", 1.0)
    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.52)
    stamped = rospy.get_param("~stamped", False)
    twist_frame = rospy.get_param("~frame_id", '')
    if stamped:
        TwistMsg = TwistStamped

    pub_thread = PublishThread(repeat)

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)

        print(msg)
        print(vels(speed,turn))
        while(1):
            key = getKey(settings, key_timeout)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                speed = min(speed_limit, speed * speedBindings[key][0])
                turn = min(turn_limit, turn * speedBindings[key][1])
                if speed == speed_limit:
                    print("Linear speed limit reached!")
                if turn == turn_limit:
                    print("Angular speed limit reached!")
                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            elif key == 't' or key == 'T':
                while(1):
                    # 메인 스레드에서 카메라 스레드 실행
                    camera_thread = threading.Thread(target=camera_thread)
                    camera_thread.start()
                    
                    # 카메라 스레드가 종료될 때까지 대기
                    camera_thread.join()
                    
                    key2 = getKey(settings, key_timeout)
                    time.sleep(0.25)
                    print(key)
                    if key2 == 'v':
                        break

            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break

            pub_thread.update(x, y, z, th, speed, turn)



    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        restoreTerminalSettings(settings)
