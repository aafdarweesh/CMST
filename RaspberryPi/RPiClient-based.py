import requests
from time import sleep
import pickle # to store and retrieve dictionaries from files
import json
import os



'''
new Mission json (height in m, speed in m/s, videoDuration is 10s)
{
"newMissionFlag" : true,
"missionID" : 0,
"serialNumber" : 123,
"NumberOfVideos":90,
"flightConfigurations":{"height" : 10, "speed" : 1, "locations":[]}
}
'''
#This function is responsible for retrieving the mission from the server once it is assigned
def getNewMission():
    url = "http://158.176.132.242:5000" #url of the RPiServer
    #getMission Request
    data = {}
    flag = False
    while flag == False:
        sleep(1) #sleep for 3 sec and send another request to the server, asking for the mission

        try:
          req = requests.get(url+"/readNewMission")
          print("After the request")
          print(req.json())
          flag = req.json()['newMissionFlag']
          print(flag)
          data = req.json()
          pickle_out = open("Mission.txt","wb")
          pickle.dump(req.json(), pickle_out)
          pickle_out.close()
          '''
          with open('Mission.txt', 'w') as outfile:
              print (req.json())
              pickle.dump(req.json(), outfile)
          '''
          print("RPiClient get the new Mission : " + str(req.status_code) + " !!!")
        except Exception as e:
            print (str(e))
            print("Couldn't connect to RPiServer to get the new Mission !!!")
    confirmReceivingMission(data)
    runSystsem(data)

def readMission():
    pickle_in = open("Mission.txt","rb")
    missionData = pickle.load(pickle_in)
    print(missionData)

    
def confirmReceivingMission(data):
    url = "http://158.176.132.242:5000" #url of the RPiServer
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        req = requests.post(url + "/confirmReceivingMission", data=json.dumps(data), headers=headers)
        print('Receiving mission is confirmed')
    except:
        print('Error Connecting to the server to confirm receiving the mission')

def runSystsem(data):
    print(data)
    videoDuration = 10 #video duration in sec
    numberOfVideos = data['NumberOfVideos']
    os.system('python ./StartRecording.py ' + str(videoDuration) + ' ' + str(numberOfVideos) +
    ' & python ServerTransmission.py '  + str(data['missionID']) + ' ' + str(numberOfVideos))


if __name__ == '__main__':
    getNewMission()
    readMission()
  
