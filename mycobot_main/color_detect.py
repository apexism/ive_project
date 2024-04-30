import cv2
import numpy as np
import time

color = ""

x_relative = 0
y_relative = 0
w = 0
h = 0
angle = 0

def draw_box(contour, video, center_x_img, center_y_img, con_color):
    if cv2.contourArea(contour) > 2000:
        print(con_color, cv2.contourArea(contour))
    if cv2.contourArea(contour) > 3000:
        rect = cv2.minAreaRect(contour)
        bounding_x, bounding_y, bounding_w, bounding_h = cv2.boundingRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(video, [box], 0, (0, 0, 255), 3)

        global x_relative
        global y_relative
        global w
        global h
        global angle
        global color

        (x, y), (w, h), angle = rect
        color = con_color

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
        
        text_position = (bounding_x + 5, bounding_y + 25)  # 텍스트 위치를 사각형의 좌상단 근처로 설정
        cv2.putText(video, color, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)



def c_detect():
    webcam_video = cv2.VideoCapture(2)                 # videocapture(리눅스는 0, 윈도우는 1, mycobot camera는 2)
    success, video = webcam_video.read()               

    if not success:
        print("Failed to grab frame")
        webcam_video.release()
        return

    # video = cv2.flip(video, 1)                            # 비디오 좌우반전 
    hsv_img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)        # BGR 에서 HSV 색공간으로 변환
    
    # 노란색 감지를 위한 마스크 세팅
    lower_yellow = np.array([15, 60, 75])
    upper_yellow = np.array([45, 255, 255])
    yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

    # 빨간색 감지를 위한 마스크 세팅
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    red_mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    red_mask = red_mask1 + cv2.inRange(hsv_img, lower_red2, upper_red2)
    
    # 녹색 감지를 위한 마스크 세팅
    lower_green = np.array([45, 80, 85])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)

    # 파란색 감지를 위한 HSV 범위
    # lower_blue = np.array([90, 100, 75])
    # upper_blue = np.array([120, 255, 255])
    
    lower_blue = np.array([90, 100, 75])
    upper_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv_img, lower_blue, upper_blue)
    

    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 이미지 차원으로 중심 좌표 계산
    height, width = video.shape[:2]
    center_x_img, center_y_img = width // 2, height // 2
    
    global color
    global x_relative
    global y_relative
    global w
    global h
    global angle

    if yellow_contours:
        for yellow_contour in yellow_contours:
            contour = yellow_contour
            con_color = "y"
            draw_box(contour, video, center_x_img, center_y_img, con_color)
    if red_contours:
        for red_contour in red_contours:
            contour = red_contour
            con_color = "r"
            draw_box(contour, video, center_x_img, center_y_img, con_color)
    if green_contours:
        for green_contour in green_contours:
            contour = green_contour
            con_color = "g"
            draw_box(contour, video, center_x_img, center_y_img, con_color)
    if blue_contours:
        for blue_contour in blue_contours:
            contour = blue_contour
            con_color = "b"
            draw_box(contour, video, center_x_img, center_y_img, con_color)
 
    starting_time = time.time()
    while True:
        cv2.imshow('yellow_mask', yellow_mask)
        cv2.imshow('red_mask', red_mask)
        cv2.imshow('green_mask', green_mask)
        cv2.imshow('blue_mask', blue_mask)
        cv2.imshow("Rotating Axes", video)

        cv2.moveWindow('yellow_mask', 641, 0)
        cv2.moveWindow('red_mask', 1281, 0)
        cv2.moveWindow('green_mask', 0, 481)
        cv2.moveWindow('blue_mask', 641, 481)
        cv2.moveWindow('Rotating', 0, 0)

        current_time = time.time()
        if (current_time - starting_time) > 0.5:
            break
        elif cv2.waitKey(1) & 0xFF == 27:
            break


    webcam_video.release()
    cv2.destroyAllWindows()
    
    print(color, int(x_relative), int(y_relative), int(w), int(h), angle)
    return (color, int(x_relative), int(y_relative), int(w), int(h), angle)

# c_detect()
# print(color, (int(x_relative), int(y_relative), int(w), int(h), angle))
