import requests
from time import sleep
import pickle # to store and retrieve dictionaries from files
import json
import os


#This function will invoke the detection and classification systems on the server
def confirmReceivingMission(data):
    url = "http://158.176.132.242:5000" #url of the RPiServer
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        req = requests.post(url + "/confirmReceivingMission", data=json.dumps(data), headers=headers)
        print('Receiving mission is confirmed')
    except:
        print('Error Connecting to the server to confirm receiving the mission')


def readMission():
    pickle_in = open("Mission.txt","rb")
    missionData = pickle.load(pickle_in)
    print(missionData)
    return missionData
    
    
x = False #flag
data = {}
while x != True:
  sleep(1)
  try:
    data = readMission()
    x = data['newMissionFlag']
  except:
    print("Problem in reading new mission")

confirmReceivingMission(data)
