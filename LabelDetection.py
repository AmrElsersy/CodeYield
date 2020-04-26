from matplotlib import pyplot as plt
import cv2
import numpy as np

def labelDetection(scrImagePath = 'zigzag2.jpeg'):

    img = cv2.imread(scrImagePath)
    #dictionary to store the values of the rectangles drawn around zigzag
    detectedLabels = {}
    dictionaryCounter = 0
    #filtering the image by using gaussian filter then
    img_blurred = cv2.GaussianBlur(img , (5,5), 0)
    img_gray = cv2.cvtColor(img_blurred,cv2.COLOR_BGR2GRAY)
    # Apply Threshold
    ret,thresholded_image = cv2.threshold(img_gray,130,255,0,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresholded_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # print('Contour len'+str(len(contours)))
    #A loop over contours to check which of them has lines that lies within the zigzag range
    for c in contours:
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c,True),True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        print(len(approx))
        if len(approx) >= 15 and len(approx)<40:
            cv2.drawContours(img,c,-1,(0,255,0),10)
            x,y,w,h = cv2.boundingRect(approx)
            detectedLabels[dictionaryCounter] = [x,y,x+w,y+h]
            dictionaryCounter +=1
            print('The Value :'+str(len(approx)))


    cv2.drawContours(img,contours,-1,(0,255,0),10)

    titles = ['Image','Image Blurred','After Gray Effetct','Image After Thresholding']

    images = [img,img_blurred,img_gray,thresholded_image]
    print(detectedLabels)
    for c in detectedLabels.values():
        img=cv2.rectangle(img,(c[0],c[1]),(c[2],c[3]),(255,0,0),5)
    for i in range(len(images)):
        plt.subplot(2, 3, i+1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()
    return detectedLabels
labelDetection('zigzag2.jpeg')
cv2.waitKey(0)
cv2.destroyAllWindows()
