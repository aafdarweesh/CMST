from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import os
import urllib
from time import sleep
import glob
import json
import sys
sys.path.append('../Common/')

#Common Class that are going to be used
import User, DroneConfigurations, Mission

#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

'''
Mission details Json content

{
	"UserID" : "1",
	"DronePath" : {"a":"a", "b":"b"},
	"DroneSpeed": "3",
	"DroneHeight" : "10",
	"MissinoStartTime" : "2019-03-20 23:05:24.310928'"

}
'''

@app.route('/assignNewMission', methods=['POST'])
def assignNewMission():

	#from the database get the value of the mission ID
	#missionID not from the user
	missionID = 0

	#user details
	user = User.User(int(request.json["UserID"]))
	#user.setName(request.json['UserName'])
	#user.setSurname(request.json['UserSurname'])

	#drone details
	drone = DroneConfigurations.DroneConfigurations()
	drone.setPath(request.json['DronePath'])
	drone.setSpeed(int(request.json['DroneSpeed']))
	drone.setHeight(int(request.json['DroneHeight']))

	#newMission details
	mission = Mission.Mission(drone, user, missionID)
	mission.setMissionStartTime(request.json['MissinoStartTime'])

	return jsonify({'Mission start time' : mission.getMissionStartTime()})


#request Data methods should be implmemnted according the DB interface, as it will return just the values to the user


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
