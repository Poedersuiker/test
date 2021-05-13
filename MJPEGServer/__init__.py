from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import logging
import cv2
import numpy
import datetime
import os
from time import sleep


class MJPEGServer(Thread):
    """
    TEST
    """
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger = logging.getLogger("HTTPServer")

    ch = logging.FileHandler('./test.log')

    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    def __init__(self, port=80):
        Thread.__init__(self)
        self.port = port
        self.server_address = ('', self.port)
        self.httpd = ThreadingHTTPServer(self.server_address, StreamingHandler)

    def run(self):
        self.httpd.serve_forever()


PAGE = """\
<html>
<head>
<title>SkyWeather MJPEG streaming demo</title>
</head>
<body>
<h1>SkyWeather MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="1296" height="730" />
</body>
</html>
"""


class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                filename = "/mnt/tmp/frame.jpg"
                video_capture = cv2.VideoCapture(-1)
                # video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                # width = 1920
                # height = 1080
                # video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                # video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                ret, frame = video_capture.read()
                while True:
                    sleep(0.1)
                    now = datetime.datetime.now()
                    watermark = now.strftime("%Y-%m-%d %H:%M:%S")

                    ret, frame = video_capture.read()

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    frame = cv2.putText(frame, str(watermark), (20, 460), font, 1, (255, 255, 255), 2)
                    cv2.imwrite(filename, frame)
                    _, jpeg_frame = cv2.imencode('.jpg', frame)

                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(jpeg_frame))
                    self.end_headers()
                    self.wfile.write(jpeg_frame)
                    self.wfile.write(b'\r\n')

                video_capture.release()

            except Exception as e:
                print(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        else:
            self.send_error(404)
            self.end_headers()
