from time import sleep
import datetime
import cv2
import numpy


while True:
    # Send picture
    sleep(0.1)
    now = datetime.datetime.now()
    filename = "./last.jpg"
    watermark = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
    except cv2.error as e:
        print(e)
        frame = numpy.zeros((320, 280, 3), numpy.uint8)
    except Exception as e:
        print(e)
        frame = numpy.zeros((320, 280, 3), numpy.uint8)
    else:
        print('OpenCV2 error with capture device, but no Exception')
        frame = numpy.zeros((320, 280, 3), numpy.uint8)

    video_capture.release()

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(watermark), (0, -40), font, 5, (255, 255, 255), 3)
    cv2.imwrite(filename, frame)
