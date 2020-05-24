import cv2 as cv
import numpy as np

kernel = np.ones((10, 10), np.uint8)
cap = cv.VideoCapture('MandMVideoSmall.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (11, 11), 0)
    erode = cv.erode(blur, kernel, 1)
    dilate = cv.dilate(erode, kernel, 1)
    edges = cv.Canny(dilate, 151, 155)
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, 20, param1=30, param2=15, minRadius=10, maxRadius=40)

    for i in circles[0, :]:
        cv.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
