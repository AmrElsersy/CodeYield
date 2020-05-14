import cv2 as cv
from image import detectImage
from NavBar import navBar
from cross_circle import detectIcon
from LabelBar import labelBarDetection
from LabelDetection import labelDetection


def imageprocessing(path):
	img = cv.imread(path)
	#cv.namedWindow('image',cv.WINDOW_NORMAL)
	#cv.imshow('image',img)
	imageHeight, imageWidth, imageChannels = img.shape
	#print(imageHeight, imageWidth)

	# Tuning Parameters
	rowMarginBetweenShapes = 0.1 * imageHeight
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
			self.allignment = ''

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
	text = labelDetection(path)
	for iterator in range(len(text)):
		x, y, w, h = cv.boundingRect(text[iterator])
		temporaryShape = Shape('TEXT', x + w / 2, y + h / 2, w, h, 0)
		shapesList.append(temporaryShape)

	# Retrieving labelBar
	labelBar = labelBarDetection(path)
	for iterator in range(len(labelBar)):
		x, y, w, h = cv.boundingRect(labelBar[iterator])
		temporaryShape = Shape('LABEL', x + w / 2, y + h / 2, w, h, 0)
		shapesList.append(temporaryShape)

	# Retrieving images
	image = detectImage(path)
	for iterator in range(len(image)):
		x, y, w, h = cv.boundingRect(image[iterator])
		temporaryShape = Shape('IMAGE', x + w / 2, y + h / 2, w, h, 0)
		shapesList.append(temporaryShape)

	# Retrieving navigation bar
	nav = navBar(path)

	for iterator in range(len(nav)):
		x, y, w, h = cv.boundingRect(nav[iterator])

		temporaryShape = Shape('NAV', x + w / 2, y + h / 2, w, h, 0)
		shapesList.append(temporaryShape)

	# Retrieving icons
	icon = detectIcon(path)
	for iterator in range(len(icon)):
		(x, y), rad = cv.minEnclosingCircle(icon[iterator])
		temporaryShape = Shape('ICON', int(x), int(y), int(rad) * 2, int(rad) * 2, int(rad))
		shapesList.append(temporaryShape)

	# Sorting by y-point
	shapesList = sorted(shapesList, key=lambda x: x.y, reverse=False)

	# Calc. Each row height
	def getMaxHeightPerRow(ROW):
		maxHeight = 0
		for ite in range(len(ROW.shapesPerRow)):
			maxHeight = max(maxHeight, ROW.shapesPerRow[ite].height)

		return maxHeight

	def handlingRows():
		temporaryRow = HtmlRow()

		# 1st minimum-y shape is inserted into 1st row
		temporaryRow.shapesPerRow.append(shapesList[0])

		for iterator in range(len(shapesList) - 1):
			diff = abs(shapesList[iterator].y - shapesList[iterator + 1].y)
			if diff < rowMarginBetweenShapes:
				temporaryRow.shapesPerRow.append(shapesList[iterator + 1])

			else:
				listOfRows.append(temporaryRow)
				temporaryRow = HtmlRow()
				temporaryRow.shapesPerRow.append(shapesList[iterator + 1])

		# Appending last row elements
		listOfRows.append(temporaryRow)

		# Retrieving max-height per row
		for rows in range(len(listOfRows)):
			listOfRows[rows].height = getMaxHeightPerRow(listOfRows[rows])
			# print('ROW Height',listOfRows[rows].height)

	handlingRows()

	# Retrieving maximum width of a shape for each row & calc. ratio of columns
	for rowsCounter in range(len(listOfRows)):

		for shapes in range(len(listOfRows[rowsCounter].shapesPerRow) - 1):
			if listOfRows[rowsCounter].shapesPerRow[shapes + 1].width > listOfRows[rowsCounter].shapesPerRow[
				listOfRows[rowsCounter].maxWidthIndex].width:
				listOfRows[rowsCounter].maxWidthIndex = shapes + 1

		# Retrieving maximum width for each shape for each row
		maxWidthShape = listOfRows[rowsCounter].shapesPerRow[listOfRows[rowsCounter].maxWidthIndex]

		#
		if maxWidthShape.x <= colMarginXPoint:
			maxColumnWidth = maxWidthShape.x + (maxWidthShape.width / 2)
			listOfRows[rowsCounter].column1Ratio = maxColumnWidth / imageWidth
			listOfRows[rowsCounter].column2Ratio = 1 - listOfRows[rowsCounter].column1Ratio

		else:
			maxColumnWidth = abs(maxWidthShape.x - (maxWidthShape.width / 2))
			listOfRows[rowsCounter].column1Ratio = maxColumnWidth / imageWidth
			listOfRows[rowsCounter].column2Ratio = 1 - listOfRows[rowsCounter].column1Ratio

	# Appending each shape to their belong column
	for rowsCounter in range(len(listOfRows)):

		for shapes in range(len(listOfRows[rowsCounter].shapesPerRow)):
			# Checking if the shape lies either in the left column or right one
			if listOfRows[rowsCounter].shapesPerRow[shapes].x <= (listOfRows[rowsCounter].column1Ratio * imageWidth):
				listOfRows[rowsCounter].column1Shapes.append(listOfRows[rowsCounter].shapesPerRow[shapes])

				# Assigning shape width ratio
				shapeWidthRatio = listOfRows[rowsCounter].shapesPerRow[shapes].width / (
							listOfRows[rowsCounter].column1Ratio * imageWidth)
				listOfRows[rowsCounter].shapesPerRow[shapes].widthRatio = shapeWidthRatio

				# Assigning shape height ratio
				shapeHeightRatio = listOfRows[rowsCounter].shapesPerRow[shapes].height / listOfRows[rowsCounter].height
				listOfRows[rowsCounter].shapesPerRow[shapes].heightRatio = shapeHeightRatio

				# Assigning shape allignment
				shapeAllignment = (listOfRows[rowsCounter].column1Ratio * imageWidth) / 3
				if listOfRows[rowsCounter].shapesPerRow[shapes].x <= shapeAllignment:
					listOfRows[rowsCounter].shapesPerRow[shapes].allignment = 'LEFT'

				elif listOfRows[rowsCounter].shapesPerRow[shapes].x <= 2 * shapeAllignment:
					listOfRows[rowsCounter].shapesPerRow[shapes].allignment = 'Center'

				else:
					listOfRows[rowsCounter].shapesPerRow[shapes].allignment = 'RIGHT'

			else:
				listOfRows[rowsCounter].column2Shapes.append(listOfRows[rowsCounter].shapesPerRow[shapes])
				# Assigning shape width ratios
				shapeWidthRatio = listOfRows[rowsCounter].shapesPerRow[shapes].width / (
							listOfRows[rowsCounter].column2Ratio * imageWidth)
				listOfRows[rowsCounter].shapesPerRow[shapes].widthRatio = shapeWidthRatio

				# Assigning shape height ratio
				shapeHeightRatio = listOfRows[rowsCounter].shapesPerRow[shapes].height / listOfRows[rowsCounter].height
				listOfRows[rowsCounter].shapesPerRow[shapes].heightRatio = shapeHeightRatio

				# Assigning shape allignment
				column1XPoint = (listOfRows[rowsCounter].column1Ratio * imageWidth)
				shapeAllignment = (imageWidth - column1XPoint) / 3
				if listOfRows[rowsCounter].shapesPerRow[shapes].x <= (shapeAllignment + column1XPoint):
					listOfRows[rowsCounter].shapesPerRow[shapes].allignment = 'LEFT'

				elif listOfRows[rowsCounter].shapesPerRow[shapes].x <= (2 * shapeAllignment + column1XPoint):
					listOfRows[rowsCounter].shapesPerRow[shapes].allignment = 'Center'

				else:
					listOfRows[rowsCounter].shapesPerRow[shapes].allignment = 'RIGHT'
	for i in range(len(listOfRows)):

		print('Column 1 Started')
		for j in range(len(listOfRows[i].column1Shapes)):
			print(listOfRows[i].column1Shapes[j].name, ',', listOfRows[i].column1Shapes[j].allignment)

		print('Column 2 Started')
		for k in range(len(listOfRows[i].column2Shapes)):
			print(listOfRows[i].column2Shapes[k].name, ',', listOfRows[i].column2Shapes[k].allignment)
		print('ROW' + str(i + 1) + 'Finished')

		# print('ROW Height' + str(i + 1), listOfRows[i].height)

	return listOfRows

# cv.waitKey(0)
# cv.destroyAllWindows()
