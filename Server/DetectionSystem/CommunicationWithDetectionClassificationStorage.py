
import pickle
import os
import sys

from time import sleep

import random

import math

#Structure of the Direcotries to be used for storing the data
# C:\CMSTData
# --> \MissionID
# --> \--> Mission.txt
# --> \--> ReceivedDataMetaData.txt
# --> \--> \DetectionFolder
# --> \--> \--> \Video#
# --> \--> \--> \--> \Detected
# --> \--> \--> \--> \Cropped


#Main Directory
MAIN_DIRECTORY = 'C:\\CMSTData'


#Data given on the run (MissionID, drone speed, drone height)
missionID = str(sys.argv[1])
drone_height = int(sys.argv[2])
drone_speed = int(sys.argv[3])
number_of_videos = int(sys.argv[4])

#Common variables (Detection)
location_of_detection_program = 'C:\\tensorflow1\\models\\research\\object_detection'
name_of_detection_program = 'Object_detection_video2.py'
location_of_the_video = MAIN_DIRECTORY + '\\' + missionID + '\\ReceivedData\\' #in our case the video's location


#this function runs the detection system on the given video (in the directories specified above)
def runDetectionSystem(video_number):
	print('Run detection system for video number : ' + str(video_number))
	try:
		os.system('activate tensorflow1 & cd ' + location_of_detection_program + ' & python ' + name_of_detection_program + ' ' + str(missionID) + ' ' + str(video_number))
		return True
	except:
		print('Problem Running Video ' + str(video_number) + '.mp4' + 'on the detection system')
		return False
		
	
#Common variables (Classification)
location_of_classification_program = 'C:\\Users\\Administrator\\Desktop\\TurtleClassification'
name_of_classification_program = 'TestCNN.py'
location_of_the_image = MAIN_DIRECTORY + '\\' + missionID +'\\DetectionFolder' #then add 'video#\\Cropped\\'
	
#This function runs the classification system on the given image (in the directories specified above)
def runClassificationSystem(video_number, file_name):

	print('Run classification system for video number ' + str(video_number) + ' file name : ' + str(file_name))
	
	#write the address to the file 
	F = open(location_of_classification_program + "\\TestImageAddress.txt","w") 
	F.write(location_of_the_image + '\\' + str(video_number) + '\\Cropped\\' + file_name)
	F.close()

	try:
		os.system('activate MATLAB & cd ' + location_of_classification_program + ' & python ' + name_of_classification_program)
		return True
	except:
		print('Problem Running image ' + str(file_name) + 'on the classification system')
		return False

#This function reads the results of the classification program on the spcified image
#reference : https://stackoverflow.com/questions/9383740/what-does-pythons-eval-do
def readClassificationResults():
	#write the address to the file 
	F = open(location_of_classification_program + "\\Result.txt","r") 
	contents = F.read()
	F.close()
	result = eval(contents)
	return result


#this function return list of files in directory (will be used to get the files detected and feed it to the classification system)
def listOfFilesInDirectory(directory):
	list_of_files = []
	try:
		list_of_files = os.listdir(directory)
		return list_of_files
	except:
		print('No Such file or Directory Error for : ' + directory)
		return list_of_files


#this function returns list of names without the extension (will be used to get the frame id in that video, as we identify the name by the frame number)
def listOfNamesWithoutExtension(list_of_files):
	list_of_files_names = [] #list of files names without the extension
	for x in list_of_files:
		list_of_files_names.append(x.split('.')[0])	

	return list_of_files_names
	
	
	
#Calculate the number of frames in the same region

frames_in_region = int(((1.2 *drone_height)/drone_speed)*30) #1.2m is the length of the area covered, (for 1m height) 30 is the number of frames per second, drone_speed in m/s
	
#This function will choose frames from the detection directory accroding to the region 
#(specified by the height, and the speed, lense of the camera "fixed in our case")
def selectFrames(video_number):

	#the detection Folder location 
	detection_directory = MAIN_DIRECTORY + '\\' + missionID + '\\DetectionFolder' + '\\' + str(video_number)

	list_of_detected_frames = listOfNamesWithoutExtension(listOfFilesInDirectory(detection_directory + '\\Detected'))
	
	#list_of_detected_frames.sort()
	random.shuffle(list_of_detected_frames)
	
	print('List of detected frames in the video : ' + str(video_number))
	print(list_of_detected_frames)
	print('\n\n\n')
	
	
	
	number_of_regions = int(math.ceil(300/frames_in_region))
	
	print('Limits are number of regions : ' + str(number_of_regions) + ' , number of frames in region : ' + str(frames_in_region))
	
	
	for region_number in range(1, number_of_regions):
		take_frame_flag = True
		for x in list_of_detected_frames:
			if(take_frame_flag == True and int(x) < int(region_number*frames_in_region) and int(x) > int((region_number-1)*frames_in_region)):
				#region results will be stored in the storage system
				region_result = {}
				region_result['frameURL'] =  detection_directory + '\\Detected' + '\\' + str(x) + '.jpg'
				region_result['videoURL'] = location_of_the_video + str(video_number) + '.mp4'
				region_result['timeOfAppearance'] = float(int(x)/30.0)
				
				take_frame_flag = False
				
				count_detected_objects = 0
				list_of_detected_objects = listOfNamesWithoutExtension(listOfFilesInDirectory(detection_directory + '\\Cropped')) #list of cropped data
				for y in list_of_detected_objects:
					if x == y.split('-')[0]: #Check if the file name has the same prefix
						count_detected_objects += 1 # increment the number of detected objects
				
				#store the number of detected objects in that frame
				region_result['numberOfDetectedObjects'] = count_detected_objects
				region_result['objectsDetected'] = []
				
				if count_detected_objects > 1:
					for i in range(1, count_detected_objects + 1):
						runClassificationSystem(video_number, str(x) + '-' + str(i) + '.jpg')
						classification_result = readClassificationResults()
						#store the data of the classified object in the region result
						region_result['objectsDetected'].append({'frameCroppedURL' : str(x) + '-' + str(i) + '.jpg', 'detectedSpecie' : classification_result[1], 'detectedScore' : classification_result[0]})
				else:
					runClassificationSystem(video_number, str(x) + '.jpg')
					classification_result = readClassificationResults()
					#store the data of the classified object in the region result
					region_result['objectsDetected'].append({'frameCroppedURL' : str(x) + '.jpg', 'detectedSpecie' : classification_result[1], 'detectedScore' : classification_result[0]})
				
				print('\n\n\n\n')
				print(region_result)
				print('\n\n\n\n')
				
				break #skip checking the rest
			
			#send the data of the region_result to the storage system




#Create Video folder for the videoID (inside the DetectionFolder with (Detected, Cropped) subFolders
def createVideoDirectory(video_number):
	#create new Directory for the mission
	newpath = MAIN_DIRECTORY + '\\' + str(missionID) + '\\DetectionFolder\\' + str(video_number) 
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		
	if not os.path.exists(newpath + '\\Detected'):
		os.makedirs(newpath + '\\Detected')
	
	if not os.path.exists(newpath + '\\Cropped'):
		os.makedirs(newpath + '\\Cropped')
	


def runProgramOnReceivedVideos():
	listOfReceivedVideos = []
	listOfDetectedVideos = []
	#Stop the prorgam after processing all videos expected to be received
	while len(listOfDetectedVideos) < number_of_videos:
		try :
			with open (MAIN_DIRECTORY + '\\' + missionID + '\\' + 'ReceivedDataMetaData.txt', 'rb') as fp:
				listOfReceivedVideos = pickle.load(fp)
		except:
				print("Nothing in the file")

		listOfDetectedVideos.sort()
		listOfReceivedVideos.sort()

		print('list of received videos')
		print(listOfReceivedVideos)
		
		print('list of detected videos')
		print(listOfDetectedVideos)

		for x in listOfReceivedVideos:
			print('Check the list of received videos')
			if x not in listOfDetectedVideos:
				print('Checking video number ' + str(x))
				createVideoDirectory(x) #create video directory in the data
				
				listOfDetectedVideos.append(x) #add the video number to the detected videos
				runDetectionSystem(x) #run the detection system on that video
				selectFrames(x) #select frames (eliminate redundant detections in the same region), then run the classification system
			sleep(1)
	#When a mission is done, update its state in the database
			
#run the system
runProgramOnReceivedVideos()
