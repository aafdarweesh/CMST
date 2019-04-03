
from flask import Flask, jsonify, request, render_template, send_from_directory, send_file
from flask_cors import CORS, cross_origin
import os
import urllib
from time import sleep
import glob
import json
import sys

import uu #to encode and decode the video into string (or base64)
import requests #for the HTTP requests
# Schedule Library imported
import schedule #pip install schedule

#static file directory
#static_file_dir = os.path.join(os.path.dirname(os.path.realpath('logFile')), 'static')



#fixed parameters
videoDuration = 10 #(video duration is 10 sec as it was suitable for 3G transmission rate)
numberOfVideos = 0 #Estimated Number of videos
logFile = open("logFile.txt","w") #This file contains the system logs
listOfReceivedVideos = [] #This list contians the videos that already received by the detection system



#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#start a mission http request (will run startRecording program, that is responsible for the videos, with the given details)
#reference : https://www.programcreek.com/python/example/82317/schedule.every
@app.route('/startMission', methods=['POST'])
def startMission():
    global videoDuration, numberOfVideos, logFile
    print(request.json)
    try :
        numberOfVideos = int(request.json['EstimatedMissionDuration'])//videoDuration #calculate the number of videos depending on the mission duration
        #logFile.write("New Mission was received, MissionID : " + str(int(request.json['MissionID'])) + " Number of Videos : " + str(numberOfVideos) + " !!!")
        print("New Mission was received, MissionID : " + request.json['missionID'] + " Number of Videos : " + str(numberOfVideos) + " !!!")
    except :
        #logFile.write("Couldn't Retrieve Mission details (EstimatedMissionDuration)!!!")
        print("Couldn't Retrieve Mission details (EstimatedMissionDuration)!!!")
    try:
        #os.system('pkill -9 ./StartRecording.py')
        #os.system('python ./StartRecording.py ' + str(videoDuration) + ' ' + str(numberOfVideos))
        #logFile.write("startRecording runs successfully!!!")
        print("StartRecording runs successfully!!!")
        #updateStatusWithServer() #update the status of the system every 3 seconds with the server
        os.system('pkill -9 ./ServerTransmission.py')
        os.system('python ./ServerTransmission.py ' + str(numberOfVideos))
        #logFile.write("Schedule is assigned for the !!!")
        print("Schedule is assigned for the transmission!!!")
    except:
        #logFile.write("startRecording and schedule Exception!!!")
        print("startRecording and schedule Exception!!!")
    return jsonify("Thank you!!!")

#return LogFile of the system
#reference : https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
@app.route('/logFile', methods=['GET'])
def tripMetaData():
    return send_file("./logFile.txt")


#delete all videos in the local buffer (and confirm the operation)
@app.route('/AfterTripDeletion',methods=['DELETE'])
def deleteAllVideos():
        try :
                os.system('rm ./videoBuffer/*.*')
                return {'True'}
        except :
                return {'False'}


if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8083)
