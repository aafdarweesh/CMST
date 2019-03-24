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


app.route('/UpdateIP', methods=['POST'])
def UpdateIP():

    global rPi

    rPi.setSerialNumber(request.json['serialNumber'])
    rPi.setIP(request.remote_addr)

    return jsonify({'SerialNumber' : rPi.getSerialNumber, 'IP' : rPi.getIP()})

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8081)
