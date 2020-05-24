# uncomment the line with the photo name you want to run

import numpy as np
import cv2 as cv

#img = cv.imread("one.jpg", cv.IMREAD_COLOR)
#img = cv.imread("two.jpg", cv.IMREAD_COLOR)
#img = cv.imread("three.jpg", cv.IMREAD_COLOR)
#img = cv.imread("four.jpg", cv.IMREAD_COLOR)
#img = cv.imread("candyBig.jpg", cv.IMREAD_COLOR)
#img = cv.imread("candyBigSmaller.jpg", cv.IMREAD_COLOR)
img = cv.imread("candyBigSmallerTiny.jpg", cv.IMREAD_COLOR)

font = cv.FONT_HERSHEY_SIMPLEX
kernel = np.ones((10, 10), np.uint8)
p1 = 0
p2 = 0

# Store number of m&m's
blue = 0
brown = 0
green = 0
orange = 0
red = 0
yellow = 0

# set estimated value of colors
colors = {
    "blue": (255, 170, 18),
    "brown": (0, 18, 33),
    "green": (80, 231, 0),
    "orange": (0, 114, 250),
    "red": (51, 0, 200),
    "yellow": (13, 218, 238),
}

mod = img.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
height, width, channels = img.shape

# cv.namedWindow("Canny")

def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        #print("H:", hsv[y, x, 0], "   S:", hsv[y, x, 1], "  V:", hsv[y, x, 2])
        print("xCoord: ", x, "yCoord: ", y, "B:", img[y, x, 0], "   G:", img[y, x, 1], "  R:", img[y, x, 2])


def onMouse2(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # print("H:", hsv[y, x, 0], "   S:", hsv[y, x, 1], "  V:", hsv[y, x, 2])
        print("xCoord: ", x, "yCoord: ", y, "B:", img[y, x])


def change1(val):
    None


def change2(val):
    None


# used to test canny threshold values
cv.createTrackbar("p1", "Canny", 0, 255, change1)
cv.createTrackbar("p2", "Canny", 0, 255, change2)

# blur -> erode -> dilate -> find edges with canny -> find circles with HoughCircles
blur = cv.GaussianBlur(hsv, (11, 11), 0)
erode = cv.erode(blur, kernel, 1)
dilate = cv.dilate(erode, kernel, 1)
edges = cv.Canny(dilate, 151, 155)
circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, 20, param1=30, param2=15, minRadius=5, maxRadius=40)
res = img.copy

# create a mask for each circle and use the mask to find the mean color inside of them
mean_list = []
for i in circles[0, :]:
    mask = np.zeros(img.shape, np.uint8)
    cv.circle(mask, (i[0], i[1]), i[2], (255, 255, 255), cv.FILLED)
    mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    mean_list.append((cv.mean(img, mask)[0], cv.mean(img, mask)[1], cv.mean(img, mask)[2]))
    cv.circle(mod, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv.circle(mod, (i[0], i[1]), 2, (0, 0, 255), 3)

# match the mean color against the dictionary colors to determine what color the m&m is
for i in mean_list:
    min_diff = 99999999999999999999
    match = ""
    blue_diff = ((abs(i[0] - colors["blue"][0])) + (abs(i[1] - colors["blue"][1])) + (abs(i[2] - colors["blue"][2])))
    brown_diff = ((abs(i[0] - colors["brown"][0])) + (abs(i[1] - colors["brown"][1])) + (abs(i[2] - colors["brown"][2])))
    green_diff = ((abs(i[0] - colors["green"][0])) + (abs(i[1] - colors["green"][1])) + (abs(i[2] - colors["green"][2])))
    orange_diff = ((abs(i[0] - colors["orange"][0])) + (abs(i[1] - colors["orange"][1])) + (abs(i[2] - colors["orange"][2])))
    red_diff = ((abs(i[0] - colors["red"][0])) + (abs(i[1] - colors["red"][1])) + (abs(i[2] - colors["red"][2])))
    yellow_diff = ((abs(i[0] - colors["yellow"][0])) + (abs(i[1] - colors["yellow"][1])) + (abs(i[2] - colors["yellow"][2])))

    if blue_diff < min_diff:
        match = "blue"
        min_diff = blue_diff
    if brown_diff < min_diff:
        match = "brown"
        min_diff = brown_diff
    if green_diff < min_diff:
        match = "green"
        min_diff = green_diff
    if orange_diff < min_diff:
        match = "orange"
        min_diff = orange_diff
    if red_diff < min_diff:
        match = "red"
        min_diff = red_diff
    if yellow_diff < min_diff:
        match = "yellow"
        min_diff = yellow_diff

    if match == "blue":
        blue = blue + 1
    elif match == "brown":
        brown = brown + 1
    elif match == "green":
        green = green + 1
    elif match == "orange":
        orange = orange + 1
    elif match == "red":
        red = red + 1
    elif match == "yellow":
        yellow = yellow + 1

# print number of each m&m on the image
blue_str = "Blue: " + str(blue)
brown_str = "Brown: " + str(brown)
green_str = "Green: " + str(green)
orange_str = "Orange: " + str(orange)
red_str = "Red: " + str(red)
yellow_str = "Yellow: " + str(yellow)

cv.putText(mod, yellow_str, (5, height-10), font, .8, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(mod, yellow_str, (5, height-10), font, .8, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(mod, red_str, (5, height-40), font, .8, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(mod, red_str, (5, height-40), font, .8, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(mod, orange_str, (5, height-70), font, .8, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(mod, orange_str, (5, height-70), font, .8, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(mod, green_str, (5, height-100), font, .8, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(mod, green_str, (5, height-100), font, .8, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(mod, brown_str, (5, height-130), font, .8, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(mod, brown_str, (5, height-130), font, .8, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(mod, blue_str, (5, height-160), font, .8, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(mod, blue_str, (5, height-160), font, .8, (255, 255, 255), 1, cv.LINE_AA)

cv.imshow("img", mod)
# cv.imshow("Canny", edges)
cv.setMouseCallback("img", onMouse, 0)
# cv.setMouseCallback("res", onMouse2, 0)

cv.waitKey(0)

# # # Code to test Canny threshold ranges # # #

# while 1:
#     if cv.getTrackbarPos("p1", "Canny") != p1:
#         p1 = cv.getTrackbarPos("p1", "Canny")
#         mod = img.copy()
#
#     if cv.getTrackbarPos("p2", "Canny") != p2:
#         p2 = cv.getTrackbarPos("p2", "Canny")
#         mod = img.copy()
#
#     edges = cv.Canny(dilate, p1, p2)
#
#     circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, 30, param1=30, param2=15, minRadius=0, maxRadius=50)
#
#     for i in circles[0, :]:
#         cv.circle(mod, (i[0], i[1]), i[2], (0, 255, 0), 2)
#         cv.circle(mod, (i[0], i[1]), 2, (0, 0, 255), 3)
#
#     cv.putText(mod, "Yellow", (5, height-10), font, .8, (0, 0, 0), 4, cv.LINE_AA)
#     cv.putText(mod, "Yellow", (5, height-10), font, .8, (255, 255, 255), 1, cv.LINE_AA)
#     cv.putText(mod, "Red", (5, height-40), font, .8, (0, 0, 0), 4, cv.LINE_AA)
#     cv.putText(mod, "Red", (5, height-40), font, .8, (255, 255, 255), 1, cv.LINE_AA)
#     cv.putText(mod, "Green", (5, height-70), font, .8, (0, 0, 0), 4, cv.LINE_AA)
#     cv.putText(mod, "Green", (5, height-70), font, .8, (255, 255, 255), 1, cv.LINE_AA)
#     cv.putText(mod, "Brown", (5, height-100), font, .8, (0, 0, 0), 4, cv.LINE_AA)
#     cv.putText(mod, "Brown", (5, height-100), font, .8, (255, 255, 255), 1, cv.LINE_AA)
#     cv.putText(mod, "Blue", (5, height-130), font, .8, (0, 0, 0), 4, cv.LINE_AA)
#     cv.putText(mod, "Blue", (5, height-130), font, .8, (255, 255, 255), 1, cv.LINE_AA)
#
#     cv.imshow("img", mod)
#     cv.imshow("Canny", edges)
#
#     cv.setMouseCallback("img", onMouse, 0)
#     cv.setMouseCallback("res", onMouse2, 0)
#
#     k = cv.waitKey(1)
#     if k == 27:
#         break

cv.destroyAllWindows()
