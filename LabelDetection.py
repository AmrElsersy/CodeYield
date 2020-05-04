from matplotlib import pyplot as plt
import cv2
import numpy as np

def labelDetection(scrImagePath):
    sigma = 0.33  # Canny's formula
    dilationIterations = 1
    epsilonFactor = 0.03
    img = cv2.imread(scrImagePath)
    kernel = np.ones((1, 1), np.uint8)
    #list to store the values of the rectangles drawn around zigzag
    detectedLabels = []
    #filtering the image by using gaussian filter then
    # img_blurred = cv2.GaussianBlur(img , (5,5), 0)


    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, lower, upper)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)
    dil = cv2.dilate(edges, kernel, iterations=4)
    erod = cv2.erode(dil,kernel,iterations=1)
    # dilate = cv2.dilate(edges, kernel, iterations=2)
    # Apply Threshold
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hierarchyCounter = 0
    # print('Contour len'+str(len(contours)))
    #A loop over contours to check which of them has lines that lies within the zigzag range
    for c in contours:
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c,True),True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) >= 21 and len(approx)<40 and hierarchy.ravel()[hierarchyCounter*4 + 3] == -1:
            cv2.drawContours(img,c,-1,(0,255,0),10)

            x,y,w,h = cv2.boundingRect(approx)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),5)
            dictionary={ 'x':x,
                         'y':y,
                         'w':w,
                         'h':h}
            # print(dictionary)
            print(len(approx))
            detectedLabels.append(approx)
            # print('The Value :'+str(len(approx)))
        hierarchyCounter += 1

    #cv2.imshow('text',img)
    return detectedLabels

