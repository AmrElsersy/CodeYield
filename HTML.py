import math

def convert100_to_col_12(width):
    if(((width*12)%100) > 50):
        return math.ceil(width*12/100)
    elif (((width*12)%100) < 50):
        return math.floor(width*12/100)
    # return "col-" + str (int( (width/100)*12))
#There was a problem with floating percentage, their sum would never equal 12 like 60 - 40

class HTML_Generator():
    def __init__(self):
        self.html_header = '''<!DOCTYPE html>\n<html>\n<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Bootstrap</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">\n</head>\n'''
        self.html_footer = '''</div>
        \n</body>\n</html>'''
        self.body = '''<body style="width:100wh;  height:100vh;">\n
<div class="container h-100">
            '''

    def addRow(self, rowContent):
        self.body += rowContent
    
    def print(self):
        print(self.body)


    def concatinateHTML(self):
        return self.html_header + self.body + self.html_footer


class Row():
    def __init__(self,height):
        self.div_openTag = '''\n<div class="row" style="width:100%; height:{}% ">\n\t'''.format(height)
        self.div_closedTag = '''\n</div> '''
        self.content = ''' '''
        # print('New Row : '+self.div_openTag,self.content,self.div_closedTag)

    def addColumn(self, columnContent):
        self.content += columnContent

    def concatinateHTML(self):
        # self.content = self.div_openTag + self.content + self.div_closedTag
        return self.div_openTag + self.content + self.div_closedTag

class Column():
    def __init__(self,Width):
        self.div_openTag = '''\n<div class="col-{}" height="100%" >'''.format(convert100_to_col_12(Width))
        self.div_closedTag = '''\n</div>'''
        self.content = ''' '''
        self.width = Width 
        # print('New Column :'+self.div_openTag,self.content,self.div_closedTag)
 
    def concatinateHTML(self):
        return self.div_openTag + self.content + self.div_closedTag

    def addImage(self,width,height,alignment):
        self.content += '''
        <img src="https://sekatandsipter.com/wp-content/uploads/2019/08/sekat-and-sipter-letter-webpix-1.jpg" style="width: {}%; height:{}%;">         
            '''.format(width,height)
    
    def addTextInput(self,width,height,alignment):
        self.content += '''        
        <div class="form-group" style="padding-top: 10px; width: {}%; height: {}%;">
                <input type="text" class="form-control" placeholder="Enter Text" style=" width: 100%; height: 100%;">
        </div>
        '''.format(width,height)


    def addNavbar(self,width,height,alignment):
        self.content += '''\n\t<div style=" width: {}%; height: {}%;>\t
            asdasdasd
        </div>'''.format(width,height)

    def addText(self,width,height,alignment):
        self.content += '''\n\t   <div  class="" style=" width: {}%; height: {}%; margin:auto; text-align: center;     
        display: flex;
        align-items: center;
        justify-content: center;" >\t 
        
        <p> Lorem ipsum dolor </p> 
        </div>'''.format(width,height)

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
    def __repr__(self):
        return self.name

class HtmlRow:
    def __init__(self):
        self.shapesPerRow = []
        self.column1Shapes = []
        self.column2Shapes = []
        self.column1Ratio = 0
        self.column2Ratio = 0
        self.height = 0
        self.maxWidthIndex = 0
    
    def print(self):
        print(self.column1Shapes,self.column2Shapes)


listOfRows = []

row1 = HtmlRow()
row2 = HtmlRow()
row3 = HtmlRow()
# ======= ROW 1 
row1.height = 10
row1.column1Ratio = 20
row1.column2Ratio = 80

navBar = Shape("navbar",1,1,100,50,1)
row1.column1Shapes.append(navBar)
# ======= ROW 2
row2.height = 40
row2.column1Ratio = 40
row2.column2Ratio = 60

image = Shape("image",1,1,100,80,1)
text1 = Shape("text",1,1,40,20,1)
text2 = Shape("text",1,1,80,80,1)

row2.column1Shapes.append(text1)
row2.column1Shapes.append(text2)

row2.column2Shapes.append(image)

# ======= ROW 3
row3.height = 10
row3.column1Ratio = 20
row3.column2Ratio = 80

text3 = Shape("text",1,1,100,100,1)
textInput = Shape("textInput",1,1,100,100,1)

row3.column1Shapes.append(text3)
row3.column2Shapes.append(textInput)

# listOfRows.append(row1)
listOfRows.append(row2)
listOfRows.append(row3)


#testing the list of rows after adding elements
# for row in listOfRows:
#     row.print()
#     for shape in row.column1Shapes:
#         print(shape.name)
#     for shape in row.column2Shapes:
#         print(shape.name)

HTML_Page = HTML_Generator()

for row in listOfRows:
    New_row = Row(row.height)
    New_col1 = Column(row.column1Ratio)
    New_col2 = Column(row.column2Ratio)
    for shape in row.column1Shapes:
        if(shape.name == 'image'):
            New_col1.addImage(shape.width,shape.height,'none')
        elif(shape.name == 'textInput'):
            New_col1.addTextInput(shape.width,shape.height,'none')
        elif(shape.name == 'navbar'):
            New_col1.addNavbar(shape.width,shape.height,'none')
        elif(shape.name == 'text'):
            New_col1.addText(shape.width,shape.height,'none')

    for shape in row.column2Shapes:
        if(shape.name == 'image'):
            New_col2.addImage(shape.width,shape.height,'none')
        elif(shape.name == 'textInput'):
            New_col2.addTextInput(shape.width,shape.height,'none')
        elif(shape.name == 'navbar'):
            New_col2.addNavbar(shape.width,shape.height,'none')
        elif(shape.name == 'text'):
            New_col2.addText(shape.width,shape.height,'none')
    
    New_row.addColumn(New_col1.concatinateHTML())
    New_row.addColumn(New_col2.concatinateHTML())
    # print(New_col1.content + New_col2.content)
    # print(New_row.content)
    
    HTML_Page.addRow(New_row.concatinateHTML())


html = HTML_Page.concatinateHTML()
# HTML_Page.print()
HTML_File = open('Index.html','w+')
for line in html:
    HTML_File.write(line)
print('Done')