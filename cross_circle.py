import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Tuning Parameters
sigma = 0.33 # Canny's formula
houghLineLength = 100
houghLineGap = 10
dilationIterations = 3
erosionIterations = 2
epsilonFactor = 0.025
houghLineThickness = 2
minContourArea = 2000


def detectIcon(path):

    # Image Preparation & Kernel defintion of 5*5 Matrix
    img = cv.imread(path)
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    kernel = np.ones((3, 3), np.uint8)

    # Automatic canny edge detection using sigma value = 0.33
    v = np.median(grayImg)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv.Canny(img, lower, upper)

    # Dilating output of canny to achieve a huge edges
    dil = cv.dilate(edges, kernel, iterations=dilationIterations)

    # Using probabilistic hough line transform to get clear & semi complete lines
    processingImg = dil.copy()
    lines = cv.HoughLinesP(processingImg, 1, np.pi / 180, 100, minLineLength=houghLineLength, maxLineGap=houghLineGap)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(processingImg, (x1, y1), (x2, y2), (255, 255, 255), houghLineThickness)

    # Eroding to remove noise edges
    erode = cv.erode(processingImg, kernel, iterations=erosionIterations)

    # Finding contours
    contours, hierarchy = cv.findContours(processingImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    iconsDetected = []
    dictionaryCounter = 0
    # Drawing contours
    for cont in contours:
        epsilon = epsilonFactor * cv.arcLength(cont, True)
        approx = cv.approxPolyDP(cont, epsilon, True)

        x, y, w, h = cv.boundingRect(approx)
        #print(x, y, w, h)
        #print(len(approx))
        # Checking if it is a rectangle
        if len(approx) > 7 and len(approx) < 10:
            (x, y), rad = cv.minEnclosingCircle(cont)
            center = (int(x), int(y))
            rad = int(rad)
            img = cv.circle(img, center, rad, (255, 0, 0), 1)
            #print(x, y)
            iconsDetected.append(approx)
            dictionaryCounter += 1

    cv.imshow('re',img)
    return iconsDetected


