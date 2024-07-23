from flask import Flask, send_file, Response, render_template
from flask_socketio import SocketIO, emit
import shared_stuff as sf
import mss
from io import BytesIO
# from PIL import Image
from PIL import ImageGrab
# import os
# import sys
# import ifaddr
# import re
from screen_share import ScreenShareCamera

## flask #####################################################################
class flask_server_wrapper:
    # showTxt("flask_server_wrapper")
  
    app = Flask(__name__)
    socketio = SocketIO(app)
    monitor = {"top": 100, "left": 100, "width": 800, "height": 800}  # Define capture area
    
    def __init__(self):
        # Extract values as individual variables
        top = self.monitor["top"]
        left = self.monitor["left"]
        width = self.monitor["width"]
        height = self.monitor["height"]

        # Initialize the camera with positional arguments
        print(f"ScreenShareCamera: top={top}, left={left}, width={width}, height={height}")
        self.video_camera = ScreenShareCamera(top, left, width, height)

    def capture_and_stream(self):
        pass
        # while True:
        #     frame = self.video_camera.get_frame()
        #     if frame is not None:
        #         self.socketio.emit('screen_data', frame, namespace='/screen')
        #     else:
        #         # If there's an issue capturing the frame, wait a short time and retry
        #         time.sleep(0.1) 

    @socketio.on('connect', namespace='/screen')
    def handle_connect():
        # showTxt('Client connected')
        # todo: to be deleted
        self.socketio.start_background_task(self.capture_and_stream)

    @socketio.on('disconnect')
    def handle_disconnect():
        pass
        # showTxt('Client disconnected')

    @socketio.on('message')
    def handle_message(message):
#        import pdb; pdb.set_trace()

        print("in handle_message1")
        if sf.key_input_g == '':
            return
        sf.key_source_g = "socketio"
        sf.key_input_g = ''  # Reset key input
        print("in handle_message2")
        if message[0:7]=='keyup':
            print("in handle_message3")
            sf.key_input_g = ''
        else:
            print("in handle_message4")
        # elif message[0:7]=='keydown:':
            socket_key_input = message[8:9]
            # print(f"flask_server_wrapper/in handle_message: socket_key_input={socket_key_input}")
            if socket_key_input in {'a', 'd'}:
                sf.key_input_g = socket_key_input.upper()
            else:
                pass

    @app.route('/')
    def index():
        return send_file('..\\..\\public\\index.html')

    @app.route('/bg.jpg')
    def background():
        return send_file('..\\..\\assets\\milky_way-galaxy_ZBYYSDXC8O.jpg')

    @app.route('/feed')
    def video_feed():
        def gen():
            print("in gen")
            while True:
                img_buffer = BytesIO()
                ImageGrab.grab().save(img_buffer, 'JPEG', quality=50)
                img_buffer.seek(0)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpg\r\n\r\n' + img_buffer.read() + b'\r\n\r\n')

        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
