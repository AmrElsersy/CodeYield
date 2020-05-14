import cv2
import numpy as np
import random

# Tuning Parameters
sigma = 0.33  # Canny's formula
dilationIterations = 2
epsilonFactor = 0.01

def labelDetection(scrImagePath):

    img = cv2.imread(scrImagePath)
    kernel = np.ones((1, 1), np.uint8)

    detectedLabels = []

    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, lower, upper)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)
    dil = cv2.dilate(edges, kernel, iterations=dilationIterations)
    erod = cv2.erode(dil,kernel,iterations=1)


    # Smoothing the image using 2d_Filter
    kernel0 = np.ones((5, 5), np.float32) / 25
    filter = cv2.filter2D(erod, -1, kernel0)


    # Apply Threshold
    contours, hierarchy = cv2.findContours(filter,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hierarchyCounter = 0

    #A loop over contours to check which of them has lines that lies within the zigzag range
    for c in contours:
        approx = cv2.approxPolyDP(c, epsilonFactor * cv2.arcLength(c,True),True)

        #cv2.drawContours(img,c,-1,(random.randint(0,255), random.randint(0,255), random.randint(0,255)),10)

        if len(approx) > 10 and len(approx) < 40 and (hierarchy[0][hierarchyCounter][2] == -1) and (hierarchy[0][hierarchyCounter][3] == -1) :

            x,y,w,h = cv2.boundingRect(approx)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(random.randint(0,255), random.randint(0,255), random.randint(0,255)),5)

            detectedLabels.append(approx)

        hierarchyCounter += 1

    #cv2.imshow('text',img)
    return detectedLabels

