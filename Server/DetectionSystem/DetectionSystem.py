from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import os
import urllib
from time import sleep
import glob
import json
import sys

import requests
import uu

import pickle

import subprocess

import mysql.connector

from datetime import datetime 

from shutil import copyfile


#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



MAIN_DIRECTORY = 'C:\\CMSTData'

'''
json file format that will be sent to the detection server
#incase having GPS module
{
'missionID' : 'missionID',
'videoID' : 'videoID',
'videoContent' : 'videoContent',
'startingTime' : 'startingTime',
'location' : {'lat': 35.24797179165725, 'lng': 33.022986722853716}
}

#if no GPS module
{
"missionID" : "missionID",
"videoID" : "videoID",
"videoContent" : "videoContent",

}
'''


#This function receives the video from the RaspberryPi Client
#This function will be moved to the detection system
@app.route('/ReceiveVideo', methods = ['POST'])
def ReceiveVideo():
	global MAIN_DIRECTORY
	videoName = ''
    #videoName += str(request.json['missionID'])
	videoName += str(request.json['videoID'])
	
	print("Before the video content conversion")
	receivedEncodedVideo = open(MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + "\\ReceivedData\\videoTemp.txt", 'w')
	receivedEncodedVideo.write(request.json['videoContent'])

	try:
		#Decode the encoded video back to the same format
		uu.decode(MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + "\\ReceivedData\\videoTemp.txt", MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + "\\ReceivedData\\" + videoName + ".mp4")
		print('After decoding the video')
	except:
		print('Invaid format for video decoding')
		return jsonify("Invalid format for decoding!")
		 
	try:
		#sleep(3) #as the decoding is working independent, this delay is to copy after the decoding process
		uiVideoLocation = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(request.json['missionID']) + '\\' + 'ReceivedData\\' + str(request.json['videoID']) + '.mp4'
		copyfile(MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + "\\ReceivedData\\" + videoName + ".mp4", uiVideoLocation)
		
	except Exception as e:
		print('Failed copying the file into the UI directory')
		print (str(e))
		
	#Read from the mission the received videos 
	itemlist = []
	try :
		with open (MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + '\\ReceivedDataMetaData.txt', 'rb') as fp:
			itemlist = pickle.load(fp)
			data['listOfReceivedVideos'] = itemlist
	except:
		print("Nothing in the file")
			
	#write in the file that the video is received
	itemlist.append(request.json['videoID'])
	with open(MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + '\\ReceivedDataMetaData.txt', 'wb') as fp:
		pickle.dump(itemlist, fp)
	
	
	
	#print(videoName)
	
	#get the location of the video
	newpath = MAIN_DIRECTORY + '\\' + str(request.json['missionID'])
	lat = 0.0
	lng = 0.0
	with open(newpath + '\\Missions.txt') as json_file:
		newMission = json.load(json_file)
		#print(newMission)
		lat = newMission['flightConfigurations']['videoLocations'][int(request.json['videoID'])]['lat']
		lng = newMission['flightConfigurations']['videoLocations'][int(request.json['videoID'])]['lng']
	
	#Update the database 
	#Data related to the video : (videoURL, missionID, startingTime, location) "starting time, relative to the mission starting time, assuming video duration is 10sec"
	#INSERT INTO `detection`.`video` (`videoUrl`, `missionID`, `latitude`, `longitude`, `startingTime`) VALUES ('resources/videos/video3.mp4', '1', '35.334666', '33.493127', '30');
	#Connect to the database
	mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="detection")

	mycursor = mydb.cursor()

	sql = 'INSERT INTO detection.video (videoUrl, missionID, latitude, longitude, startingTime) VALUES ('
	sql += '\''  + str('./CMSTData' + '/' + str(request.json['missionID']) + "/ReceivedData/" + videoName +'.mp4')
	sql += '\',\'' + str(request.json['missionID']) + '\', ' + str(lat) + ',' + str(lng) + ',' + str(int(videoName)*5) +')'
		
	mycursor.execute(sql)
	mydb.commit()
	
	return jsonify("Received!")

'''
received Mission json (height in m, speed in m/s, videoDuration is 10s)
{
"newMissionFlag" : true,
"missionID" : 0,
"serialNumber" : 123,
"NumberOfVideos":90,
"flightConfigurations":{"height" : 10, "speed" : 1, "locations":[]}
}
'''
@app.route('/confirmReceivingMission', methods=['Post'])
#The pi confirms that it received the mission with the starting timestamp
#reference 1 : https://stackoverflow.com/questions/546017/how-do-i-run-another-script-in-python-without-waiting-for-it-to-finish
#reference 2 : https://docs.python.org/3/library/subprocess.html
#refernece 3 : https://stackoverflow.com/questions/34046634/insert-into-a-mysql-database-timestamp
def confirmReceivingMission():
	#Connect to the database
	mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="detection")

	mycursor = mydb.cursor()
	
	#Update the status of the mission to running
	#UPDATE `detection`.`mission` SET `startingTimeStamp`='2019-08-20 15:21:15', `state`='1' WHERE `missionID`='5';
	sql = 'UPDATE detection.mission SET startingTimeStamp = \' ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
	sql += '\', state = \'1\' WHERE missionID=' + str(request.json['missionID']) + ';'
	mycursor.execute(sql)
	mydb.commit()

	try:
		
		#if pi received the mission (start the communication with the detection system and classification system)
		#communication system parameters (missionID, drone_height, drone_speed, number_of_videos)
		runningCommand = 'python ./CommunicationWithDetectionClassificationStorage.py ' + str(request.json['missionID'])
		runningCommand += ' ' + str(request.json['flightConfigurations']['height'])
		runningCommand += ' ' + str(request.json['flightConfigurations']['speed'])
		runningCommand += ' ' + str(request.json['NumberOfVideos'])
		#run pipLine fir that program (the communication with the detection and classification systems)
		#p = subprocess.Popen([sys.executable, runningCommand], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		os.system(runningCommand)
		
		#Update the status of the mission to running
		#UPDATE `detection`.`mission` SET `startingTimeStamp`='2019-08-20 15:21:15', `state`='1' WHERE `missionID`='5';
		sql = 'UPDATE detection.mission SET endingTimeStamp = \' ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
		sql += '\' , state = \'2\' WHERE missionID = ' + str(request.json['missionID']) + ';'
		mycursor.execute(sql)
		mydb.commit()
		
		return('True')
	except:
		return('False')

	
	


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)
