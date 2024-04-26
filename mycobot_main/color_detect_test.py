import cv2
import numpy as np
from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)

x_relative = 0
y_relative = 0
w = 0
h = 0
angle = 0

def draw_box(contour, video, center_x_img, center_y_img):
    if cv2.contourArea(contour) > 500:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(video, [box], 0, (0, 0, 255), 3)

        global x_relative
        global y_relative
        global w
        global h
        global angle

        (x, y), (w, h), angle = rect

        # 이미지 중심을 기준으로 좌표 조정
        x_relative = x - center_x_img
        y_relative = y - center_y_img

        cv2.circle(video, (int(x), int(y)), 5, (255, 255, 0), -1)
        # 나머지 코드 ...
        # 회전 변환 행렬 생성
        M = cv2.getRotationMatrix2D((x, y), angle, 1)
        
        # 회전된 축 그리기
        x_axis = np.array([[-w/2, w/2], [0, 0], [1, 1]])
        y_axis = np.array([[0, 0], [-h/2, h/2], [1, 1]])
        
        transformed_x_axis = np.dot(M, x_axis)
        transformed_y_axis = np.dot(M, y_axis)
        
        # 회전된 x축 그리기
        cv2.line(video, (int(transformed_x_axis[0][0] + x), int(transformed_x_axis[1][0] + y)),
                    (int(transformed_x_axis[0][1] + x), int(transformed_x_axis[1][1] + y)), (0, 255, 0), 2)
        
        # 회전된 y축 그리기
        cv2.line(video, (int(transformed_y_axis[0][0] + x), int(transformed_y_axis[1][0] + y)),
                    (int(transformed_y_axis[0][1] + x), int(transformed_y_axis[1][1] + y)), (0, 255, 0), 2)

def c_detect():
    while True:
        # 웹캠 비디오 가져오기
        webcam_video = cv2.VideoCapture(2)

        # ret, frame = cap.read()
        # if not ret:
        #     print("Failed to grab frame")
        #     continue

        # while True:
        # 비디오 프레임 읽어오기
        success, video = webcam_video.read()

        if not success:
            print("Failed to grab frame")
            continue

        # 좌우 대칭으로 뒤집기
        # video = cv2.flip(video, 1)

        # BGR 이미지를 HSV 이미지로 변환
        hsv_img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 

        # 노란색 감지를 위한 마스크 세팅
        lower_yellow = np.array([15, 150, 20])
        upper_yellow = np.array([35, 255, 255])
        yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

        # 빨간색 감지를 위한 마스크 세팅
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        red_mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        red_mask = red_mask1 + cv2.inRange(hsv_img, lower_red2, upper_red2)
        
        # 녹색 감지를 위한 마스크 세팅
        lower_green = np.array([60, 80, 90])
        upper_green = np.array([80, 255, 255])
        green_mask = cv2.inRange(hsv_img, lower_green, upper_green)

        # 파란색 감지를 위한 HSV 범위
        lower_blue = np.array([90, 100, 75])
        upper_blue = np.array([120, 255, 255])
        blue_mask = cv2.inRange(hsv_img, lower_blue, upper_blue)

        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 이미지 차원으로 중심 좌표 계산
        height, width = video.shape[:2]
        center_x_img, center_y_img = width // 2, height // 2

        if yellow_contours:
            for yellow_contour in yellow_contours:
                print("@@@@@@")
                contour = yellow_contour
                color = "y"
                draw_box(contour, video, center_x_img, center_y_img)
        if red_contours:
            for red_contour in red_contours:
                print("#####")
                contour = red_contour
                color = "r"
                draw_box(contour, video, center_x_img, center_y_img)
        if green_contours:
            for green_contour in green_contours:
                print("$$$$$$$")
                contour = green_contour
                color = "g"
                draw_box(contour, video, center_x_img, center_y_img)
        if blue_contours:
            for blue_contour in blue_contours:
                print("^^^^^^^^")
                contour = blue_contour
                color = "b"
                draw_box(contour, video, center_x_img, center_y_img)                    
                    
        # 화면에 이미지 표시
        cv2.imshow("Rotating Axes", video) 
            
        # # ESC 키 누를 시 프로그램 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 웹캠 해제 및 창 닫기
    webcam_video.release()
    cv2.destroyAllWindows()


c_detect()