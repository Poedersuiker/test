from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import logging
import cv2
import numpy
import datetime
import os


class MJPEGServer:
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
        self.port = port
        self.server_address = ('', self.port)
        self.httpd = ThreadingHTTPServer(self.server_address, StreamingHandler)
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
                video_capture = cv2.VideoCapture(0)
                while True:
                    # Send picture
                    now = datetime.datetime.now()
                    filename = now.strftime("./last.jpg")
                    watermark = now.strftime("%Y-%m-%d %H:%M:%S")
                    try:
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

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(watermark), (0, -40), font, 5, (255, 255, 255), 3)
                    cv2.imwrite(filename, frame)

                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                video_capture.release()
            except Exception as e:
                print(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        else:
            self.send_error(404)
            self.end_headers()
