
import pickle
import os


#Common variables (Detection)
location_of_detection_program = 'C:\\tensorflow1\\models\\research\\object_detection'
name_of_detection_program = 'Object_detection_video.py'
location_of_the_video = 'C:\\Users\\Administrator\\Desktop\\CMSTControllingSystem\\CMST\\Server\\DetectionSystem\\ReceivedData\\' #in our case the video's location


#this function runs the detection system on the given video (in the directories specified above)
def runDetectionSystem(file_name):

	try:
		os.system('activate tensorflow1 & cd ' + location_of_detection_program + ' & python ' + name_of_detection_program + ' ' + location_of_the_video + file_name)
		return True
	except:
		print('Problem Running Video ' + str(file_name) + 'on the detection system')
		return False
		
	
#Common variables (Classification)
location_of_classification_program = 'C:\\Users\\Administrator\\Desktop\\TurtleClassification'
name_of_classification_program = 'TestCNN.py'
location_of_the_image = 'C:\\New Project\\Detected\\Cropped\\'
	
#This function runs the classification system on the given image (in the directories specified above)
def runClassificationSystem(file_name):
	#write the address to the file 
	F = open(location_of_classification_program + "\\TestImageAddress.txt","w") 
	F.write(location_of_the_image + file_name)
	F.close()

	try:
		os.system('activate MATLAB & cd ' + location_of_classification_program + ' & python ' + name_of_classification_program)
		return True
	except:
		print('Problem Running image ' + str(file_name) + 'on the classification system')
		return False

#This function reads the results of the classification program on the spcified image
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
def listOfNamesWithoutExtension(list_of_data):
	list_of_files_names = [] #list of files names without the extension
	for x in list_of_files:
		list_of_files_names.append(x.split('.')[0])	

	return list_of_files_names
	
	
	
#Calculate the number of frames in the same region
drone_height = int(sys.argv[1])
drone_speed = int(sys.argv[2])
frames_in_region = ((1.2 *drone_height)//drone_speed)*30 #1.2m is the length of the area covered, (for 1m height) 30 is the number of frames per second, drone_speed in m/s
	
#This function will choose frames from the detection directory accroding to the region 
#(specified by the height, and the speed, lense of the camera "fixed in our case")
def selectFrames(detection_directory, classification_directory, videoURL):
	list_of_detected_frames = listOfNamesWithoutExtension(listOfFilesInDirectory(detection_directory + '\\Detected'))
	take_frame_flag = True
	region_number = 1
	for x in list_of_detected_frames:
		if(take_frame_flag == True and x < (region_number*frames_in_region)):
			#region results will be stored in the storage system
			region_result = {}
			region_result['frameURL'] =  detection_directory + '\\Detected' + '\\' + str(x) + '.jpg'
			region_result['videoURL'] = videoURL
			region_result['timeOfAppearance'] = x/30.0
			
			take_frame_flag = False
			
			count_detected_objects = 0
			list_of_detected_objects = listOfNamesWithoutExtension(listOfFilesInDirectory(detection_directory + '\\Cropped')) #list of cropped data
			for y in list_of_detected_objects:
				if x == y.split('-')[0]: #Check if the file name has the same prefix
					count_detected_objects += 1 # increment the number of detected objects
			
			#store the number of detected objects in that frame
			region_result['numberOfDetectedObjects'] = count_detected_objects
			region_result['objectsDetected'] = []
			
			for i in range(1, count_detected_objects + 1):
				runClassificationSystem(str(x) + '-' + str(i) + '.jpg')
				classification_result = readClassificationResults()
				#store the data of the classified object in the region result
				region_result['objectsDetected'].append({'frameCroppedURL' : str(x) + '-' + str(i) + '.jpg', 'detectedSpecie' : classification_result[0], 'detectedScore' : classification_result[1]})
			
			#send the data of the region_result to the storage system

