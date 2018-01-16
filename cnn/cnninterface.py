import cv2
import numpy as np
import tempfile

import gestureCNN as myNN

minValue = 70

x0 = 400
y0 = 200
height = 200
width = 200

kernel = np.ones((15, 15), np.uint8)
kernel2 = np.ones((1, 1), np.uint8)
skinkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Which mask mode to use BinaryMask or SkinMask (True|False)
binaryMode = True
counter = 0
# This parameter controls number of image samples to be taken PER gesture
numOfSamples = 301
mod = 0


def skinMask(frame, x0, y0, width, height):
    # HSV values
    low_range = np.array([0, 50, 80])
    upper_range = np.array([30, 200, 255])

    cv2.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0), 1)
    roi = frame[y0:y0 + height, x0:x0 + width]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Apply skin color range
    mask = cv2.inRange(hsv, low_range, upper_range)

    mask = cv2.erode(mask, skinkernel, iterations=1)
    mask = cv2.dilate(mask, skinkernel, iterations=1)

    # blur
    mask = cv2.GaussianBlur(mask, (15, 15), 1)
    # cv2.imshow("Blur", mask)

    # bitwise and mask original frame
    res = cv2.bitwise_and(roi, roi, mask=mask)
    # color to grayscale
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    return res


def binaryMask(frame, x0, y0, width, height):
    cv2.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0), 1)
    roi = frame[y0:y0 + height, x0:x0 + width]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    # blur = cv2.bilateralFilter(roi,9,75,75)

    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    ret, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # ret, res = cv2.threshold(blur, minValue, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)

    return res


def load_model():
    global mod, binaryMode, x0, y0, width, height

    print "Will load default weight file"
    mod = myNN.loadCNN(0)


def process_frame(frame):
    if binaryMode == True:
        roi = binaryMask(frame, x0, y0, width, height)
    else:
        roi = skinMask(frame, x0, y0, width, height)

    # cv2.imwrite("src.png", frame)

    fn = tempfile.mkstemp(".png")[1]
    cv2.imwrite(fn, roi)
    data = open(fn).read()
    return data


def process_image(img_file):
    frame = cv2.imread(img_file)
    return process_frame(frame)
