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


#Common Class that are going to be used
import User, DroneConfigurations, Mission, RaspberryPi

#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



MAIN_DIRECTORY = 'C:\\CMSTData'

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
    uu.decode("./ReceivedData/videoTemp.txt", "./ReceivedData/" + videoName + ".mp4")

    itemlist = []
    try :
        with open ('ReceivedDataMetaData.txt', 'rb') as fp:
            itemlist = pickle.load(fp)
            data['listOfReceivedVideos'] = itemlist
    except:
            print("Nothing in the file")
			
    itemlist.append(request.json['videoID'])
    with open('ReceivedDataMetaData.txt', 'wb') as fp:
        pickle.dump(itemlist, fp)

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
        with open ('ReceivedDataMetaData.txt', 'rb') as fp:
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
new Mission json
{
"newMissionFlag" : true,
"missionID" : 0,
"serialNumber" : 123,
"EstimatedMissionDuration":100,
"flightConfigurations":{"height" : 10, "locations":[]}
}
'''
#reference : https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
@app.route('/assignNewMission', methods=['POST'])
#assign the new mission to the RaspberryPi, this method will be invoked upon update on the DB for new mission
def assignMission():
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
    with open('Missions.txt', 'w') as outfile:
        print (request.json)
        json.dump(request.json, outfile)
    return jsonify(request.json)

'''
new Mission json
{
"newMissionFlag" : true,
"missionID" : 0,
"EstimatedMissionDuration":100,
"flightConfigurations":{"height" : 10, "locations":[]}
}
'''
#reference : https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
@app.route('/readNewMission', methods=['Get'])
def readNewMission():

    with open('Missions.txt') as json_file:
        newMission = json.load(json_file)

    return jsonify(newMission)




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=80)
