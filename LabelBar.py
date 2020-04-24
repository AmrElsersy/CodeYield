import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import  random
import imutils


# Tuning Parameters
sigma = 0.33 # Canny's formula
houghLineLength = 100
houghLineGap = 20
dilationIterations = 5
erosionIterations = 1
epsilonFactor = 0.01
minAspectRatio = 0.5
maxAspectRatio = 4
rectMinApprox = 4
rectMaxApprox = 10
minAreaFilter = 5000



def labelBarDetection(srcImagePath):

    # Image Preparation & Kernel defintion of 5*5 Matrix
    img = cv.imread(srcImagePath, cv.IMREAD_COLOR)
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    kernel = np.ones((5, 5), np.uint8)
    # Automatic canny edge detection using sigma value = 0.33
    v = np.median(grayImg)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv.Canny(grayImg, lower, upper)

    # Dilating output of canny to achieve a huge edges
    dil = cv.dilate(edges, kernel, iterations=dilationIterations)

    # Using probabilistic hough line transform to get clear & semi complete lines
    processingImg = dil.copy()
    lines = cv.HoughLinesP(processingImg, 1, np.pi / 180, 100, minLineLength=houghLineLength, maxLineGap=houghLineGap)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(processingImg, (x1, y1), (x2, y2), (255, 255, 255), 5)

    # Eroding to remove noise edges
    erode = cv.erode(processingImg, kernel, iterations=erosionIterations)

    # Finding contours
    contours, hierarchy = cv.findContours(erode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filtering founded contours
    filtered = []
    for c in contours:
        if cv.contourArea(c) < minAreaFilter: continue
        filtered.append(c)

    # print(len(filtered))
    detectedLabelBars = [[0 for x in range(len(filtered))] for y in range(4)]

    # Drawing contours
    for cont in filtered:
        epsilon = epsilonFactor * cv.arcLength(cont, True)
        approx = cv.approxPolyDP(cont, epsilon, True)
        counter = 0
        x, y, w, h = cv.boundingRect(cont)
        aspectRatio = float(w) / h
        # Checking if it is a rectangle
        if (aspectRatio >= minAspectRatio and aspectRatio <= maxAspectRatio) and \
                (len(approx) >= rectMinApprox and len(approx) <= rectMaxApprox):

            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            detectedLabelBars[counter].append(x,y,w,h)
            counter += 1

        # col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # cv.drawContours(img, [approx], -1, col, 5)


    return detectedLabelBars

    titles = ['Orignal','Gray','Canny','Processing','erode','dil']
    images = [img,grayImg,edges,processingImg,erode,dil]

    rows = 2
    columns = 4
    iterations = len(images)
    for ite in range(iterations):
        plt.subplot(rows,columns, ite+1 ), plt.imshow(images[ite])
        plt.title(titles[ite])
    plt.show()



cv.waitKey(0)
cv.destroyAllWindows()

