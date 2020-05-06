import requests
import base64


    
def sendrequest():


           with open("sendimg.png",'rb') as img:
                data = base64.b64encode(img.read())

           response2 = requests.post('http://192.168.1.5:5000/uploadimg',data=data)
           print(response2.text)


  

     
sendrequest()
          















