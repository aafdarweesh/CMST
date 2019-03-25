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
    req = urllib.request.Request(url='http://StorageIP:8082/RetreiveMission', data=data1, headers={'content-type': 'application/json'}, method='POST')

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

#This request is evoked once the RaspberryPi is on and connected to the internet to update the IP with the server
@app.route('/UpdateIP', methods=['POST'])
def UpdateIP():

    global rPi
    print("anything ")

    rPi.setSerialNumber(request.json['serialNumber'])
    rPi.setIP(request.remote_addr)
    #to check that the stored IP is the IP of the RaspberryPi that we need to evoke
    sendPiMessage()

    return jsonify({'SerialNumber' : rPi.getSerialNumber(), 'IP' : rPi.getIP()})



#Status method is responsible for checking the Synchronization between the RaspberryPi data and the storage "which detection system evoke"
@app.route('/UpdateStatus', methods=['PUT'])
def UpdateStatus():
    #The Json file contains the number of videos generated, a list of sent videos to the detection system, new RaspberryPi IP, and mission ID"
    #The method checks the data with the storage and Detection system, and update the list of the videos
    #the updated list of videos will be sent back to the RaspberryPi, to delete the already received videos
    #incase of a failure the RaspberryPi will manage it according to the scenario 



if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8081)
