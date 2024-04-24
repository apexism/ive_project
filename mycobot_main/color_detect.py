import cv2
import numpy as np

def c_detect():
    webcam_video = cv2.VideoCapture(2)
    success, video = webcam_video.read()

    if not success:
        print("Failed to grab frame")
        webcam_video.release()
        return

    # video = cv2.flip(video, 1)
    hsv_img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([15, 150, 20])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 이미지 차원으로 중심 좌표 계산
    height, width = video.shape[:2]
    center_x_img, center_y_img = width // 2, height // 2

    if yellow_contours:
        for yellow_contour in yellow_contours:
            if cv2.contourArea(yellow_contour) > 500:
                rect = cv2.minAreaRect(yellow_contour)
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                cv2.drawContours(video, [box], 0, (0, 0, 255), 3)

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

    while True:
        cv2.imshow("Rotating Axes", video)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    webcam_video.release()
    cv2.destroyAllWindows()

    return (int(x_relative), int(y_relative), int(w), int(h), angle)

# c_detect()
