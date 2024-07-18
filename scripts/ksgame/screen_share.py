import io
from PIL import ImageGrab
import base64

class ScreenShareCamera():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_frame(self):
        """Capture and return the frame as JPEG bytes."""
        try:
            img = ImageGrab.grab()
            cropped_image = img.crop((self.x, self.y, self.x + self.width, self.y + self.height))
            buffer = io.BytesIO()
            cropped_image.save(buffer, format="JPEG")
            frame = buffer.getvalue()
            return frame
        except Exception as e:
            print(f"Error capturing screen region: {e}")
            return None
