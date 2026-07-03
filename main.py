import cv2
from src.pose_detector import PoseDetector

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create PoseDetector object
detector = PoseDetector()

while True:

    success, frame = cap.read()

    if not success:
        break

    # Flip the frame for a mirror view
    frame = cv2.flip(frame, 1)

    # Detect pose and get landmarks
    frame, landmarks = detector.detect_pose(frame)

    # If landmarks are detected
    if landmarks:

        mp_pose = detector.mp_pose

        # Extract important landmarks
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Display coordinates on screen
        cv2.putText(
            frame,
            f"Nose: ({nose.x:.2f}, {nose.y:.2f})",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"L Shoulder: ({left_shoulder.x:.2f}, {left_shoulder.y:.2f})",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"R Shoulder: ({right_shoulder.x:.2f}, {right_shoulder.y:.2f})",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Display the webcam
    cv2.imshow("PostureSense AI", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()