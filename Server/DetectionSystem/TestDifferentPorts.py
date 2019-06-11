from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import os

#Initialize the server "as flask object"
app = Flask(__name__)
#CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8083)

#ports available : 80, 8000, 3000, 8082, 8083 (I guess only few that are reserved for something else)
