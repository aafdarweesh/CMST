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


@app.route('/RaspberryPiClientTest', methods=['POST'])
def RPiClientTest():
    url = "http://localhost:8083" #url of the RPiClient

    #startMission Request
    data = {'missionID' : '1', 'EstimatedMissionDuration' : '100'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try :
        req = requests.post(url+"/startMission", data=json.dumps(data), headers=headers)

        print("RPiClient startMission status : " + str(req.status_code) + " !!!")
    except :
        print("Couldn't connect to RaspberryPi to start new mission !!!")
    #Retrieve logFile
    try:
        r = urllib.request.urlretrieve(url + "/logFile", "logFile.txt")
        print("RPiClient Retrieve logFile status  : " + str(r) + " !!!")
    except:
        print("Problem Retrieve logFile!!!")


    #print(request.data)
    return 'Thank you !!!'


#This function receives the video from the RaspberryPi Client
#This function will be moved to the detection system
@app.route('/ReceiveVideo', methods = ['POST'])
def ReceiveVideo():
    videoName = ''
    videoName += str(request.json['missionID'])
    videoName += str(request.json['videoID'])

    receivedEncodedVideo = open("videoTemp.txt", 'w')
    receivedEncodedVideo.write(request.json['videoContent'])

    #Decode the encoded video back to the same format
    uu.decode("videoTemp.txt", videoName + ".h264")
    return jsonify("Received!")


#This function will be moved to the storage system, as it will Retrieve a list of received videos for that mission
@app.route('/ListOfReceivedVideos', methods=['GET'])
def GetListOfReceivedVideos():
    data = {'listOfReceivedVideos' : ['0','1','2','3']}
    return json.dumps(data)


@app.route('/RaspberryPiServerTest', methods=['POST'])
def RPiServerTest():
    return 'Thank you !!!'

if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8082)
