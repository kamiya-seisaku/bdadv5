from flask import Flask, send_file, Response, render_template
from flask_socketio import SocketIO, emit
import shared_stuff as sf
# import mss
from io import BytesIO
from PIL import ImageGrab
# from screen_share import ScreenShareCamera

## flask #####################################################################
class flask_server_wrapper:
    app = Flask(__name__)
    socketio = SocketIO(app)
    monitor = {"top": 100, "left": 100, "width": 800, "height": 800}  # Define capture area
    
    def __init__(self):
        pass
        # top = self.monitor["top"]
        # left = self.monitor["left"]
        # width = self.monitor["width"]
        # height = self.monitor["height"]

        # print(f"ScreenShareCamera: top={top}, left={left}, width={width}, height={height}")
        # self.video_camera = ScreenShareCamera(top, left, width, height)

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
                # capture_size = {'x': 500, 'y': 500, 'width': 800, 'height': 600}
                # c = capture_size
                # x, y, width, height = c['x'], c['y'], c['width'], c['height']
                x, y, width, height = 0, 75, 500, 400
                # x, y, width, height = 2, 285, 900, 500
                img_buffer = BytesIO()
                ImageGrab.grab(bbox =(x, y, x + width, y + height)).save(img_buffer, 'JPEG', quality=50)
                img_buffer.seek(0)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpg\r\n\r\n' + img_buffer.read() + b'\r\n\r\n')
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
