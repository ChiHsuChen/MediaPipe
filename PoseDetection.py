import time
import cv2
import mediapipe as mp

mpDrawing = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

pose = mpPose.Pose()
video_path = './Video/P1499866.MP4'
video_out_path = './Video/P1499866_POSE.MP4'

custom_connection_drawing_spec = mpDrawing.DrawingSpec(color=(0, 255, 0), thickness=5)

cap = cv2.VideoCapture(video_path)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# 獲取影片的原始幀率
fps = cap.get(cv2.CAP_PROP_FPS)
# 獲取影片的寬度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

processed_video = cv2.VideoWriter(video_out_path,fourcc,fps,(width//2,height//2))

while cap.isOpened():
    success, img = cap.read()

    if not success:
        print("Ignoring empty video frame.")
        continue

    startTime = time.time()

    image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # 將影像縮小
    height, width = image.shape[:2]
    resized_image = cv2.resize(image, (width // 2, height // 2))

    results = pose.process(resized_image)
    mpDrawing.draw_landmarks(resized_image, results.pose_landmarks, mpPose.POSE_CONNECTIONS,
                             connection_drawing_spec=custom_connection_drawing_spec)

    endTime = time.time()
    fps = 1 / (endTime - startTime)

    # print out pose landmarks
    print('pose landmarks => ' + str(results.pose_landmarks))

    # cv2.putText(image,"FPS:" + str(fps))
    cv2.putText(resized_image, "FPS:" + str(int(fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX,
                1, (100, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('MediaPipe Pose', resized_image)
    processed_video.write(resized_image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.Release()
processed_video.release()

