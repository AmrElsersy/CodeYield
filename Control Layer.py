import cv2 as cv
from image import detectImage
from NavBar import navBar
from cross_circle import detectIcon
from LabelBar import labelBarDetection
from LabelDetection import labelDetection

path = "data/test2.jpeg"
img = cv.imread(path)
imageHeight, imageWidth, imageChannels = img.shape
#print(imageHeight,imageWidth)

# Tuning Parameters
rowMarginBetweenShapes = 100
colMarginXPoint = int(imageHeight / 2)
noOfColumnsPerRow = 2


class Shape:
    def __init__(self, name, x, y, width, height, radius):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.widthRatio = 0
        self.heightRatio = 0
        # Right-Left-Center
        self.allignment = ""

class HtmlRow:
    def __init__(self):
        self.shapesPerRow = []
        self.column0 = []
        self.column1 = []
        self.column1Ratio = 0
        self.column2Ratio = 0
        self.height = 0
        self.maxWidthIndex = 0


shapesList = []
listOfRows = []

# Retrieving labels
text = []
text = labelDetection(path)
for iterator in range(len(text)):
    x,y,w,h = cv.boundingRect(text[iterator])
    temporaryShape = Shape("TEXT", x + w / 2, abs(y - h / 2), w, h, 0)
    shapesList.append(temporaryShape)

# Retrieving labelBar
labelBar = []
labelBar = labelBarDetection(path)
for iterator in range(len(labelBar)):
    x, y, w, h = cv.boundingRect(labelBar[iterator])
    temporaryShape = Shape("LABEL", x + w / 2, abs(y - h / 2), w, h, 0)
    shapesList.append(temporaryShape)

# Retrieving images
image = []
image = detectImage(path)
for iterator in range(len(image)):
    x, y, w, h = cv.boundingRect(image[iterator])
    temporaryShape = Shape("IMAGE", x + w / 2, abs(y - h / 2), w, h, 0)
    shapesList.append(temporaryShape)

# Retrieving navigation bar
nav = []
nav = navBar(path)
for iterator in range(len(nav)):
    x, y, w, h = cv.boundingRect(nav[iterator])
    temporaryShape = Shape("NAV", x + w / 2, abs(y - h / 2), w, h, 0)
    shapesList.append(temporaryShape)

# Retrieving icons
icon = []
icon = detectIcon(path)
for iterator in range(len(icon)):
    (x, y), rad = cv.minEnclosingCircle(icon[iterator])
    temporaryShape = Shape("ICON", int(x), int(y), int(rad)*2, 0, int(rad))
    shapesList.append(temporaryShape)





# Sorting by y-point
shapesList = sorted(shapesList, key=lambda x: x.y, reverse=False)

# for i in range(len(shapesList)):
#     print(shapesList[i].name)



incrementRowFlag = False
temporaryRow = HtmlRow()

# 1st minimum-y shape is inserted into 1st row
temporaryRow.shapesPerRow.append(shapesList[0])
startYPoint = 0
endYPoint = shapesList[0].y + shapesList[0].height / 2
#print(temporaryRow.shapesPerRow[0].height)

for iterator in range(len(shapesList) - 1):
    diff = abs(shapesList[iterator].y - shapesList[iterator + 1].y)
    if diff < rowMarginBetweenShapes:
        # Calc. height of each row
        endYPoint = max(endYPoint, shapesList[iterator+1].y + shapesList[iterator+1].height / 2)
        if incrementRowFlag == True:
            # Inserting height of each row
            temporaryRow.height = endYPoint - startYPoint
            startYPoint = endYPoint

            # Inserting a new row
            temporaryRow = HtmlRow()
            incrementRowFlag = False
            temporaryRow.shapesPerRow.append(shapesList[iterator+1])
    else:
        incrementRowFlag = True
        listOfRows.append(temporaryRow)

# Appending last row elements
listOfRows.append(temporaryRow)

#print(len(listOfRows))
#print(listOfRows[0].height)

# Retrieving maximum width of a shape for each row
for rowsCounter in range(len(listOfRows)):

    for shapes in range(len(listOfRows[rowsCounter] - 1)):

        if listOfRows[rowsCounter].shapesPerRow[shapes+1].w > listOfRows[rowsCounter].shapesPerRow[shapes].w:
            listOfRows[rowsCounter].maxWidthIndex = shapes+1

    maxWidthShape = listOfRows[rowsCounter].shapesPerRow[ listOfRows[rowsCounter].maxWidthIndex ]






