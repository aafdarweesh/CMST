import requests
from time import sleep
import pickle # to store and retrieve dictionaries from files
import json
import os



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
#This function is responsible for retrieving the mission from the server once it is assigned
def getNewMission():
    url = "http://158.176.132.242:80" #url of the RPiServer
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
    runSystsem(data)

def readMission():
    pickle_in = open("Mission.txt","rb")
    missionData = pickle.load(pickle_in)
    print(missionData)


def runSystsem(data):
    print(data)
    videoDuration = 10
    numberOfVideos = data['EstimatedMissionDuration'] / videoDuration
    os.system('python ./StartRecording.py ' + str(videoDuration) + ' ' + str(numberOfVideos) +
    ' & python ServerTransmission.py ' + str(numberOfVideos))


if __name__ == '__main__':
    getNewMission()
    readMission()
  
