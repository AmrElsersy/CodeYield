import math
from _sha3 import sha3_224

from Controlfunction import imageprocessing


def htmlGenerator(path):
    def convert100_to_col_12(width):
        if ((width * 12) % 100) > 50:
            return math.ceil(width * 12 / 100)
        elif ((width * 12) % 100) < 50:
            return math.floor(width * 12 / 100)

    class HTML_Generator():
        def __init__(self):
            self.html_header = '''<!DOCTYPE html>
	        <html>
	        <head>
	            <meta charset="UTF-8">
	            <meta name="viewport" content="width=device-width, initial-scale=1.0">
	            <meta http-equiv="X-UA-Compatible" content="ie=edge">
	            <title>Bootstrap</title>
	            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
	            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
	        </head>        
	        '''

            self.html_footer = '''</div>
	        \n</body>\n</html>'''

            self.body = '''<body style="width:100wh;  height:100vh;">
	        <div class="container-fluid h-100">
	        '''

        def addRow(self, rowContent):
            self.body += rowContent

        def print(self):
            print(self.body)

        def concatinateHTML(self):
            return self.html_header + self.body + self.html_footer

    class Row():
        def __init__(self, height, row_num):
            color = "#FFA500"
            if row_num % 2 != 0:
                color = "#808080"

            self.div_openTag = '''\n<div class="row" style="width:100%; height:{}% ; background-color:{}; ">\n\t'''.format(
                height, color)
            self.div_closedTag = '''\n</div> '''
            self.content = ''' '''
            # print('New Row : '+self.div_openTag,self.content,self.div_closedTag)

        def addColumn(self, columnContent):
            self.content += columnContent

        def concatinateHTML(self):
            # self.content = self.div_openTag + self.content + self.div_closedTag
            return self.div_openTag + self.content + self.div_closedTag

    class Column():
        def __init__(self, Width):
            self.div_openTag = '''\n<div class="col-md-{}" style="height:100%" >'''.format(convert100_to_col_12(Width))
            self.div_closedTag = '''\n</div>'''
            self.content = ''' '''
            self.width = Width
            # print('New Column :'+self.div_openTag,self.content,self.div_closedTag)

        def concatinateHTML(self):
            return self.div_openTag + self.content + self.div_closedTag

        def addImage(self, width, height, alignment, circle=False):

            if circle:
                self.content += '''
	            <div class="text-center" style="width: {}; height:{};">
	            <img src="https://sekatandsipter.com/wp-content/uploads/2019/08/sekat-and-sipter-letter-webpix-1.jpg" style="width: 80%; height:80%;" class = "img-thumbnail img-circle">         
	            </div>            
	            '''.format(width, height)
            else:
                self.content += '''
	            <div class="text-center" style="width: {}; height:{};">
	            <img src="https://sekatandsipter.com/wp-content/uploads/2019/08/sekat-and-sipter-letter-webpix-1.jpg" style="width: 80%; height:80%;" class = "img-thumbnail">         
	            </div>            
	            '''.format(width, height)

        def addTextInput(self, width, height, alignment):
            self.content += '''        
	        <div class="form-group" style="padding-top: 10px; width: {}px; height: {}px;">
	                <input type="text" class="form-control" placeholder="Enter Text" style=" width: 100%; height: 100%;">
	        </div>
	        '''.format(width, height)

        def addNavbar(self, width, height, alignment):
            # <div style="width:15%">
            self.content += '''
	        <nav class="navbar navbar-default">
	                <div class="container-fluid">
	                  <div class="navbar-header">
	                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
	                      <span class="icon-bar"></span>
	                      <span class="icon-bar"></span>
	                      <span class="icon-bar"></span>                        
	                    </button>
	                  </div>
	                  <div class="collapse navbar-collapse" id="myNavbar">
	                    <ul class="nav navbar-nav">
	                      <li class="active"><a href="#">Home</a></li>
	                      <li><a href="#">Page 2</a></li>
	                      <li><a href="#">Page 3</a></li>
	                    </ul>
	                  </div>
	                </div>
	        </nav>
	        '''
            # </div>

        def addText(self, width, height, alignment):

            self.content += '''
	        <div  class="" style=" width: {}px; height: {}px; margin:auto; text-align: center;">
	        <h3> Lorem ipsum </h3> 
	        </div>'''.format(width, height)

            # <p> Lorem ipsum dolor Lorem ipsum dolor Lorem ipsum dolor Lorem ipsum dolor</p>
            # display: flex;
            # align-items: center;
            # justify-content: center;

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
            print(self.column1Shapes, self.column2Shapes)

    # listOfRows = []
    #
    # row1 = HtmlRow()
    # row2 = HtmlRow()
    # row3 = HtmlRow()
    # row4 = HtmlRow()
    # row5 = HtmlRow()
    #
    # navBar = Shape("NAV",1,1,100,50,1)
    # image = Shape("IMAGE",1,1,100,80,1)
    # text = Shape("TEXT",1,1,40,20,1)
    # textInput = Shape("LABEL",1,1,100,100,1)
    #
    # # ======= ROW 1
    # row1.height = 10
    # row1.column1Ratio = 100
    # row1.column2Ratio = 0
    #
    # row1.column1Shapes.append(navBar)
    # # ======= ROW 2
    # row2.height = 20
    # row2.column1Ratio = 50
    # row2.column2Ratio = 50
    #
    # row2.column1Shapes.append(text)
    # row2.column2Shapes.append(image)
    #
    # # ======= ROW 3
    # row3.height = 20
    # row3.column1Ratio = 50
    # row3.column2Ratio = 50
    #
    # row3.column2Shapes.append(text)
    # row3.column1Shapes.append(image)
    #
    # #======== ROW 4
    # row4.height = 20
    # row4.column1Ratio = 40
    # row4.column2Ratio = 60
    #
    # name = Shape("TEXT",1,1,40,20,1)
    # email = Shape("TEXT",1,1,40,20,1)
    # row4.column1Shapes.append(name)
    # row4.column1Shapes.append(email)
    # row4.column2Shapes.append(textInput)
    # row4.column2Shapes.append(textInput)
    #
    #
    #
    # listOfRows.append(row1)
    # listOfRows.append(row2)
    # listOfRows.append(row3)
    # listOfRows.append(row4)

    listOfRows = imageprocessing(path)
    # =================================================================================

    HTML_Page = HTML_Generator()

    for i, row in enumerate(listOfRows):
        New_row = Row(row.height, i)
        print("Column 1 Ratio" + str(row.column1Ratio*100))
        New_col1 = Column(row.column1Ratio*100)
        New_col2 = Column(row.column2Ratio*100)
        for shape in row.column1Shapes:
            print('Name: '+shape.name+', Width : ' + str(shape.width) + ', Height :' + str(shape.height) + ', Alignment:'+'column ratio'+str(row.column1Ratio*100))
            if (shape.name == 'IMAGE'):
                New_col1.addImage(shape.width, shape.height, 'none', False)
            elif (shape.name == 'ICON'):
                New_col1.addImage(shape.width, shape.height, 'none', True)
            elif (shape.name == 'LABEL'):
                New_col1.addTextInput(shape.width, shape.height, 'none')
            elif (shape.name == 'NAV'):
                New_col1.addNavbar(shape.width, shape.height, 'none')
            elif (shape.name == 'TEXT'):
                New_col1.addText(shape.width, shape.height, 'none')

        for shape in row.column2Shapes:
            print('Name: '+shape.name+', Width : ' + str(shape.width) + ', Height :' + str(shape.height) + ', Alignment:'+'column ratio'+str(row.column1Ratio*100))
            if (shape.name == 'IMAGE'):
                New_col2.addImage(shape.width, shape.height,'none')
            elif (shape.name == 'ICON'):
                New_col1.addImage(shape.width, shape.height, 'none', True)
            elif (shape.name == 'LABEL'):
                New_col2.addTextInput(shape.width, shape.height, 'none')
            elif (shape.name == 'NAV'):
                New_col2.width = 0;
                New_col2.addNavbar(shape.width, shape.height, 'none')
            elif (shape.name == 'TEXT'):
                New_col2.addText(shape.width, shape.height, 'none')

        New_row.addColumn(New_col1.concatinateHTML())
        New_row.addColumn(New_col2.concatinateHTML())
        # print(New_col1.content + New_col2.content)
        # print(New_row.content)

        HTML_Page.addRow(New_row.concatinateHTML())

    html = HTML_Page.concatinateHTML()
    # HTML_Page.print()

    HTML_File = open('Index.html', 'w+')
    for line in html:
        HTML_File.write(line)
    HTML_File.close()
    print('Done')
htmlGenerator('raye2_test.jpg')
