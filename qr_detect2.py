import cv2
import numpy as np
import math
from pyzbar.pyzbar import decode

def read_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        decoded_objects = decode(frame)
        if decoded_objects:
            for obj in decoded_objects:
                print('QR Code:', obj.data.decode())

                points = obj.polygon
                # Create convex hull around points if there are more than 4
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                    hull = list(map(tuple, np.squeeze(hull)))
                else:
                    hull = points

                n = len(hull)
                for j in range(n):
                    cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
                    cv2.putText(frame, f'({hull[j][0]}, {hull[j][1]})', hull[j], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Calculate the area of the polygon formed by the points of the QR code
                pixel_count = cv2.contourArea(np.array(hull))
                print(f"QR code pixel count: {pixel_count}")

                if pixel_count != 0:
                    depth = math.sqrt((1600) / pixel_count) / 0.0016
                    print(f"depth: {depth}")

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_code()
