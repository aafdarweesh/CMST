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


@app.route('/TestSerialNumber', methods=['POST'])
def TestSerialNumber():
    print(request.data)
    return 'Thank you !!!'

if __name__ == '__main__':
	app.run(host='localhost', debug=True, port=8082)
