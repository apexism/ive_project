import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code():
    # 웹캠 캡처
    cap = cv2.VideoCapture(2)

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # QR 코드 디코드
        decoded_objects = decode(frame)

        # 디코드된 객체가 있을 경우
        if decoded_objects:
            for obj in decoded_objects:
                # QR 코드 정보 출력
                # print('QR Code:', obj.data)
                # QR 코드 위치 표시
                points = obj.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                    hull = list(map(tuple, np.squeeze(hull)))
                else:
                    hull = points
                n = len(hull)
                d = [[]]
                for j in range(0, n):
                    cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
                    # 좌표 표시
                    cv2.putText(frame, f'({hull[j][0]}, {hull[j][1]})', hull[j], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    center_x =+ hull[j][0]
                    center_y =+ hull[j][1]
                    # if j < n:
                    #     d.append(np.sqrt(pow((hull[j][0]-hull[j+1][0]),2) + pow((hull[j][1]-hull[j+1][1]),2)))
                    # else:
                    #     d.append(np.sqrt(pow((hull[j][0]-hull[0][0]),2) + pow((hull[0][1]-hull[0][1]),2)))
                cv2.putText(frame, f'({center_x}, {center_y})', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #most_long = max(d)
                # cam_distance = 
                # cv2.putText(frame, f'depth : {cam_distance}mm', (30, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # 화면에 출력
            cv2.imshow("QR Code Scanner", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_code()
