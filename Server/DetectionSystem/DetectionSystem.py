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

import pickle

import subprocess

import mysql.connector

from datetime import datetime 



#Common Class that are going to be used
import User, DroneConfigurations, Mission, RaspberryPi

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

    #Decode the encoded video back to the same format
	uu.decode(MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + "\\ReceivedData\\videoTemp.txt", MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + "\\ReceivedData\\" + videoName + ".mp4")

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
	sql += '\''  + str('C:/CMSTData' + '/' + str(request.json['missionID']) + "/ReceivedData/" + videoName +'.mp4,')
	sql += '\',\'' + str(request.json['missionID']) + '\', ' + str(lat) + ',' + str(lng) + ',' + str(int(videoName)*10) +')'
	
	mycursor.execute(sql)
	mydb.commit()
	
	return jsonify("Received!")


#This request is evoked once the RaspberryPi is on and connected to the internet to update the IP with the server
@app.route('/UpdateIP', methods=['POST'])
def UpdateIP():

    global rPi
    print("anything ")

    rPi.setSerialNumber(request.json['serialNumber'])
    rPi.setIP(request.remote_addr)
    #to check that the stored IP is the IP of the RaspberryPi that we need to evoke
    #sendPiMessage()

    rPiAddress = open('RPiIPAddress.txt', 'w')
    rPiAddress.write(request.remote_addr)


    return jsonify({'SerialNumber' : rPi.getSerialNumber(), 'IP' : rPi.getIP()})


'''
json file format that will be sent to the server to update the status
{
'missionID' : 'missionID',
'serialNumber' : 'serialNumber',
'listOfGeneratedVideos' : {'1' : 'completed', '2' : 'completed', ...},
'logFile' : 'logFile'
}
'''
#Status method is responsible for checking the Synchronization between the RaspberryPi data and the storage "which detection system evoke"
@app.route('/UpdateStatus', methods=['POST'])
def UpdateStatus():
    #The Json file contains the number of videos generated, a list of sent videos to the detection system, new RaspberryPi IP, and mission ID"
    #The method checks the data with the storage and Detection system, and update the list of the videos
    #the updated list of videos will be sent back to the RaspberryPi, to delete the already received videos
    #incase of a failure the RaspberryPi will manage it according to the scenario


    print("received data from RPiClient IP : " + str(request.remote_addr) + " : ")
    print(request.json)
    url = 'http://localhost:8082' #Detection system IP
    data = {'listOfReceivedVideos' : []}
    try :
        with open (MAIN_DIRECTORY + '\\' + str(request.json['missionID']) + '\\ReceivedDataMetaData.txt', 'rb') as fp:
            itemlist = pickle.load(fp)
            data['listOfReceivedVideos'] = itemlist
    except:
            print("Nothing in the file")
	#directory = os.listdir("./ReceivedData")
	#data['listOfReceivedVideos'] = directory

	#for filename in directory:
	#	data['listOfReceivedVideos'].append(int(filter(lambda x: x.isdigit(), filename)[0]))
    '''
	try :
        storageData = requests.get(url + "/ListOfReceivedVideos")
        data['listOfReceivedVideos'] = json.loads(storageData.text)['listOfReceivedVideos']
        print("connected to the storage server!!!")
    except :
        print("Couldn't connect to the storage server!!!")
    #print(jsonify(json.dumps(data)))
	'''
    return json.dumps(data)



'''
new Mission json (height in m, speed in m/s, videoDuration is 10s)
{
"newMissionFlag" : true,
"missionID" : 0,
"serialNumber" : 123,
"NumberOfVideos":90,
"flightConfigurations":{"height" : 10, "speed" : 1, "locations":[]}
}
'''
#reference 1 : https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
#reference 2 : https://www.w3schools.com/python/python_mysql_insert.asp
@app.route('/assignNewMission', methods=['POST'])
#assign the new mission to the RaspberryPi, this method will be invoked upon update on the DB for new mission
def assignMission():

	#Connect to the database
	mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="detection")

	mycursor = mydb.cursor()

	#insert locations list 
	lengthOfLocation = len(request.json['flightConfigurations']['locations'])

	sql = "INSERT INTO detection.path (pathID, areaID, numberOfSteps) VALUES (NULL, 1," + str(lengthOfLocation) + ");"
	mycursor.execute(sql)
	mydb.commit()


	pathID = 0
	#get the path id 
	sql = "SELECT * FROM path ORDER BY pathID DESC"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()


	pathID = myresult[0][0]
	#print('Locations pathID is : ' + str(pathID))
	
	
	#insert the locations into the database 
	for i in range(len(request.json['flightConfigurations']['locations'])):
		sql = "INSERT INTO detection.pathsteps (pathID, stepNumber, latitude, longitude) VALUES (" 
		sql += str(pathID) + ", " + str(i+1) + ", " + str(request.json['flightConfigurations']['locations'][i]['lat']) 
		sql += ", " + str(request.json['flightConfigurations']['locations'][i]['lng'])  + ");"
		
		mycursor.execute(sql)
		mydb.commit()

	#insert the new mission to the database
	sql = "INSERT INTO mission (missionID, username, droneID, pathID, length, numberOfVideos, state) VALUES "
	sql += "(NULL, \'tommy\', \'" + str(request.json['serialNumber']) + "\', " + str(pathID) + ", 10, " 
	sql += str(len(request.json['flightConfigurations']['videoLocations'])) + ", 0);"
	print(sql)
	mycursor.execute(sql)
	mydb.commit()

	#print(mycursor.rowcount, "record inserted.")

	#get the mission id 
	sql = "SELECT * FROM mission ORDER BY missionID DESC"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	missionID = myresult[0][0]
	
	data = request.json
	data['missionID'] = missionID
	
	#create new Directory for the mission
	newpath = MAIN_DIRECTORY + '\\' + str(data['missionID'])
	if not os.path.exists(newpath):
		os.makedirs(newpath) #create the new mission directory (will store all data related to the mission there (images, videos, some meta files)
		os.makedirs(newpath + '\\ReceivedData') #This directory will be used to store the received videos

		with open(newpath + '\\ReceivedDataMetaData.txt', 'w'):
			pass

	with open(newpath + '\\Missions.txt', 'w') as outfile:
		print (data)
		json.dump(data, outfile)
	return jsonify(data)

    #get the new mission details from the storage for the given RaspberryPi
	'''
	req = urllib.request.Request(url='http://StorageIP:8082/RetrieveMission', data=data1, headers={'content-type': 'application/json'}, method='POST')

	with urllib.request.urlopen(req) as f:
	print(f.read().decode("utf-8"))
	pass
	'''
	#newMission = data received from the StorageIP
	#rPi = data received from the StorageIP


	#encode the data
	#uncomment if we are using VPN to connect with the Pi
	'''
	newMission = newMission.encode('ascii') # data should be bytes

	req = urllib.request.Request(url='http://' + rPi.getIP() + ':8000/NewMission', data=data1, headers={'content-type': 'application/json'}, method='POST')
	res = ''
	with urllib.request.urlopen(req) as f:
	res = f.read().decode("utf-8")
	pass


	if res == 'Valid Operation':
	return 'Valid Operation'
	else :
	return res

	'''

	
	

	


'''
new Mission json (height in m, speed in m/s, videoDuration is 10s)
{
"newMissionFlag" : true,
"missionID" : 0,
"serialNumber" : 123,
"NumberOfVideos":90,
"flightConfigurations":{"height" : 10, "speed" : 1, "locations":[]}
}
'''
#reference 1 : https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
#reference 2 : https://stackoverflow.com/questions/1274405/how-to-create-new-folder
@app.route('/readNewMission', methods=['Post'])
def readNewMission():

	#trying to fetch the mission data from the database
	try:

		#Connect to the database
		mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="detection")

		mycursor = mydb.cursor()


		#get the mission id 
		sql = "SELECT * FROM mission WHERE droneID = \'" + str(request.json['serialNumber']) + "\' ORDER BY missionID ASC"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		missionID = myresult[0][0]
		
		newpath = MAIN_DIRECTORY + '\\' + str(missionID)
		with open(newpath + '\\Missions.txt') as json_file:
			newMission = json.load(json_file)
		
			return jsonify(newMission)
			
		return 'Couldn\'t find mission file'
	except:
			return 'Couldn\'t connect to the DB new mission'
	
	#collect the mission from the database

	'''

	global MAIN_DIRECTORY
	with open('Missions.txt') as json_file:
		newMission = json.load(json_file)

		#create new Directory for the mission
		newpath = MAIN_DIRECTORY + '\\' + str(newMission['missionID'])
		if not os.path.exists(newpath):
				os.makedirs(newpath) #create the new mission directory (will store all data related to the mission there (images, videos, some meta files)
				os.makedirs(newpath + '\\ReceivedData') #This directory will be used to store the received videos

				with open(newpath + '\\ReceivedDataMetaData.txt', 'w'):
						pass

		return jsonify(newMission)
	'''
	

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
