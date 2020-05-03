import cv2 as cv
# from image import detectImage
# from NavBar import navBar

from LabelBar import labelBarDetection
from LabelDetection import labelDetection

# Tuning Parameters
rowMarginBetweenShapes = 10
colMargin = 100



path = "data/all.png"


class Shape:
    def __init__(self, name, x, y, width, height, radius):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.heigh = height
        self.radius = radius


class HtmlRow:
    shapesPerRow = []
    rowsHeight = []
    columns = []


shapesList = []
listOfRows = []

text = []
labelBar = []

text = labelDetection(path)
# for iterator in range(len(text)):
#   x,y,w,h = cv.boundingRect(text[iterator])
#  rowsColumnsList.append(["TEXT", x+w/2, h/2-y, w, h])


labelBar = labelBarDetection(path)

for iterator in range(len(labelBar)):
    x, y, w, h = cv.boundingRect(labelBar[iterator])
    temporaryShape = Shape("BAR", x + w / 2, abs(y - h / 2), w, h, 0)
    shapesList.append(temporaryShape)

# Sorting by y-point
shapesList = sorted(shapesList, key=lambda x: x.y, reverse=False)

incrementRowFlag = False
temporaryRow = HtmlRow
# 1st minimum-y shape is inserted into 1st row
temporaryRow.shapesPerRow.append(shapesList[0])

for iterator in range(len(shapesList) - 1):
    diff = abs(shapesList[iterator].y - shapesList[iterator + 1].y)
    if diff < rowMarginBetweenShapes:
        if incrementRowFlag == True:
            temporaryRow = HtmlRow
        temporaryRow.shapesPerRow.append(shapesList[iterator+1])
    else:
        incrementRowFlag = True
        listOfRows.append(temporaryRow)

# Appending last row elements
listOfRows.append(temporaryRow)

for rowsCounter in range(len(listOfRows)):

    for columnsCounter in range(7):

        for shapesCounter in range(len(listOfRows[rowsCounter].shapesPerRow)):
            # Retrieving list of shapes in rowsCounter-index row
            temporaryShape = listOfRows[rowsCounter].shapesPerRow[shapesCounter]
            if temporaryShape.x <= colMargin:
                listOfRows[rowsCounter].columns.append(temporaryShape)
                

