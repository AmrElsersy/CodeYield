from flask import Flask
from flask import request
from HTML import htmlGenerator
import base64
import time
import os
import os.path
import socket

app = Flask(__name__)

@app.route('/uploadimg', methods=['POST'])
def upload():
    
    image = base64.b64decode(request.get_data())
    timenow=str(time.time()).split('.')[0]
    
    with open ("Receivedimg/"+timenow+".png","wb") as received_img:
        received_img.write(image)
    path = "Receivedimg/"+timenow+".png"
    htmlGenerator(path)
    my_path = os.path.abspath(os.path.dirname(__file__))
    os.system('google-chrome ' + my_path +'/Index.html')
    return "Converting is finished"
    

if __name__ == '__main__':
    ip_address = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    app.run(debug=True, host=ip_address,port=5000)
