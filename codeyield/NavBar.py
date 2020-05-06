import cv2
import numpy as np



# ========== Tracing ================
threshold = 150 # 150 tuned
# blockSize = 9 # 9 tuned 
hough_threshold = 200
epsilon = 0.01 # tuned
rect_ratio = 3 # 3 tuned
clean = 50 # 20-30 tuned
sigma = 33
window_w = 1280
window_h = 720



# =============================================
class Rect():
    def __init__(self,aprox,i,firstChiled):
        self.approx = aprox
        self.i = i 
        self.firstChild = firstChiled
    def print(self):
        pass
        # print(self.approx)
        # print("###")

def sortByX(rect):
    x,y,w,h = cv2.boundingRect(rect)
    return x
    

def cleanDuplicatedRectangles(rectangles):

    for rect in rectangles:
        rect.print()

    if len(rectangles) == 0:
        return []
    # iterate over rectangles and check if one is parent of another so remove it 
    for i, rectangle in enumerate(rectangles):
        # it may be wrong as it may just skip i not start from it
        for j,rect in enumerate (rectangles[i+1:]) :
            if rectangle.firstChild == rect.i:
                del rectangles[j]
                break
            elif rectangle.i == rect.firstChild:
                del rectangles[i]
                break

    for rect in rectangles:
        rect.print()
    # return list of contours
    list_rects = [rect.approx for rect in rectangles]
    return list_rects
    

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


def navBar(path):
    global window_h
    global window_w
    global navbars
    global threshold 
    global hough_threshold 
    global epsilon 
    global rect_ratio
    # load the image
    image = cv2.imread(path)
    image = cv2.resize(image,(window_w,window_h))
    grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)



    navbars = []
    rectangles = []
    lines = []
    other = []

    # ============ Edges =====================
    v = np.median(grayImage)
    global sigma
    sigma = sigma /100
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(grayImage, lower, upper) 
    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(edges,kernel,iterations=2)
    # ============ Contours ==================
    contours , hierarchy  = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # sort the contours by area
    # contours = sorted(contours, key = cv2.contourArea, reverse = True) 

    for i , cnt in enumerate(contours):
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
                rectangle = Rect(approx,i,hierarchy[0][i][3])
                rectangles.append(rectangle)    
            # big ratio means a narrow rectangle means a line
            elif ratio > rect_ratio and area_cnt < 10000 :
                lines.append(approx)
        else:
            other.append(approx)
            # print("len",len_cnt," ","area",area_cnt,"approx",len(approx),"ratio",ratio)

    # Drawing
    # for shape in other:
    #     cv2.drawContours(image,[shape],-1,(255,255,0),3)

    # for rect in rectangles:
    #     cv2.drawContours(image,[rect.approx],-1,(255,0,0),3)
    # for line in lines:
    #     cv2.drawContours(image,[line],-1,(0,255,0),3)


    rectangles = cleanDuplicatedRectangles(rectangles)

    
    # check if the rectangle have 3 lines 
    for rect in rectangles :
        rectLines = numLine(rect,lines)
        # print("rectlines",rectLines)
        if rectLines == 3:
            navbars.append(rect)
            cv2.drawContours(image,[rect],-1,(0,0,255),3)

    #cv2.imshow('navbar', image)
    return navbars
