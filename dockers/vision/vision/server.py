from flask import Response, Flask, render_template, send_from_directory
import threading
import imutils
import time
import cv2

outputFrame = None
lock = threading.Lock()
app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/body.css")
def body():
  return send_from_directory('templates', 'body.css')

@app.route("/feed")
def feed():
  return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

def generate():
  global outputFrame, lock

  while True:
    with lock:
      if outputFrame is None:
        continue
      (flag, encodedImage) = cv2.imencode(".jpg", cv2.cvtColor(outputFrame, cv2.COLOR_BGR2RGB))
      if not flag:
        continue
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

def serve():
  app.run(host='0.0.0.0', port='80', debug=False, threaded=True, use_reloader=False)