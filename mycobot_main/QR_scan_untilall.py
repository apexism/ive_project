import cv2
from pyzbar import pyzbar
import time

def scan_qr_codes(image):
    """이미지에서 QR 코드를 스캔하고 검출된 QR 코드의 데이터를 반환합니다."""
    qr_codes = pyzbar.decode(image)
    return [qr_code.data.decode('utf-8') for qr_code in qr_codes]

def scan_frame(frame, height, width, scan_size, step_right, step_down, show=False):
    detected_qr_codes = set()
    qr_code_locations = []

    y = 0
    while y + scan_size[1] <= height:
        x = 0
        while x + scan_size[0] <= width:
            roi = frame[y:y+scan_size[1], x:x+scan_size[0]]
            qr_codes = scan_qr_codes(roi)
            for code in qr_codes:
                if code not in detected_qr_codes:
                    detected_qr_codes.add(code)
                    qr_code_locations.append((code, (x, y)))
            if show:
                display = cv2.rectangle(frame.copy(), (x, y), (x + scan_size[0], y + scan_size[1]), (0, 255, 0), 2)
                cv2.imshow("Scanning QR Codes", display)
                cv2.waitKey(1)  # Refresh display
            x += step_right
        y += step_down
    return detected_qr_codes, qr_code_locations

# 카메라 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

detected_qr_codes = set()

try:
    while len(detected_qr_codes) < 6:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 캡쳐할 수 없습니다.")
            continue

        height, width, _ = frame.shape
        scan_size = (213, 240)
        step_right = 106
        step_down = 120

        # 스캔 (이미지 표시)
        new_scan_results, locations = scan_frame(frame, height, width, scan_size, step_right, step_down, show=True)
        detected_qr_codes.update(new_scan_results)

        print("Current detected QR Codes:", len(detected_qr_codes))
        time.sleep(0.5)  # 각 스캔 사이에 간격을 둡니다.

except KeyboardInterrupt:
    print("Scanning stopped.")

finally:
    cap.release()
    cv2.destroyAllWindows()

# QR 코드 데이터를 첫 번째 필드(고유 번호)를 기준으로 정렬
sorted_qr_codes = sorted(detected_qr_codes, key=lambda x: int(x.split(',')[0]))

# 최종 검출된 QR 코드 출력
print("Detected QR Codes:")
for qr in sorted_qr_codes:
    print(qr)
