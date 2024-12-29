import cv2
import mediapipe as mp
import numpy as np
import os

# MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True,
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

EAR_THRESH = 0.25  # EAR threshold for closed eyes
WAIT_TIME = 2  # Time threshold for drowsiness detection in seconds
D_TIME = 0

duration = 0.3  # seconds
freq = 580  # Hz

# Landmark indices for eyes
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def calculate_ear(eye):
    vertical_1 = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    vertical_2 = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    horizontal = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))

    # EAR
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear


cap = cv2.VideoCapture(0)
t1 = cv2.getTickCount() / cv2.getTickFrequency()  # calculate the start time

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB for MediaPipe process
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get eye landmarks for both eyes
            left_eye = [(int(face_landmarks.landmark[idx].x * frame.shape[1]),
                         int(face_landmarks.landmark[idx].y * frame.shape[0])) for idx in LEFT_EYE]

            right_eye = [(int(face_landmarks.landmark[idx].x * frame.shape[1]),
                          int(face_landmarks.landmark[idx].y * frame.shape[0])) for idx in RIGHT_EYE]

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            # Display EAR value on the frame
            cv2.putText(frame, f'EAR: {avg_ear:.2f}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Calculate drowsiness time
            t2 = cv2.getTickCount() / cv2.getTickFrequency()
            if left_ear < EAR_THRESH and right_ear < EAR_THRESH:
                D_TIME += (t2 - t1)
            else:
                D_TIME = 0

            t1 = t2

            # alert if drowsiness detected
            if D_TIME >= WAIT_TIME:
                cv2.putText(frame, "DROWSINESS ALERT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

            # Draw eye landmarks
            for (x, y) in left_eye + right_eye:
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

    cv2.imshow("Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
