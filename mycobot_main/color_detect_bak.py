import cv2
import numpy as np



def c_detect():
    # 웹캠 비디오 가져오기
    webcam_video = cv2.VideoCapture(2)

    # while True:
    # 비디오 프레임 읽어오기
    success, video = webcam_video.read()

    # 좌우 대칭으로 뒤집기
    video = cv2.flip(video, 1)

    # BGR 이미지를 HSV 이미지로 변환
    hsv_img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) 

    # 노란색 객체를 위한 HSV 색상 범위 정의
    lower_yellow = np.array([15, 150, 20])
    upper_yellow = np.array([35, 255, 255])

    # 노란색 객체를 마스킹하여 검출
    yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow) 

    # 마스킹된 이미지에서 외곽선 찾기
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    # 외곽선이 존재할 경우 경계 상자 그리기
    if len(yellow_contours) != 0:
        for yellow_contour in yellow_contours:
            if cv2.contourArea(yellow_contour) > 500:
                # 최소 회전 경계 상자 찾기
                rect = cv2.minAreaRect(yellow_contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                
                # 회전된 경계 상자 그리기
                cv2.drawContours(video, [box], 0, (0, 0, 255), 3)
                
                # 회전된 사각형의 중심 좌표 가져오기
                (x, y), (w, h), angle = rect
                print(angle)
                
                # 회전된 축의 중심 그리기
                cv2.circle(video, (int(x), int(y)), 5, (255, 255, 0), -1)
                
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
                
                
                
    while True:
        # 화면에 이미지 표시
        cv2.imshow("Rotating Axes", video)
            
        # # ESC 키 누를 시 프로그램 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 웹캠 해제 및 창 닫기
    webcam_video.release()
    cv2.destroyAllWindows()

    return (int(x), int(y), int(w), int(h), angle)

# c_detect()