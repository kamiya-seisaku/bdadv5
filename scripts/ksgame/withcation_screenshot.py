# Withcation:https://withcation.com/2021/02/21/post-1590
# PIL.ImageGrabの仕様がひどすぎたのでスクリーンショットを自作した

import sys
# if sys.platform != 'darwin': raise OSError(f'unsupported OS.<{sys.platform=}>')
import subprocess
import numpy as np
import AppKit
import cv2
def rect(
    x: int or float or str,
    y: int or float or str,
    w: int or float or str,
    h: int or float or str
):
    x, y, w, h = map(float, [x, y, w, h])
    screens = AppKit.NSScreen.screens()
    if len(screens) > 1:
        raise SystemError(
            'unsupported more than one screens.'
            f'<{len(screens)=}>'
        )
    f = screens[0].frame
    if callable(f):
        f = f()
    x_max, y_max = f.size.width, f.size.height
    w_max, h_max = x_max - x - w, y_max - y - h
    if 0 <= x < x_max and 0 <= y < y_max and 0 <= w <= w_max and 0 <= h <= h_max:
        subprocess.run(f'screencapture -c -R {x},{y},{w},{h}'.split(' '))
        board = AppKit.NSPasteboard.generalPasteboard()
        return cv2.imdecode(np.frombuffer(bytes(board.dataForType_(board.types()[0])), np.uint8), -1)
    else:
        raise ValueError(
            f'arguments must be 0<=x<{int(x_max)}, 0<=y<{int(y_max)}, 0<=w<={int(w_max)}, 0<=h<={int(h_max)}.'
            f'<{(x, y, w, h)=}>'
        )
    if __name__ == '__main__':
        x, y, w, h = 400, 200, 300, 180
        rect(x, y, w, h)
