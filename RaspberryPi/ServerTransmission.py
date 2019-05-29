from time import sleep
import sys
import json
import uu #to encode and decode the video into string (or base64)
import requests #for the HTTP requests
# Schedule Library imported
import schedule #pip install schedule
import os



numberOfVideos = int(sys.argv[1])
logFile = open("logFile.txt","w") #This file contains the system logs


#This function returns a list of fully (completed) generated videos
def checkFullyGeneratedVideos():
    print("Inside checkFullyGeneratedVideos!!!")
    #Open the videoMetaData File
    metaDataFile = open('./videoMetaData.txt', 'r')
    content = metaDataFile.readlines()

    resultedList = {}

    global numberOfVideos
    for videoCounter in range(numberOfVideos):
        print("Check Video Number : " + str(videoCounter))

        #listOfMeta = content.splitlines()
        for listOfMeta in content:
            x = listOfMeta.split(' ')
            if x[0] == str(videoCounter) and x[1] == 'ended':
                resultedList[str(videoCounter)] = "completed"
                break
    print("Resulted List :")
    print(resultedList)
    return resultedList

'''
json file format that will be sent to the server to update the status
{
'missionID' : 'missionID',
'serialNumber' : 'serialNumber',
'listOfGeneratedVideos' : {'1' : 'completed', '2' : 'completed', ...},
'logFile' : 'logFile'
}
'''
#This function updates the status of the system with the server and receives a list of received videos by the server
#according to the received list, it will call delete function which will delete the extra videos
#The update the list to be sent to the detection system
#reference 1 : https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests
#reference 2 : https://stackoverflow.com/questions/37825844/how-to-compare-two-dictionaries-to-check-if-a-key-is-present-in-both-of-them?rq=1
#reference 3 : https://pythonspot.com/json-encoding-and-decoding-with-python/
def updateStatusWithServer():
    print("Inside updateStatusWithServer!!!")
    listOfReceivedVideos = []
    while (len(listOfReceivedVideos) != numberOfVideos):
        print("While loop!")
        readLogFile = open('logFile.txt', 'r')

        generatedListOfVideos = checkFullyGeneratedVideos()

        url = "http://localhost:8081" #url of the RPiServer
        data = {'missionID' : 'missionID', 'serialNumber' : 'serialNumber',
        'listOfGeneratedVideos' : generatedListOfVideos,
        'logFile' : readLogFile.read()}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try :
            req = requests.post(url + "/UpdateStatus", data=json.dumps(data), headers=headers)

            print("Request Content : ")
            print(req.text)
            #print(dict(req.content))
            listOfReceivedVideos = json.loads(req.text)['listOfReceivedVideos']
            print("listOfReceivedVideos : ")
            print(listOfReceivedVideos)

            print("Update Status With the server RaspberryPi : ")
            print(generatedListOfVideos.keys())

            #send the new videos (or not received videos) to the detection server to be examined
            for x in generatedListOfVideos.keys():
                if x not in listOfReceivedVideos:
                    convertFormatH264IntoMP4(int(x)) #conver the video format into mp4
                    sendVideoToDetection(int(x)) #sends the video to the detection video
                else :
                    deleteVideo(x) #deletes the video if it is already received in the server
        except :
            print("Couldn't Connect to the Server!!!")
        sleep(5) #sleep for 5 sec




#This function changes the format of the video from .h264 to mp4 (so it is better for the server)
def convertFormatH264IntoMP4(videoNumber):
    os.system('MP4Box -fps 30 -add video' + str(videoNumber) + '.h264 video' + str(videoNumber) + '.mp4  ')
    os.system('rm video' + str(videoNumber) + '.h264')


#reference : https://stackoverflow.com/questions/45623885/how-to-convert-an-mp4-to-a-text-file-and-back
#reference 2 : https://docs.python.org/2/library/uu.html
#Encode the video into txt file and send the content of the encoded video back as a string
def videoIntoString(videoNumber):
    print("Inside Video into String function!")
    uu.encode('./videoBuffer/video' + str(videoNumber) + '.mp4', './videoBuffer/videoTemp.txt')
    f = open('./videoBuffer/videoTemp.txt','r')
    #Log the step into the logFile
    #logFile.write("Converted the videoNumber : " + str(videoNumber) + " into txtfile.")

    return f.read()

'''
json file format that will be sent to the detection server
{
'missionID' : 'missionID',
'videoID' : 'videoID',
'videoContent' : 'videoContent'
}
'''
#reference : https://stackoverflow.com/questions/9733638/post-json-using-python-requests
#This function is responsible for sending the completed videos periodically to the detection server
def sendVideoToDetection(videoNumber):
    global logFile
    print("Inside Send video to Detection System function!")

    url = "http://158.176.132.242:8082/ReceiveVideo" #url of the detection server
    data = {'missionID' : 'missionID', 'videoID' : str(videoNumber), 'videoContent' : str(videoIntoString(videoNumber))}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try :
        req = requests.post(url, data=json.dumps(data), headers=headers)

        print("The result of sending videoNumber : " + str(videoNumber) + " to the detection server : " + str(req.status_code))
    except :
        print("Couldn't connect to the detection server!!!")
    #according to some sources : req.status_codes
    #logFile.write("The result of sending videoNumber : " + str(videoNumber) + " to the detection server : " + str(req.status))


#This function will delete the already sent videos from the videoBuffer folder
def deleteVideo(videoNumber):
        try :
                if os.path.exists('./videoBuffer/video' + str(videoNumber) + '.mp4') == True:
                    os.system('rm ./videoBuffer/video' + str(videoNumber) + '.mp4')

                    if os.path.exists('./videoBuffer/video' + str(videoNumber) + '.mp4') == True:
                            logFile.write("Couldn't delete videoNumber : " + str(videoNumber) + " although it does exist")
                    else :
                        logFile.write("videoNumber : " + str(videoNumber) + " is DELETED!!!")
        except :
                logFile.write("Couldn't delete videoNumber : " + str(videoNumber) + " due to exception")

#Run the transmission program
updateStatusWithServer()
