import withcation_screenshot as scap
import cv2
if __name__ == '__main__':
    x, y, w, h = 400, 200, 300, 180
    cv2.imwrite('sample.png', scap.rect(x, y, w, h))
