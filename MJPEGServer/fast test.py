from time import sleep
import datetime
import cv2


video_capture = cv2.VideoCapture(-1)
filename = "./last.jpg"
ret, frame = video_capture.read()

while video_capture.isOpened():
    # Send picture
    sleep(0.1)
    now = datetime.datetime.now()
    watermark = now.strftime("%Y-%m-%d %H:%M:%S")
    ret, frame = video_capture.read()

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.putText(frame, str(watermark), (0, -40), font, 5, (255, 255, 255), 3)
    cv2.imwrite(filename, frame)

video_capture.release()