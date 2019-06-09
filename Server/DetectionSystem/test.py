import os


#newpath = r'C:\Users\Administrator\Desktop\CMSTControllingSystem\CMST\Server\DetectionSystem\Mission2' 
#if not os.path.exists(newpath):
#    os.makedirs(newpath)



#os.rename(r'C:\Users\Administrator\Desktop\CMSTControllingSystem\CMST\Server\DetectionSystem\ReceivedData\test.txt',r'C:\Users\Administrator\Desktop\CMSTControllingSystem\CMST\Server\DetectionSystem\test.txt')
#os.sendfile(r'C:\Users\Administrator\Desktop\CMSTControllingSystem\CMST\Server\DetectionSystem\ReceivedData\test.txt',r'C:\Users\Administrator\Desktop\CMSTControllingSystem\CMST\Server\DetectionSystem\test.txt')


####################
#Tests
####################
MAIN_DIRECTORY = 'C:\\CMSTData'
missionID = 1
video_number = videoID = 0

location_of_the_video = MAIN_DIRECTORY + '\\' + str(missionID) + '\\ReceivedData\\' #in our case the video's location


x = 66
i = 1

'''
#create new Directory for the mission in the UI
newpathUI = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(missionID)
if not os.path.exists(newpathUI):
	os.makedirs(newpathUI) #create the new mission directory (will store all data related to the mission there (images, videos, some meta files)
	os.makedirs(newpathUI + '\\ReceivedData') #This directory will be used to store the received videos
	os.makedirs(newpathUI + '\\DetectionFolder')

uiVideoLocation = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(missionID) + '\\' + 'ReceivedData\\' + str(video_number) + '.mp4'
os.rename(location_of_the_video + str(video_number) + '.mp4', uiVideoLocation)

#Create Video folder for the videoID for UI (inside the DetectionFolder with (Detected, Cropped) subFolders
def createVideoDirectoryUI(video_number):
	#create new Directory for the mission
	newpath = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(missionID) + '\\DetectionFolder\\' + str(video_number) 
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		
	if not os.path.exists(newpath + '\\Detected'):
		os.makedirs(newpath + '\\Detected')
	
	if not os.path.exists(newpath + '\\Cropped'):
		os.makedirs(newpath + '\\Cropped')

createVideoDirectoryUI(0)



#Move the detected frame to the UI to be rendered
uiFrameLocation = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(missionID) +'\\DetectionFolder\\' + str(video_number) + '\\Detected\\' + str(x) + '.jpg'
os.rename('C:\\CMSTData\\' + str(missionID) +'\\DetectionFolder\\' + str(video_number) + '\\Detected\\' + str(x) + '.jpg', uiFrameLocation)


#Move the cropped frame to the UI to be rendered
uiFrameCroppedLocation = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(missionID) +'\\DetectionFolder\\' + str(video_number) + '\\Cropped\\' + str(x) + '-' + str(i) + '.jpg'
os.rename('C:\\CMSTData\\' + str(missionID) +'\\DetectionFolder\\' + str(video_number) + '\\Cropped\\' + str(x) + '-' + str(i) + '.jpg', uiFrameCroppedLocation)


#Move the cropped frame to the UI to be rendered
uiFrameCroppedLocation = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(missionID) +'\\DetectionFolder\\' + str(video_number) + '\\Cropped\\' + str(x) + '.jpg'
os.rename('C:\\CMSTData\\' + str(missionID) +'\\DetectionFolder\\' + str(video_number) + '\\Cropped\\' + str(x) + '.jpg', uiFrameCroppedLocation)

'''


'''
#Store the data in the database for that region
#INSERT INTO `detection`.`detectedobject` (`sightingUrl`, `objectNumber`, `property1Value`, `objectName`, `accuracy`, `url`) VALUES ('resources/sightings/163937_web11.jpg', '1', 'Loggerhead', 'Sea Turtle', '50', '/resources/wallpaper.jpg');
#Connect to the database
mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="detection")

#khaled's file
import mysql.connector



missionID = 4
x = 66
i = 2
video_number = 0

classification_result = [0.5345, 'green']


mycursor = mydb.cursor()



sql = 'INSERT INTO detection.video (videoUrl, missionID, latitude, longitude, startingTime) VALUES ('
sql += '\''  + str('./CMSTData' + '/' + str(missionID) + "/ReceivedData/" + str(video_number) +'.mp4')
sql += '\',\'' + str(missionID) + '\', ' + str(2.35) + ',' + str(6.31) + ',' + str(int(video_number)*10) +')'

mycursor.execute(sql)
mydb.commit()


#INSERT INTO `detection`.`sighting` (`sightingUrl`, `videoUrl`, `timeOfAppearance`, `numberOfObjects`) VALUES ('resources/sightings/123.png', 'resources/videos/video1.mp4', '7', '1');
sqlMain1 = 'INSERT INTO detection.sighting (sightingUrl, videoUrl, timeOfAppearance, numberOfObjects) VALUES ('
sqlMain1 += '\'' + './CMSTData/' + str(missionID) +'/DetectionFolder/' + str(video_number) + '/Detected/' + str(x) + '.jpg' + '\','
sqlMain1 += '\'' + './CMSTData/' + str(missionID) +'/ReceivedData/' + str(video_number) + '.mp4\','
sqlMain1 += '\'' + str(float(int(x)/30.0)) + '\', \'' + str(1) + '\')'

#execute the sql code
mycursor.execute(sqlMain1)
mydb.commit()




sqlMain = 'INSERT INTO detection.detectedobject (sightingUrl, objectNumber, property1Value, objectName, accuracy, url) VALUES ('
sqlMain += '\'' + './CMSTData/' + str(missionID) +'/DetectionFolder/' + str(video_number) + '/Detected/' + str(x) + '.jpg' + '\''


sql = ',\'' + str(i) + '\',\'' + str(classification_result[1]) + '\', \'Sea Turtle\', \'' + str(classification_result[0]) + '\', \''
sql += './CMSTData/' + str(missionID) +'/DetectionFolder/' + str(video_number) + '/Cropped/' + str(x) + '-' + str(i) + '.jpg\')'

#execute the sql code
mycursor.execute(sqlMain + sql)
mydb.commit()


sql = ',\'1\',\'' + str(classification_result[1]) + '\', \'Sea Turtle\', \'' + str(classification_result[0]) + '\', \''
sql += str('./CMSTData/' + str(missionID) +'/DetectionFolder/' + str(video_number) + '/Cropped/' + str(x) + '.jpg\')')

#execute the sql code
mycursor.execute(sqlMain + sql)
mydb.commit()

'''

from shutil import copyfile


uiVideoLocation = 'C:\\ui_server\\htdocs\\Turtles\\CMSTData\\' + str(20) + '\\' + 'ReceivedData\\' + str(0) + '.mp4'
copyfile(MAIN_DIRECTORY + '\\' + str(20) + "\\ReceivedData\\" + str(0) + ".mp4", uiVideoLocation)