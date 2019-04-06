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
import User, DroneConfigurations, Mission, RaspberryPi

import requests

#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

rPi = RaspberryPi.RaspberryPi()


#Mainly to check the feasibility of accessing RaspberryPi after updating the IP
def sendPiMessage():
    global rPi

    #encode the data
    data1 = json.dumps({'HELLO WORLD' :  rPi.getSerialNumber()})
    data1 = data1.encode('ascii') # data should be bytes

    req = urllib.request.Request(url='http://' + rPi.getIP() + ':8082/TestSerialNumber', data=data1, headers={'content-type': 'application/json'}, method='POST')

    with urllib.request.urlopen(req) as f:
        print(f.read().decode("utf-8"))
        pass
    return


#assign the new mission to the RaspberryPi, this method will be invoked upon update on the DB for new mission
def assignMission(serialNumber):
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



@app.route('/RaspberryPiClientTest', methods=['POST'])
def RPiClientTest():

    rPiAddress = open('RPiIPAddress.txt', 'r')
    address = rPiAddress.read()

    url = "http://" + str(address) + ":8083" #url of the RPiClient

    #startMission Request
    data = {'missionID' : '1', 'EstimatedMissionDuration' : '100'}

    print("assignNewMission")
    print(data)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try :
        req = requests.post(url+"/startMission", data=json.dumps(data), headers=headers)

        print("RPiClient startMission status : " + str(req.status_code) + " !!!")
    except :
        print("Couldn't connect to RaspberryPi to start new mission !!!")

    #print(request.data)
    return 'Thank you !!!'


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
    url = 'http://localhost:8082'
    data = {'listOfReceivedVideos' : []}
    try :
        storageData = requests.get(url + "/ListOfReceivedVideos")
        data['listOfReceivedVideos'] = json.loads(storageData.text)['listOfReceivedVideos']
        print("connected to the storage server!!!")
    except :
        print("Couldn't connect to the storage server!!!")
    #print(jsonify(json.dumps(data)))
    return json.dumps(data)


if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8081)
