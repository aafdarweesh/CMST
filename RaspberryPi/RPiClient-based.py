import requests
from time import sleep
import pickle # to store and retrieve dictionaries from files
import json
import os





serialNumber = os.popen('cat /proc/cpuinfo | grep Serial | cut -d \' \' -f 2').read()
serialNumber = serialNumber.split('\n')[0]
print('Serial Number of the Pi is : ' + serialNumber)
                   
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
    data = {"serialNumber": serialNumber}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    flag = False
    while flag == False:
        sleep(1) #sleep for 3 sec and send another request to the server, asking for the mission

        try:
            req = requests.post(url+"/readNewMission", data=json.dumps(data), headers=headers)
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
            print("Couldn't connect to RPiServer to get the new Mission !!! OR no New Mission Assigned!!!")
    
    runSystsem(data)
    
    
    
def runSystsem(data):
    print(data)
    videoDuration = 10 #video duration in sec
    numberOfVideos = data['NumberOfVideos']
    os.system('python ./StartRecording.py ' + str(videoDuration) + ' ' + str(numberOfVideos) +
    ' & python ServerTransmission.py '  + str(data['missionID']) + ' ' + str(numberOfVideos) + ' & python ConfirmReceivingMission.py')


if __name__ == '__main__':
    getNewMission()
    
  
