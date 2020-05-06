from flask import Flask
from flask import request
from Controlfunction import imageprocessing
import base64
import time
import os

app = Flask(__name__)

@app.route('/uploadimg', methods=['POST'])
def upload():
    
    image = base64.b64decode(request.get_data())
    timenow=str(time.time()).split('.')[0]
    
    with open ("Receivedimg/"+timenow+".png","wb") as received_img:
        received_img.write(image)
    path = "Receivedimg/"+timenow+".png"
    imageprocessing(path)
    os.system("shotwell " + path)
    return "Thank You"
    

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.5',port=5000)
