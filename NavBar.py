import cv2
import numpy as np

# ========== Tracing ================
lower = 100 # 100 tuned
upper = 300 # 300 tuned
threshold = 150 # 150 tuned
# blockSize = 9 # 9 tuned 
hough_threshold = 200
epsilon = 0.01 # tuned
rect_ratio = 3 # 3 tuned
clean = 20 # 20-30 tuned

def setClean(x):
    global clean
    clean = x
    navBar()
def setRectRatio(x):
    if x < 1 : 
        return
    global rect_ratio
    rect_ratio = x
    navBar()
def setThreshold(x):
    global threshold
    threshold = x
    navBar()

cv2.namedWindow("window")

cv2.createTrackbar("thresold","window",0,255,setThreshold)
cv2.createTrackbar("ratio","window",2,10,setRectRatio)
cv2.createTrackbar("clean","window",0,100,setClean)
# =============================================
window_w = 1280
window_h = 720
# path = "all.png"
# path = "shapes.jpg"
path = "test.png"
image = cv2.imread(path)
image = cv2.resize(image,(window_w,window_h))
cv2.imshow("window",image)

def sortByX(rect):
    x,y,w,h = cv2.boundingRect(rect)
    return x
    

def cleanDuplicatedRectangles(rectangles):
    global clean
    if len(rectangles) == 0:
        return []
    for i, rectangle in enumerate(rectangles):
        x,y,w,h = cv2.boundingRect(rectangle)
        for j,rect in enumerate (rectangles[i+1:]) :
            xi,yi,wi,hi = cv2.boundingRect(rect)
            if abs(xi-x) < clean and abs(yi-y) < clean and abs(wi-w) < clean and abs(hi-h) < clean:
                del rectangles[j]
                break
    return rectangles
    

def numLine(rect , lines):
    rect_x,rect_y,rect_w,rect_h = cv2.boundingRect(rect)
    num = 0
    for line in lines:
        # get the Contour Rectangle 
        x,y,w,h = cv2.boundingRect(line)
        # if the line inside the rectangle 
        if x > rect_x and x < rect_x + rect_w and y > rect_y and y < rect_y+rect_h:
            num = num +1
    return num

def navBar():
    global lower 
    global upper 
    global threshold 
    global hough_threshold 
    global epsilon 
    global rect_ratio
    global window_h
    global window_w
    rectangles = []
    lines = []
    global path
    image = cv2.imread(path)
    image = cv2.resize(image,(window_w,window_h))

    # ============ Gray Scale ================
    grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # ============ Threshold (Better) ========    
    _ , thresh = cv2.threshold(grayImage,threshold,255,cv2.THRESH_BINARY)
    cv2.imshow("window",thresh)
    # ============ Edges =====================
    # gives a worse result (try again)
    # edges = cv2.Canny(thresh,lower,upper)
    # cv2.imshow("window",edges)
    # ============ Contours ==================
    _ , contours , _  = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # sort the contours by area
    contours = sorted(contours, key = cv2.contourArea, reverse = True) 
    print(len(contours))
    for cnt in contours:
        len_cnt = cv2.arcLength(cnt,True)
        area_cnt = cv2.contourArea(cnt)      

        # skip small curves and the biggest curves
        if(len_cnt < 50) or (len_cnt > 2 * window_w):
            continue

        # get Corners 
        approx = cv2.approxPolyDP(cnt,len_cnt*epsilon,True)

        # Contours Rectangle
        x,y,w,h = cv2.boundingRect(approx)
        ratio = max(w,h)/min(w,h) 

        # if 4 corners
        if len(approx) == 4 :
            # small ratio -> rectangle with a big area
            if ratio < rect_ratio:
                rectangles.append(approx)    
            # big ratio means a narrow rectangle means a line
            elif ratio > rect_ratio and area_cnt < 10000 :
                lines.append(approx)

        print("len",len_cnt," ","area",area_cnt,"approx",len(approx),"ratio",ratio)

    # Drawing
    # for rect in rectangles:
    #     cv2.drawContours(image,[rect],-1,(255,0,0),3)
    # for line in lines:
    #     cv2.drawContours(image,[line],-1,(0,255,0),3)

    print(len(rectangles),len(lines))
    rectangles = cleanDuplicatedRectangles(rectangles)
    print("after Cleaning",len(rectangles))
    
    # check if the rectangle have 3 lines 
    for rect in rectangles :
        rectLines = numLine(rect,lines)
        # print("rectlines",rectLines)
        if rectLines == 3:
            # print("Navbar")
            cv2.drawContours(image,[rect],-1,(0,0,255),3)

    # cv2.imshow("thresh",thresh)
    cv2.imshow("window",image)

cv2.waitKey(0)
cv2.destroyAllWindows()
