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



@app.route('/UpdateIP', methods=['POST'])
def UpdateIP():

    global rPi
    print("anything ")

    rPi.setSerialNumber(request.json['serialNumber'])
    rPi.setIP(request.remote_addr)

    sendPiMessage()

    return jsonify({'SerialNumber' : rPi.getSerialNumber(), 'IP' : rPi.getIP()})

if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8081)
