from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import os
import urllib
from time import sleep
import glob
#Common Class that are going to be used
from Common import User, DroneConfigurations, Mission


app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})




@app.route('/missionDetails', methods=['POST'])
def main():
	#user details
	user = User(request.json['UserID'])
	#user.setName(request.json['UserName'])
	#user.setSurname(request.json['UserSurname'])

	#drone details
	drone = DroneConfigurations()
	drone.setPath(request.json['DronePath'])
	drone.setSpeed(request.json['DroneSpeed'])
	drone.setHeight(request.json['DroneHeight'])

	#newMission details
	mission = Mission(drone, user)
	mission.setMissionStartTime(request.json['MissinoStartTime'])

	print("Print the user details, drone details, and finally mission details")
	print(user)
	print(drone)
	print(mission)

	return






@app.route('/tripDetails', methods=['GET'])
@cross_origin()
def tripDetails():
	global videoDuration, tripDuration
	return jsonify({'videoDuration' : str(videoDuration), 'tripDuration' : str(tripDuration)})

@app.route('/startTrip', methods=['POST', 'OPTION'])
@cross_origin()
def startTrip():

	print("\n\n\n\n" + str(request.json) + "\n\n\n\n")
	#trip = {'tripDuration' : request.json['tripDuration'], 'videoDuration' : request.json['videoDuration']}
	global videoDuration, tripDuration, missionOnTheRun
	videoDuration = int(request.json['videoDuration'])#int(request.form['videoDuration'])#
	tripDuration = int(request.json['tripDuration'])#int(request.form['tripDuration'])#


	if videoDuration == 0 or tripDuration == 0:
		print("Error in the input")
		return jsonify('ERROR')
	numberOfVideos = tripDuration//videoDuration
	#send start mission request to the Pi
	print("Connected to the server with POST request")
	startRequest = 'False'
	try:
		startRequest = urllib.request.urlopen("http://192.168.43.147:1234/startMission/" + str(videoDuration) + "/" + str(numberOfVideos))
		os.system('rm ./videoBuffer/*.*')
	except:
		startRequest = 'False'



	if startRequest != 'False' :
		print("Connected to the PI")
		videoCounter = 0
		missionStarted = True
		missionOnTheRun = True
		while missionStarted == True:
			checkVideoStored = False
			while checkVideoStored == False:
				urllib.request.urlretrieve("http://192.168.43.147:1234/tripMetaData", "tripMetaData.txt")
				#read file and check that video is fulle received

				f = open('tripMetaData.txt', 'r')
				content = f.readlines()

				#listOfMeta = content.splitlines()
				for listOfMeta in content:
					x = listOfMeta.split(' ')
					if x[0] == str(videoCounter) and x[1] == 'ended':
						checkVideoStored = True
				if checkVideoStored == False : #wait a bit
					sleep(1)

			#retrieve the video from the PI
			try:
				urllib.request.urlretrieve("http://192.168.43.147:1234/video/" + str(videoCounter), "./videoBuffer/video" + str(videoCounter) + ".h264")
				videoCounter += 1 #next video
			except :
				print("Couldn't retrieve the data from Raspberry pi")
			#delete video
			if videoCounter != 0:
				try :
					urllib.request.urlretrieve("http://192.168.43.147:1234/deleteVideo/" + str(videoCounter-1),"")
					print("The file was deleted")
				except :
					print("Couldn't delete the file")



			sleep(1)

			#Finish the mission
			if videoCounter == numberOfVideos:
				missionStarted = False

		#Assure that all files (videos) on Raspberry pi were successfully deleted
		try :
			urllib.request.urlretrieve("http://192.168.43.147:1234/AfterTripDeletion","")
			print("All videos were deleted from Raspberry pi")
		except :
			print("Couldn't delete all videos from Raspberry pi")



	else :
		print("Couln't Connect to the PI")

	missionOnTheRun = False #the mission is finished
	return jsonify({'videoDuration' : str(videoDuration), 'tripDuration' : str(tripDuration)})


#Check if there is a mission or not running
@app.route('/missionIsRunning', methods=['GET'])
@cross_origin()
def checkMissionIsRunning():
	global missionOnTheRun, videoDuration, tripDuration

	if videoDuration == 0 or tripDuration == 0 :
		return jsonify('No mission records')

	files = []
	for file in glob.glob("./results/*.*"):
	    files.append(file)

	filesReceived = []
	for file in glob.glob("./videoBuffer/*.*"):
	    filesReceived.append(file)
	if missionOnTheRun == True:
		return jsonify('(Detected : ' + str(len(files)) + ', ' + str(100*len(filesReceived)/(tripDuration//videoDuration)) + '%) \nRUNNING ... ')
	else :
		return jsonify('(Detected : ' + str(len(files)) + ', ' + str(100*len(filesReceived)/(tripDuration//videoDuration)) + '%) \nCOMPLETED !')

#Return the list of detected turtles if any
@app.route('/resultList', methods=['GET'])
@cross_origin()
def resultList():
	files = []
	for file in glob.glob("./results/*.*"):
	    files.append('http://192.168.43.175:8080/uploads/' + file[10:])
	   # files.append('..' + os.path.join(app.config['UPLOAD_FOLDER'], file[1:]))
	#print(jsonify('http://127.0.0.1:8080/uploads/' + files[0]))
	return jsonify(files)#jsonify('http://127.0.0.1:8080/uploads/' + files[0])#render_template('resultDisplay.html', result = files)#jsonify(files)

UPLOAD_FOLDER = '/home/hogo/Desktop/Graduation/HttpFileTransfer/Version3/TestReact2/results/'
#send the image back as a response to the request
@app.route('/uploads/<filename>', methods = ['GET'])
@cross_origin()
def send_file(filename):
    #print(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)



if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
