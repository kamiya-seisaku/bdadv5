#to start server: flask run
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import mss
import io
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

monitor = {"top": 100, "left": 100, "width": 800, "height": 800}  # Define capture area

def capture_and_stream():
    with mss.mss() as sct:
        while True:
            img = sct.grab(monitor)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=75)
            socketio.emit('screen_data', output.getvalue())

@app.route('/')
def index():
    return render_template('index.html')  # Basic HTML to display the stream

@socketio.on('connect')
def connect():
    socketio.start_background_task(capture_and_stream)

if __name__ == '__main__':
    socketio.run(app)
