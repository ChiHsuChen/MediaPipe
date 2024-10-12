import time
import cv2
import mediapipe as mp

mpDrawing = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

pose = mpPose.Pose()

while True:
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success,img = cap.read()

        if not success:
            print("Ignoring empty camera frame.")          
            continue

        startTime = time.time()

        image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        results = pose.process(image)
        mpDrawing.draw_landmarks(image, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        endTime = time.time()
        fps = 1/(endTime - startTime)

        #cv2.putText(image,"FPS:" + str(fps))
        cv2.putText(image,"FPS:" + str(int(fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX,
                   3, (100, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(5) & 0xFF == 27:
          break
        
    cap.Release()

