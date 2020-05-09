import cv2
import numpy as np



def detectImage(path):

    img = cv2.imread(path)
    v = np.median(img)
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    edges = cv2.Canny(img, lower, upper)

    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(edges,kernel,iterations=4)

    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    approx_shapes = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.04*cv2.arcLength(contour,True),True)
        approx_shapes.append(approx)
    imagesNumber = 0
    imageParameter = []
    n = 0
    image_approx = []

    while n < len(approx_shapes):
        if(len(approx_shapes[n]) == 4):
            triangleNumber = 0
            for i in range(len(approx_shapes)):
                if(hierarchy[0][i][3] == n and len(approx_shapes[i]) == 3):
                    triangleNumber += 1
            if(triangleNumber == 4):
                width = abs(approx_shapes[n].ravel()[4] - approx_shapes[n].ravel()[0])
                height = abs(approx_shapes[n].ravel()[5] - approx_shapes[n].ravel()[1])
                centerx = (approx_shapes[n].ravel()[0] + approx_shapes[n].ravel()[4])/2
                centery = (approx_shapes[n].ravel()[1] + approx_shapes[n].ravel()[5])/2
                imageParameter.append({'CenterX' : centerx,'CenterY' : centery,'Width' : width,'Height' : height})
                imagesNumber += 1
                image_approx.append(approx_shapes[n])
                cv2.drawContours(img, [approx_shapes[n]], 0, (0, 0, 255), 2)
                cv2.putText(img, "Image", (int(centerx), int(centery - height/2 - 10)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
            n += 1
        else:
            n += 1
    #cv2.imshow('image',img)
    return  image_approx