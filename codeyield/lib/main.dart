import 'dart:convert';
import 'dart:ffi';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:get_ip/get_ip.dart';

void main() {
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    title: "Front-end Conveter",
    home: LandingScreen(),
  ));
}

class LandingScreen extends StatefulWidget {
  @override
  _LandingScreenState createState() => _LandingScreenState();
}

class _LandingScreenState extends State<LandingScreen> {

  File imageFile;
  int deviceNumber = 2;
  String base64Image;
  String ipAddress;

  _openGallary() async {
    var picture = await ImagePicker.pickImage(source: ImageSource.gallery);
    this.setState((){
      imageFile = picture;
    });
  }
  _openCamera() async {
    var picture = await ImagePicker.pickImage(source: ImageSource.camera);
    this.setState((){
      imageFile = picture;
    });
  }

  Future<void> postServer(String url) async {
    try {
      await http.post(url,body: base64Image);
    } on SocketException catch (err) {
      if(deviceNumber < 10) {
        deviceNumber++;
        String url = 'http://' + ipAddress + deviceNumber.toString() + ':5000/uploadimg';
        postServer(url);
      }
      else {
        print(err);
      }
    }
    finally {
      print('http://' + ipAddress + deviceNumber.toString() + ':5000/uploadimg');
    }
  }


  Future<void> _showChoiceDialog(BuildContext context) {
    return showDialog(context: context,builder: (BuildContext context) {
      return AlertDialog(
          title: Text("Please select an image"),
          content: Text("There's no image selected !")
      );
    });
  }

  Widget _decideImageView() {
    if(imageFile == null) {
      return Text("No Image Selected !",style: TextStyle(color: Colors.white), textAlign: TextAlign.center);
    }
    else {
      return Image.file(imageFile,width: 400,height: 400);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.deepOrange,
        title: Text("Front-end Selection",style: TextStyle(color: Colors.black54)),
      ),
      body: Center(
        child: Container(
          color: Colors.grey,
          alignment: Alignment.center,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  Expanded(child: _decideImageView()),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  RaisedButton(color: Colors.deepOrange,elevation: 5.0,onPressed: () async {
                    if(imageFile == null) {
                      _showChoiceDialog(context);
                    }
                    else {
                      base64Image = base64Encode(imageFile.readAsBytesSync());
                      ipAddress = await GetIp.ipAddress;
                      ipAddress = ipAddress.substring(0,ipAddress.length-1);
                      String url = 'http://' + ipAddress + deviceNumber.toString() + ':5000/uploadimg';
                      postServer(url);
                    }
                  },
                    child: Text("Convert image",style: TextStyle(color: Colors.black54)),
                  ),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  RaisedButton(color: Colors.deepOrange,elevation: 5.0,onPressed: () {
                    _openCamera();
                  },
                    child: Text("Take a photo",style: TextStyle(color: Colors.black54)),
                  ),
                  RaisedButton(color: Colors.deepOrange,elevation: 5.0,onPressed: () {
                    _openGallary();
                  },
                    child: Text("Select from gallary",style: TextStyle(color: Colors.black54)),
                  )
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}