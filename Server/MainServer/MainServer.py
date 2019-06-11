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
    #the updated list of videos will be sent back to the RaspberryPi, to delete the already received videos
    #incase of a failure the RaspberryPi will manage it according to the scenario


    print("received data from RPiClient IP : " + str(request.remote_addr) + " : ")
    print(request.json)
	
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
	sql += "(NULL, \'tommy\', \'" + str(request.json['serialNumber']) + "\', " + str(pathID) + ", 5, " 
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

	#create new Directory for the mission in the UI
	newpathUI = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(data['missionID'])
	if not os.path.exists(newpathUI):
		os.makedirs(newpathUI) #create the new mission directory (will store all data related to the mission there (images, videos, some meta files)
		os.makedirs(newpathUI + '\\ReceivedData') #This directory will be used to store the received videos
		os.makedirs(newpathUI + '\\DetectionFolder')

	
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
	print(request.json)
	#trying to fetch the mission data from the database
	try:

		#Connect to the database
		mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="detection")

		mycursor = mydb.cursor()

		#Main RaspberryPi serialNumber : request.json['serialNumber'] , '000000003762bf30'

		#get the mission id 
		sql = "SELECT * FROM mission WHERE droneID = \'" + str(request.json['serialNumber']) + "\' AND state=0 ORDER BY missionID DESC"
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
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)
