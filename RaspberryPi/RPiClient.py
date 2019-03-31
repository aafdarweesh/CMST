from flask import Flask, jsonify, request, render_template, send_from_directory
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
import schedule

#fixed parameters
videoDuration = 10 #(video duration is 10 sec as it was suitable for 3G transmission rate)
numberOfVideos = 0 #Estimated Number of videos
logFile = open("logFile.txt","w+") #This file contains the system logs
listOfReceivedVideos = [] #This list contians the videos that already received by the detection system



#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#start a mission http request (will run startRecording program, that is responsible for the videos, with the given details)
@app.route('/startMission', methods='POST')
def startMission():
    global videoDuration, numberOfVideos
    try :
        numberOfVideos = ceil(int(request.json['EstimatedMissionDuration'])/videoDuration) #calculate the number of videos depending on the mission duration
    except :
        logFile.write("Couldn't Retreive Mission details (EstimatedMissionDuration)!!!")
    try:
	os.system('pkill -9 ./startRecording.py')
            os.system('python ./startRecording.py ' + str(videoDuration) + ' ' + str(numberOfVideos))
            schedule.every(3).seconds.do(updateStatusWithServer()) #update the status of the system every 3 seconds with the server
            return {'True'}
    except:
            return {'False'}

#return LogFile of the system
@app.route('/logFile')
def tripMetaData():
    return static_file('logFile.txt', root='./')


#delete all videos in the local buffer (and confirm the operation)
@app.route('/AfterTripDeletion')
def deleteAllVideos():
        try :
                os.system('rm ./videoBuffer/*.*')
                return {'True'}
        except :
                return {'False'}



#Mainly for testing
@app.route('/specificVideo')
def specificVideo():
        return static_file('specificVideo.mov', root='./')



#This function returns a list of fully (completed) generated videos
def checkFullyGeneratedVideos():
    #Open the videoMetaData File
    metaDataFile = open('videoMetaData.txt', 'r')
    content = f.readlines()

    resultedList = {}

    global numberOfVideos
    for videoCounter in range(numberOfVideos):

    	#listOfMeta = content.splitlines()
    	for listOfMeta in content:
    		x = listOfMeta.split(' ')
    		if x[0] == str(videoCounter) and x[1] == 'ended':
    			resultedList[str(videoCounter)] = "completed"
                break

    return resultedList

'''
json file format that will be sent to the server to update the status
{
'missionID' : 'missionID',
'serialNumber' : 'serialNumber',
'listOfGeneratedVideos' : {'1' : 'completed', '2' : 'completed', ...},
'logFile' : 'logFile'
}
'''
#This function updates the status of the system with the server and receives a list of received videos by the server
#according to the received list, it will call delete function which will delete the extra videos
#The update the list to be sent to the detection system
#reference : https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests
#reference 2 : https://stackoverflow.com/questions/37825844/how-to-compare-two-dictionaries-to-check-if-a-key-is-present-in-both-of-them?rq=1
def updateStatusWithServer():

    readLogFile = open('logFile.txt', 'r')

    generatedListOfVideos = checkFullyGeneratedVideos()

    url = "" #url of the RPiServer
    data = {'missionID' : 'missionID', 'serialNumber' : 'serialNumber',
    'listOfGeneratedVideos' : generatedListOfVideos,
    'logFile' : readLogFile.read()}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    req = requests.post(url, data=json.dumps(data), headers=headers)

    listOfReceivedVideos = req.content.json['listOfReceivedVideos']

    #send the new videos (or not received videos) to the detection server to be examined
    for x in generatedListOfVideos.keys():
        if x not in listOfReceivedVideos:
            sendVideoToDetection(int(x)) #sends the video to the detection video
        else :
            deleteVideo(x) #deletes the video if it is already received in the server



'''
json file format that will be sent to the detection server
{
'missionID' : 'missionID',
'videoID' : 'videoID',
'videoContent' : 'videoContent'
}
'''

#reference : https://stackoverflow.com/questions/45623885/how-to-convert-an-mp4-to-a-text-file-and-back
#reference 2 : https://docs.python.org/2/library/uu.html
#Encode the video into txt file and send the content of the encoded video back as a string
def videoIntoString(videoNumber):
    uu.encode('./videoBuffer/video' + str(videoNumber) + '.h264', './videoBuffer/videoTemp.txt')
    f = open('./videoBuffer/videoTemp.txt','r')
    #Log the step into the logFile
    logFile.write("Converted the videoNumber : " + str(videoNumber) + " into txtfile.")

    return f.read()


#reference : https://stackoverflow.com/questions/9733638/post-json-using-python-requests
#This function is responsible for sending the completed videos periodically to the detection server
def sendVideoToDetection(videoNumber):

    url = "" #url of the detection server
    data = {'missionID' : 'missionID', 'videoID' : 'videoID', 'videoContent' : videoIntoString(videoNumber)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    req = requests.post(url, data=json.dumps(data), headers=headers)

    #according to some sources : req.status_codes
    logFile.write("The result of sending videoNumber : " + str(videoNumber) + " to the detection server : " + str(req.status))


#This function will delete the already sent videos from the videoBuffer folder
def deleteVideo(videoNumber):
        try :
                if os.path.exists('./videoBuffer/video' + str(videoNumber) + '.h264') == True:
                    os.system('rm ./videoBuffer/video' + str(videoNumber) + '.h264')

                    if os.path.exists('./videoBuffer/video' + str(videoNumber) + '.h264') == True:
                            logFile.write("Couldn't delete videoNumber : " + str(videoNumber) + " although it does exist")
                    else :
                        logFile.write("videoNumber : " + str(videoNumber) + " is DELETED!!!")
        except :
                logFile.write("Couldn't delete videoNumber : " + str(videoNumber) + " due to exception")


if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8083)
