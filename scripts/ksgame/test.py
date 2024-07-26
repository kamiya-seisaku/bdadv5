from PIL import ImageGrab
from PIL import Image

img = ImageGrab.grab(bbox=(300, 300, 900, 900))

# Convert to PIL Image if necessary
if not isinstance(img, Image.Image):
    img = Image.fromarray(img)

img.save("captured_image.png")  # Saves as PNG in the current directory
