import numpy as np
import cv2 as cv
import imutils
import pytesseract

image = r"C:\Users\robotics\PycharmProjects\ReceiptAutomation\BackEndAutomation\Image Proccessing\i1Abv.png"
def proccess(image):
    image = cv.imread(image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    cv.imshow("Otsu", thresh)
    dist = cv.distanceTransform(thresh, cv.DIST_L2, 5)
    dist = cv.normalize(dist, dist, 0, 1.0, cv.NORM_MINMAX)
    dist = (dist * 255).astype("uint8")
    cv.imshow("Dist", dist)
    dist = cv.threshold(dist, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    cv.imshow("Dist Otsu", dist)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
    opening = cv.morphologyEx(dist, cv.MORPH_OPEN, kernel)
    cv.imshow("Opening", opening)
    cnts = cv.findContours(opening.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    chars = []
    for c in cnts:
        (x, y, w, h) = cv.boundingRect(c)
        if w >= 35 and h >= 100:
            chars.append(c)
    chars = np.vstack([chars[i] for i in range(0, len(chars))])
    hull = cv.convexHull(chars)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv.drawContours(mask, [hull], -1, 255, -1)
    mask = cv.dilate(mask, None, iterations=2)
    cv.imshow("Mask", mask)
    final = cv.bitwise_and(opening, opening, mask=mask)
    cv.imshow("Final", final)
    return final

proccess(image)