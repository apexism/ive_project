import cv2
import numpy as np

def capture_image_and_get_hsv_average():
    # 웹캠 캡쳐 초기화
    cap = cv2.VideoCapture(2)

    # 웹캠으로부터 이미지 캡쳐
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        cap.release()
        return

    # BGR 이미지를 HSV 이미지로 변환
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 중앙 픽셀의 위치 계산
    height, width = frame.shape[:2]
    x_center = width // 2
    y_center = height // 2

    # 중앙의 100x100 픽셀 영역 선택
    half_size = 30  # 정사각형의 각 변의 절반 길이
    square_region = hsv_image[y_center - half_size:y_center + half_size, 
                              x_center - half_size:x_center + half_size]

    # 선택한 영역의 평균 HSV 값을 계산
    average_hsv = np.mean(square_region, axis=(0, 1))

    # 결과 출력
    print(f'Average HSV value in the central 100x100 pixel region: {average_hsv}')

    # 캡쳐된 이미지와 선택된 영역을 표시
    cv2.rectangle(frame, (x_center - half_size, y_center - half_size), 
                  (x_center + half_size, y_center + half_size), (0, 255, 0), 2)
    cv2.imshow('Captured Image', frame)

    # 사용자가 키를 누를 때까지 대기
    cv2.waitKey(0)

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

# 함수 실행
capture_image_and_get_hsv_average()
