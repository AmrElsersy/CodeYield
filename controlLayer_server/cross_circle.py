import cv2 as cv
import numpy as np
import random


# Tuning Parameters
sigma = 0.33 # Canny's formula
houghLineLength = 100
houghLineGap = 10
dilationIterations = 3
erosionIterations = 2
epsilonFactor = 0.03
minContourArea = 500


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

    # Eroding to remove noise edges
    erode = cv.erode(processingImg, kernel, iterations=erosionIterations)

    # Finding contours
    contours, hierarchy = cv.findContours(processingImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    iconsDetected = []
    hierarchyCounter = 0
    # Drawing contours


    for cont in contours:
        epsilon = epsilonFactor * cv.arcLength(cont, True)
        approx = cv.approxPolyDP(cont, epsilon, True)

        #x, y, w, h = cv.boundingRect(approx)
        #cv.drawContours(img,[cont], 0, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 5)

        # Checking if it is a rectangle
        if len(approx) > 4 and len(approx) < 10 and (hierarchy[0][hierarchyCounter][2] !=-1) and cv.contourArea(cont) > minContourArea:
            (x, y), rad = cv.minEnclosingCircle(cont)
            center = (int(x), int(y))
            rad = int(rad)
            img = cv.circle(img, center, rad, (0, 255, 0), 5)
            iconsDetected.append(approx)

        hierarchyCounter += 1

    #cv.imshow('circle',img)
    return iconsDetected


