from matplotlib import pyplot as plt
import cv2
import numpy as np

def labelDetection(scrImagePath):
    img = cv2.imread(scrImagePath)
    img = cv2.GaussianBlur(img , (5,5), 0)
    # img = cv2.medianBlur(img,5)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Apply Threshold
    ret,thresholded_image = cv2.threshold(img_gray,130,255,0)
    contours, hierarchy = cv2.findContours(thresholded_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print('Contour len'+str(len(contours)))
    for c in contours:
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c,True),True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        print(len(approx))
        if len(approx) >= 20 and len(approx)<30:
            x,y,w,h = cv2.boundingRect(approx)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),5)


    # cv2.drawContours(img,contours,-1,(0,255,0),10)

    titles = ['Image','After Gray Effetct','Image After Thresholding']
    images = [img,img_gray,thresholded_image]

    for i in range(len(images)):
        plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()