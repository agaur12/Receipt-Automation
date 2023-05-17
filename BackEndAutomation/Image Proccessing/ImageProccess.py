import numpy as np
import cv2 as cv
import imutils

def proccess(image):
    image = cv.imread(image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] 
    cv2.imshow("Otsu", thresh)
    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
    dist = (dist * 255).astype("uint8")
    cv2.imshow("Dist", dist)
    dist = cv2.threshold(dist, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imshow("Dist Otsu", dist)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    opening = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
    cv2.imshow("Opening", opening)
    cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    chars = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w >= 35 and h >= 100:
            chars.append(c)
    chars = np.vstack([chars[i] for i in range(0, len(chars))])
    hull = cv2.convexHull(chars)
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [hull], -1, 255, -1)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("Mask", mask)
    final = cv2.bitwise_and(opening, opening, mask=mask)
    cv2.imshow("Final", final)
    return final
