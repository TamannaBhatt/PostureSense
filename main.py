import cv2
from src.pose_detector import PoseDetector

cap = cv2.VideoCapture(0)

detector = PoseDetector()

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, results = detector.detect_pose(frame)

    cv2.imshow("PostureSense AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()