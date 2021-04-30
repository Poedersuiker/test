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

    logger = logging.getLogger("Telegram Connector")

    ch = logging.FileHandler('/var/log/Frontdoor/fd.log')

    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    def __init__(self, port=80):
        self.port = port
        self.httpd = ThreadingHTTPServer('localhost', StreamingHandler)
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
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame

                        # Send picture
                        now = datetime.now()
                        filename = now.strftime("%Y%m%d%H%M%S.jpg")
                        watermark = now.strftime("%Y-%m-%d %H:%M:%S")
                        try:
                            video_capture = cv2.VideoCapture(0)
                            ret, frame = video_capture.read()
                        except cv2.error as e:
                            self.logger.error(e)
                            frame = numpy.zeros((320, 280, 3), numpy.uint8)
                        except Exception as e:
                            self.logger.error(e)
                            frame = numpy.zeros((320, 280, 3), numpy.uint8)
                        else:
                            self.logger.error('OpenCV2 error with capture device, but no Exception')
                            frame = numpy.zeros((320, 280, 3), numpy.uint8)

                        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, str(watermark), (0, -40), font, 5, (255, 255, 255), 3)
                        cv2.imwrite(filename, frame)
                        if os.path.exists(filename):
                            os.remove(filename)
                            self.logger.info("Picture %s send" % filename)
                        else:
                            self.logger.warning("Problem sending picture")
                            self.TelegramConnector.send_message('Problem with frontdoor picture')
                        video_capture.release()
                        
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                traceback.print_exc()
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


        # Send picture
        now = datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S.jpg")
        watermark = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()
        except cv2.error as e:
            self.logger.error(e)
            frame = numpy.zeros((320, 280, 3), numpy.uint8)
        except Exception as e:
            self.logger.error(e)
            frame = numpy.zeros((320, 280, 3), numpy.uint8)
        else:
            self.logger.error('OpenCV2 error with capture device, but no Exception')
            frame = numpy.zeros((320, 280, 3), numpy.uint8)

        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(watermark), (0, -40), font, 5, (255, 255, 255), 3)
        cv2.imwrite(filename, frame)
        if os.path.exists(filename):
            os.remove(filename)
            self.logger.info("Picture %s send" % filename)
        else:
            self.logger.warning("Problem sending picture")
            self.TelegramConnector.send_message('Problem with frontdoor picture')
        video_capture.release()