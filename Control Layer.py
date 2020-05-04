import cv2 as cv
from image import detectImage
from NavBar import navBar
from cross_circle import detectIcon
from LabelBar import labelBarDetection
from LabelDetection import labelDetection

path = "data/test4.jpg"
img = cv.imread(path)
imageHeight, imageWidth, imageChannels = img.shape
print(imageHeight,imageWidth)

# Tuning Parameters
rowMarginBetweenShapes = 0.33*imageHeight
colMarginXPoint = int(imageWidth / 2)
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
        # Right-Left
        self.allignment = ""

class HtmlRow:
    def __init__(self):
        self.shapesPerRow = []
        self.column1Shapes = []
        self.column2Shapes = []
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


def handlingRows():

    incrementRowFlag = False
    temporaryRow = HtmlRow()

    # 1st minimum-y shape is inserted into 1st row
    temporaryRow.shapesPerRow.append(shapesList[0])

    # print(temporaryRow.shapesPerRow[0].height)

    for iterator in range(len(shapesList) - 1):
        diff = abs(shapesList[iterator].y - shapesList[iterator + 1].y)
        if diff < rowMarginBetweenShapes:
            # Calc. height of each row
            if incrementRowFlag == True:
                # Creating a new row
                temporaryRow = HtmlRow()
                incrementRowFlag = False
            temporaryRow.shapesPerRow.append(shapesList[iterator + 1])
        else:
            incrementRowFlag = True
            listOfRows.append(temporaryRow)

    # Appending last row elements
    listOfRows.append(temporaryRow)

    startYPoint = 0
    endYPoint = 0

    #print(len(listOfRows[0].shapesPerRow))

    # Calc. Each row height
    # for rowsCounter in range(len(listOfRows)):
    #
    #     for shapes in range(len(listOfRows[rowsCounter].shapesPerRow)):
    #         endYPoint = max(endYPoint, listOfRows[rowsCounter].shapesPerRow[shapes].y +  (listOfRows[rowsCounter].shapesPerRow[shapes].height / 2))
    #
    #     listOfRows[rowsCounter].height = endYPoint - startYPoint
    #     startYPoint = endYPoint

    for rowsCounter in range(len(listOfRows)):
        # Accessing last element of list to retrieve maximum-y point shape that will represent the height of each row
        listOfRows[rowsCounter].height = listOfRows[rowsCounter].shapesPerRow[-1].y +  listOfRows[rowsCounter].shapesPerRow[-1].height / 2
        print('ROW Height',listOfRows[rowsCounter].height)


handlingRows()

#print(len(shapesList))
#print(len(listOfRows))
#print(listOfRows[0].height)

# Retrieving maximum width of a shape for each row & calc. ratio of columns
for rowsCounter in range(len(listOfRows)):

    for shapes in range(len(listOfRows[rowsCounter].shapesPerRow)-1):
        if listOfRows[rowsCounter].shapesPerRow[shapes+1].width > listOfRows[rowsCounter].shapesPerRow[ listOfRows[rowsCounter].maxWidthIndex ].width:
            listOfRows[rowsCounter].maxWidthIndex = shapes+1

    # Retrieving maximum width for each shape for each row
    maxWidthShape = listOfRows[rowsCounter].shapesPerRow[ listOfRows[rowsCounter].maxWidthIndex ]

    #
    if maxWidthShape.x <= colMarginXPoint:
        maxColumnWidth = maxWidthShape.x + (maxWidthShape.width / 2)
        listOfRows[rowsCounter].column1Ratio = maxColumnWidth / imageWidth
        listOfRows[rowsCounter].column2Ratio = 1 - listOfRows[rowsCounter].column1Ratio
    else:
        maxColumnWidth = maxWidthShape.x + (maxWidthShape.width / 2)
        listOfRows[rowsCounter].column2Ratio = maxColumnWidth / imageWidth
        listOfRows[rowsCounter].column1Ratio = 1 - listOfRows[rowsCounter].column2Ratio

#print(listOfRows[1].height)
# Appending each shape to their belong column
for rowsCounter in range(len(listOfRows)):

    for shapes in range(len(listOfRows[rowsCounter].shapesPerRow)):
        # Checking if the shape lies either in the left column or right one
        if listOfRows[rowsCounter].shapesPerRow[shapes].x <= (listOfRows[rowsCounter].column1Ratio * imageWidth):
            listOfRows[rowsCounter].column1Shapes.append(listOfRows[rowsCounter].shapesPerRow[shapes])
            # Assigning shape width ratio
            shapeWidthRatio = listOfRows[rowsCounter].shapesPerRow[shapes].width / (listOfRows[rowsCounter].column1Ratio * imageWidth)
            listOfRows[rowsCounter].shapesPerRow[shapes].widthRatio = shapeWidthRatio

            # Assigning shape height ratio
            shapeHeightRatio = listOfRows[rowsCounter].shapesPerRow[shapes].height / listOfRows[rowsCounter].height
            listOfRows[rowsCounter].shapesPerRow[shapes].heightRatio = shapeHeightRatio

            # Assigning shape allignment
            shapeAllignment = (listOfRows[rowsCounter].column1Ratio * imageWidth) / 2
            if listOfRows[rowsCounter].shapesPerRow[shapes].x <= shapeAllignment:
                listOfRows[rowsCounter].shapesPerRow[shapes].allignment = "LEFT"
            else:
                listOfRows[rowsCounter].shapesPerRow[shapes].allignment = "RIGHT"

        else:
            listOfRows[rowsCounter].column2Shapes.append(listOfRows[rowsCounter].shapesPerRow[shapes])
            # Assigning shape width ratios
            shapeWidthRatio = listOfRows[rowsCounter].shapesPerRow[shapes].width / (
                        listOfRows[rowsCounter].column1Ratio * imageWidth)
            listOfRows[rowsCounter].shapesPerRow[shapes].widthRatio = shapeWidthRatio

            # Assigning shape height ratio
            shapeHeightRatio = listOfRows[rowsCounter].shapesPerRow[shapes].height / listOfRows[rowsCounter].height
            listOfRows[rowsCounter].shapesPerRow[shapes].heightRatio = shapeHeightRatio

            # Assigning shape allignment
            shapeAllignment = (listOfRows[rowsCounter].column2Ratio * imageWidth) / 2
            if listOfRows[rowsCounter].shapesPerRow[shapes].x <= shapeAllignment:
                listOfRows[rowsCounter].shapesPerRow[shapes].allignment = "LEFT"
            else:
                listOfRows[rowsCounter].shapesPerRow[shapes].allignment = "RIGHT"


for i in range(len(listOfRows)):

    print('Column 1 Started')
    for j in range(len(listOfRows[i].column1Shapes)):
        print(listOfRows[i].column1Shapes[j].name)

    print('Column 2 Started')
    for k in range(len(listOfRows[i].column2Shapes)):
        print(listOfRows[i].column2Shapes[k].name)
    print('ROW Finished')


cv.waitKey(0)
cv.destroyAllWindows()
