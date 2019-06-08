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
missionID = 0
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
'''

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

