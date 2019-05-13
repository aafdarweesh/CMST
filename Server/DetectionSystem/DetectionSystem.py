from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import os
import urllib
from time import sleep
import glob
import json
import sys
sys.path.append('../Common/')

import requests
import uu

#Common Class that are going to be used
import User, DroneConfigurations, Mission, RaspberryPi

#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


'''
json file format that will be sent to the detection server
{
'missionID' : 'missionID',
'videoID' : 'videoID',
'videoContent' : 'videoContent'
}


{
"missionID" : "missionID",
"videoID" : "videoID",
"videoContent" : "videoContent"
}
'''


#This function receives the video from the RaspberryPi Client
#This function will be moved to the detection system
@app.route('/ReceiveVideo', methods = ['POST'])
def ReceiveVideo():
    videoName = ''
    videoName += str(request.json['missionID'])
    videoName += str(request.json['videoID'])

    print("Before the video content conversion")
    receivedEncodedVideo = open("./ReceivedData/videoTemp.txt", 'w')
    receivedEncodedVideo.write(request.json['videoContent'])

    #Decode the encoded video back to the same format
    uu.decode("./ReceivedData/videoTemp.txt", "./ReceivedData/" + videoName + ".h264")
    return jsonify("Received!")




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=80)
