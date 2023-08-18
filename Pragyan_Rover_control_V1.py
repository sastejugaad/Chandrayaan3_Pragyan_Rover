"""
Install Flask,Pi camera and adafruit servokit library
Install controller app on the phone.
Connect both to Rover and phone to same network.
Get rover IP address and port
Put this in the app and enjoy
https://youtu.be/HEDTC4hjLJs
"""
import io
import time
import picamera
from flask import Flask, render_template, Response
import socket
import threading
from adafruit_servokit import ServoKit

app = Flask(__name__)

# Initialize PCA9685 servo driver
kit = ServoKit(channels=16)
# Set the servo channel based on your setup
right_wheel1 = 0
right_wheel2 = 1
right_wheel3 = 2
left_wheel1 = 3
left_wheel2 = 4
left_wheel3 = 5
fwd_speed = 0#90
bck_speed = 180#120
# Replace with the appropriate servo channel number


@app.route('/')
def index():
    """Main route, returns index.html"""
    return render_template('index.html')

def generate():
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        # Adjust the framerate and quality parameters
        camera.framerate = 20  # Lower the framerate if needed
        # camera.quality = 20    # Reduce the image quality if needed

        # Let the camera warm up
        time.sleep(2)

        # Create an in-memory stream
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True, quality=20):
            # Rewind the stream for reading
            stream.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

            # Reset the stream for the next frame
            stream.seek(0)
            stream.truncate()

@app.route('/video_feed')
def video_feed():
    """Video feed route, streams video frames"""
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def udp_server():
    host = ''
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))

    print("UDP Server running on port", port)
    while True:
        message, address = s.recvfrom(8192)
        messageString = message.decode("utf-8")
        print("Received data:", messageString)

        # Check if the message is 'f' to turn the servo clockwise
        if messageString == 'l':
            kit.servo[right_wheel1].angle = fwd_speed
            kit.servo[right_wheel2].angle = fwd_speed
            kit.servo[right_wheel3].angle = fwd_speed
            kit.servo[left_wheel1].angle = fwd_speed
            kit.servo[left_wheel2].angle = fwd_speed
            kit.servo[left_wheel3].angle = fwd_speed
        if messageString == 'r':
            kit.servo[right_wheel1].angle = bck_speed
            kit.servo[right_wheel2].angle = bck_speed
            kit.servo[right_wheel3].angle = bck_speed
            kit.servo[left_wheel1].angle = bck_speed
            kit.servo[left_wheel2].angle = bck_speed
            kit.servo[left_wheel3].angle = bck_speed
        if messageString == 'f':
            kit.servo[right_wheel1].angle = fwd_speed
            kit.servo[right_wheel2].angle = fwd_speed
            kit.servo[right_wheel3].angle = fwd_speed
            kit.servo[left_wheel1].angle = bck_speed
            kit.servo[left_wheel2].angle = bck_speed
            kit.servo[left_wheel3].angle = bck_speed
        if messageString == 'b':
            kit.servo[right_wheel1].angle = bck_speed
            kit.servo[right_wheel2].angle = bck_speed
            kit.servo[right_wheel3].angle = bck_speed
            kit.servo[left_wheel1].angle = fwd_speed
            kit.servo[left_wheel2].angle = fwd_speed
            kit.servo[left_wheel3].angle = fwd_speed
            # Replace 0 with the appropriate angle for clockwise rotation
        # Check if the message is 's' to stop the servo
        elif messageString == 's':
            kit.servo[right_wheel1].angle = None
            kit.servo[right_wheel2].angle = None
            kit.servo[right_wheel3].angle = None
            kit.servo[left_wheel1].angle = None
            kit.servo[left_wheel2].angle = None
            kit.servo[left_wheel3].angle = None
            #kit.servo[servo_channel].angle = None

if __name__ == '__main__':
    # Start the UDP server in a separate thread
    udp_thread = threading.Thread(target=udp_server)
    udp_thread.start()

    # Start the Flask web server
    # Use this port number and input it in the app
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
