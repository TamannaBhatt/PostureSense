import cv2

class Dashboard:

    @staticmethod
    def draw(frame, features, analysis, session_time, bad_posture_time):

        height, width = frame.shape[:2]
        panel_width = 320

        dashboard = frame.copy()

        cv2.rectangle(
            dashboard,
            (width - panel_width, 0),
            (width, height),
            (40, 40, 40),
            -1
        )

        cv2.putText(
            dashboard,
            "POSTURESENSE AI",
            (width - 300, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        y = 90

        items = [
            f"Neck Angle : {features['neck_angle']:.1f}",
            f"Back Angle : {features['back_angle']:.1f}",
            f"Shoulder Tilt : {features['shoulder_tilt']:.3f}",
            f"Head Offset : {features['head_offset']:.3f}",
            "",
            f"Score : {analysis['score']}",
            f"Status : {analysis['status']}",
            "",
            f"Session : {session_time}",
            f"Bad Time : {bad_posture_time}s"
        ]

        for item in items:

            cv2.putText(
                dashboard,
                item,
                (width - 300, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2
            )

            y += 35

        return dashboard